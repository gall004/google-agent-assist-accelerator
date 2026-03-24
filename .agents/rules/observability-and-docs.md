---
trigger: always_on
description: Logging, Documentation & README Currency
---

## 1. Python Logging Standards
* **Rule:** Use Python's `logging` module with explicit levels. Never leave bare `print()` statements.
* **Enforcement:**
  * `logging.error()` — Exceptions and callout failures.
  * `logging.warning()` — Unexpected but recoverable conditions.
  * `logging.info()` — Key execution milestones (e.g., "Pub/Sub message received for conversation: {id}").
  * `logging.debug()` — Detailed diagnostic data (e.g., full request/response payloads). Remove or guard these before merging.

## 2. Docstring Headers
* **Rule:** Every public Python function and class MUST have a docstring. Every exported TypeScript function MUST have a JSDoc comment.
* **Enforcement (Python):**
  ```python
  def process_event(event_data: dict) -> dict:
      """Process an Agent Assist event notification.

      Args:
          event_data: The decoded Pub/Sub message payload.

      Returns:
          A dict containing the processed event metadata.

      Raises:
          ValueError: If event_data is missing required fields.
      """
  ```

## 3. README Currency Mandate
* **Rule:** Any time a new environment variable, deployment prerequisite, service endpoint, or infrastructure component is introduced, the `README.md` must be updated in the same commit.
* **Enforcement:** The README must always maintain:
  1. Project overview and architecture description.
  2. Directory structure.
  3. Environment variables table.
  4. Local development setup instructions.
  5. Deployment instructions.

## 4. No Silent Failures
* **Rule:** Every `try/except` block must explicitly log the error before re-raising or returning.
* **Enforcement:** Catch blocks must call `logging.error()` with the exception message and traceback. Never swallow exceptions silently.
