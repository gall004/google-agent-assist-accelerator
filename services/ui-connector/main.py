"""UI Connector — main entry point.

Creates the Flask + SocketIO application, registers route blueprints,
starts the Redis Pub/Sub listener, and runs the server.

This is a thin composition module that wires together the handler
modules. All business logic is in the handlers/ directory.
"""

import logging
import sys

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

import config
from redis_client import create_redis_client, SERVER_ID
from handlers.socketio_events import (
    register_socketio_events,
    redis_pubsub_handler,
    psubscribe_exception_handler,
)
from handlers.proxy_routes import proxy_bp
from handlers.registration_routes import registration_bp
from handlers.conversation_routes import _init_conversation_routes

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure the Flask application.

    Returns:
        A tuple of (app, socketio, redis_client).
    """
    app = Flask(__name__)
    CORS(app, origins=config.CORS_ALLOWED_ORIGINS)
    socketio = SocketIO(app, cors_allowed_origins=config.CORS_ALLOWED_ORIGINS)

    redis_client = create_redis_client()

    # Register route blueprints.
    app.register_blueprint(proxy_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(_init_conversation_routes(redis_client))

    # Register SocketIO event handlers.
    register_socketio_events(socketio, redis_client)

    # Start Redis Pub/Sub listener thread.
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.psubscribe(**{f"{SERVER_ID}:*": redis_pubsub_handler})
    pubsub.run_in_thread(
        sleep_time=0.001,
        exception_handler=psubscribe_exception_handler,
    )
    logger.info("Redis Pub/Sub listener started for SERVER_ID=%s", SERVER_ID)

    # Health check endpoint.
    @app.route("/healthz")
    def healthz():
        """Health check for Cloud Run / Kubernetes liveness probes.

        Returns:
            200 if the service is ready.
        """
        try:
            redis_client.ping()
        except Exception:
            logger.error("Health check failed: Redis unreachable", exc_info=True)
            return "Redis unreachable", 503
        return "ok", 200

    # Error handler.
    @app.errorhandler(500)
    def server_error(e):
        """Handle Flask internal server errors.

        Args:
            e: The exception.

        Returns:
            A 500 response with error details.
        """
        logger.error("Internal server error: %s", e, exc_info=True)
        return "Internal server error", 500

    return app, socketio, redis_client


app, socketio, redis_client = create_app()

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=config.PORT,
        debug=False,
        use_reloader=False,
    )
