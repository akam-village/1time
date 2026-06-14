---
name: agent-harness-design
description: Design, scaffold, audit, and refactor Agent Harness files for coding-agent repositories. Use when Codex needs to create or improve harness structures such as .github/copilot-instructions.md, .github/instructions/*.instructions.md, .github/prompts/*.prompt.md, .github/agents/*.agent.md, .github/skills/*/SKILL.md, CLAUDE.md, .claude/* adapters, routing maps, prompt/skill/script separation, harness linting, or reusable agent operating procedures.
---

# Agent Harness Design

## Overview

Use this skill to design the harness that makes coding agents behave consistently in a repository: durable rules, role definitions, task entry points, reusable procedures, deterministic scripts, and tool-specific adapters.

Keep the harness small enough to maintain. Prefer one authoritative source, explicit routing, single-responsibility files, and scripts for deterministic computation.

## Workflow

1. Identify the user intent: new harness design, existing harness audit, scaffold generation, prompt/skill/script classification, adapter design, or anti-pattern cleanup.
2. Inspect the repository before proposing changes. Use `rg --files` when available and look for `.github/`, `.claude/`, `CLAUDE.md`, `.codex/`, `AGENTS.md`, `scripts/`, and existing docs.
3. Load only the reference files needed for the task:
   - `references/core-model.md` for the conceptual model, layer order, and design principles.
   - `references/file-responsibilities.md` for what belongs in each harness file.
   - `references/classification-rules.md` for deciding between instructions, prompts, agents, skills, and scripts.
   - `references/routing-and-dependencies.md` for router/adapters and dependency direction.
   - `references/anti-patterns.md` for audit and cleanup work.
   - `references/starter-profiles.md` for minimal, standard, and adapter-heavy rollout plans.
   - `references/templates.md` when drafting concrete files.
4. For audits, run `scripts/analyze_harness.py` first, then `scripts/lint_harness.py`. Treat the scripts as evidence, not as a substitute for judgment.
5. For scaffolding, run `scripts/scaffold_harness.py` only after choosing a profile and confirming the target root. Review generated files and tailor placeholders to the repository.
6. When editing harness files, preserve user-specific project facts. Move misplaced content to the correct layer instead of deleting it when it still has value.
7. Finish with a short report: what changed, which rules or references informed the change, remaining gaps, and any validation run.

## Design Rules

- Define one canonical source of truth for stable agent rules. Use adapters such as `CLAUDE.md` or `.claude/` only as thin routers or tool-specific wrappers.
- Put durable policy in instructions, user-invoked task entry points in prompts, reusable procedures in skills, role boundaries in agents, and deterministic work in scripts.
- Keep dependency direction one way: router or top-level instructions may point downward; lower layers should not redefine upper-layer policy.
- Avoid duplicated rules. Prefer "see X" over copying the same norm into multiple files.
- Keep the first version small. Add agents, prompts, skills, and scripts only when repeated usage justifies the maintenance cost.
- When a script exists for harness work, pair it with a skill or reference that explains invocation, inputs, outputs, and interpretation.

## Scripts

Run from this skill directory unless passing an absolute script path:

```bash
python scripts/analyze_harness.py /path/to/repo
python scripts/lint_harness.py /path/to/repo
python scripts/scaffold_harness.py /path/to/repo --profile minimal --adapters claude
python scripts/scaffold_harness.py /path/to/repo --profile standard --adapters claude --dry-run
```

`analyze_harness.py` reports discovered harness files and scale signals. `lint_harness.py` checks naming, required files, frontmatter, size limits, and common anti-patterns. `scaffold_harness.py` creates starter files without overwriting existing files unless `--force` is provided.

## Output Expectations

For design work, provide a concise architecture proposal with chosen profile, canonical root, adapter strategy, file list, and migration steps.

For audit work, lead with findings ordered by impact, include file paths, and distinguish errors from warnings.

For scaffolding or edits, list created or changed files and mention validation commands that passed or could not be run.
