"""Conversation integration key routes for the UI Connector.

Provides /conversation-name GET/POST/DELETE endpoints for mapping
external conversation identifiers (e.g. phone numbers) to Dialogflow
conversation names in Redis.
Extracted from Google's main.py lines 187–239.
"""

import hashlib
import logging

from flask import Blueprint, request, make_response, jsonify

from auth import token_required

logger = logging.getLogger(__name__)

conversation_bp = Blueprint("conversation", __name__)


def _init_conversation_routes(redis_client):
    """Initialize conversation routes with a Redis client reference.

    Args:
        redis_client: A redis.StrictRedis instance.

    Returns:
        The configured Blueprint.
    """

    @conversation_bp.route("/conversation-name", methods=["POST"])
    @token_required
    def set_conversation_name():
        """Map a conversation integration key to a Dialogflow conversation name.

        Useful when the Dialogflow conversation name cannot be sent to the
        agent desktop directly (e.g. mapping a phone number).

        Returns:
            200 with the mapping on success, 400 if required fields are missing.
        """
        data = request.get_json()
        if not data:
            return make_response("Request body required", 400)

        integration_key = data.get("conversationIntegrationKey", "")
        conversation_name = data.get("conversationName", "")

        if not integration_key or not conversation_name:
            return make_response("Missing required fields", 400)

        hashed_key = hashlib.sha256(integration_key.encode("utf-8")).hexdigest()
        result = redis_client.set(hashed_key, conversation_name)

        if not result:
            logger.error("Redis SET failed for integration key: %s", integration_key)
            return make_response("Internal error", 500)

        logger.info("SET conversation mapping: %s -> %s", integration_key, conversation_name)
        return jsonify({integration_key: conversation_name})

    @conversation_bp.route("/conversation-name", methods=["GET"])
    @token_required
    def get_conversation_name():
        """Look up a Dialogflow conversation name by integration key.

        Returns:
            200 with the conversation name, 400 if the key is missing.
        """
        integration_key = request.args.get("conversationIntegrationKey", "")
        if not integration_key:
            return make_response("Missing conversationIntegrationKey", 400)

        hashed_key = hashlib.sha256(integration_key.encode("utf-8")).hexdigest()
        conversation_name = redis_client.get(hashed_key)

        logger.info("GET conversation mapping: %s -> %s", integration_key, conversation_name)
        return jsonify({
            "conversationName": (
                conversation_name.decode("utf-8") if conversation_name else ""
            )
        })

    @conversation_bp.route("/conversation-name", methods=["DELETE"])
    @token_required
    def del_conversation_name():
        """Delete a conversation integration key mapping from Redis.

        Returns:
            200 on success, 400 if key is missing, 404 if key not found.
        """
        integration_key = request.args.get("conversationIntegrationKey", "")
        if not integration_key:
            return make_response("Missing conversationIntegrationKey", 400)

        hashed_key = hashlib.sha256(integration_key.encode("utf-8")).hexdigest()
        result = redis_client.delete(hashed_key)

        logger.info("DEL conversation mapping: %s, result=%s", integration_key, result)
        if not result:
            return make_response("Not found", 404)
        return make_response("Success", 200)

    return conversation_bp
