---
trigger: always_on
description: Project Governance & Meta-Documentation Standards
---

## 1. The CONTRIBUTING.md Currency Mandate
* **Rule:** If you introduce a new testing pattern, modify the Git branching strategy, add a deployment prerequisite, or change coding standards, you MUST proactively update `CONTRIBUTING.md` in the same commit.
* **Enforcement:** `CONTRIBUTING.md` must always serve as a strictly accurate, single source of truth for a new developer joining the project.

## 2. Licensing & Copyright
* **Rule:** Ensure the root `LICENSE` file remains intact. Do not overwrite or delete it during project scaffolding.
* **Enforcement:** If making widespread project updates and the copyright year is outdated, proactively offer to update it.

## 3. Versioning & Releases
* **Automated SemVer:** This repository uses `release-please` via GitHub Actions. You MUST NEVER manually update the `version` field in `package.json` files or manually edit the `CHANGELOG.md`.
* **Commit Discipline:** Because releases are automated based on commit history, you must strictly adhere to Conventional Commits for every single commit.

## 4. Monorepo Dependency Isolation
* **Rule:** Each service under `services/` maintains its own dependency manifest (`requirements.txt` for Python, `package.json` for Node/React). Cross-service imports are forbidden.
* **Enforcement:** Shared logic must be extracted into a documented common library or explicitly duplicated with a justification comment.

## 5. Service Boundary Integrity
* **Rule:** Each service directory must contain its own `Dockerfile`, dependency file, test directory, and can be built/tested independently.
* **Enforcement:** CI/CD pipelines use path filters to trigger builds only for changed services. Breaking this isolation breaks the pipeline.
