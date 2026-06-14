# Starter Profiles

Choose the smallest profile that can be maintained.

## Minimal Profile

Use for individual projects, small teams, or first adoption.

```text
repo-root/
  CLAUDE.md                         optional adapter/router
  .github/
    copilot-instructions.md          repository-wide rules
    instructions/
      coding-style.instructions.md   first durable rule set
    agents/
      engineer.agent.md              one broad implementation role
    prompts/
      implement-feature.prompt.md    most common task entry
```

Goal: Replace repeated chat reminders with file references.

Completion signal: The agent can find project rules and the most common task path without the user restating them.

## Standard Profile

Use for active team development with recurring implementation, review, testing, and docs work.

```text
repo-root/
  CLAUDE.md
  .github/
    copilot-instructions.md
    instructions/
      architecture.instructions.md
      coding-style.instructions.md
      testing.instructions.md
      review.instructions.md
      security.instructions.md
      docs.instructions.md
    agents/
      backend-engineer.agent.md
      frontend-engineer.agent.md
      test-engineer.agent.md
      reviewer.agent.md
      docs-writer.agent.md
      harness-engineer.agent.md
    prompts/
      implement-feature.prompt.md
      fix-bug.prompt.md
      refactor.prompt.md
      write-tests.prompt.md
      review-pr.prompt.md
      update-docs.prompt.md
    skills/
      repository-analysis/SKILL.md
      implementation-planning/SKILL.md
      safe-refactoring/SKILL.md
      test-generation/SKILL.md
      pr-review/SKILL.md
      documentation-update/SKILL.md
```

Goal: Make common workflows repeatable and reviewable.

Completion signal: Different agents can execute the same common task at similar quality.

## Adapter-Heavy Profile

Use when multiple coding-agent tools must share one canonical harness.

```text
repo-root/
  CLAUDE.md
  AGENTS.md
  .github/               canonical harness
  .claude/               Claude-specific wrappers only
  .codex/                Codex-specific wrappers only, if needed
```

Goal: Share policy across tools while keeping tool-specific behavior isolated.

Completion signal: Adapters point to the same canonical rules and contain no duplicated policy.

## Rollout Phases

1. Minimal routing: create the canonical root, top-level instructions, and one router.
2. Domain rules: split durable rules into focused instruction files.
3. Reusable skills: convert repeated procedures into skills with verification.
4. Role definitions: add agents only for meaningful responsibility boundaries.
5. Automation: add scripts where deterministic checks or context compression help.
6. Maintenance: periodically remove unused files and merge duplicated rules.

## Choosing What To Add Next

Add a prompt when users repeatedly ask for the same task by name.

Add a skill when agents repeatedly follow the same multi-step procedure.

Add a script when the procedure includes deterministic data collection, transformation, generation, or validation.

Add an agent when role stance and ownership materially affect the result.

Add an adapter when a tool needs a specific entry file, command style, or capability note.
