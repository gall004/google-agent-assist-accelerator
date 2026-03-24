"""JWT authentication module for the UI Connector service.

Handles JWT generation, validation, and the multi-provider auth dispatch.
Ported from Google's auth.py with governance upgrades:
- JWT secret loaded from environment variable instead of file mount.
- Explicit error logging in catch blocks.
- Proper docstrings on all public functions.
"""

import datetime
import logging
from functools import wraps

import jwt
from flask import request, jsonify

import config
import auth_options

logger = logging.getLogger(__name__)


def check_auth(token):
    """Dispatch authentication to the configured identity provider.

    Args:
        token: The authorization token from the client request.

    Returns:
        True if the token is valid for the configured provider, False otherwise.
    """
    provider = config.AUTH_OPTION

    if provider == "SalesforceLWC":
        return auth_options.check_salesforce_lwc_token(token)
    elif provider == "Salesforce":
        return auth_options.check_salesforce_token(token)
    elif provider == "GenesysCloud":
        return auth_options.check_genesyscloud_token(token)
    elif provider == "Twilio":
        return auth_options.check_twilio_token(token)
    elif provider == "Skip":
        logger.warning("AUTH_OPTION='Skip' — token verification bypassed")
        return True

    logger.warning("Unknown AUTH_OPTION '%s', rejecting authentication", provider)
    return False


def check_jwt(token):
    """Validate a JWT token.

    Args:
        token: The encoded JWT string.

    Returns:
        A tuple of (is_valid: bool, message: str).
    """
    try:
        data = jwt.decode(
            token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )
        if "gcp_agent_assist_project" not in data:
            return False, "The target project in your token is missing."
        if data["gcp_agent_assist_project"] != config.GCP_PROJECT_ID:
            return False, "The target project in your token is invalid."
        if "exp" not in data:
            return False, "The expiration time in your token is missing."
        if data["exp"] < datetime.datetime.now(datetime.timezone.utc).timestamp():
            return False, "Your token has expired."
        return True, "Your token is valid."
    except jwt.ExpiredSignatureError:
        return False, "Your token has expired."
    except jwt.InvalidTokenError as exc:
        logger.error("JWT validation failed: %s", exc)
        return False, "Failed to parse your token."


def generate_jwt(user_info=None):
    """Generate a short-lived JWT for an authenticated agent desktop.

    Args:
        user_info: Optional dict with user metadata to embed in the token.

    Returns:
        The encoded JWT string.
    """
    gcp_agent_assist_user = ""
    if user_info:
        gcp_agent_assist_user = user_info.get("gcp_agent_assist_user", "")

    payload = {
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=config.JWT_TOKEN_LIFETIME),
        "gcp_agent_assist_project": config.GCP_PROJECT_ID,
        "gcp_agent_assist_user": gcp_agent_assist_user,
    }
    return jwt.encode(payload, config.JWT_SECRET_KEY, config.JWT_ALGORITHM)


def check_app_auth(auth_data):
    """Validate application-level authentication (e.g. Twilio).

    Args:
        auth_data: Dict containing app credentials.

    Returns:
        True if application auth succeeds, False otherwise.
    """
    if config.APP_AUTH_OPTION == "Twilio":
        return auth_options.check_twilio_app_auth(auth_data)
    return False


def token_required(func):
    """Decorator that verifies JWT before allowing endpoint access.

    Returns 401 with a descriptive message if the token is missing or invalid.
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing."}), 401
        is_valid, message = check_jwt(token)
        if is_valid:
            return func(*args, **kwargs)
        return jsonify({"message": message}), 401

    return decorator
