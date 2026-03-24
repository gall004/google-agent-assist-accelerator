"""Event processor for Cloud Pub/Sub messages.

Processes Agent Assist event notifications received via Pub/Sub pull
subscriptions, extracts conversation metadata, and publishes to Redis
Pub/Sub channels for consumption by UI Connector instances.
"""

import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def get_conversation_name_without_location(conversation_name):
    """Strip the location segment from a Dialogflow conversation name.

    Converts a fully-qualified name like
    ``projects/P/locations/L/conversations/C`` to ``projects/P/conversations/C``.

    Args:
        conversation_name: The full Dialogflow conversation resource name.

    Returns:
        The conversation name without the location segment.
    """
    if "/locations/" in conversation_name:
        parts = conversation_name.split("/")
        return "/".join(parts[i] for i in [0, 1, -2, -1])
    return conversation_name


def process_pubsub_message(message, data_type, redis_client):
    """Process a single Pub/Sub message and publish to Redis.

    Decodes the message payload, extracts the conversation name, looks up
    the UI Connector server ID in Redis, and publishes the event to the
    appropriate Redis Pub/Sub channel.

    Args:
        message: A ``google.cloud.pubsub_v1.subscriber.message.Message``.
        data_type: The event type string (e.g. ``human-agent-assistant-event``).
        redis_client: A ``redis.StrictRedis`` instance.

    Returns:
        True if the message was processed successfully, False otherwise.
    """
    try:
        data = message.data.decode("utf-8")
        data_object = json.loads(data)
    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.warning("Malformed Pub/Sub message, skipping: %s", message.message_id)
        return False

    if "conversation" not in data_object:
        logger.warning(
            "Missing 'conversation' field in Pub/Sub message %s",
            message.message_id,
        )
        return False

    conversation_name = get_conversation_name_without_location(
        data_object["conversation"]
    )

    msg_data = {
        "conversation_name": conversation_name,
        "data": data,
        "data_type": data_type,
        "ack_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publish_time": message.publish_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "message_id": message.message_id,
    }

    if data_type == "new-recognition-result-notification-event":
        msg_data["participant_role"] = message.attributes.get(
            "participant_role", ""
        )
        msg_data["new_recognition_result_message_id"] = message.attributes.get(
            "message_id", ""
        )

    return _publish_to_redis(redis_client, conversation_name, msg_data)


def _publish_to_redis(redis_client, conversation_name, msg_data):
    """Look up the UI Connector server ID and publish to Redis channel.

    Args:
        redis_client: A ``redis.StrictRedis`` instance.
        conversation_name: The normalized conversation resource name.
        msg_data: The message payload dict to publish.

    Returns:
        True if published successfully, False if no server mapping exists.
    """
    try:
        if not redis_client.exists(conversation_name):
            logger.warning(
                "No UI Connector instance registered for conversation: %s. "
                "Client must send join-conversation first.",
                conversation_name,
            )
            return False

        server_id = redis_client.get(conversation_name).decode("utf-8")
        channel = f"{server_id}:{conversation_name}"
        redis_client.publish(channel, json.dumps(msg_data))

        logger.info(
            "Published to Redis channel=%s, message_id=%s, data_type=%s",
            channel,
            msg_data["message_id"],
            msg_data["data_type"],
        )
        return True

    except Exception:
        logger.error(
            "Redis error while publishing for conversation: %s",
            conversation_name,
            exc_info=True,
        )
        return False
