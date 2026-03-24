"""Unit tests for the health check endpoint and main module."""

from unittest.mock import MagicMock, patch

import pytest

import main
from main import app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests for the /healthz endpoint."""

    def test_healthy(self, client):
        """Returns 200 when Redis is reachable and subscribers are running."""
        main._redis = MagicMock()
        main._redis.ping.return_value = True
        main._subscriber_futures = [MagicMock(cancelled=lambda: False)]

        response = client.get("/healthz")

        assert response.status_code == 200
        assert response.data == b"ok"

    def test_redis_not_initialized(self, client):
        """Returns 503 when Redis client is None."""
        main._redis = None

        response = client.get("/healthz")

        assert response.status_code == 503

    def test_redis_unreachable(self, client):
        """Returns 503 when Redis ping fails."""
        main._redis = MagicMock()
        main._redis.ping.side_effect = Exception("Connection refused")
        main._subscriber_futures = []

        response = client.get("/healthz")

        assert response.status_code == 503

    def test_subscriber_cancelled(self, client):
        """Returns 503 when a subscriber future has been cancelled."""
        main._redis = MagicMock()
        main._redis.ping.return_value = True

        cancelled_future = MagicMock()
        cancelled_future.cancelled.return_value = True
        main._subscriber_futures = [cancelled_future]

        response = client.get("/healthz")

        assert response.status_code == 503
