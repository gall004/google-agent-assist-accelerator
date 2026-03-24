---
trigger: always_on
description: Zero-Hardcoding, Environment Configuration & Secrets Management
---

## 1. Zero Hardcoding Policy
* **Rule:** Never hardcode secrets, credentials, GCP project IDs, OR environment-specific configurations (like Redis hosts, JWT secret keys, Dialogflow project paths, or external API endpoints).
* **Enforcement (Python):** Always extract values using `os.environ.get('VARIABLE_NAME')` or a `config.py` module with appropriate fallbacks.
* **Enforcement (React):** Always use `import.meta.env.VITE_VARIABLE_NAME` for client-accessible variables. Server-only values must never be exposed to the frontend bundle.

## 2. Environment Variable Lifecycle
* **The Currency Mandate:** Any time a new environment variable is introduced into the codebase, you MUST simultaneously:
  1. Add it to `.env.example` with a descriptive dummy value or instructional comment.
  2. Implement it in the code using `os.environ` (Python) or `import.meta.env` (React).
  3. Update `README.md` → Environment Variables table to reflect the new requirement.
  4. Explicitly inform the user in your handover message that they must add the new key to their local `.env` or deployment configuration.
* **Never commit `.env`, `.env.local`, or `.env.prod` to version control.**

## 3. Google Secret Manager at Runtime
* **Rule:** Sensitive values (JWT secret key, service account keys, API tokens) must be stored in Google Secret Manager and accessed at runtime — never baked into container images or committed to source.
* **Enforcement:** Dockerfiles must NOT contain `ENV` directives with real secret values. Use `ENTRYPOINT` scripts that fetch secrets from Secret Manager or rely on Cloud Run's native secret mounting.

## 4. CORS Configuration
* **Rule:** Allowed CORS origins must be explicitly configured via environment variable, never hardcoded, and never set to `*` in production.
* **Enforcement:** Default to an empty allowlist. The `ALLOWED_ORIGINS` env var specifies comma-separated origins.
