# Classification Rules

Use these rules when deciding where content belongs.

## Quick Decision Tree

```text
Is it a durable rule that should apply across many future tasks?
  yes -> instructions
  no -> continue

Is it an entry point the user intentionally invokes?
  yes -> prompt
  no -> continue

Is it a reusable procedure an agent can apply across tasks?
  yes -> skill
  no -> continue

Is it a role, stance, or responsibility boundary?
  yes -> agent
  no -> continue

Is it deterministic collection, transformation, calculation, or validation?
  yes -> script, documented by a skill
  no -> direct task context or ordinary project documentation
```

## Instructions

Use instructions for stable policy.

Good content:

- "All API handlers validate external input before use."
- "Use repository interfaces rather than direct DB calls from application services."
- "Review security issues before style issues."

Bad content:

- "Run `git diff`, then open each changed file." That is a skill procedure.
- "This week we are migrating auth." That is temporary task context.
- "When implementing feature X, add files A, B, C." That is a prompt or plan.

## Prompts

Use prompts for user-invoked task entries.

Good content:

- Purpose and success criteria.
- Required user inputs such as feature name, target files, issue link, or PR number.
- Scope boundaries and references to relevant instructions or skills.

Bad content:

- Full coding style policy.
- Long reusable implementation recipes.
- Tool-specific boilerplate that belongs in an adapter.

## Agents

Use agents for role, stance, and responsibility boundaries.

Good content:

- "Backend engineer owns server-side code, data access, and API endpoints."
- Judgment criteria and trade-offs.
- Which instructions and skills to consult.
- What to delegate or avoid changing.

Bad content:

- 50-line implementation steps.
- Duplicated testing, review, or security policy.
- Project facts that belong in top-level instructions.

## Skills

Use skills for reusable standard operating procedures.

Good content:

- Preconditions.
- Ordered steps.
- Expected outputs.
- Verification.
- Script invocation and interpretation.

Bad content:

- Permanent policy with no procedure.
- A one-off task request.
- An undocumented script dump.

## Scripts

Use scripts when deterministic execution is better than agent reasoning.

Good uses:

- List and classify harness files.
- Validate naming and frontmatter.
- Build a dependency graph.
- Generate starter files.
- Extract metrics or produce stable reports.

Script placement:

| Script use | Location |
|---|---|
| Used by multiple skills | `scripts/` |
| Used by one skill only | The skill directory, usually `scripts/` below that skill |

Every script needs a nearby skill or reference explaining how to run it, what inputs it expects, what output means, and what failures imply.

## Smell Tests

- If the same sentence appears in three files, choose one source and replace the others with pointers.
- If a file says "Step 1", check whether it should be a skill.
- If a prompt has rules that should apply when the prompt is not used, move them to instructions.
- If an agent file explains how to run commands, move that procedure to a skill.
- If a script has no documented caller, add a skill reference or remove the script.
