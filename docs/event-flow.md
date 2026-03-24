# Event Flow

## Overview

Agent Assist publishes event notifications to Cloud Pub/Sub topics configured in conversation profiles. Four distinct topic types carry different event payloads.

## Event Types & Schemas

### 1. Human Agent Assistant Event
- **Topic:** `human-agent-assistant-event`
- **Payload:** [HumanAgentAssistantEvent](https://cloud.google.com/dialogflow/es/docs/reference/rest/v2beta1/HumanAgentAssistantEvent)
- **Content:** Agent Assist suggestions (FAQ, Smart Reply, summarization, etc.)

### 2. Conversation Lifecycle Event
- **Topic:** `conversation-lifecycle-event`
- **Payload:** [ConversationEvent](https://cloud.google.com/dialogflow/es/docs/reference/rest/v2beta1/ConversationEvent)
- **Content:** Conversation start/end notifications
- **Example:**
  ```json
  {
    "conversation": "projects/your-project-id/locations/global/conversations/your-conversation-id",
    "type": "CONVERSATION_STARTED"
  }
  ```

### 3. New Message Event
- **Topic:** `new-message-event`
- **Payload:** [ConversationEvent](https://cloud.google.com/dialogflow/es/docs/reference/rest/v2beta1/ConversationEvent)
- **Content:** New messages from either participant

### 4. New Recognition Result Notification
- **Topic:** `new-recognition-result-notification-event`
- **Payload:** `ConversationEvent` with additional Pub/Sub attributes (`participant_role`, `message_id`)
- **Content:** Real-time speech recognition results

## Processing Pipeline

```
Dialogflow → Pub/Sub Topic → Push to Interceptor HTTP endpoint
  → Interceptor decodes & publishes to Redis channel {connector_id}:{conversation_name}
    → UI Connector subscribes to Redis channel {connector_id}:*
      → UI Connector pushes event via WebSocket to Agent Desktop
```

## Redis Channel Format

- **Key pattern:** `{connector_id}:{conversation_name}`
- **Mapping stored:** `<conversation_name, connector_id>` in Redis
- Each UI Connector instance subscribes to its own wildcard channel `{connector_id}:*`
