# Routing And Dependencies

## Router Pattern

A router is a short file that tells the agent what to read next. It should not teach the full policy.

Common routers:

| Router | Scope |
|---|---|
| `CLAUDE.md` | Claude Code entry file |
| `AGENTS.md` | Generic agent entry file, when used by the host |
| `.claude/agents/*.md` | Claude-specific wrappers around canonical agents |
| `.claude/skills/*/SKILL.md` | Claude-specific tool notes around canonical skills |

Router contents:

- Project one-liner.
- Canonical harness root.
- Task-to-reference map.
- Optional role-to-agent map.
- Brief post-work checks.
- Rule saying detailed policy belongs in the canonical harness.

## Dependency Direction

Keep dependencies one way:

```text
router/adapters
  -> top-level project instructions
    -> domain instructions
      -> agents
        -> prompts
          -> skills
            -> scripts
```

Shortcuts are allowed when a user directly invokes a prompt or skill, but lower layers should not redefine upper-layer policy.

## Task Routing Map

Use a repository-specific version of this table:

| Task | Required references | Optional references |
|---|---|---|
| New feature | `copilot-instructions.md`, `architecture.instructions.md` | `implement-feature.prompt.md`, `implementation-planning/SKILL.md` |
| Bug fix | `copilot-instructions.md`, `coding-style.instructions.md` | `fix-bug.prompt.md`, `repository-analysis/SKILL.md` |
| Refactor | `architecture.instructions.md`, `testing.instructions.md` | `refactor.prompt.md`, `safe-refactoring/SKILL.md` |
| Test work | `testing.instructions.md` | `write-tests.prompt.md`, `test-generation/SKILL.md` |
| PR review | `review.instructions.md`, `security.instructions.md` | `review-pr.prompt.md`, `pr-review/SKILL.md` |
| Docs update | `docs.instructions.md` | `update-docs.prompt.md`, `documentation-update/SKILL.md` |
| Security change | `security.instructions.md` | `fix-bug.prompt.md`, security-specific skill if present |
| Harness change | harness design spec or this skill | `lint_harness.py`, `scaffold_harness.py` |

## Agent Launch Map

Role maps are optional. Add them only when role separation improves quality or parallelism.

| Role | Definition | Trigger |
|---|---|---|
| Backend engineer | `.github/agents/backend-engineer.agent.md` | Server-side code, APIs, data access |
| Frontend engineer | `.github/agents/frontend-engineer.agent.md` | UI, client state, frontend integration |
| Test engineer | `.github/agents/test-engineer.agent.md` | Test strategy or test implementation |
| Reviewer | `.github/agents/reviewer.agent.md` | PR or code review |
| Docs writer | `.github/agents/docs-writer.agent.md` | Docs, comments, changelog |
| Harness engineer | `.github/agents/harness-engineer.agent.md` | Harness file changes |

Avoid creating roles that the team will not maintain.

## Adapter Rules

- A tool-specific adapter may name tool commands, capabilities, or constraints.
- A tool-specific adapter should point to canonical instructions rather than restating them.
- If two adapters need the same rule, move that rule to the canonical harness.
- If the canonical harness cannot represent a tool-specific behavior, keep the behavior in the adapter and label it as tool-specific.
