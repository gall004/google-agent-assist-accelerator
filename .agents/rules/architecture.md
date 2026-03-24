---
trigger: always_on
description: Architecture, DRY Principle & Service Design
---

## 1. The DRY Principle
* **Rule:** Never duplicate logic across services. Apply the Rule of Three.
* **Enforcement:** Abstract shared logic into service-level `utils.py` (Python) or `lib/` (React).

## 2. Single Responsibility & File Size
* **File Size:** Files should aim for 150 lines maximum. Any file exceeding 250 lines MUST be aggressively refactored.
* **Handler Separation:** Route handlers should be thin — extract business logic into dedicated modules.

## 3. Service Boundary Isolation
* **Rule:** Each service under `services/` is an independent deployable unit. No cross-service imports.
* **Enforcement:**
  * Python services: Each has its own `requirements.txt`, `Dockerfile`, `main.py`, and `tests/`.
  * React services: Each has its own `package.json`, `Dockerfile`, `vite.config.ts`, and `tests/`.
  * Communication between services occurs only via well-defined APIs (HTTP, WebSocket, Pub/Sub).

## 4. Configuration as Code
* **Rule:** All service configuration must be centralized in a `config.py` (Python) or environment-based module (React).
* **Enforcement:** No magic strings scattered across route handlers. Config values are read from environment variables with sane defaults.
