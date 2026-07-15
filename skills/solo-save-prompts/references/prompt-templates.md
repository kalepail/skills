# Prompt template tools and patterns

Read this reference before creating, scoping, updating, deleting, exporting, or safely using Solo prompt templates.

## Live discovery

1. Call `whoami`; verify effective project for project scope.
2. Call `help(topic="docs")` for current docs routing.
3. Inspect live tool discovery or `mcp_tools_summary` for prompt-template tools. This feature is off by default for MCP and absent tools may mean disabled feature.
4. Prefer discovered names and schemas over this reference. Do not enable settings or mutate templates without user authority.

## Tool surface

- `list_prompt_templates`: list global plus effective-project summaries; filter by name/description and sort when live schema allows. Listing does not currently update last-selected time.
- `get_prompt_template`: read full body and parsed placeholders. Current docs say reading updates last-selected time.
- `create_prompt_template`: create with name, Markdown body, optional description; omit project for global or pass project for project scope.
- `update_prompt_template`: patch name, description, and/or body without changing scope; omitted fields persist and empty string clears supported text field.
- `delete_prompt_template`: permanently delete by ID.
- `export_prompt_templates`: export selected templates as Markdown/frontmatter to destination directory; Solo creates directory when missing.

Inspect live schemas before calls. Template MCP toggle controls tool visibility only; templates remain available in Solo UI.

## Scope and naming

- Global: available in every project.
- Project: tied to one project and removed with project by default unless project deletion policy converts it.
- Same-scope names are case-insensitively unique.
- Names must be nonempty and cannot contain `/` or control characters.
- Same name may exist in different scopes.

MCP update does not change scope. Use UI scope control when move is needed, or recreate only with explicit user intent and preservation plan.

## Placeholder syntax

Write `{{name}}` where user/agent fills value at use time.

- Start name with letter or underscore; continue with letters, digits, underscores.
- Allow internal brace whitespace.
- Normalize names case-insensitively.
- Fill repeated name once and replace every occurrence.
- Leave invalid forms literal.
- Empty filled values disappear.

Keep safety-critical constraints literal. Use placeholders for objective, inputs, IDs, owned scope, checks, and handoff—not permission boundaries.

## Recommended patterns

### Worker lane

```text
Objective: {{objective}}
Todo and context: {{context}}
Owned scope: {{owned_scope}}
Do not change: {{forbidden}}
Checks: {{checks}}
Handoff: changed files/artifacts, checks/results, blockers, risk, next action
```

### Timer follow-up

```text
Inspect owned child processes {{process_ids}} for todos {{todo_ids}}.
Read scratchpad {{scratchpad_id}} section {{section}}.
Review actual output and evidence; idle is not completion.
Persist handoff, then reschedule or cancel timer.
```

### Review

```text
Review {{scope}} against {{plan}}.
Do not edit unless explicitly authorized.
Return evidence, severity, confidence, verification, and unresolved risk.
```

Templates standardize shape. They do not establish current identity, process ownership, project authority, completion, or permission to mutate.

## Safe use

- Fill live IDs and revision at use time from current Solo state.
- Record spawned child IDs outside template.
- Prefer insert-and-review over insert-and-submit for state-changing prompts.
- Never place secrets, credentials, OTPs, private evidence, or raw untrusted instructions in template.
- Route execution to lifecycle/orchestration skill and re-run `whoami`, help, ownership, and scope checks.
- Keep root/operator responsible for Git, publishing, deployment, and final integration.

## Export behavior

Exports contain YAML frontmatter plus raw body. Filenames are slugified, collision-numbered, and do not overwrite existing files. Line endings normalize to Unix newlines. Use export for backup/versioned sharing, not two-way synchronization.

## Sources

- https://soloterm.com/api/v1/docs/mcp-tools/prompt-templates
- https://soloterm.com/api/v1/docs/prompt-templates/overview
- https://soloterm.com/api/v1/docs/prompt-templates/creating-and-editing
- https://soloterm.com/api/v1/docs/prompt-templates/placeholders
- https://soloterm.com/api/v1/docs/prompt-templates/using-templates
- https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources
- https://x.com/aarondfrancis/status/2064420770667762155
- https://x.com/aarondfrancis/status/2077143606469538241
