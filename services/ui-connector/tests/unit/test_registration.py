"""Unit tests for registration routes.

Tests cover: successful user registration, auth failure, successful
app registration, app auth failure, and missing request body.
"""

import json
from unittest.mock import patch, MagicMock

import pytest

# Patch config and external dependencies before importing.
with patch.dict("os.environ", {
    "GCP_PROJECT_ID": "test-project",
    "JWT_SECRET_KEY": "test-secret-key",
    "JWT_ALGORITHM": "HS256",
    "JWT_TOKEN_LIFETIME": "60",
    "AUTH_OPTION": "Skip",
}):
    with patch("dialogflow.google.auth.default", return_value=(MagicMock(), "test-project")):
        with patch("dialogflow.AuthorizedSession"):
            from main import app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestRegisterToken:
    """Tests for the /register endpoint."""

    @patch("handlers.registration_routes.check_auth", return_value=True)
    @patch("handlers.registration_routes.generate_jwt", return_value="mock-jwt-token")
    def test_successful_registration(self, mock_jwt, mock_auth, client):
        """Returns 200 with JWT on successful authentication."""
        response = client.post(
            "/register",
            headers={"Authorization": "Bearer valid-token"},
            json={"gcp_agent_assist_user": "agent1"},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["token"] == "mock-jwt-token"

    @patch("handlers.registration_routes.check_auth", return_value=False)
    def test_auth_failure(self, mock_auth, client):
        """Returns 401 when authentication fails."""
        response = client.post(
            "/register",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401


class TestRegisterAppToken:
    """Tests for the /register-app endpoint."""

    @patch("handlers.registration_routes.check_app_auth", return_value=True)
    @patch("handlers.registration_routes.generate_jwt", return_value="mock-app-jwt")
    def test_successful_app_registration(self, mock_jwt, mock_auth, client):
        """Returns 200 with JWT on successful app authentication."""
        response = client.post(
            "/register-app",
            json={"accountSid": "AC123", "authToken": "tok123"},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["token"] == "mock-app-jwt"

    @patch("handlers.registration_routes.check_app_auth", return_value=False)
    def test_app_auth_failure(self, mock_auth, client):
        """Returns 401 when app authentication fails."""
        response = client.post(
            "/register-app",
            json={"accountSid": "wrong", "authToken": "wrong"},
        )
        assert response.status_code == 401

    def test_missing_body(self, client):
        """Returns 400 when request body is missing."""
        response = client.post(
            "/register-app",
            content_type="application/json",
            data="",
        )
        assert response.status_code == 400
