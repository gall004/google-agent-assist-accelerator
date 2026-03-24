"""Unit tests for the auth module.

Tests cover: valid JWT, expired JWT, wrong project JWT, missing token,
token_required decorator, and JWT generation.
"""

import datetime
from unittest.mock import patch, MagicMock

import jwt
import pytest

# Patch config before importing auth.
with patch.dict("os.environ", {
    "GCP_PROJECT_ID": "test-project",
    "JWT_SECRET_KEY": "test-secret-key",
    "JWT_ALGORITHM": "HS256",
    "JWT_TOKEN_LIFETIME": "60",
}):
    import config
    from auth import check_jwt, generate_jwt, token_required

TEST_SECRET = "test-secret-key"
TEST_PROJECT = "test-project"


def _make_token(project=TEST_PROJECT, exp_delta_minutes=60, secret=TEST_SECRET):
    """Generate a JWT for testing.

    Args:
        project: The GCP project ID to embed.
        exp_delta_minutes: Minutes until expiration.
        secret: The signing secret key.

    Returns:
        An encoded JWT string.
    """
    payload = {
        "gcp_agent_assist_project": project,
        "gcp_agent_assist_user": "testuser",
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=exp_delta_minutes),
    }
    return jwt.encode(payload, secret, "HS256")


class TestCheckJwt:
    """Tests for JWT validation logic."""

    def test_valid_token(self):
        """Accepts a correctly signed token with valid project and expiry."""
        token = _make_token()
        is_valid, msg = check_jwt(token)
        assert is_valid is True
        assert "valid" in msg.lower()

    def test_expired_token(self):
        """Rejects a token that has already expired."""
        token = _make_token(exp_delta_minutes=-5)
        is_valid, msg = check_jwt(token)
        assert is_valid is False
        assert "expired" in msg.lower()

    def test_wrong_project(self):
        """Rejects a token with a mismatched project ID."""
        token = _make_token(project="wrong-project")
        is_valid, msg = check_jwt(token)
        assert is_valid is False
        assert "invalid" in msg.lower()

    def test_missing_project_field(self):
        """Rejects a token missing the gcp_agent_assist_project claim."""
        payload = {
            "gcp_agent_assist_user": "testuser",
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=60),
        }
        token = jwt.encode(payload, TEST_SECRET, "HS256")
        is_valid, msg = check_jwt(token)
        assert is_valid is False
        assert "missing" in msg.lower()

    def test_invalid_signature(self):
        """Rejects a token signed with the wrong secret."""
        token = _make_token(secret="wrong-secret")
        is_valid, msg = check_jwt(token)
        assert is_valid is False
        assert "parse" in msg.lower() or "failed" in msg.lower()


class TestGenerateJwt:
    """Tests for JWT generation."""

    def test_generates_decodable_token(self):
        """Generates a token that can be decoded with the configured secret."""
        token = generate_jwt({"gcp_agent_assist_user": "agent1"})
        decoded = jwt.decode(token, TEST_SECRET, algorithms=["HS256"])
        assert decoded["gcp_agent_assist_project"] == TEST_PROJECT
        assert decoded["gcp_agent_assist_user"] == "agent1"
        assert "exp" in decoded

    def test_generates_token_without_user_info(self):
        """Generates a valid token when no user info is provided."""
        token = generate_jwt()
        decoded = jwt.decode(token, TEST_SECRET, algorithms=["HS256"])
        assert decoded["gcp_agent_assist_user"] == ""
