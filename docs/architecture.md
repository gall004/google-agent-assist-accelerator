# System Architecture

## Overview

The Google Agent Assist Accelerator consists of four primary services and supporting infrastructure that bridge Google's Agent Assist API with agent desktop UIs.

## Data Flow

```
                    ┌─────────────────────────────────────────────┐
                    │                 GCP                          │
                    │                                             │
┌────────────┐     │  ┌──────────┐    ┌────────────────────┐     │
│ Dialogflow │─────┼─▶│ Pub/Sub  │───▶│ Cloud Pub/Sub      │     │
│ Agent      │     │  │ Topics   │    │ Interceptor        │     │
│ Assist     │     │  │ (4 types)│    │ (Cloud Run)        │     │
└────────────┘     │  └──────────┘    └─────────┬──────────┘     │
                    │                            │                │
                    │                            ▼                │
                    │                   ┌────────────────┐        │
                    │                   │ Redis          │        │
                    │                   │ (Memorystore)  │        │
                    │                   └────────┬───────┘        │
                    │                            │                │
                    │                   ┌────────▼───────┐        │
                    │                   │ UI Connector   │        │
                    │                   │ (Cloud Run)    │        │
                    │                   └────────┬───────┘        │
                    └────────────────────────────┼────────────────┘
                                                 │ WebSocket
                                                 ▼
                                        ┌────────────────┐
                                        │ Agent Desktop  │
                                        │ UI (React)     │
                                        └────────────────┘
```

## Services

### Cloud Pub/Sub Interceptor
- **Runtime:** Python 3.12 / Flask
- **Deploy target:** Cloud Run
- **Responsibility:** Receives Agent Assist event notifications from 4 Pub/Sub topics and publishes them to Redis Pub/Sub channels keyed by `{connector_id}:{conversation_name}`.

### UI Connector
- **Runtime:** Python 3.12 / Flask + SocketIO
- **Deploy target:** Cloud Run
- **Responsibility:** Manages WebSocket connections with agent desktops, subscribes to Redis Pub/Sub channels, proxies Dialogflow API requests, and handles JWT-based authentication.

### UI (React)
- **Runtime:** Node 20 / React + Vite
- **Deploy target:** Cloud Run (static build) or CDN
- **Responsibility:** Agent-facing desktop UI that integrates Google's Agent Assist UI modules. Connects to UI Connector via WebSocket for real-time suggestions.

### Sidecar
- **Runtime:** Node 20 / React + Vite
- **Deploy target:** Local development / demo environments
- **Responsibility:** Simulates phone calls, dispatches test events, and provides controls for local development without requiring a live telephony system.

## Event Types

| Pub/Sub Topic | Event Payload | Source |
|---|---|---|
| `human-agent-assistant-event` | `HumanAgentAssistantEvent` | Agent Assist suggestions |
| `conversation-lifecycle-event` | `ConversationEvent` | Conversation start/end |
| `new-message-event` | `ConversationEvent` | New messages |
| `new-recognition-result-notification-event` | `ConversationEvent` | Speech recognition results |

## Infrastructure

All infrastructure is managed via Terraform modules under `infra/`:

| Module | Resources |
|---|---|
| `cloud-run` | Cloud Run services for Interceptor and Connector |
| `redis` | Memorystore for Redis instance |
| `pubsub` | Pub/Sub topics and push subscriptions |
| `networking` | Serverless VPC Connector, firewall rules |
| `iam` | Service accounts and IAM role bindings |
