# Google Agent Assist Accelerator

An enterprise-grade, production-ready integration layer for [Google Agent Assist](https://cloud.google.com/agent-assist/docs). This accelerator extends Google's published architecture with custom features, improved reliability patterns, and a modular design for embedding Agent Assist into various CRM and CCaaS platforms.

## Architecture Overview

```
┌──────────────┐     ┌──────────────────────┐     ┌───────────────┐
│  Dialogflow  │────▶│  Cloud Pub/Sub Topics │────▶│  Pub/Sub      │
│  Agent Assist│     │  (4 event types)      │     │  Interceptor  │
└──────────────┘     └──────────────────────┘     └───────┬───────┘
                                                          │
                                                          ▼
┌──────────────┐     ┌──────────────────────┐     ┌───────────────┐
│  Agent       │◀───▶│  UI Connector        │◀───▶│  Redis        │
│  Desktop UI  │     │  (WebSocket + REST)  │     │  (Memorystore)│
└──────────────┘     └──────────────────────┘     └───────────────┘
```

**Event flow:** Dialogflow publishes Agent Assist events → Pub/Sub topics → Interceptor processes and forwards to Redis → UI Connector subscribes and pushes to the Agent Desktop via WebSocket.

## Directory Structure

```
├── .agents/                    # Governance rules & workflows
│   ├── rules/                  # Always-on coding rules
│   └── workflows/              # SDLC, scaffold, deploy, validate
├── .github/                    # CI/CD pipelines & PR template
│   └── workflows/              # ci, deploy-staging, deploy-production, release
├── services/
│   ├── cloud-pubsub-interceptor/   # Python/Flask — Pub/Sub → Redis bridge
│   ├── ui-connector/               # Python/Flask — WebSocket relay + Dialogflow proxy
│   ├── ui/                         # React — Agent Assist frontend
│   └── sidecar/                    # React — Local dev simulator
├── infra/                      # Terraform IaC for GCP resources
├── scripts/                    # Operational scripts
└── docs/                       # Cross-cutting documentation
```

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js 22+](https://nodejs.org/) (LTS)
- [Docker](https://docs.docker.com/get-docker/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Terraform 1.7+](https://developer.hashicorp.com/terraform/downloads)
- A GCP project with Agent Assist, Dialogflow, Pub/Sub, Memorystore, and Secret Manager APIs enabled

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Service | Description |
|---|---|---|
| `GCP_PROJECT_ID` | All | Your GCP project ID |
| `GCP_REGION` | All | GCP region (default: `us-central1`) |
| `REDIS_HOST` | Interceptor, Connector | Redis/Memorystore host |
| `REDIS_PORT` | Interceptor, Connector | Redis port (default: `6379`) |
| `JWT_SECRET_KEY` | Connector | JWT signing key (Secret Manager in prod) |
| `ALLOWED_ORIGINS` | Connector | Comma-separated CORS origins |
| `AUTH_OPTION` | Connector | Auth provider: `Salesforce`, `GenesysCloud`, `Twilio`, `Skip` |
| `SUBSCRIPTION_*` | Interceptor | Pub/Sub subscription IDs (4 event types) |
| `LOG_LEVEL` | All | Logging level (default: `INFO`) |
| `VITE_UI_CONNECTOR_URL` | UI | URL of the UI Connector service |

See `.env.example` for the complete list with descriptions.

## Local Development

```bash
# One-time setup
cp .env.example .env
npm install

# Start all services (Redis + connector + ui + sidecar)
npm run dev
```

See [docs/local-development.md](docs/local-development.md) for the full setup guide.
## Deployment

Services are deployed to **Google Cloud Run** via GitHub Actions:

- **Staging:** Auto-deploys on merge to `develop`
- **Production:** Deploys on merge to `main` (requires GitHub Environment approval)

See `docs/architecture.md` for the full deployment architecture.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow, testing standards, and coding guidelines.

## License

See [LICENSE](LICENSE) for details.
