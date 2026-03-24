"""SocketIO event handlers for the UI Connector.

Manages WebSocket connections, conversation room joining/leaving,
and the Redis Pub/Sub handler that relays events to connected clients.
Extracted from Google's main.py lines 40–306.
"""

import json
import logging
import time

from flask import request
from flask_socketio import emit, join_room, leave_room, rooms
from socketio.exceptions import ConnectionRefusedError

from auth import check_jwt
from redis_client import SERVER_ID, get_conversation_name_without_location

logger = logging.getLogger(__name__)


def redis_pubsub_handler(message):
    """Handle messages received from Redis Pub/Sub.

    Parses the message and emits it to the appropriate SocketIO room
    based on the conversation name.

    Args:
        message: A Redis Pub/Sub message dict with 'data' key.
    """
    try:
        msg_object = json.loads(message["data"])
        # socketio is injected at registration time via closure.
        redis_pubsub_handler._socketio.emit(
            msg_object["data_type"],
            msg_object,
            to=msg_object["conversation_name"],
        )
        logger.info(
            "Relayed %s event for conversation %s via channel %s",
            msg_object["data_type"],
            msg_object["conversation_name"],
            message.get("channel", "unknown"),
        )
    except (json.JSONDecodeError, KeyError):
        logger.error(
            "Failed to parse Redis Pub/Sub message: %s",
            message,
            exc_info=True,
        )


def psubscribe_exception_handler(ex, pubsub, thread):
    """Handle exceptions from the Redis Pub/Sub listener thread.

    Args:
        ex: The exception that occurred.
        pubsub: The Redis PubSub instance.
        thread: The listener thread.
    """
    logger.error("Redis Pub/Sub listener error: %s", ex, exc_info=True)
    time.sleep(2)


def register_socketio_events(socketio, redis_client):
    """Register all SocketIO event handlers.

    Args:
        socketio: The Flask-SocketIO instance.
        redis_client: A redis.StrictRedis instance.
    """
    # Store socketio reference for the redis handler.
    redis_pubsub_handler._socketio = socketio

    @socketio.on("connect")
    def connect(auth=None):
        """Authenticate WebSocket connections via JWT.

        Args:
            auth: Optional dict with 'token' key from the client.
        """
        logger.info("Connection request from sid=%s", request.sid)
        if isinstance(auth, dict) and "token" in auth:
            is_valid, log_info = check_jwt(auth["token"])
            logger.info(log_info)
            if is_valid:
                return True

        socketio.emit("unauthenticated")
        raise ConnectionRefusedError("authentication failed")

    @socketio.on("disconnect")
    def disconnect(reason):
        """Clean up Redis mappings when a client disconnects.

        Args:
            reason: The disconnect reason string.
        """
        logger.info("Client disconnected, reason=%s, sid=%s", reason, request.sid)
        room_list = rooms()
        if len(room_list) > 1:
            room_list.pop(0)  # First entry is the client's own SID room.
            try:
                redis_client.delete(*room_list)
            except Exception:
                logger.error(
                    "Failed to clean up Redis mappings for sid=%s",
                    request.sid,
                    exc_info=True,
                )

    @socketio.on("join-conversation")
    def on_join(message):
        """Join a SocketIO room for a conversation.

        Args:
            message: The Dialogflow conversation name.

        Returns:
            A tuple of (success: bool, conversation_name: str).
        """
        logger.info("join-conversation: %s", message)
        conversation_name = get_conversation_name_without_location(message)
        join_room(conversation_name)
        redis_client.set(conversation_name, SERVER_ID)
        logger.info("Joined conversation room: %s", conversation_name)
        return True, conversation_name

    @socketio.on("leave-conversation")
    def on_leave(message):
        """Leave a SocketIO room for a conversation.

        Args:
            message: The Dialogflow conversation name.

        Returns:
            A tuple of (success: bool, conversation_name: str).
        """
        logger.info("leave-conversation: %s", message)
        conversation_name = get_conversation_name_without_location(message)
        leave_room(conversation_name)
        redis_client.delete(conversation_name)
        logger.info("Left conversation room: %s", conversation_name)
        return True, conversation_name

    @socketio.on_error_default
    def default_error_handler(e):
        """Handle unhandled SocketIO event errors.

        Args:
            e: The exception that occurred.
        """
        logger.error(
            "SocketIO error in %s event: %s",
            request.event["message"],
            e,
            exc_info=True,
        )
