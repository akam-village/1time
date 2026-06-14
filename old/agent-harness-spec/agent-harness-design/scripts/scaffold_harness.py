#!/usr/bin/env python3
"""Create starter Agent Harness files."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


TODAY = date.today().isoformat()


def fm(description: str) -> str:
    return f"""---
description: "{description}"
version: "1.0.0"
last_updated: "{TODAY}"
owner: "TODO"
---
"""


def top_instructions() -> str:
    return (
        fm("Repository-wide coding-agent instructions")
        + """
# Repository Agent Instructions

## Project Overview

TODO: Describe the repository purpose, audience, main stack, and non-negotiable constraints in two or three short paragraphs.

## Technology Stack

| Area | Choice |
|---|---|
| Language | TODO |
| Framework | TODO |
| Database | TODO |
| Infrastructure | TODO |

## Core Rules

- TODO: Add only durable, repository-wide rules here.
- Keep task procedures in skills and task entry points in prompts.

## Domain Terms

| Term | Meaning |
|---|---|
| TODO | TODO |

## References

- Architecture: `.github/instructions/architecture.instructions.md`
- Coding style: `.github/instructions/coding-style.instructions.md`
- Testing: `.github/instructions/testing.instructions.md`
- Security: `.github/instructions/security.instructions.md`
""".lstrip()
    )


def instruction(title: str, description: str) -> str:
    return (
        fm(description)
        + f"""
# {title}

## Principles

- TODO: Add durable rules for this domain.

## Required Patterns

| Pattern | Use when | Reference |
|---|---|---|
| TODO | TODO | TODO |

## Prohibited Patterns

- TODO: Add prohibited patterns with reasons and preferred alternatives.
""".lstrip()
    )


def prompt(title: str, description: str, skill: str) -> str:
    return (
        fm(description)
        + f"""
# {title}

## Intent

TODO: State what the user wants this task entry to accomplish.

## Inputs

- Target: TODO
- Constraints: TODO
- Non-goals: TODO

## References

- `.github/copilot-instructions.md`
- `.github/skills/{skill}/SKILL.md`

## Output

TODO: Define expected response or artifacts.
""".lstrip()
    )


def agent(title: str, description: str, skills: list[str]) -> str:
    skill_lines = "\n".join(f"- `{name}`: TODO" for name in skills)
    return (
        fm(description)
        + f"""
# {title}

## Role

TODO: Define responsibility area.

## Judgment Criteria

- TODO: Add trade-offs and stance for this role.

## References

| File | When to read |
|---|---|
| `.github/copilot-instructions.md` | Always |

## Skills

{skill_lines}

## Boundaries

- TODO: Define what this role should not own.
""".lstrip()
    )


def skill(name: str, description: str) -> str:
    return f"""---
name: {name}
description: {description}
---

# {name.replace("-", " ").title()}

## Overview

TODO: Describe this reusable procedure.

## Preconditions

- TODO

## Steps

1. TODO
2. TODO
3. TODO

## Verification

- TODO

## Output

TODO: Define required report or artifact.
"""


def claude_router(profile: str) -> str:
    routes = [
        ("New feature", "`.github/instructions/architecture.instructions.md`, `.github/prompts/implement-feature.prompt.md`"),
        ("Bug fix", "`.github/instructions/coding-style.instructions.md`, `.github/prompts/fix-bug.prompt.md`"),
        ("Refactor", "`.github/instructions/architecture.instructions.md`, `.github/instructions/testing.instructions.md`, `.github/prompts/refactor.prompt.md`"),
        ("Tests", "`.github/instructions/testing.instructions.md`, `.github/prompts/write-tests.prompt.md`"),
        ("Review", "`.github/instructions/review.instructions.md`, `.github/instructions/security.instructions.md`, `.github/prompts/review-pr.prompt.md`"),
        ("Docs", "`.github/instructions/docs.instructions.md`, `.github/prompts/update-docs.prompt.md`"),
    ]
    if profile == "minimal":
        routes = routes[:1]
    route_rows = "\n".join(f"| {task} | {refs} |" for task, refs in routes)
    return f"""# CLAUDE.md

This file is a router. The canonical harness is in `.github/`.

## Project

TODO: Describe this project in two or three lines.

Canonical instructions: `.github/copilot-instructions.md`

## Before Work

1. Read `.github/copilot-instructions.md`.
2. Read the task-specific files below.
3. Inspect nearby existing code before editing.

## Task Routing

| Task | Read |
|---|---|
{route_rows}

## Rule

Do not add detailed policy here. Move policy to `.github/` and keep this file as a router.
"""


MINIMAL_FILES = {
    ".github/copilot-instructions.md": top_instructions,
    ".github/instructions/coding-style.instructions.md": lambda: instruction("Coding Style Instructions", "Coding style, naming, and formatting rules"),
    ".github/agents/engineer.agent.md": lambda: agent("Engineer Agent", "General implementation agent role definition", ["repository-analysis", "implementation-planning"]),
    ".github/prompts/implement-feature.prompt.md": lambda: prompt("Implement Feature Prompt", "Task entry for feature implementation", "implementation-planning"),
}


STANDARD_EXTRA_FILES = {
    ".github/instructions/architecture.instructions.md": lambda: instruction("Architecture Instructions", "Architecture rules and accepted patterns"),
    ".github/instructions/testing.instructions.md": lambda: instruction("Testing Instructions", "Testing strategy and test code rules"),
    ".github/instructions/review.instructions.md": lambda: instruction("Review Instructions", "Code review standards and merge criteria"),
    ".github/instructions/security.instructions.md": lambda: instruction("Security Instructions", "Security requirements and prohibited patterns"),
    ".github/instructions/docs.instructions.md": lambda: instruction("Documentation Instructions", "Documentation and comment rules"),
    ".github/agents/backend-engineer.agent.md": lambda: agent("Backend Engineer Agent", "Backend implementation role definition", ["repository-analysis", "implementation-planning", "test-generation"]),
    ".github/agents/frontend-engineer.agent.md": lambda: agent("Frontend Engineer Agent", "Frontend implementation role definition", ["repository-analysis", "implementation-planning", "test-generation"]),
    ".github/agents/test-engineer.agent.md": lambda: agent("Test Engineer Agent", "Test design and implementation role definition", ["repository-analysis", "test-generation"]),
    ".github/agents/reviewer.agent.md": lambda: agent("Reviewer Agent", "Code review role definition", ["pr-review"]),
    ".github/agents/docs-writer.agent.md": lambda: agent("Docs Writer Agent", "Documentation role definition", ["documentation-update", "repository-analysis"]),
    ".github/agents/harness-engineer.agent.md": lambda: agent("Harness Engineer Agent", "Agent Harness maintenance role definition", ["repository-analysis"]),
    ".github/prompts/fix-bug.prompt.md": lambda: prompt("Fix Bug Prompt", "Task entry for bug fixes", "repository-analysis"),
    ".github/prompts/refactor.prompt.md": lambda: prompt("Refactor Prompt", "Task entry for refactoring", "safe-refactoring"),
    ".github/prompts/write-tests.prompt.md": lambda: prompt("Write Tests Prompt", "Task entry for test creation", "test-generation"),
    ".github/prompts/review-pr.prompt.md": lambda: prompt("Review PR Prompt", "Task entry for PR review", "pr-review"),
    ".github/prompts/update-docs.prompt.md": lambda: prompt("Update Docs Prompt", "Task entry for documentation updates", "documentation-update"),
    ".github/skills/repository-analysis/SKILL.md": lambda: skill("repository-analysis", "Gather repository context before implementation, review, or documentation work. Use when task-relevant files, patterns, or dependencies must be discovered."),
    ".github/skills/implementation-planning/SKILL.md": lambda: skill("implementation-planning", "Create an implementation plan from requirements and repository context. Use before non-trivial code changes."),
    ".github/skills/safe-refactoring/SKILL.md": lambda: skill("safe-refactoring", "Refactor while preserving behavior through small verified steps. Use when changing structure without changing external behavior."),
    ".github/skills/test-generation/SKILL.md": lambda: skill("test-generation", "Design and implement focused tests for target code. Use when adding or repairing test coverage."),
    ".github/skills/pr-review/SKILL.md": lambda: skill("pr-review", "Review diffs for correctness, security, tests, design, and maintainability. Use for PR or code review tasks."),
    ".github/skills/documentation-update/SKILL.md": lambda: skill("documentation-update", "Update documentation based on code or behavior changes. Use when docs, comments, or changelogs need maintenance."),
}


def write_file(root: Path, relative: str, content: str, force: bool, dry_run: bool) -> str:
    path = root / relative
    if path.exists() and not force:
        return f"skip existing {relative}"
    if dry_run:
        return f"would write {relative}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return f"wrote {relative}"


def scaffold(root: Path, profile: str, adapters: list[str], force: bool, dry_run: bool) -> list[str]:
    files = dict(MINIMAL_FILES)
    if profile == "standard":
        files.update(STANDARD_EXTRA_FILES)
        files.pop(".github/agents/engineer.agent.md", None)

    results: list[str] = []
    for relative, factory in sorted(files.items()):
        results.append(write_file(root, relative, factory(), force, dry_run))

    if "claude" in adapters:
        results.append(write_file(root, "CLAUDE.md", claude_router(profile), force, dry_run))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Repository root where harness files should be created")
    parser.add_argument("--profile", choices=["minimal", "standard"], default="minimal")
    parser.add_argument("--adapters", default="claude", help="Comma-separated adapters to create, e.g. claude or none")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without writing")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    adapters = [] if args.adapters.strip().lower() == "none" else [item.strip().lower() for item in args.adapters.split(",") if item.strip()]

    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)

    for result in scaffold(root, args.profile, adapters, args.force, args.dry_run):
        print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
