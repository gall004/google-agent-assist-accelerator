"""Unit tests for the event processor module.

Tests cover: valid message processing, missing conversation field,
malformed JSON, Redis key not found, recognition result attributes,
and Redis publish failures.
"""

import json
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from handlers.event_processor import (
    get_conversation_name_without_location,
    process_pubsub_message,
)


CONVERSATION_NAME = "projects/test-project/conversations/conv-001"
CONVERSATION_NAME_WITH_LOCATION = (
    "projects/test-project/locations/us-central1/conversations/conv-001"
)
SERVER_ID = "SERVER_001"


def _make_message(data_dict, attributes=None, message_id="msg-123"):
    """Create a mock Pub/Sub message.

    Args:
        data_dict: Dict to JSON-encode as the message payload.
        attributes: Optional dict of Pub/Sub message attributes.
        message_id: The message ID string.

    Returns:
        A MagicMock mimicking a Pub/Sub Message.
    """
    msg = MagicMock()
    msg.data = json.dumps(data_dict).encode("utf-8")
    msg.message_id = message_id
    msg.publish_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    msg.attributes = attributes or {}
    return msg


class TestGetConversationNameWithoutLocation:
    """Tests for location stripping from conversation names."""

    def test_strips_location(self):
        """Removes the /locations/X/ segment from a conversation name."""
        result = get_conversation_name_without_location(
            CONVERSATION_NAME_WITH_LOCATION
        )
        assert result == CONVERSATION_NAME

    def test_preserves_name_without_location(self):
        """Returns the name unchanged when no location segment exists."""
        result = get_conversation_name_without_location(CONVERSATION_NAME)
        assert result == CONVERSATION_NAME

    def test_handles_global_location(self):
        """Strips the global location segment correctly."""
        name = "projects/test-project/locations/global/conversations/conv-001"
        result = get_conversation_name_without_location(name)
        assert result == CONVERSATION_NAME


class TestProcessPubsubMessage:
    """Tests for the main message processing function."""

    def test_valid_lifecycle_event(self):
        """Processes a valid conversation lifecycle event and publishes to Redis."""
        redis_mock = MagicMock()
        redis_mock.exists.return_value = 1
        redis_mock.get.return_value = SERVER_ID.encode("utf-8")

        event_data = {"conversation": CONVERSATION_NAME, "type": "CONVERSATION_STARTED"}
        message = _make_message(event_data)

        result = process_pubsub_message(
            message, "conversation-lifecycle-event", redis_mock
        )

        assert result is True
        redis_mock.exists.assert_called_once_with(CONVERSATION_NAME)
        redis_mock.get.assert_called_once_with(CONVERSATION_NAME)
        redis_mock.publish.assert_called_once()

        published_data = json.loads(redis_mock.publish.call_args[0][1])
        assert published_data["conversation_name"] == CONVERSATION_NAME
        assert published_data["data_type"] == "conversation-lifecycle-event"

    def test_missing_conversation_field(self):
        """Returns False when the conversation field is missing."""
        redis_mock = MagicMock()
        event_data = {"type": "CONVERSATION_STARTED"}
        message = _make_message(event_data)

        result = process_pubsub_message(
            message, "conversation-lifecycle-event", redis_mock
        )

        assert result is False
        redis_mock.publish.assert_not_called()

    def test_malformed_json(self):
        """Returns False when the message payload is not valid JSON."""
        redis_mock = MagicMock()
        message = MagicMock()
        message.data = b"not valid json"
        message.message_id = "msg-bad"

        result = process_pubsub_message(
            message, "conversation-lifecycle-event", redis_mock
        )

        assert result is False
        redis_mock.publish.assert_not_called()

    def test_no_server_mapping_in_redis(self):
        """Returns False when no UI Connector is registered for the conversation."""
        redis_mock = MagicMock()
        redis_mock.exists.return_value = 0

        event_data = {"conversation": CONVERSATION_NAME}
        message = _make_message(event_data)

        result = process_pubsub_message(
            message, "human-agent-assistant-event", redis_mock
        )

        assert result is False
        redis_mock.publish.assert_not_called()

    def test_recognition_result_includes_attributes(self):
        """Includes participant_role and message_id for recognition events."""
        redis_mock = MagicMock()
        redis_mock.exists.return_value = 1
        redis_mock.get.return_value = SERVER_ID.encode("utf-8")

        event_data = {"conversation": CONVERSATION_NAME}
        attributes = {"participant_role": "HUMAN_AGENT", "message_id": "rec-456"}
        message = _make_message(event_data, attributes=attributes)

        result = process_pubsub_message(
            message,
            "new-recognition-result-notification-event",
            redis_mock,
        )

        assert result is True
        published_data = json.loads(redis_mock.publish.call_args[0][1])
        assert published_data["participant_role"] == "HUMAN_AGENT"
        assert published_data["new_recognition_result_message_id"] == "rec-456"

    def test_redis_publish_failure(self):
        """Returns False when Redis publish raises an exception."""
        redis_mock = MagicMock()
        redis_mock.exists.return_value = 1
        redis_mock.get.return_value = SERVER_ID.encode("utf-8")
        redis_mock.publish.side_effect = Exception("Redis connection lost")

        event_data = {"conversation": CONVERSATION_NAME}
        message = _make_message(event_data)

        result = process_pubsub_message(
            message, "new-message-event", redis_mock
        )

        assert result is False

    def test_strips_location_from_conversation_name(self):
        """Normalizes conversation names with location segments before processing."""
        redis_mock = MagicMock()
        redis_mock.exists.return_value = 1
        redis_mock.get.return_value = SERVER_ID.encode("utf-8")

        event_data = {"conversation": CONVERSATION_NAME_WITH_LOCATION}
        message = _make_message(event_data)

        result = process_pubsub_message(
            message, "conversation-lifecycle-event", redis_mock
        )

        assert result is True
        redis_mock.exists.assert_called_once_with(CONVERSATION_NAME)
