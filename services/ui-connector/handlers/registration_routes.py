"""JWT registration routes for the UI Connector.

Provides /register and /register-app endpoints for agent desktops
to obtain JWT tokens after authenticating with their platform credentials.
Extracted from Google's main.py lines 98–115.
"""

import logging

from flask import Blueprint, request, make_response, jsonify

from auth import check_auth, generate_jwt, check_app_auth

logger = logging.getLogger(__name__)

registration_bp = Blueprint("registration", __name__)


@registration_bp.route("/register", methods=["POST"])
def register_token():
    """Register a JWT token after verifying the user's platform credentials.

    The Authorization header is validated against the configured identity
    provider (Salesforce, GenesysCloud, Twilio, etc.).

    Returns:
        200 with JWT token on success, 401 on authentication failure.
    """
    auth = request.headers.get("Authorization", "")
    if not check_auth(auth):
        logger.warning("Token registration failed: authentication rejected")
        return make_response(
            "Could not authenticate user",
            401,
            {"Authentication": "valid token required"},
        )

    user_info = request.get_json(force=True, silent=True)
    token = generate_jwt(user_info)
    logger.info("JWT registered successfully")
    return jsonify({"token": token})


@registration_bp.route("/register-app", methods=["POST"])
def register_app_token():
    """Register a JWT token after verifying application-level credentials.

    Used for server-to-server authentication (e.g. Twilio accountSid/authToken).

    Returns:
        200 with JWT token on success, 401 on authentication failure.
    """
    data = request.get_json()
    if not data:
        return make_response("Request body required", 400)

    if not check_app_auth(data):
        logger.warning("App token registration failed: authentication rejected")
        return make_response(
            "Could not authenticate application",
            401,
            {"Authentication": "valid application level auth required"},
        )

    token = generate_jwt(data)
    logger.info("App JWT registered successfully")
    return jsonify({"token": token})
