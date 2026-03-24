---
description: Scaffold a new backend or frontend service in the monorepo
---

# Scaffold Service Workflow

Execute this workflow when adding a new service to `services/`.

1. Verify the current git branch is NOT `main` or `develop`:
   ```bash
   git branch --show-current
   ```

2. Create the service directory structure:
   ```bash
   # For Python service:
   mkdir -p services/<service-name>/{handlers,tests/unit,tests/integration}

   # For React service:
   mkdir -p services/<service-name>/{src/{components,lib,hooks,types,styles},tests/unit,tests/e2e,public}
   ```

3. Create the required foundational files:
   - **Python:** `main.py`, `config.py`, `requirements.txt`, `Dockerfile`
   - **React:** `package.json`, `vite.config.ts`, `tsconfig.json`, `Dockerfile`

4. Add a `/healthz` endpoint (Python) or health check page (React) per `defensive-programming.md`.

5. Write initial unit tests per `testing-standards.md` TDD mandate:
   - Health check returns 200
   - Config loads environment variables correctly

6. Update path filters in `.github/workflows/ci.yml` to include the new service.

7. Run the Documentation Verification Gate from `sdlc-workflow.md`:
   - Update `README.md` → Directory Structure
   - Update `.env.example` if new env vars introduced
   - Update `docker-compose.yml` to include the new service

8. **🛑 STOP — Present the scaffold to the user for review before committing.**
