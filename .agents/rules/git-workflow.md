---
trigger: always_on
description: Safe Git Workflow for Monorepo
---

## 1. The Branch Check Mandate
* Before you write, modify, or delete any code files, you must determine the current Git branch by running: `git branch --show-current`.
* If the current branch is `main` or `develop`, YOU MUST NOT make any file changes yet.

## 2. Automatic Branch Creation
* **Protected Branches:** If the user requests a feature, refactor, or bug fix while on the `main` or `develop` branch, you must proactively generate a contextual branch name using the convention `<type>/<scope>/<description>` (e.g., `feat/ui-connector/jwt-refresh`) and run `git checkout -b <branch-name>`.
* **Other Branches:** If already on a non-protected feature branch:
  * If the user's request is related to the current work, keep going on the same branch.
  * If the request is unrelated, prompt the user via `notify_user` asking if they want a new branch.
* Only after confirming your branch state may you proceed with modifying the codebase.

## 3. Conventional Commits
* **Rule:** Every commit message MUST follow the Conventional Commits specification: `feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`, `ci:`.
* **Enforcement:** Include a concise scope when applicable (e.g., `feat(ui-connector): add CORS origin validation`). Commit messages must be descriptive enough that `git log --oneline` serves as a readable project changelog.

## 4. The Pre-Flight Self-Review Checklist
* Before you stage, commit, and present your work, you MUST independently verify:
  1. **No Debug Leftovers:** You have removed all temporary `print()`, `console.log()`, or bare debug statements used during development.
  2. **No Hardcoded Values:** You have not hardcoded any GCP project IDs, secrets, credentials, or environment-specific URLs anywhere in the codebase.
  3. **No Commented-Out Code:** Blocks of commented-out code have been removed. Use version control to preserve history, not comments.
  4. **No Disabled Linters:** You have not used `# noqa`, `// eslint-disable-next-line`, or `@ts-ignore` without explicit documented justification.
  5. **No Build Artifacts:** No `__pycache__/`, `node_modules/`, `dist/`, `*.egg-info/`, or `.env.local` in the working tree.

## 5. Human-in-the-Loop Code Review & Handoff
* **The Hard Stop:** When you have completed a feature on a feature branch and passed the Pre-Flight Checklist, YOU MUST NOT merge the branch into `develop` or `main` automatically.
* **The Commit & Push:**
  1. Stage all changes with `git add .`.
  2. Commit with a descriptive conventional commit message.
  3. Push the feature branch to the remote repository.
* **The Handoff:** After pushing, STOP and present a "Review Summary" to the user.
* **NO AUTOMATED PRs:** You MUST NOT run `gh pr create` or `gh pr merge` without explicit user permission.

## 6. No Direct Pushes to Protected Branches
* **CRITICAL RULE:** You are NEVER permitted to push commits directly to the `main` or `develop` branch.
* **Pull Requests Only:** All code integrations into `main` or `develop` MUST occur via Pull Requests.
