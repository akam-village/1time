# Anti-Patterns

Use this file during audits and refactors. Prefer moving useful content to the correct layer over deleting it.

## AP-01: Procedures In Instructions

Symptom: `*.instructions.md` contains step-by-step work such as "Step 1: run git diff."

Why it hurts: Instructions should be durable policy. Procedures change more often and belong in skills.

Fix: Move the steps to a skill and leave a short rule or pointer in the instruction file.

## AP-02: Long Procedures In Agents

Symptom: `*.agent.md` contains a long implementation, review, or testing recipe.

Why it hurts: Agent files should define stance and boundaries. Long recipes are harder to share between agents.

Fix: Create or reuse a skill. Keep the agent file to role, judgment criteria, references, and boundaries.

## AP-03: Durable Policy In Prompts

Symptom: A prompt repeats coding style, security, or architecture rules.

Why it hurts: The rule is skipped when the prompt is not used and drifts from the canonical policy.

Fix: Move durable policy to instructions. In the prompt, reference the instruction file.

## AP-04: Rule Duplication

Symptom: The same rule appears in top-level instructions, a domain instruction file, prompts, and agents.

Why it hurts: The files will eventually disagree.

Fix: Pick the most specific durable source and replace other copies with references.

## AP-05: Router Becomes Policy Manual

Symptom: `CLAUDE.md`, `AGENTS.md`, or another router contains detailed coding standards, architecture policy, or procedures.

Why it hurts: Routers are always-loaded and tool-specific. They become bloated and create duplicate truth.

Fix: Keep the router under about 100 lines. Move policy to the canonical harness.

## AP-06: Temporary Work In Durable Files

Symptom: Instructions include date-bounded migration notes, sprint tasks, or temporary exceptions.

Why it hurts: Temporary context becomes stale and keeps influencing future work.

Fix: Put temporary context in the task prompt, issue, PR, project doc, or current conversation.

## AP-07: Adapter Duplicates Canonical Harness

Symptom: `.claude/`, `.codex/`, or another adapter copies the same policy as `.github/`.

Why it hurts: Tool-specific copies drift and make maintenance expensive.

Fix: Make the adapter a thin pointer with only tool-specific differences.

## AP-08: Script Without Skill

Symptom: A script exists in `scripts/` or a skill directory but no skill explains when or how to use it.

Why it hurts: The script becomes a black box and agents may misuse it.

Fix: Document invocation, inputs, outputs, and failure interpretation in a skill or reference.

## AP-09: Starter Harness Too Large

Symptom: A new project begins with dozens of agents, prompts, and skills copied from a template.

Why it hurts: Unused harness files decay quickly and reduce trust.

Fix: Start minimal. Add files only when recurring work proves the need.

## AP-10: Cyclic References

Symptom: A prompt defines a skill, the skill redefines prompt scope, and an agent restates both.

Why it hurts: Agents cannot determine authority when files conflict.

Fix: Restore dependency direction and single-source rules.
