"""Identity provider authentication adapters.

Implements token verification for supported CCaaS/CRM platforms:
Salesforce, SalesforceLWC, GenesysCloud, and Twilio.

Ported from Google's auth_options.py with:
- Explicit timeouts on all HTTP requests (10 seconds).
- Proper error logging in catch blocks.
- Complete docstrings.
"""

import logging
from urllib.parse import urlencode

import requests

import config

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10  # seconds


def check_salesforce_token(token):
    """Verify an access token using Salesforce OpenID Connect.

    Args:
        token: The Salesforce OAuth access token.

    Returns:
        True if the token belongs to the configured Salesforce organization.

    Raises:
        requests.RequestException: On network failure (logged, returns False).
    """
    try:
        response = requests.get(
            f"https://{config.SALESFORCE_DOMAIN}/services/oauth2/userinfo",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            user_info = response.json()
            if user_info.get("organization_id") == config.SALESFORCE_ORGANIZATION_ID:
                return True
            logger.warning(
                "Salesforce org mismatch for user %s", user_info.get("user_id")
            )
        else:
            logger.warning(
                "Salesforce token verification failed: %s %s",
                response.status_code,
                response.reason,
            )
    except requests.RequestException:
        logger.error("Salesforce token verification request failed", exc_info=True)
    return False


def check_salesforce_lwc_token(token):
    """Verify Salesforce Org ID using Client Credentials OAuth flow.

    Uses the token to call the oauth2/userinfo endpoint and compare
    the organization ID against the configured value.

    Args:
        token: An access_token from the Salesforce OAuth2/token endpoint.

    Returns:
        True if the access org ID matches config, False otherwise.
    """
    import re

    access_token = re.sub(r"Bearer ", "", token, flags=re.IGNORECASE)

    if not config.SALESFORCE_ORGANIZATION_ID:
        logger.error("SALESFORCE_ORGANIZATION_ID is not set. Auth will fail.")
        return False

    try:
        response = requests.get(
            f"https://{config.SALESFORCE_DOMAIN}/services/oauth2/userinfo?"
            + urlencode({"access_token": access_token}),
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            user_info = response.json()
            user_org = user_info.get("organization_id", "")
            config_org = config.SALESFORCE_ORGANIZATION_ID
            min_len = min(len(user_org), len(config_org))
            if min_len and user_org[:min_len] == config_org[:min_len]:
                return True
            logger.warning(
                "Salesforce LWC org mismatch for user %s",
                user_info.get("user_id"),
            )
        else:
            logger.warning(
                "Salesforce LWC token verification failed: %s %s",
                response.status_code,
                response.reason,
            )
    except requests.RequestException:
        logger.error("Salesforce LWC verification request failed", exc_info=True)
    return False


def check_genesyscloud_token(token):
    """Verify a Genesys Cloud token via the Users API.

    Args:
        token: A Genesys Cloud bearer token.

    Returns:
        True if the token is valid (200 response from /api/v2/users/me).
    """
    try:
        response = requests.get(
            f"https://api.{config.GENESYS_CLOUD_ENVIRONMENT}/api/v2/users/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return True
        logger.warning(
            "Genesys Cloud token verification failed: %s %s",
            response.status_code,
            response.reason,
        )
    except requests.RequestException:
        logger.error("Genesys Cloud verification request failed", exc_info=True)
    return False


def check_twilio_token(token):
    """Verify a Twilio Flex plugin token.

    Args:
        token: A Twilio flex plugin token.

    Returns:
        True if the verification endpoint returns 200.
    """
    if not config.TWILIO_FLEX_ENVIRONMENT:
        logger.error("TWILIO_FLEX_ENVIRONMENT is not set. Auth will fail.")
        return False

    try:
        response = requests.post(
            f"https://{config.TWILIO_FLEX_ENVIRONMENT}/verify",
            json={"Token": token},
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return True
        logger.warning(
            "Twilio token verification failed: %s %s",
            response.status_code,
            response.reason,
        )
    except requests.RequestException:
        logger.error("Twilio verification request failed", exc_info=True)
    return False


def check_twilio_app_auth(auth_data):
    """Verify Twilio application-level auth using Account API.

    Args:
        auth_data: Dict with 'accountSid' and 'authToken' keys.

    Returns:
        True if the Account API validates the credentials.
    """
    if config.APP_AUTH_OPTION != "Twilio" or not config.TWILIO_ACCOUNT_SID:
        return False

    try:
        response = requests.get(
            config.TWILIO_ACCOUNTS_API_URL,
            auth=(auth_data.get("accountSid", ""), auth_data.get("authToken", "")),
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("sid") == config.TWILIO_ACCOUNT_SID:
                return True
    except requests.RequestException:
        logger.error("Twilio app auth request failed", exc_info=True)
    return False
