# MCP discovery and protocol

Use this reference for Solo MCP transport, live discovery, identity, scope, tool routing, output controls, prompts, and resources.

## Transport and feature availability

Enable **Settings > MCP > MCP server** and use generated client configuration. Normal clients launch Solo's bundled stdio helper; no public MCP host or port exists. Helper reconnects across Solo restarts and buffers bounded in-flight requests. Solo-launched process identity persists across helper/app restarts; external clients retain session only for helper lifetime.

Treat live MCP discovery as authority. Core and feature availability varies by Solo version and settings. Scratchpad, todo, timer, key-value, and prompt-template tools can be toggled. Hosted docs may advertise tools absent from current runtime; for example, one observed runtime exposed 95 tools without six documented workspace tools.

## Discovery sequence

1. Call `whoami` and inspect actor, process, and effective project.
2. Call `help()` for overview.
3. Call one canonical topic: `processes`, `timers`, `coordination`, `locks`, `scratchpads`, `todos`, `spawning`, `inspection`, `readiness`, `projects`, `docs`, or `solo.yml`.
4. Call `mcp_tools_summary()` for enabled names grouped by category. Remember it omits schemas.
5. Use client tool discovery for exact current input schema before calling a tool.
6. If expected tool is absent, check feature toggle/version; do not invent call or silently switch to destructive substitute.

## Scope and identity

Resolve project in order:

1. Explicit `project_id` on current call.
2. Session selection from `select_project`.
3. Project bound to identified Solo process.

Use `list_projects` first when no scope exists. `select_project` changes only current MCP session default.

Use Solo process IDs returned by Solo tools. Do not substitute OS PID or another orchestrator's agent ID. Pass OS `pid` to `whoami`/`identify_session` only as fallback. Assert `solo_process_id` only with caller's own `SOLO_PROCESS_ID`; never use identity calls to target another process. Use `delivery_process_id` for timer recipient and `project_id` for scope.

## Catalog routing

| Need | Discover/help topic | Typical live tools |
|---|---|---|
| Projects/scope | `projects`, `inspection` | `list_projects`, `select_project`, `get_project`, `get_project_status`, `get_project_stats` |
| Processes/output | `processes`, `inspection` | `list_processes`, `get_process_status`, rendered/raw output and search, lifecycle/input tools |
| Services | `readiness` | `services_list`, `get_process_ports`, `wait_for_bound_port` |
| Agents | `spawning`, `processes` | `list_agent_tools`, `spawn_agent`, `spawn_process`, `send_input` |
| Shared state | `coordination`, `locks` | KV and advisory lease tools |
| Durable notes/tasks | `scratchpads`, `todos` | feature tool families with revisions, locks, tags, blockers, comments |
| Scheduling | `timers` | delay, idle-any/all, list, pause/resume/cancel |
| Setup/support | overview, `docs` | `help`, `mcp_tools_summary`, smoke test, integration setup, feedback draft |

Documented workspace tools are `list_workspaces`, `create_workspace`, `update_workspace`, `delete_workspace`, `reorder_workspaces`, and `move_project_to_workspace`. Call them only when live discovery exposes them.

## Output and search controls

- Rendered/raw process reads: default 50 lines, maximum 200 in observed MCP schemas.
- Rendered/raw searches: case-insensitive substring; default 20, maximum 100 matches.
- Scratchpad read: `full|content|headings|section`, line offset/limit, optional content-only response.
- Scratchpad find: literal query, scope, case flag, 1–100 matches, 0–3 context lines.
- Todo list: filters, text query, tags, sort, offset/limit; observed default 50, maximum 200.
- Todo/comment writes: prefer default `response_mode=slim`; request `rich` only when hydrated payload is needed.

## Prompts

Discover with standard `prompts/list`; load with `prompts/get`:

- `worker_bootstrap`: identity, locks, KV, scratchpads, todos, readiness, timers.
- `wait_for_bound_port`: bounded listener-readiness workflow.
- `timer_followup`: process injected timer body and shared-state follow-up.

Each returns one user message. Prefer prompt protocol over copying stale playbook text.

## Resources

Discover/read through standard `resources/list` and `resources/read`:

```text
solo://proj/{project_id}/scratchpad/{slug}--{scratchpad_id}
solo://proj/{project_id}/todo/{slug}--{todo_id}
```

Resources are `text/markdown`, cursor-paginated, and read-only. Scratchpad listing skips archived items. Todo resource includes comments. Visibility follows feature toggles. Use scratchpad/todo tools for writes.

## Sources

- https://soloterm.com/api/v1/docs/integrations/mcp-server
- https://soloterm.com/api/v1/docs/mcp-tools/overview
- https://soloterm.com/api/v1/docs/mcp-tools/setup-support
- https://soloterm.com/api/v1/docs/mcp-tools/project
- https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal
- https://soloterm.com/api/v1/docs/mcp-tools/output
- https://soloterm.com/api/v1/docs/mcp-tools/services
- https://soloterm.com/api/v1/docs/mcp-tools/workspaces
- https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources
