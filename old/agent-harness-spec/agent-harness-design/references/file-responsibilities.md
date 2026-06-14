# File Responsibilities

## Standard Locations

| File or directory | Responsibility | Put here | Keep out |
|---|---|---|---|
| `.github/copilot-instructions.md` | Repository-wide durable policy | Project summary, stack, domain terms, essential conventions, high-level directory map | Task procedures, temporary work, long algorithms |
| `.github/instructions/*.instructions.md` | Domain-specific durable rules | Architecture, coding style, testing, security, review, docs policy | Step-by-step task execution, one-off requests |
| `.github/prompts/*.prompt.md` | User-invoked task entry points | Task objective, input variables, scope, acceptance criteria, references to skills | Permanent coding rules, long reusable procedures |
| `.github/agents/*.agent.md` | Role and responsibility definitions | Role, judgment criteria, boundaries, files and skills to consult | Long task steps, duplicated policy |
| `.github/skills/<skill-name>/SKILL.md` | Reusable standard procedure | Preconditions, steps, outputs, verification, script invocation | Project-wide policy that belongs in instructions |
| `scripts/` | Shared deterministic tools | Data collection, transforms, validation, reports used by multiple skills | Undocumented one-off scripts |
| `.github/skills/<name>/scripts/` or skill-local scripts | Skill-specific deterministic tools | Helpers used by one skill | Shared utilities used elsewhere |
| `CLAUDE.md`, `AGENTS.md`, `.claude/*` | Tool adapter and router | Where to read next, tool-specific invocation rules | Full policy copies from canonical files |

## Naming

- Use kebab-case for harness file stems and skill directories.
- Instructions end with `.instructions.md`.
- Prompts end with `.prompt.md`.
- Agent definitions end with `.agent.md` unless the host tool requires another suffix.
- Skill directories use action-oriented names such as `repository-analysis`, `safe-refactoring`, or `test-generation`.
- Codex-discoverable skill files must be named exactly `SKILL.md`.

## Frontmatter

For Codex skills, use only:

```yaml
---
name: skill-name
description: Clear trigger description and supported tasks.
---
```

For repository harness files, use a small metadata block when the host tool supports it:

```yaml
---
description: "One-line purpose"
version: "1.0.0"
last_updated: "YYYY-MM-DD"
owner: "Team or maintainer"
---
```

Do not rely on frontmatter to carry important instructions. The body should remain understandable if metadata is ignored.

## Size Guidelines

| File type | Soft limit | Split when |
|---|---:|---|
| `CLAUDE.md` or router | 100 lines | It starts teaching policy instead of routing |
| `copilot-instructions.md` | 500 lines | It contains multiple independent domains |
| `*.instructions.md` | 200 lines | A domain has subdomains with distinct audiences |
| `*.agent.md` | 120 lines | It starts describing procedures |
| `*.prompt.md` | 150 lines | It contains reusable steps |
| `SKILL.md` | 500 lines | Detailed variants or examples dominate the procedure |

These are not hard limits. Use them as prompts to examine maintainability.

## Standard Instruction Files

Start with only the files that the repository can keep current:

| File | Use when |
|---|---|
| `architecture.instructions.md` | Architecture decisions repeat or must stay consistent |
| `coding-style.instructions.md` | Language, formatting, and naming rules are stable |
| `testing.instructions.md` | Test strategy, naming, fixtures, and coverage matter |
| `security.instructions.md` | The project handles secrets, user input, auth, data, or production systems |
| `review.instructions.md` | PR quality gates and review style should be consistent |
| `docs.instructions.md` | Documentation conventions affect recurring work |

## Standard Skills

Common reusable procedures:

| Skill | Purpose |
|---|---|
| `repository-analysis` | Gather structure, related files, existing patterns, and dependencies |
| `implementation-planning` | Convert requirements and repo context into an implementation plan |
| `safe-refactoring` | Preserve behavior through small steps and repeated verification |
| `test-generation` | Derive and implement focused tests from target code |
| `pr-review` | Review diffs consistently against correctness, security, tests, and design |
| `documentation-update` | Update docs in response to code or behavior changes |
