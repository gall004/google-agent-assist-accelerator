"""Redis client factory for the UI Connector service.

Creates a Redis client with retry logic, generates a unique server ID,
and manages the Redis Pub/Sub subscription thread for receiving events
from the Cloud Pub/Sub Interceptor.
"""

import logging
import random
from datetime import datetime

import redis

import config

logger = logging.getLogger(__name__)

# Unique server ID for this UI Connector instance.
SERVER_ID = "{}-{}".format(random.uniform(0, 322321), datetime.now().timestamp())


def create_redis_client():
    """Create a Redis client with retry and health check configuration.

    Returns:
        redis.StrictRedis: A configured Redis client instance.

    Raises:
        redis.exceptions.ConnectionError: If the connection cannot be established.
    """
    try:
        client = redis.StrictRedis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            health_check_interval=10,
            socket_connect_timeout=15,
            retry_on_timeout=True,
            socket_keepalive=True,
            retry=redis.retry.Retry(
                redis.backoff.ExponentialBackoff(cap=5, base=1), 5
            ),
            retry_on_error=[
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
                redis.exceptions.ResponseError,
            ],
        )
        logger.info(
            "Redis client created (SERVER_ID=%s, host=%s:%s)",
            SERVER_ID,
            config.REDIS_HOST,
            config.REDIS_PORT,
        )
        return client
    except redis.exceptions.ConnectionError:
        logger.error(
            "Failed to create Redis client at %s:%s",
            config.REDIS_HOST,
            config.REDIS_PORT,
        )
        raise


def get_conversation_name_without_location(conversation_name):
    """Strip the location segment from a Dialogflow conversation name.

    Args:
        conversation_name: The full Dialogflow conversation resource name.

    Returns:
        The conversation name without the location segment.
    """
    if "/locations/" in conversation_name:
        parts = conversation_name.split("/")
        return "/".join(parts[i] for i in [0, 1, -2, -1])
    return conversation_name
