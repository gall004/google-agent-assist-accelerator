# Local Development

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for running services outside Docker)
- Node.js 20+ (for React services outside Docker)
- Google Cloud SDK (for integration tests and deployment)

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/gall004/google-agent-assist-accelerator.git
cd google-agent-assist-accelerator

# 2. Configure environment
cp .env.example .env
# Edit .env with your GCP project values

# 3. Start all services
docker compose up --build
```

This starts:
- **Redis** on `localhost:6379`
- **Cloud Pub/Sub Interceptor** on `localhost:8081`
- **UI Connector** on `localhost:8080`
- **UI** on `localhost:3000`
- **Sidecar** on `localhost:5173`

## Running Individual Services

### Python Services

```bash
cd services/ui-connector

# Create virtual env
python -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Run
python main.py
```

### React Services

```bash
cd services/ui
npm ci
npm run dev
```

## Testing Locally

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full testing guide.

```bash
# Python unit tests
cd services/ui-connector && pytest tests/unit/ -v

# React unit tests
cd services/ui && npx vitest run
```
