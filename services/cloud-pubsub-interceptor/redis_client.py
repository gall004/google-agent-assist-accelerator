"""Redis client factory for the Cloud Pub/Sub Interceptor.

Provides a configured Redis client with retry logic and exponential
backoff, extracted from Google's original inline setup.
"""

import logging

import redis

import config

logger = logging.getLogger(__name__)


def create_redis_client():
    """Create a Redis client with retry and health check configuration.

    Returns:
        redis.StrictRedis: A configured Redis client instance.

    Raises:
        redis.exceptions.ConnectionError: If initial connection fails
            after all retry attempts.
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
            "Redis client created for %s:%s",
            config.REDIS_HOST,
            config.REDIS_PORT,
        )
        return client
    except redis.exceptions.ConnectionError:
        logger.error(
            "Failed to create Redis client for %s:%s",
            config.REDIS_HOST,
            config.REDIS_PORT,
        )
        raise
