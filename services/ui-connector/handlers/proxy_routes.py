"""Dialogflow proxy routes for the UI Connector.

Forwards authenticated requests from the agent desktop to the
Dialogflow API. Extracted from Google's main.py lines 118–184.
"""

import gzip
import logging

from flask import Blueprint, request

import dialogflow
from auth import token_required

logger = logging.getLogger(__name__)

proxy_bp = Blueprint("proxy", __name__)


def _call_dialogflow(location):
    """Forward a request to the Dialogflow API and return the response.

    Args:
        location: The Dialogflow API location (e.g. 'global').

    Returns:
        A tuple of (body, status_code, headers) for Flask to return.
    """
    logger.info("Proxying %s %s", request.method, request.full_path)
    try:
        if request.method == "GET":
            response = dialogflow.get_dialogflow(location, request.full_path)
        elif request.method == "POST":
            data = None if request.path.endswith(":complete") else request.get_json()
            response = dialogflow.post_dialogflow(location, request.full_path, data)
        else:
            response = dialogflow.patch_dialogflow(
                location, request.full_path, request.get_json()
            )

        logger.info(
            "Dialogflow response: status=%s", response.status_code
        )
        return response.raw.data, response.status_code, response.headers.items()

    except Exception:
        logger.error("Dialogflow proxy failed for %s", request.full_path, exc_info=True)
        return "Upstream service error", 502


# --- Routes without tail path ---

@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/conversations",
    methods=["POST"],
)
@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/suggestions:searchKnowledge",
    methods=["POST"],
)
@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/statelessSuggestion:generate",
    methods=["POST"],
)
@token_required
def call_dialogflow_without_tail(version, project, location):
    """Proxy Dialogflow requests that have no tail path component."""
    return _call_dialogflow(location)


# --- Routes with tail path ---

@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/answerRecords/<path:tail>",
    methods=["PATCH"],
)
@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/conversations/<path:tail>",
    methods=["GET", "POST", "PATCH"],
)
@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/conversationProfiles/<path:tail>",
    methods=["GET"],
)
@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/conversationModels/<path:tail>",
    methods=["GET"],
)
@proxy_bp.route(
    "/<version>/projects/<project>/locations/<location>/generators/<path:tail>",
    methods=["GET"],
)
@token_required
def call_dialogflow_with_tail(version, project, location, tail):
    """Proxy Dialogflow requests that include a tail path component."""
    return _call_dialogflow(location)
