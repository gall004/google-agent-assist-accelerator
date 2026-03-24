"""Dialogflow API proxy utilities.

Provides authorized HTTP proxy methods for forwarding requests from
the agent desktop to the Dialogflow API. Uses Google Application
Default Credentials with explicit timeouts.
"""

import logging

import google.auth
from google.auth.transport.requests import AuthorizedSession

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 30  # seconds

CREDENTIALS, PROJECT_ID = google.auth.default(
    scopes=["https://www.googleapis.com/auth/dialogflow"]
)
AUTHED_SESSION = AuthorizedSession(CREDENTIALS)


def get_target_url(location, path):
    """Build the Dialogflow API URL for a given location and path.

    Args:
        location: The Dialogflow location (e.g. 'global', 'us-central1').
        path: The API request path.

    Returns:
        The full Dialogflow API URL.
    """
    if location == "global":
        return f"https://dialogflow.googleapis.com/{path}"
    return f"https://{location}-dialogflow.googleapis.com/{path}"


def get_dialogflow(location, path):
    """Forward a GET request to the Dialogflow API.

    Args:
        location: The Dialogflow location.
        path: The API request path.

    Returns:
        The requests.Response object from Dialogflow.

    Raises:
        requests.RequestException: On network failure (logged and re-raised).
    """
    url = get_target_url(location, path)
    logger.debug("GET %s", url)
    try:
        return AUTHED_SESSION.get(url, stream=True, timeout=REQUEST_TIMEOUT)
    except Exception:
        logger.error("Dialogflow GET failed: %s", url, exc_info=True)
        raise


def post_dialogflow(location, path, data=None):
    """Forward a POST request to the Dialogflow API.

    Args:
        location: The Dialogflow location.
        path: The API request path.
        data: Optional JSON payload dict.

    Returns:
        The requests.Response object from Dialogflow.

    Raises:
        requests.RequestException: On network failure (logged and re-raised).
    """
    url = get_target_url(location, path)
    logger.debug("POST %s", url)
    try:
        return AUTHED_SESSION.post(
            url, json=data, stream=True, timeout=REQUEST_TIMEOUT
        )
    except Exception:
        logger.error("Dialogflow POST failed: %s", url, exc_info=True)
        raise


def patch_dialogflow(location, path, data):
    """Forward a PATCH request to the Dialogflow API.

    Args:
        location: The Dialogflow location.
        path: The API request path.
        data: The JSON payload dict.

    Returns:
        The requests.Response object from Dialogflow.

    Raises:
        requests.RequestException: On network failure (logged and re-raised).
    """
    url = get_target_url(location, path)
    logger.debug("PATCH %s", url)
    try:
        return AUTHED_SESSION.patch(
            url, json=data, stream=True, timeout=REQUEST_TIMEOUT
        )
    except Exception:
        logger.error("Dialogflow PATCH failed: %s", url, exc_info=True)
        raise
