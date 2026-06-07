# Templates

Use these as starting points, not as universal boilerplate. Remove sections that the repository cannot maintain.

## Router: CLAUDE.md

```markdown
# CLAUDE.md

This file is a router. The canonical harness is in `.github/`.

## Project

<!-- Two or three lines: what this repository does, main stack, key constraints. -->

Canonical instructions: `.github/copilot-instructions.md`

## Before Work

1. Read `.github/copilot-instructions.md`.
2. Read the task-specific files below.
3. Inspect nearby existing code before editing.

## Task Routing

| Task | Read |
|---|---|
| New feature | `.github/instructions/architecture.instructions.md`, `.github/prompts/implement-feature.prompt.md` |
| Bug fix | `.github/instructions/coding-style.instructions.md`, `.github/prompts/fix-bug.prompt.md` |
| Refactor | `.github/instructions/architecture.instructions.md`, `.github/instructions/testing.instructions.md`, `.github/prompts/refactor.prompt.md` |
| Tests | `.github/instructions/testing.instructions.md`, `.github/prompts/write-tests.prompt.md` |
| Review | `.github/instructions/review.instructions.md`, `.github/instructions/security.instructions.md`, `.github/prompts/review-pr.prompt.md` |
| Docs | `.github/instructions/docs.instructions.md`, `.github/prompts/update-docs.prompt.md` |

## Rule

Do not add detailed policy here. Move policy to `.github/` and keep this file as a router.
```

## Top-Level Instructions

```markdown
---
description: "Repository-wide coding-agent instructions"
version: "1.0.0"
last_updated: "YYYY-MM-DD"
owner: "Team"
---

# Repository Agent Instructions

## Project Overview

<!-- Purpose, audience, main stack, runtime constraints. -->

## Technology Stack

| Area | Choice |
|---|---|
| Language | <!-- ... --> |
| Framework | <!-- ... --> |
| Database | <!-- ... --> |
| Infrastructure | <!-- ... --> |

## Core Rules

- <!-- Durable, repository-wide rule. -->
- <!-- Keep details in focused instruction files. -->

## Domain Terms

| Term | Meaning |
|---|---|
| <!-- term --> | <!-- definition --> |

## References

- Architecture: `.github/instructions/architecture.instructions.md`
- Coding style: `.github/instructions/coding-style.instructions.md`
- Testing: `.github/instructions/testing.instructions.md`
- Security: `.github/instructions/security.instructions.md`
```

## Instruction File

```markdown
---
description: "<domain> rules for coding agents"
version: "1.0.0"
last_updated: "YYYY-MM-DD"
owner: "Team"
---

# <Domain> Instructions

## Principles

- <!-- Durable rule. -->

## Required Patterns

| Pattern | Use when | Reference |
|---|---|---|
| <!-- pattern --> | <!-- situation --> | <!-- path --> |

## Prohibited Patterns

- <!-- Prohibition and reason. -->
```

## Prompt File

```markdown
---
description: "Task entry for <task>"
version: "1.0.0"
last_updated: "YYYY-MM-DD"
owner: "Team"
---

# <Task> Prompt

## Intent

<!-- What the user is asking the agent to accomplish. -->

## Inputs

- Target: <!-- file, issue, PR, module, feature name -->
- Constraints: <!-- scope, non-goals, deadlines -->

## References

- `.github/copilot-instructions.md`
- `.github/instructions/<domain>.instructions.md`
- `.github/skills/<skill>/SKILL.md`

## Output

<!-- Expected response or artifact. -->
```

## Agent File

```markdown
---
description: "<role> agent role definition"
version: "1.0.0"
last_updated: "YYYY-MM-DD"
owner: "Team"
---

# <Role> Agent

## Role

<!-- Responsibility area. -->

## Judgment Criteria

- <!-- Trade-offs and stance. -->

## References

| File | When to read |
|---|---|
| `.github/instructions/<domain>.instructions.md` | <!-- condition --> |

## Skills

- `<skill-name>`: <!-- when used -->

## Boundaries

- <!-- What this role should not own. -->
```

## Skill File

````markdown
---
name: <skill-name>
description: Reusable procedure for <task>. Use when <trigger>.
---

# <Skill Name>

## Overview

<!-- One or two sentences. -->

## Preconditions

- <!-- Required context or files. -->

## Steps

1. <!-- Inspect or gather context. -->
2. <!-- Execute the procedure. -->
3. <!-- Verify. -->

## Scripts

```bash
python scripts/<script>.py <args>
```

## Output

<!-- Required report or artifact. -->
````
