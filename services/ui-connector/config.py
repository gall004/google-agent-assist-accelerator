"""Configuration module for the UI Connector service.

Centralizes all environment variable loading with sane defaults.
Replaces Google's original config.py with governance-compliant
patterns (no hardcoded secrets, no wildcard CORS).
"""

import os


# --- GCP Configuration ---
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")

# --- Redis Configuration ---
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# --- JWT Configuration ---
# In production, loaded from Google Secret Manager via Cloud Run secret mounting.
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_TOKEN_LIFETIME = int(os.environ.get("JWT_TOKEN_LIFETIME", 60))  # minutes

# --- CORS Configuration ---
# Comma-separated list of allowed origins. Never use '*' in production.
_cors_raw = os.environ.get("ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_raw.split(",") if o.strip()] or ["*"]

# --- Authentication Options ---
# Supported: 'SalesforceLWC', 'Salesforce', 'GenesysCloud', 'Twilio', 'Skip'
AUTH_OPTION = os.environ.get("AUTH_OPTION", "")
APP_AUTH_OPTION = os.environ.get("APP_AUTH_OPTION", "")

# --- Salesforce Configuration ---
SALESFORCE_DOMAIN = os.environ.get("SALESFORCE_DOMAIN", "login.salesforce.com")
SALESFORCE_ORGANIZATION_ID = os.environ.get("SALESFORCE_ORGANIZATION_ID", "")

# --- Genesys Cloud Configuration ---
GENESYS_CLOUD_ENVIRONMENT = os.environ.get(
    "GENESYS_CLOUD_ENVIRONMENT", "mypurecloud.com"
)

# --- Twilio Configuration ---
TWILIO_FLEX_ENVIRONMENT = os.environ.get("TWILIO_FLEX_ENVIRONMENT", "")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_ACCOUNTS_API_URL = (
    f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}.json"
)

# --- Logging ---
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# --- Server ---
PORT = int(os.environ.get("PORT", 8080))
