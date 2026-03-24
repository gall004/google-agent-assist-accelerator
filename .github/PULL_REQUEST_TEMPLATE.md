## Summary

<!-- Brief description of what this PR does -->

## Type of Change

- [ ] `feat` — New feature
- [ ] `fix` — Bug fix
- [ ] `refactor` — Code restructuring (no behavior change)
- [ ] `chore` — Tooling, CI, docs
- [ ] `test` — Tests only

## Services Affected

- [ ] `cloud-pubsub-interceptor`
- [ ] `ui-connector`
- [ ] `ui`
- [ ] `sidecar`
- [ ] `infra` (Terraform)
- [ ] Root (docs, CI, governance)

## Testing

- [ ] Unit tests pass (`pytest` / `vitest`)
- [ ] Coverage ≥80% for new code
- [ ] Sad-path tests included

## Documentation Verification Gate

- [ ] `README.md` updated (if directory structure or env vars changed)
- [ ] `CONTRIBUTING.md` updated (if testing or workflow patterns changed)
- [ ] `.env.example` updated (if new environment variables introduced)
- [ ] Architecture docs updated (if service interactions changed)

## Pre-Flight Checklist

- [ ] No debug leftovers (`print()`, `console.log()`)
- [ ] No hardcoded values (project IDs, secrets, URLs)
- [ ] No commented-out code
- [ ] No disabled linters without documented justification
- [ ] No build artifacts in working tree
