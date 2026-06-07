# Core Model

## Purpose

An Agent Harness is the repository-local operating environment that helps coding agents act with consistent intent, rules, procedures, memory pointers, tools, and guardrails. It turns ad hoc chat instructions into maintainable files that agents can discover, route through, and reuse.

The harness should answer five questions:

| Question | Harness concern |
|---|---|
| What is this project and what matters here? | Mission and project facts |
| What rules are always true? | Policies and guardrails |
| Which role should handle this work? | Agent definitions |
| Which task is the user asking for? | Prompts and routing |
| Which repeated procedure or computation should be reused? | Skills and scripts |

## Layer Model

Use this as the default layer order. Rename directories for the host tool if needed, but preserve the responsibilities.

```text
Layer 0: Routing adapters
  CLAUDE.md, AGENTS.md, .claude/*, tool-specific entry files

Layer 1: Durable rules
  .github/copilot-instructions.md
  .github/instructions/*.instructions.md

Layer 2: Role definitions
  .github/agents/*.agent.md

Layer 3: User-invoked task entries
  .github/prompts/*.prompt.md

Layer 4: Reusable procedures
  .github/skills/*/SKILL.md

Layer 5: Deterministic tools
  scripts/*, .github/skills/<name>/scripts/*, skill-local helper scripts
```

## Design Principles

1. Choose one source of truth. Duplicated rules drift.
2. Give each file one responsibility.
3. Let the caller determine the entry point: users call prompts, agents use skills, skills call scripts.
4. Separate reasoning from computation. Agents interpret, plan, and decide; scripts collect, calculate, transform, and validate.
5. Prefer progressive disclosure. Keep always-loaded files short and move details into files that are read only when needed.

## Canonical Root and Adapters

The original harness pattern uses `.github/` as the canonical root because GitHub Copilot can discover it and other tools can point to it. Generalize this to "one canonical root plus thin adapters."

Recommended default:

| Role | Location |
|---|---|
| Canonical harness | `.github/` |
| Claude Code router | `CLAUDE.md` and optionally `.claude/` |
| Codex-specific extension | `.codex/` or installed Codex skill, only for Codex-specific behavior |
| Shared scripts | `scripts/` |

Adapters should route to the canonical harness and describe only tool-specific behavior. They should not restate project policy.

## Change Cadence

| Layer | Expected change rate | Typical trigger |
|---|---|---|
| Routing adapter | Low | Tool migration or repository layout change |
| Durable rules | Low to medium | Team policy or architecture changes |
| Role definitions | Low | Team role or delegation model changes |
| Prompts | Medium | New recurring user tasks |
| Skills | High | Better procedures discovered during work |
| Scripts | High | Automation opportunities and validation improvements |

High-change content should not live in always-loaded files.
