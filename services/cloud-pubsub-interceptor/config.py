"""Configuration module for the Cloud Pub/Sub Interceptor service.

Centralizes all environment variable loading with sane defaults.
All config values are read from environment variables per the
zero-hardcoding policy defined in security-and-config.md.
"""

import os


# --- GCP Configuration ---
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")

# --- Redis Configuration ---
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# --- Pub/Sub Subscription IDs ---
# Each maps to one of the 4 Agent Assist event types.
SUBSCRIPTION_HUMAN_AGENT_ASSISTANT = os.environ.get(
    "SUBSCRIPTION_HUMAN_AGENT_ASSISTANT",
    "human-agent-assistant-event-sub",
)
SUBSCRIPTION_CONVERSATION_LIFECYCLE = os.environ.get(
    "SUBSCRIPTION_CONVERSATION_LIFECYCLE",
    "conversation-lifecycle-event-sub",
)
SUBSCRIPTION_NEW_MESSAGE = os.environ.get(
    "SUBSCRIPTION_NEW_MESSAGE",
    "new-message-event-sub",
)
SUBSCRIPTION_RECOGNITION_RESULT = os.environ.get(
    "SUBSCRIPTION_RECOGNITION_RESULT",
    "new-recognition-result-notification-event-sub",
)

# --- Logging ---
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# --- Health Check ---
HEALTH_CHECK_PORT = int(os.environ.get("PORT", 8080))
