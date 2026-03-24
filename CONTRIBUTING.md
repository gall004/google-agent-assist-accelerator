# Contributing to Google Agent Assist Accelerator

This document is the single source of truth for development workflow, testing standards, and coding guidelines. It is updated automatically whenever a new pattern, prerequisite, or workflow is introduced.

## Branching Strategy

We use **simplified GitFlow** with two permanent protected branches:

| Branch | Purpose |
|---|---|
| `main` | Production-ready. Every commit is deployable. |
| `develop` | Integration branch. Features merge here first. |
| `feat/<scope>/<desc>` | New features |
| `fix/<scope>/<desc>` | Bug fixes |
| `chore/<scope>/<desc>` | Tooling, CI, docs |

### Rules

1. **Never push directly to `main` or `develop`.** All changes require a Pull Request.
2. **Use conventional commits:** `feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`, `ci:`.
3. **Check your branch** before writing code: `git branch --show-current`.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/gall004/google-agent-assist-accelerator.git
cd google-agent-assist-accelerator

# Copy environment variables
cp .env.example .env
# Fill in your values

# Start all services
docker compose up --build
```

## Testing

### Python Services (cloud-pubsub-interceptor, ui-connector)

```bash
cd services/<service-name>
pip install -r requirements.txt
pip install pytest pytest-cov ruff

# Lint
ruff check .

# Unit tests
pytest tests/unit/ -v --tb=short --cov=. --cov-report=term-missing

# Integration tests (requires GCP credentials)
pytest tests/integration/ -v --tb=short -m integration
```

### React Services (ui, sidecar)

```bash
cd services/<service-name>
npm ci

# Lint
npx eslint .

# Type check
npx tsc --noEmit

# Unit tests
npx vitest run --coverage

# Build
npm run build
```

### Coverage Threshold

- **≥80% line coverage** for new code in all services.
- Every public function or route handler must have at least one sad-path test.

## Code Standards

### File Size
- Target ≤150 lines per file. Files exceeding 250 lines must be refactored.

### Logging
- **Python:** Use `logging` module with explicit levels. No bare `print()`.
- **TypeScript:** No bare `console.log()` in production code.

### Documentation
- Every public Python function: docstring with Args, Returns, Raises.
- Every exported TypeScript function: JSDoc comment.

### Error Handling
- Every `try/except` must log the error before re-raising.
- Never swallow exceptions silently.
- All endpoints validate input and return descriptive 400 errors for malformed requests.

## Definition of Done

Before submitting a PR, verify:

- [ ] Tests pass with ≥80% coverage
- [ ] No debug leftovers, commented-out code, or hardcoded values
- [ ] Conventional commit message includes scope
- [ ] `README.md` updated if env vars, services, or prerequisites changed
- [ ] `.env.example` updated if new env vars introduced
- [ ] CONTRIBUTING.md updated if testing patterns changed
