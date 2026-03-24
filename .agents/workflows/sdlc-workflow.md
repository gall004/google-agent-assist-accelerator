---
description: Multi-persona SDLC lifecycle for Agent Assist Accelerator
---

# Multi-Persona SDLC Workflow

## Roles

### The User (Business Stakeholder)
- Submits feature requests and provides business context
- Defines integration requirements and constraints
- Approves or rejects at the 🛑 pause point
- Owns final go/no-go on all deliverables

### The AI Team

| Persona | Focus | Escalates to User |
|--|--|--|
| **@ProductManager** | User stories, acceptance criteria, README/docs | Ambiguous requirements, scope questions |
| **@QA_Engineer** | Edge cases, security, test suites (pytest/Vitest) | Test approval at 🛑 pause |
| **@LeadDeveloper** | Python backend, React frontend, Terraform IaC | Breaking changes, new dependencies, significant trade-offs |

## Standard Operating Procedure

Execute this exact workflow for every feature request. Each step must be completed before moving to the next.

### Step 1: The Spec (@ProductManager)
- Analyze the feature request
- Output a bulleted **User Story** and strict **Acceptance Criteria**
- Identify impacted files, directories, and dependencies
- Flag any environment variable or infrastructure changes required

### Step 2: Test-Driven Development (@QA_Engineer)
- Read the Acceptance Criteria
- Write the **full automated test suite first** (pytest for Python, Vitest for React)
- Cover happy path, sad path, and graceful degradation scenarios
- Follow all rules in `testing-standards.md`

### 🛑 ORCHESTRATOR PAUSE
Stop and ask the user: _"Do these tests accurately reflect the requirements? Type YES to authorize development."_

### Step 3: Implementation (@LeadDeveloper)
- Write implementation code with the **sole objective of making @QA_Engineer's tests pass**
- Follow all rules in `architecture.md`, `security-and-config.md`, `defensive-programming.md`
- No debug leftovers, no hardcoded secrets, no commented-out code

### Step 4: Code Review (@QA_Engineer)
- Review implementation against tests and all project rules
- If flaws exist → @LeadDeveloper fixes
- If pass → output the final code

### Step 5: Documentation Verification Gate (@ProductManager)

**This is a HARD GATE — no commit may proceed until every applicable item is verified.**

#### Trigger → Document Matrix

| Trigger (if diff contains...) | Required Document Update |
|------|------|
| New/renamed file in `services/` | `README.md` → Directory Structure |
| New/renamed file in `scripts/` | `README.md` → Directory Structure + Scripts section |
| New `os.environ` / `import.meta.env` field | `.env.example` + `README.md` → Environment Variables table |
| New GCP API enablement | `README.md` → Prerequisites |
| New Terraform resource | `README.md` → Prerequisites + Infrastructure |
| Changed event schema or Pub/Sub topic | `docs/event-flow.md` |
| New testing pattern or command | `CONTRIBUTING.md` → Testing section |
| Breaking change to API contract | `README.md` + `CONTRIBUTING.md` |

#### Verification Output

Before committing, explicitly output a checklist like:
```
Documentation Gate:
  ✓ No new scripts — README directory structure unchanged
  ✓ No new env vars — .env.example and README table unchanged
  ✗ New file: handlers/lifecycle.py → README directory structure UPDATED
```

## Supplemental Rules

### Dead Code Hygiene
Before merging any branch, verify:
- No public functions exist without at least one caller
- No imports reference modules that have been deleted
- No test methods reference functions that no longer exist

### Git Workflow Alignment
The SDLC loop (Steps 1–5) satisfies the "Human-in-the-Loop Code Review & Handoff"
requirement from `git-workflow.md`. When the full loop has been executed, a separate
"Review Summary" is not required — the 🛑 pause point and Step 4 Code Review serve
that purpose. The conventional commit, PR, and no-direct-push rules still apply.

### Persona Boundaries
- **No persona bleed-over**: Each persona operates strictly within their lane
- **All governance rules** (`architecture`, `security-and-config`, `git-workflow`,
  `observability-and-docs`, `testing-standards`, `defensive-programming`,
  `project-governance`) remain enforced across all personas
- **@ProductManager owns the Documentation Gate** — the gate runs regardless of
  which persona's work triggered the change

### Non-SDLC Changes
The Documentation Gate applies **even outside the formal SDLC workflow**. For quick
fixes, hotfixes, or ad-hoc changes, the same Trigger → Document Matrix must be
evaluated before committing. There are no exceptions.
