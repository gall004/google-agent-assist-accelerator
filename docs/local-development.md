# Local Development

## Prerequisites

- [Docker Desktop](https://docs.docker.com/get-docker/) (for Redis)
- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js 22+](https://nodejs.org/) (LTS)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (for integration tests)

## Step 1: Environment Setup

```bash
# Clone and configure
git clone https://github.com/gall004/google-agent-assist-accelerator.git
cd google-agent-assist-accelerator
cp .env.example .env
```

Edit `.env` with your values. For a local-only test of the CTI → Soft Pop flow, the defaults work as-is. Set `AUTH_OPTION=Skip` to bypass JWT authentication.

## Step 2: Start Redis

Redis runs via Docker Compose, simulating the Google Cloud Memorystore boundary used in production.

```bash
docker compose up -d redis
```

Verify it's healthy:

```bash
docker compose ps
# Should show redis service as "healthy"
```

> **Note:** Redis data persists in a Docker volume (`redis-data`). Run `docker compose down -v` to clear it.

## Step 3: Start the UI Connector (Terminal 1)

```bash
cd services/ui-connector
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Load env vars from root
export $(grep -v '^#' ../../.env | xargs)
python main.py
```

Runs on **http://localhost:8080**. You should see: `Redis Pub/Sub listener started`.

## Step 4: Start the UI Service (Terminal 2)

```bash
cd services/ui
npm install
npm run dev
```

Runs on **http://localhost:5173**. The Active Call Bar shows a green "Connected" dot once the ui-connector is reachable.

## Step 5: Start the Sidecar Simulator (Terminal 3)

```bash
cd services/sidecar
npm install
npm run dev
```

Runs on **http://localhost:5174**. This is your main testing surface.

## Step 6: Test the End-to-End Flow

1. Open **http://localhost:5174** in your browser
2. You'll see the mock Dynamics 365 layout with:
   - Left sidebar, main content ("No customer record selected"), CTI Developer Panel, and the Agent Assist iframe on the right
3. **Click "📞 Start Call"** — Soft Pop toast slides in from the top-right of the iframe
4. **Click the Soft Pop notification** — CRM record updates with caller details
5. **Click "✅ Answer Call"** — status bar changes to CONNECTED
6. **Click "⏹ End Call"** — status changes to ENDED

### What You're Validating

| Flow | What to Observe |
|---|---|
| WebSocket | Green "Connected" dot in the ui status bar |
| CTI Events | Status bar: RINGING → CONNECTED → ENDED |
| Soft Pop | Toast slides in, auto-dismisses after 15s |
| postMessage | Clicking Soft Pop updates CRM record in sidecar |

> **Note:** The Google Agent Assist Container V2 will show connection errors without a real `CONVERSATION_PROFILE`. This is expected — it lights up once connected to a live Dialogflow backend.

## Running Tests

```bash
# Python (ui-connector)
cd services/ui-connector && pytest tests/unit/ -v

# React (ui)
cd services/ui && npx vitest run

# React (sidecar)
cd services/sidecar && npx vitest run
```

## Stopping Services

```bash
# Stop Redis
docker compose down

# Stop Redis and clear data
docker compose down -v
```
