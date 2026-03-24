"""Cloud Pub/Sub Interceptor — main entry point.

Starts the pull-based Pub/Sub subscribers and a minimal Flask health
check server. The subscribers continuously pull messages from 4
Agent Assist event subscriptions and publish them to Redis.
"""

import logging
import sys
import threading

from flask import Flask

import config
from redis_client import create_redis_client
from subscriber import start_subscribers

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Module-level state for health checking.
_redis = None
_subscriber_futures = []


def _start_background_services():
    """Initialize Redis client and start Pub/Sub subscribers.

    Called once on startup. Stores references for health checks.
    """
    global _redis, _subscriber_futures
    _redis = create_redis_client()
    _subscriber_futures = start_subscribers(_redis)
    logger.info("All Pub/Sub subscribers started successfully")


@app.route("/healthz")
def healthz():
    """Health check endpoint for Cloud Run / Kubernetes liveness probes.

    Returns:
        200 if Redis is reachable and subscribers are running.
        503 if any critical dependency is unhealthy.
    """
    try:
        if _redis is None:
            return "Redis client not initialized", 503
        _redis.ping()
    except Exception:
        logger.error("Health check failed: Redis unreachable", exc_info=True)
        return "Redis unreachable", 503

    cancelled = [f for f in _subscriber_futures if f.cancelled()]
    if cancelled:
        logger.error(
            "Health check failed: %d/%d subscribers cancelled",
            len(cancelled),
            len(_subscriber_futures),
        )
        return "Subscribers unhealthy", 503

    return "ok", 200


def main():
    """Start the interceptor service.

    Launches Pub/Sub pull subscribers in background threads and runs the
    Flask health check server in the foreground.
    """
    logger.info("Starting Cloud Pub/Sub Interceptor (pull-based)")
    _start_background_services()

    # Run Flask health check server (foreground).
    app.run(
        host="0.0.0.0",
        port=config.HEALTH_CHECK_PORT,
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    main()
