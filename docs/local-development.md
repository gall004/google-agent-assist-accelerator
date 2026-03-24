# Local Development

## Prerequisites

- [Docker Desktop](https://docs.docker.com/get-docker/) (for Redis)
- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js 22+](https://nodejs.org/) (LTS)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (for integration tests)

## One-Time Setup

```bash
# 1. Clone and configure
git clone https://github.com/gall004/google-agent-assist-accelerator.git
cd google-agent-assist-accelerator
cp .env.example .env

# 2. Install root dev dependencies (concurrently)
npm install

# 3. Install service dependencies
cd services/ui && npm install && cd ../..
cd services/sidecar && npm install && cd ../..

# 4. Set up the Python backend
cd services/ui-connector
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd ../..
```

Edit `.env` with your values. For a local-only test of the CTI → Soft Pop flow, the defaults work as-is. Set `AUTH_OPTION=Skip` to bypass JWT authentication.

## Start Everything (Single Command)

```bash
npm run dev
```

This starts all four services in one terminal with color-coded output:

| Prefix | Service | Port | Hot Reload |
|---|---|---|---|
| `redis` | Redis (Docker) | 6379 | N/A |
| `connector` | UI Connector (Python) | 8080 | No (restart manually) |
| `ui` | Agent Assist Widget (Vite) | 5173 | ✅ Yes |
| `sidecar` | Dynamics CRM Simulator (Vite) | 5174 | ✅ Yes |

> **Note:** The ui-connector requires an activated `.venv` in your shell before running `npm run dev`. If you get import errors, run `source services/ui-connector/.venv/bin/activate` first.

## Stop Everything

```bash
# Ctrl+C to stop all services, then:
npm run dev:stop     # stops the Redis container
npm run dev:reset    # stops Redis AND clears persisted data
```

## Test the End-to-End Flow

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

## Running Services Individually

If you prefer separate terminals (e.g., to isolate logs):

```bash
# Terminal 1: Redis
docker compose up -d redis

# Terminal 2: UI Connector
cd services/ui-connector && source .venv/bin/activate
export $(grep -v '^#' ../../.env | xargs)
python main.py

# Terminal 3: UI
cd services/ui && npm run dev

# Terminal 4: Sidecar
cd services/sidecar && npm run dev
```
