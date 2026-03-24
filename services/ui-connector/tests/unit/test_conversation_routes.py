"""Unit tests for conversation integration key routes.

Tests cover: set/get/delete conversation name, missing required fields,
and not-found delete.
"""

import hashlib
import json
from unittest.mock import patch, MagicMock

import pytest

# Patch config and external dependencies before importing.
with patch.dict("os.environ", {
    "GCP_PROJECT_ID": "test-project",
    "JWT_SECRET_KEY": "test-secret-key",
    "JWT_ALGORITHM": "HS256",
    "JWT_TOKEN_LIFETIME": "60",
}):
    with patch("dialogflow.google.auth.default", return_value=(MagicMock(), "test-project")):
        with patch("dialogflow.AuthorizedSession"):
            from main import app, redis_client


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _auth_header():
    """Generate a valid Authorization header for testing."""
    from auth import generate_jwt
    token = generate_jwt({"gcp_agent_assist_user": "tester"})
    return {"Authorization": token}


class TestSetConversationName:
    """Tests for POST /conversation-name."""

    def test_set_mapping_success(self, client):
        """Creates a mapping between integration key and conversation name."""
        with patch.object(redis_client, "set", return_value=True):
            response = client.post(
                "/conversation-name",
                headers=_auth_header(),
                json={
                    "conversationIntegrationKey": "18005551234",
                    "conversationName": "projects/p/conversations/c",
                },
            )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "18005551234" in data

    def test_set_missing_fields(self, client):
        """Returns 400 when required fields are missing."""
        response = client.post(
            "/conversation-name",
            headers=_auth_header(),
            json={"conversationIntegrationKey": ""},
        )
        assert response.status_code == 400

    def test_set_without_auth(self, client):
        """Returns 401 when Authorization header is missing."""
        response = client.post(
            "/conversation-name",
            json={"conversationIntegrationKey": "key", "conversationName": "name"},
        )
        assert response.status_code == 401


class TestGetConversationName:
    """Tests for GET /conversation-name."""

    def test_get_existing_mapping(self, client):
        """Returns the conversation name for a known integration key."""
        hashed = hashlib.sha256("18005551234".encode("utf-8")).hexdigest()
        with patch.object(
            redis_client, "get",
            return_value=b"projects/p/conversations/c",
        ):
            response = client.get(
                "/conversation-name?conversationIntegrationKey=18005551234",
                headers=_auth_header(),
            )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["conversationName"] == "projects/p/conversations/c"

    def test_get_missing_key_param(self, client):
        """Returns 400 when the integration key param is missing."""
        response = client.get(
            "/conversation-name",
            headers=_auth_header(),
        )
        assert response.status_code == 400

    def test_get_nonexistent_key(self, client):
        """Returns empty string for nonexistent integration key."""
        with patch.object(redis_client, "get", return_value=None):
            response = client.get(
                "/conversation-name?conversationIntegrationKey=unknown",
                headers=_auth_header(),
            )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["conversationName"] == ""


class TestDeleteConversationName:
    """Tests for DELETE /conversation-name."""

    def test_delete_existing_mapping(self, client):
        """Deletes an existing mapping and returns 200."""
        with patch.object(redis_client, "delete", return_value=1):
            response = client.delete(
                "/conversation-name?conversationIntegrationKey=18005551234",
                headers=_auth_header(),
            )
        assert response.status_code == 200

    def test_delete_nonexistent_key(self, client):
        """Returns 404 when the integration key does not exist."""
        with patch.object(redis_client, "delete", return_value=0):
            response = client.delete(
                "/conversation-name?conversationIntegrationKey=unknown",
                headers=_auth_header(),
            )
        assert response.status_code == 404

    def test_delete_missing_key_param(self, client):
        """Returns 400 when the integration key param is missing."""
        response = client.delete(
            "/conversation-name",
            headers=_auth_header(),
        )
        assert response.status_code == 400
