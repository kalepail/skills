---
name: solo-save-prompts
description: Create, inspect, update, delete, fill, and export global or project Solo prompt templates with reusable placeholders. Use when saving recurring prompts, standardizing worker briefs or handoffs across agent tools, managing template scope, or backing templates up as Markdown. Do not use for current task state or durable project decisions.
---

# Save Solo Prompts

Store reusable prompt shape, not current orchestration state.

## Discover Current Template Surface

1. Call `whoami`; confirm effective project before project-scoped template work.
2. Call `help(topic="docs")` and inspect `mcp_tools_summary` or live tool discovery for prompt-template tools.
3. If tools are absent, report that prompt-template MCP feature may be disabled; do not guess schemas or enable settings without authority.
4. Read existing template before update; preserve omitted fields.

Read [prompt-templates.md](references/prompt-templates.md) before choosing scope, designing placeholders, updating/deleting, exporting, or creating templates that mention orchestration.

## Choose Scope

- Use global template for provider-neutral prompt used across projects.
- Use project template for repository-specific paths, rules, checks, and handoff shape.
- Keep names concise and unique within scope.
- Do not store live process IDs, todo IDs, revisions, branches, or transient state; fill them through placeholders at use time.

## Design Reusable Template

Use stable contract:

```text
Objective: {{objective}}
Authoritative inputs: {{inputs}}
Ownership: {{owned_scope}}
Forbidden work: {{forbidden}}
Acceptance: {{checks}}
Handoff: {{handoff}}
```

Make safety-critical constraints literal, not optional placeholders. Repeated placeholder name should represent same value.

## Manage Templates

- List before create to avoid same-scope duplicate.
- Get full body and parsed placeholders before update.
- Patch only intended fields.
- Delete only with explicit intent; deletion is permanent.
- Export for backup or repository sharing, not live synchronization.
- Prefer insert-and-review over immediate submit when rendered prompt can spawn agents, mutate files, control processes, or publish.

## Keep Boundaries Clear

- Use template to standardize worker prompt, timer follow-up, review, handoff, or integration checklist.
- Put current facts in scratchpad/todo/KV, not template.
- Execute workflow only through relevant lifecycle/orchestration skill after identity, scope, and ownership checks.
- Never include credentials, tokens, private evidence, or another actor's process IDs.
- Keep root/operator responsible for Git, integration, publishing, and deployment.
