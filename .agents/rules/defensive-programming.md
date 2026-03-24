---
trigger: always_on
description: Error Handling & Graceful Degradation
---

## 1. Defensive Input Validation
* **Rule:** All public-facing endpoints must validate input before processing. Never trust client-provided data.
* **Enforcement:**
  * Validate required fields exist and are of expected types.
  * Return descriptive `400 Bad Request` responses for malformed input.
  * Log invalid requests at `WARNING` level for observability.

## 2. Upstream Failure Handling
* **Rule:** All calls to external services (Dialogflow API, Redis, Pub/Sub) must include timeout configuration and graceful error handling.
* **Enforcement:**
  * Set explicit timeouts on all HTTP requests and Redis operations.
  * Wrap external calls in try/except blocks with specific exception handling.
  * Return appropriate HTTP status codes (502 for upstream failures, 504 for timeouts).

## 3. Circuit Breaker Pattern (Future)
* **Rule:** For services with high call volume to Dialogflow, implement a circuit breaker to prevent cascading failures.
* **Enforcement:** This will be implemented in Phase 3+. For now, ensure retry logic uses exponential backoff with jitter.

## 4. Health Check Endpoints
* **Rule:** Every deployable service must expose a `/healthz` endpoint that returns `200 OK` when the service is ready.
* **Enforcement:** Health checks should verify critical dependencies (Redis connectivity, Pub/Sub subscription status) and return `503 Service Unavailable` if dependencies are down.
