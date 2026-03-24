"""Pub/Sub pull subscriber for Agent Assist event notifications.

Replaces Google's push-based architecture with a pull-based model using
the ``google-cloud-pubsub`` Python client. Each of the 4 event types
gets its own streaming pull subscription running in a background thread.
"""

import logging

from google.cloud import pubsub_v1

import config
from handlers.event_processor import process_pubsub_message

logger = logging.getLogger(__name__)

# Mapping of subscription config keys to event type strings.
SUBSCRIPTION_MAP = {
    config.SUBSCRIPTION_HUMAN_AGENT_ASSISTANT: "human-agent-assistant-event",
    config.SUBSCRIPTION_CONVERSATION_LIFECYCLE: "conversation-lifecycle-event",
    config.SUBSCRIPTION_NEW_MESSAGE: "new-message-event",
    config.SUBSCRIPTION_RECOGNITION_RESULT: "new-recognition-result-notification-event",
}


def _create_callback(data_type, redis_client):
    """Create a Pub/Sub message callback for a specific event type.

    Args:
        data_type: The Agent Assist event type string.
        redis_client: A ``redis.StrictRedis`` instance.

    Returns:
        A callback function suitable for ``SubscriberClient.subscribe()``.
    """

    def callback(message):
        """Process and acknowledge a Pub/Sub message.

        Args:
            message: A ``google.cloud.pubsub_v1.subscriber.message.Message``.
        """
        try:
            process_pubsub_message(message, data_type, redis_client)
        except Exception:
            logger.error(
                "Unhandled error processing %s message %s",
                data_type,
                message.message_id,
                exc_info=True,
            )
        finally:
            message.ack()

    return callback


def start_subscribers(redis_client):
    """Start streaming pull subscribers for all 4 event types.

    Creates a ``SubscriberClient`` and opens a streaming pull for each
    configured subscription. Each subscription runs in its own background
    thread managed by the client library.

    Args:
        redis_client: A ``redis.StrictRedis`` instance for publishing events.

    Returns:
        A list of ``StreamingPullFuture`` instances (one per subscription).
        Call ``.cancel()`` on each to shut down gracefully.

    Raises:
        ValueError: If ``GCP_PROJECT_ID`` is not configured.
    """
    if not config.GCP_PROJECT_ID:
        raise ValueError(
            "GCP_PROJECT_ID must be set to start Pub/Sub subscribers"
        )

    subscriber = pubsub_v1.SubscriberClient()
    futures = []

    flow_control = pubsub_v1.types.FlowControl(
        max_messages=100,
        max_bytes=10 * 1024 * 1024,
    )

    for subscription_id, data_type in SUBSCRIPTION_MAP.items():
        subscription_path = subscriber.subscription_path(
            config.GCP_PROJECT_ID, subscription_id
        )
        callback = _create_callback(data_type, redis_client)

        future = subscriber.subscribe(
            subscription_path,
            callback=callback,
            flow_control=flow_control,
        )

        logger.info(
            "Started pull subscriber for %s on %s",
            data_type,
            subscription_path,
        )
        futures.append(future)

    return futures
