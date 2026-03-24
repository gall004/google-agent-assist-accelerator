---
trigger: always_on
description: Test-Driven Development & Quality Assurance Standards
---

## 1. The TDD Mandate
* Before writing the implementation code for a new handler, utility, or component, you must first write a failing test.
* Execute the test locally to confirm it fails (Red).
* Write the implementation code to satisfy the test.
* Execute the test locally to confirm it passes (Green) before committing.

## 2. Testing Stack Rules

### Python Services (cloud-pubsub-interceptor, ui-connector)
* **pytest** (`tests/unit/`, `tests/integration/`): Use for route handlers, utility functions, auth logic.
* Cover happy path, sad path, and graceful degradation scenarios.
* Use `unittest.mock` or `pytest-mock` for mocking HTTP callouts, Redis, and Pub/Sub.
* Test both success (200/204) and failure (400/500) response scenarios.

### React Services (ui, sidecar)
* **Vitest** (`tests/unit/`): Use for hooks, utilities, state management, and isolated UI components. Use `jsdom` for React components.
* **Playwright** (`tests/e2e/`): Use strictly for multi-step user workflows and full integration tests.

## 3. Coverage Threshold
* **Rule:** ≥80% line coverage for new code in all services. Enforced in CI.
* **Enforcement:** CI will fail if coverage drops below threshold on changed files.

## 4. Sad-Path Test Enforcement
* **Rule:** TDD is not just for the "Happy Path". You must explicitly write tests that prove your code handles failure gracefully.
* **Enforcement:** For every public function or route handler, write at least:
  * One test for invalid input (e.g., missing required fields, malformed JSON).
  * One test for upstream failure (e.g., Redis unreachable, Dialogflow API timeout).
  * One test for authentication failure (e.g., expired JWT, missing token).

## 5. The Human-in-the-Loop Handover
* When presenting a completed feature to the user, you must include the test output or coverage summary in your handover message to prove the code is stable.
