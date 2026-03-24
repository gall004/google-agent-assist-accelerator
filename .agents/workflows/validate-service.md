---
description: Validate services via unit tests, integration tests, and smoke tests
---

# Validate Service Workflow

Execute this workflow to validate services after code changes or deployment.

1. Run unit tests for changed Python services:
   ```bash
   cd services/<service-name> && pytest tests/unit/ -v --tb=short
   ```

2. Run unit tests for changed React services:
   ```bash
   cd services/<service-name> && npx vitest run
   ```

3. Run integration tests (requires GCP credentials):
   ```bash
   cd services/<service-name> && pytest tests/integration/ -v --tb=short -m integration
   ```

4. Smoke test deployed services by hitting the health endpoint:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" "${SERVICE_URL}/healthz"
   ```

5. Verify the response is `200`. If not, check the service logs:
   ```bash
   gcloud run services logs read <service-name> --limit=50
   ```

6. For ui-connector, validate WebSocket connectivity:
   ```bash
   # Use wscat or equivalent to test SocketIO handshake
   curl -s "${UI_CONNECTOR_URL}/socket.io/?EIO=4&transport=polling"
   ```

7. **🛑 STOP — Present all test results and health check outputs to the user for review.**
