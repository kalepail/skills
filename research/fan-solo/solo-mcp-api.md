# Solo technical integration surface

Research date: 2026-07-15. Sources: live Solo MCP runtime, Solo docs MCP snapshot generated 2026-07-15, official raw Markdown docs, official web search, and live hosted `/api/v1/agents` manifest.

## Executive map

Solo exposes five distinct integration surfaces:

1. **Local MCP server**: stdio helper backed by running Solo app. Current queried runtime exposes **95 tools** across 10 categories, plus three MCP prompts and read-only scratchpad/todo resources. [MCP overview](https://soloterm.com/api/v1/docs/mcp-tools/overview)
2. **Local HTTP API**: loopback REST server, routes rooted at `/api`, bearer-token protected, used by CLI. Its discovery document reports `apiVersion: "1"`; do not confuse it with hosted `/api/v1`. [HTTP API](https://soloterm.com/api/v1/docs/integrations/http-api)
3. **`solo` CLI**: bundled companion binary using local HTTP API discovery and token. [CLI overview](https://soloterm.com/api/v1/docs/cli/overview)
4. **`solo://` deep links**: navigation URIs for project/process/scratchpad/todo. Scratchpad/todo forms also serve as MCP resource URIs. [Deep links](https://soloterm.com/api/v1/docs/integrations/deep-links)
5. **Hosted public API v1**: internet-facing `https://soloterm.com/api/v1/...` docs, downloads, updates, licensing, notifications, feedback, and scoped admin automation. [Agent manifest](https://soloterm.com/api/v1/agents)

Runtime/catalog discrepancy: hosted MCP docs describe six workspace tools as core (`list_workspaces`, `create_workspace`, `update_workspace`, `delete_workspace`, `reorder_workspaces`, `move_project_to_workspace`), but queried `mcp_tools_summary` returned 95 tools and none of those six. Treat runtime discovery as authority for availability; treat docs as supported/version-dependent contract. [Workspace MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/workspaces)

## Local MCP setup and transport

- Enable **Settings > MCP > MCP server**. Copy generated stdio config or run supported client setup. Supported detected CLI clients include Claude Code, Codex CLI, Gemini CLI, Amp, OpenCode, Copilot CLI, and Kimi CLI; app/IDE snippets include Cursor, Windsurf, Cline, and Claude Desktop. [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server)
- Normal clients launch bundled `mcp` helper. No public MCP host/port. Non-default app-data path is passed to helper. [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server)
- Helper reconnects with backoff across Solo restarts, buffers a bounded few MB of requests while app is unavailable, and replays after reconnect. Solo-launched agent identity/session persists per process across helper/app restarts; other clients retain stable session only for helper lifetime. [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server)
- Core groups are server-controlled. Scratchpad, todo, timer, key-value, and prompt-template groups are feature toggles. Scratchpads/todos/timers inherit MCP enablement until explicitly saved; key-value and prompt-template tools default off. [MCP tools overview](https://soloterm.com/api/v1/docs/mcp-tools/overview)

## MCP scope and identity rules

Project scope resolves in this order:

1. Explicit `project_id` on one call.
2. Session-selected project from `select_project`.
3. Project bound to identified Solo process.

`select_project` changes only current MCP session default. Use `list_projects` first when no scope exists and `whoami` to inspect selected, bound, detected, and effective IDs. [Project MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/project)

Process targets accept `process_id` or `process_name`; numeric names and `<slug>--<id>` resolve. These IDs are Solo process IDs, not OS PIDs and not IDs from another agent orchestrator. `pid` on `whoami`/`identify_session` is only host-OS fallback. `solo_process_id` on `identify_session` is caller's own `SOLO_PROCESS_ID`; never use it to impersonate or target another process. External callers may register an actor (`external.name`, optional `agent_id`, `metadata`) for locks, todos, scratchpads, and timers. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)

## Enabled MCP inventory: 95 tools

Notation: `?` means optional. `target` means one of `process_id` or `process_name`; most target calls also accept `project_id?`. Signatures show critical request fields, not full response objects. Runtime count/category membership came from live `mcp_tools_summary`; schemas came from live tool declarations and were checked against all 12 canonical `help` topics.

### Agents (4)

[Agent/terminal reference](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)

- `list_agent_tools()` — configured runtimes; returned `id` feeds `agent_tool_id`.
- `setup_agent_integration(project_id?, target?)` — write/update Solo guidance in `CLAUDE.md` (default) or `AGENTS.md`; review like any repo instruction edit.
- `spawn_agent(agent_tool_id, agent_tool_installation_id?, extra_args?: string[], include_agent_instructions?=true, name?, project_id?)` — preferred agent creator; returns Solo `process_id`, name, bootstrap instructions.
- `spawn_process(kind, agent_tool_id?, agent_tool_installation_id?, extra_args?, include_agent_instructions?, name?, project_id?)` — `kind` is `terminal` or `agent`; agent needs tool ID/installation.

Spawn does not change caller identity. Prepend returned `agent_instructions` to first prompt, then call `send_input`.

### Coordination (7)

[Coordination](https://soloterm.com/api/v1/docs/mcp-tools/coordination) and [key-value](https://soloterm.com/api/v1/docs/mcp-tools/key-value) references.

- `kv_set(key, value: JSON, ttl_seconds?, project_id?)`
- `kv_get(key, project_id?)`
- `kv_list(prefix?, limit?, project_id?)`
- `kv_delete(key, project_id?)`
- `lock_acquire(lock_key, lease_ttl_seconds, project_id?)` — non-blocking advisory lease acquisition.
- `lock_status(lock_key, project_id?)`
- `lock_release(lock_key, project_id?)` — only owning actor can release.

Use KV for small discoverable JSON state, scratchpads for long text. Stable specific lock keys; release after protected work.

### Processes and output (18)

[Process](https://soloterm.com/api/v1/docs/mcp-tools/process), [output](https://soloterm.com/api/v1/docs/mcp-tools/output), and [bulk](https://soloterm.com/api/v1/docs/mcp-tools/bulk) references.

- `list_processes(project_id?)`
- `get_process_status(target, project_id?)`
- `select_process(target, project_id?)` — changes Solo UI selection/attachment.
- `rename_process(target, new_name, project_id?)`
- `start_process(target, project_id?)`
- `stop_process(target, project_id?)`
- `restart_process(target, project_id?)`
- `close_process(target, confirm_self_close?, project_id?)` — terminal/agent removal, not command lifecycle.
- `send_input(target, input?, bytes?: number[], submit?=true, wait_ms?, project_id?)` — bytes override text/submit; `wait_ms` clamped 250–10,000 ms. Common control bytes: `3` Ctrl-C, `4` Ctrl-D, `13` Enter, `27` Escape.
- `get_process_output(target, lines?=50, project_id?)` — rendered rows, maximum 200.
- `get_process_raw_output(target, lines?=50, project_id?)` — raw stream/control sequences, maximum 200.
- `search_output(target, pattern, max_results?=20, project_id?)` — rendered, case-insensitive substring, maximum 100 matches, 1-based row numbers.
- `search_raw_output(target, pattern, max_results?=20, project_id?)` — raw, same search bounds.
- `clear_output(target, project_id?)` — clears saved buffer only; PTY/process continues.
- `get_process_ports(target, project_id?)` — process and child listeners/URLs.
- `start_all_commands(project_id?)`
- `stop_all_commands(project_id?)`
- `restart_all_commands(project_id?)`

Start/restart existing entries. Spawn new terminals/agents. Bulk calls affect command processes only. Trust checks still apply.

### Projects (8)

[Project MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/project)

- `list_projects()` — live runtime schema has no exposed filter; hosted docs additionally describe optional `workspace_id` on versions with workspace support.
- `select_project(project_id)`
- `get_project(project_id?)`
- `get_project_status(project_id?)`
- `get_project_stats(project_id?)`
- `create_project(path, name?)` — existing directory; canonical-path idempotent, existing project returned and name ignored.
- `rename_project(display_name: string|null, project_id?)` — null clears override.
- `delete_project(project_id?, confirm_delete, confirm_stop_running?, prompt_template_policy?)` — policy `delete` (default) or `convert_to_global`.

### Prompt templates (6)

Feature group, off by default. [Prompt-template MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/prompt-templates)

- `list_prompt_templates(project_id?, query?, sort?)` — global plus effective-project pool; sort `picker` (default), `name`, `updated`, `created`, `last_selected`; does not update last-selected time.
- `get_prompt_template(template_id)` — body and parsed placeholders; updates last-selected time.
- `create_prompt_template(name, body, description?, project_id?)` — omitted project creates global template; same-scope name uniqueness.
- `update_prompt_template(template_id, name?, description?, body?)` — omitted/null preserves; empty description/body clears; scope immutable.
- `delete_prompt_template(template_id)` — one ID; no MCP bulk delete.
- `export_prompt_templates(template_ids: number[], destination_dir)` — Markdown/frontmatter; creates directory; app-equivalent slug and duplicate numbering.

### Readiness (2)

[Services MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/services)

- `services_list(project_id?)` — project-wide detected listeners, readiness, URLs, ports.
- `wait_for_bound_port(target?, timeout_ms?, project_id?)` — ready listener or `ready=false, timed_out=true`.

Readiness means Solo detected local listening port and associated process. Use these for server startup; idle timers measure worker quiet, not health.

### Scratchpads (18)

[Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)

- `scratchpad_list(project_id?, query?, tags?: string[], offset?, limit?)` — metadata/snippets, no full content.
- `scratchpad_tags_list(project_id?)`
- `scratchpad_read(scratchpad_id, project_id?, mode?, section_heading?, offset?, limit?, content_only?)` — modes `full`, `content`, `headings`, `section`; omitted mode may fall back to headings for large reads.
- `scratchpad_find(scratchpad_id, query, project_id?, scope?=all, case_sensitive?=false, limit?=20, context_lines?=1)` — literal substring; scope `all|headings|content`; limit 1–100; context 0–3.
- `scratchpad_tail(scratchpad_id, project_id?, lines?=10)` — `0` gives metadata with empty content.
- `scratchpad_write(name, content, tags?, project_id?, scratchpad_id?, expected_revision?)` — create when ID/revision omitted; otherwise full replace. Leading H1 overrides name.
- `scratchpad_rename(scratchpad_id, name, expected_revision, project_id?)`
- `scratchpad_add_tags(scratchpad_id, tags[], expected_revision, project_id?)`
- `scratchpad_remove_tags(scratchpad_id, tags[], expected_revision, project_id?)`
- `scratchpad_append(scratchpad_id, content, expected_revision?, project_id?)`
- `scratchpad_append_section(scratchpad_id, heading, content, expected_revision?, project_id?)` — normalized, case-insensitive heading match.
- `scratchpad_edit(scratchpad_id, target, content, expected_revision, project_id?)` — target `{"type":"section","section_heading":"..."}` or `{"type":"line_range","offset":0,"limit":1}`.
- `scratchpad_clear(scratchpad_id, expected_revision, project_id?)`
- `scratchpad_delete(scratchpad_id, expected_revision, project_id?)`
- `scratchpad_archive(scratchpad_id, project_id?)`
- `scratchpad_transfer(scratchpad_id, target_project_id, expected_revision, project_id?)`
- `scratchpad_save_to_file(scratchpad_id, path, project_id?)`
- `scratchpad_load_from_file(name, path, project_id?, scratchpad_id?, expected_revision?)`

Prefer read plus targeted edit/append. Revisions prevent lost updates. Relative import/export paths must remain inside project, including after symlink resolution; absolute paths are honored when readable/writable.

### Setup/support (6)

[Setup/support MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/setup-support)

- `help(topic?)` — overview or canonical topic: `processes`, `timers`, `coordination`, `locks`, `scratchpads`, `todos`, `spawning`, `inspection`, `readiness`, `projects`, `docs`, `solo.yml`. Aliases include services/ports/urls/ready/status/inspect/kv/state/scope/howto/guide/yml/yaml.
- `mcp_tools_summary()` — enabled tools by category with descriptions; intentionally omits schemas.
- `mcp_smoke_test(project_id?)` — disposable scratchpad/todo create-read-update-delete check; requires both feature groups; cleanup attempted even on failure.
- `whoami(pid?, verbose?)`
- `identify_session(solo_process_id?, pid?, external?)`
- `submit_solo_feedback(message, email?, include_context?=true)` — opens prefilled feedback form for human review/manual submission.

### Timers (7)

[Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)

- `timer_set(delay_ms, body, delivery_process_id?, loop?, repeat_every_ms?, metadata?, project_id?)`
- `timer_fire_when_idle_any(processes[], max_wait_ms, body, delivery_process_id?, metadata?, project_id?)`
- `timer_fire_when_idle_all(processes[], max_wait_ms, body, delivery_process_id?, metadata?, project_id?)`
- `timer_list(limit?, project_id?)`
- `timer_cancel(timer_id, project_id?)`
- `timer_pause(timer_id, project_id?)`
- `timer_resume(timer_id, project_id?)`

Every timer delivers to exactly one Solo agent. `delivery_process_id` selects recipient; idle `processes` list only selects watchers. Entries may be Solo ID, name, or target object. `max_wait_ms` is hard deadline, not poll interval. Idle-any ignores already-idle processes; idle-all counts them and may return `already_satisfied` without creating timer. Body is injected verbatim as fresh user turn: use self-contained plain text with IDs and next action. Cancel obsolete timers.

### Todos (19)

[Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos)

- `todo_create(title, body?, priority?, tags?, response_mode?=slim, project_id?)`
- `todo_list(project_id?, status?, completed?, is_blocked?, priority?, query?, tags?, sort?, offset?, limit?=50)` — maximum 200. Status `open|in_progress|backlog|completed`; priority `high|medium|low`; sorts `priority|created-desc|created-asc|updated-desc|updated-asc|completed-desc|completed-asc`.
- `todo_tags_list(project_id?)`
- `todo_get(todo_id, include_comments?=false, project_id?)`
- `todo_update(todo_id, title?, body?, priority?, status?, tags?, response_mode?=slim, project_id?)`
- `todo_add_tag(todo_id, tag, response_mode?=slim, project_id?)`
- `todo_remove_tag(todo_id, tag, response_mode?=slim, project_id?)`
- `todo_transfer(todo_id, target_project_id, response_mode?=slim, project_id?)` — preserves comments/completion; clears blockers/locks.
- `todo_set_blockers(todo_id, blocker_ids?, response_mode?=slim, project_id?)`
- `todo_add_blocker(todo_id, blocker_id, response_mode?=slim, project_id?)`
- `todo_remove_blocker(todo_id, blocker_id, response_mode?=slim, project_id?)`
- `todo_complete(todo_id, completed, release_lock?=true, response_mode?=slim, project_id?)`
- `todo_lock(todo_id, lease_ttl_seconds?=300, response_mode?=slim, project_id?)`
- `todo_unlock(todo_id, response_mode?=slim, project_id?)`
- `todo_delete(todo_id, project_id?)`
- `todo_comment_create(todo_id, body, response_mode?=slim, project_id?)`
- `todo_comment_update(comment_id, body, response_mode?=slim, project_id?)`
- `todo_comment_delete(comment_id, project_id?)`
- `todo_comment_list(todo_id, offset?, limit?, project_id?)`

Most writes default to compact `slim` ID receipts; pass `response_mode=rich` only when hydrated object/comment is needed. Process-owned locks release when bound process closes. Completion normally releases caller's todo lock and returns affected todo IDs.

## Documented workspace MCP tools not enabled in queried runtime

[Workspace MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/workspaces)

- `list_workspaces()`
- `create_workspace(name, icon?, color?)`
- `update_workspace(workspace_id, name?|icon?|color?)` — at least one change.
- `delete_workspace(workspace_id, destination_workspace_id?)` — last workspace cannot be deleted; destination required when projects remain.
- `reorder_workspaces(workspace_ids[])` — every workspace exactly once.
- `move_project_to_workspace(project_id, workspace_id, before_project_id?|after_project_id?)` — placement hints mutually exclusive; linked checkout group moves too.

Versions exposing these also add `workspace_id?` to `list_projects` and `create_project`.

## MCP prompts and resources

Standard MCP `prompts/list` and `prompts/get` expose three built-in single-user-message playbooks: [prompts/resources reference](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)

- `worker_bootstrap` — identity, locks before shared edits, KV/scratchpad/todo durable state, readiness/timers over polling.
- `wait_for_bound_port` — bounded process readiness workflow and result interpretation.
- `timer_followup` — process injected timer body, check shared state, cancel obsolete timers.

Standard `resources/list` and `resources/read` expose enabled feature data as `text/markdown`:

```text
solo://proj/{project_id}/scratchpad/{slug}--{scratchpad_id}
solo://proj/{project_id}/todo/{slug}--{todo_id}
```

Scratchpad resource returns Markdown content. Todo resource renders todo plus comments. Listing is cursor-paginated and skips archived scratchpads. Resource visibility follows scratchpad/todo tool toggles. Both URI patterns are advertised through resource templates. Resources are read-only; mutate through tools. Live runtime listing confirmed both templates and a cursor-bearing resource page.

## Output, search, and pagination controls

| Surface | Controls |
|---|---|
| MCP rendered/raw process read | `lines` default 50, maximum 200. |
| MCP process search | Case-insensitive substring; `max_results` default 20, maximum 100; rendered or raw variants. |
| MCP scratchpad read | `mode`, `section_heading`, zero-based `offset`, line `limit`, optional `content_only`. |
| MCP scratchpad search | Literal query; scope, case flag, 1–100 matches, 0–3 context lines. |
| MCP todo list | Offset/limit, filters, query, tags, sort; default 50, maximum 200. |
| MCP write output | Todo/comment `response_mode=slim` default; `rich` explicit. |
| MCP resources | Cursor pagination. |
| Local HTTP lists | Offset/limit; default 50, maximum 500; oversize clamps and sets `limitClamped=true`. Workspace list is unpaginated. [HTTP API](https://soloterm.com/api/v1/docs/integrations/http-api) |
| CLI lists | `--offset`, `--limit`; JSON data includes `totalCount`, `hasMore`, `nextOffset`. [JSON scripting](https://soloterm.com/api/v1/docs/cli/json-output-and-scripting) |

## Safety and mutation rules

- **Command trust:** untrusted `solo.yml` command cannot manual-start, auto-start, restart, file-watch restart, or crash-restart. Trust is local, project-and-exact-variant scoped. Changes to command, working directory, environment, auto-start, auto-restart, or watch patterns can invalidate it. MCP bulk/single start and restart cannot bypass trust. [Trust and security](https://soloterm.com/api/v1/docs/commands/trust-security)
- **Project deletion:** MCP requires `confirm_delete=true`; additionally `confirm_stop_running=true` for running/starting/stopping processes. Local HTTP/CLI use running-process confirmation. Disk project files are not deleted. Prompt templates default to deletion unless converted global. [Project MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/project)
- **Self-close:** `confirm_self_close=true` only when user explicitly asked current process to close itself.
- **Identity:** `identify_session` asserts caller identity, never target identity. Use `delivery_process_id` for timers and `project_id` for scope.
- **Scratchpad concurrency:** read revision, then targeted edit/rename/delete with `expected_revision`; mismatch must fail, re-read, reconcile, retry. Append guards are optional over MCP, required by current CLI docs. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- **Filesystem paths:** scratchpad relative imports/exports stay within project and reject `..`/symlink escape. Absolute paths are deliberate direct access.
- **Locks:** advisory leases, actor-owned, short-lived; not authorization. Todo transfer clears locks/blockers.
- **Timers:** injected body becomes fresh user turn. Treat body as executable instruction context; keep self-contained and avoid markup-heavy payloads.
- **Feedback:** MCP opens draft for human review; it does not silently submit.
- **Deep links:** malformed/stale targets are ignored without navigation/error; readable slug is not authority, numeric ID is. [Deep links](https://soloterm.com/api/v1/docs/integrations/deep-links)

## `solo.yml` integration contract

Top-level schema: [solo.yml docs](https://soloterm.com/api/v1/docs/projects/solo-yml)

```yaml
name: string                    # optional
icon: relative/path.png        # optional
icon_initials: SF              # optional, 1-2 chars
processes:
  Process name:
    command: string             # required
    working_dir: string|null    # optional, inside project
    auto_start: true            # default true
    auto_restart: false         # default false
    restart_when_changed: []    # default []
    env: {}                     # string:string, default {}
```

Only command processes are YAML-backed. Missing/null `processes` means empty map. File limit 1 MB. Icon stays inside project, maximum 256 KB, extension `png|jpg|jpeg|gif|ico|webp`. Working-directory parent, absolute-outside-root, and symlink escapes are rejected. Invalid watch globs are ignored. Unknown keys are currently ignored. Repo file remains source of truth for YAML command config; runtime state stays local. [solo.yml docs](https://soloterm.com/api/v1/docs/projects/solo-yml)

## CLI inventory and patterns

CLI binary ships inside app and is normally symlinked to `~/.local/bin/solo`. It requires running app and enabled HTTP API except built-in help, `solo --version`, and local routine bundling. It discovers `http-api.json`, validates app PID/version, and uses current token automatically. Override app-data location with `--app-data-dir` or `SOLOTERM_APP_DATA_DIR`. [CLI overview](https://soloterm.com/api/v1/docs/cli/overview)

Global/diagnostic commands:

```text
solo --version                 # local CLI version
solo version                   # running app + API version
solo status                    # readiness/counts/path/port
solo doctor                    # discovery/reachability/version diagnosis
solo help [command]
solo <command> --help
```

Documented command inventory: [projects/processes CLI](https://soloterm.com/api/v1/docs/cli/projects-and-processes), [todos/scratchpads CLI](https://soloterm.com/api/v1/docs/cli/todos-and-scratchpads)

```text
solo projects list|get|create|rename|delete
solo processes list|get|spawn|start|stop|restart|rename|delete|output
solo commands start-all|stop-all|restart-all
solo processes start-all|stop-all|restart-all     # legacy aliases
solo agents list
solo todos list|get|create|update|delete|complete|incomplete
solo scratchpads list|read|create|update|append|rename|archive|unarchive|delete
solo routine                                      # local bundling group; public docs do not specify subcommands
```

Critical CLI patterns:

- Every command accepts `--json`. Success: one JSON object on stdout, `{"ok":true,"command":"...","data":...}`. Failure: stderr, nonzero, `{"ok":false,"error":{"code":"...","message":"...","command":"..."}}`. [JSON scripting](https://soloterm.com/api/v1/docs/cli/json-output-and-scripting)
- Exit codes: `0` success; `64` usage; `65` app rejection; `66` input file; `69` unavailable; `70` protocol/internal; `74` stdin I/O; `77` permission/token/discovery; `78` config/version mismatch. [JSON scripting](https://soloterm.com/api/v1/docs/cli/json-output-and-scripting)
- Project create path must exist. Project delete removes Solo state, not disk; `--confirm-stop-running` required when active.
- Process list defaults across projects; filter `--project-id` and status `stopped|starting|running|stopping|exited|failed`. Agent spawn needs `--agent-tool-id`; repeat `--arg` for extra arguments.
- Todo commands always require `--project-id`; bodies accept inline, file, or stdin (`--body-file -`). Tags normalize lowercase; update tags replace set. Todo priority defaults medium.
- Scratchpad commands always require `--project-id`; reads support `full|content|headings|section`; update/append/rename/delete require `--expected-revision`; delete also requires `--confirm`. Content accepts inline, file, or stdin.

## Local HTTP API

Local server binds `127.0.0.1` only. Default port 24678, but busy port causes random-free-port fallback. Always read discovery file. Fresh bearer token on each start; Unix file mode `0600`; file removed when API off/app exits. All endpoints, including `/api/version`, require bearer auth. Authenticated `/api/discovery` returns catalog without file-only `token` and `pid`. [HTTP API](https://soloterm.com/api/v1/docs/integrations/http-api)

Discovery path: `~/.config/soloterm/http-api.json` on macOS/Linux and `%USERPROFILE%\.config\soloterm\http-api.json` on Windows, or custom app-data directory. Important fields: `schemaVersion`, `apiVersion`, `appVersion`, `origin`, `baseUrl`, `apiBaseUrl`, `endpointBaseUrl`, `port`, `token`, `pid`, `capabilities`, and complete endpoint request/response schemas.

Request contract:

- `Authorization: Bearer <token>` always.
- JSON mutations require `Content-Type: application/json`; body maximum 2 MB. Routes accepting no body reject even `{}`.
- Optional `x-solo-request-id`: `[A-Za-z0-9._:-]`, maximum 128 bytes. Response header/body echo chosen ID.
- Optional mutation attribution: `x-solo-actor-id`, `x-solo-actor-name`; trimmed, max 120, no controls; invalid values ignored.
- Success envelope `{ok:true, requestId, data}`. Error envelope `{ok:false, requestId, error:{code,message,details}}`; automate against stable `code`/`details`, not message.
- Error/status pairs: `bad_request` 400, `unauthorized` 401, `forbidden` 403, `not_found` 404, `method_not_allowed` 405, `conflict` 409, `precondition_failed` 412, `payload_too_large` 413, `unsupported_media_type` 415, `version_mismatch` 426, `internal` 500, `service_unavailable` 503.
- Every GET also supports HEAD. OPTIONS reports allowed methods. Browser access restricted to loopback origins.
- Labels max 200; scratchpad names max 120; todo bodies/comments max 64 KB; tags max 32 × 48 chars, normalized lowercase/deduped/sorted. Boolean query values accept `true/false`, `1/0`, `yes/no`, `y/n`, `on/off`.

### Local HTTP method inventory (45 documented routes)

#### Discovery/status (3)

| Method | Path | Critical contract |
|---|---|---|
| GET | `/api/version` | `apiVersion`, `appVersion`. |
| GET | `/api/status` | readiness, app-data dir, port, project/process counts. |
| GET | `/api/discovery` | live capabilities and full endpoint schemas; no token/PID. |

#### Projects (6)

| Method | Path | Critical contract |
|---|---|---|
| GET | `/api/projects` | `workspaceId?`, `offset?`, `limit?`. |
| POST | `/api/projects` | `{name, path:absolute-existing, workspaceId?}`; canonical-path idempotent, 201 new/200 existing. |
| GET | `/api/projects/{projectId}` | one project. |
| PATCH | `/api/projects/{projectId}` | `{displayName:string|null}`. |
| DELETE | `/api/projects/{projectId}` | query `confirmStopRunning?`, `promptTemplatePolicy?`. |
| POST | `/api/projects/{projectId}/move-to-workspace` | `{workspaceId, beforeProjectId?|afterProjectId?}`; hints mutually exclusive. |

#### Workspaces (5)

| Method | Path | Critical contract |
|---|---|---|
| GET | `/api/workspaces` | all workspaces, unpaginated. |
| POST | `/api/workspaces` | `{name, icon?, color?}`. |
| PATCH | `/api/workspaces/{workspaceId}` | at least one of `name|icon|color`. |
| DELETE | `/api/workspaces/{workspaceId}` | query `destinationWorkspaceId?`; required if projects remain. |
| POST | `/api/workspaces/reorder` | `{workspaceIds:[...]}` every ID exactly once. |

#### Processes (12)

| Method | Path | Critical contract |
|---|---|---|
| GET | `/api/processes` | `projectId?`, status enum, offset/limit. |
| GET | `/api/processes/{processId}` | one process. |
| GET | `/api/processes/{processId}/output` | `lines?`, `kind=rendered|raw`, `projectId?`. |
| DELETE | `/api/processes/{processId}` | `projectId?`, `confirmStopRunning?`. |
| POST | `/api/projects/{projectId}/processes/spawn` | `{kind:terminal|agent, agentToolId?|agentToolInstallationId?, name?, extraArgs?}`; no arbitrary command. |
| POST | `/api/processes/{processId}/start` | optional project assertion. |
| POST | `/api/processes/{processId}/stop` | optional project assertion. |
| POST | `/api/processes/{processId}/restart` | optional project assertion. |
| POST | `/api/processes/{processId}/rename` | `{name}`; `newName` alias. |
| POST | `/api/projects/{projectId}/start-all` | trusted commands only; partial-result arrays. |
| POST | `/api/projects/{projectId}/stop-all` | command processes. |
| POST | `/api/projects/{projectId}/restart-all` | trusted commands only. |

#### Todos (10)

| Method | Path | Critical contract |
|---|---|---|
| GET | `/api/projects/{projectId}/todos` | completed/isBlocked/status/priority/query/comma-tags/sort/offset/limit. |
| POST | `/api/projects/{projectId}/todos` | `{title, body?, priority?=medium, tags?}`. |
| GET | `/api/projects/{projectId}/todos/{todoId}` | `includeComments?`. |
| PATCH | `/api/projects/{projectId}/todos/{todoId}` | subset `title|body|priority|status|completed|tags`; status/completed mutually exclusive. |
| DELETE | `/api/projects/{projectId}/todos/{todoId}` | permanent. |
| POST | `/api/projects/{projectId}/todos/{todoId}/complete` | empty means complete; `{completed:false}` reopens; status aliases; `releaseLock` default true. |
| GET | `/api/projects/{projectId}/todos/{todoId}/comments` | offset/limit. |
| POST | `/api/projects/{projectId}/todos/{todoId}/comments` | comment body. |
| PATCH | `/api/projects/{projectId}/todos/{todoId}/comments/{commentId}` | edit body. |
| DELETE | `/api/projects/{projectId}/todos/{todoId}/comments/{commentId}` | permanent. |

HTTP exposes `lockedBy`, `blockerIds`, `isBlocked`, and `unresolvedBlockerCount` read-only; blocker/tag/lock fine-grained mutation remains richer in MCP.

#### Scratchpads (9)

| Method | Path | Critical contract |
|---|---|---|
| GET | `/api/projects/{projectId}/scratchpads` | query/tags/includeArchived/offset/limit; omits content. |
| POST | `/api/projects/{projectId}/scratchpads` | `{name|title, content?, tags?}`. |
| GET | `/api/projects/{projectId}/scratchpads/{scratchpadId}` | offset/limit/mode/sectionHeading. |
| PUT | `/api/projects/{projectId}/scratchpads/{scratchpadId}` | replace name/content/tags plus required `expectedRevision`. |
| DELETE | `/api/projects/{projectId}/scratchpads/{scratchpadId}` | `expectedRevision` body preferred, query accepted. |
| POST | `/api/projects/{projectId}/scratchpads/{scratchpadId}/append` | content; revision optional. |
| POST | `/api/projects/{projectId}/scratchpads/{scratchpadId}/rename` | name plus required revision. |
| POST | `/api/projects/{projectId}/scratchpads/{scratchpadId}/archive` | archive. |
| POST | `/api/projects/{projectId}/scratchpads/{scratchpadId}/unarchive` | restore. |

## Deep links

| Target | URI |
|---|---|
| Project | `solo://proj/{projectId}` |
| Process | `solo://proj/{projectId}/process/{slug}--{processId}` |
| Scratchpad | `solo://proj/{projectId}/scratchpad/{slug}--{scratchpadId}` |
| Todo | `solo://proj/{projectId}/todo/{slug}--{todoId}` |

Slug: lowercase, non-alphanumeric to dashes, max 20 chars, readability only. Numeric suffix resolves object, so rename does not break link. OS handler launches/focuses Solo; links also work in Solo Markdown, terminal output, and command-palette paste. [Deep links](https://soloterm.com/api/v1/docs/integrations/deep-links)

## Hosted API v1

This is `https://soloterm.com/api/v1`, not local loopback `/api`. Live machine manifest is canonical entry point. Public routes state `auth: none`; admin routes require Sanctum bearer token with named ability. [Agent manifest](https://soloterm.com/api/v1/agents)

### Public endpoints (11)

| Method | Path | Critical parameters/return |
|---|---|---|
| GET | `/api/v1/health` | status + timestamp. |
| GET | `/api/v1/agents` | machine-readable integration manifest. |
| GET | `/api/v1/docs` | Markdown docs index. |
| GET | `/api/v1/docs/{path}` | section or `section/page`; Markdown. |
| GET | `/api/v1/download/{platform}` | platform `darwin-universal|windows-x86_64|linux-x86_64`; optional `source`; redirect, not JSON. |
| GET | `/api/v1/updates/manifest` | platform via `X-Platform` preferred or `platform|target`; optional license/device/current version; JSON or 204. |
| POST | `/api/v1/license/validate` | body requires 64-char `device_id`, `SOLO-XXXX-XXXX-XXXX-XXXX` key, `app_version`; optional device/platform/OS metadata. |
| GET | `/api/v1/license/status` | headers `X-Device-ID`, `X-App-Version` required; `X-License-Key` optional for free, included for licensed. |
| POST | `/api/v1/license/deactivate` | body `device_id`, `license_key`. |
| POST | `/api/v1/notifications/check` | body requires `app_version`, `is_licensed`; optional platform/OS/license/counts/`last_seen_id`. |
| POST | `/api/v1/feedback` | body requires device/app/OS/version/arch/message; email optional. |

### Admin endpoints (6)

| Method | Path | Ability and critical fields |
|---|---|---|
| GET | `/api/v1/admin/feedback` | `admin:feedback`; status/email/followed_up/search/per_page<=100. |
| PATCH | `/api/v1/admin/feedback/{feedback}` | `admin:feedback`; `is_resolved?`, `followed_up?`, `notes?`. |
| POST | `/api/v1/admin/emails` | `admin:email`; `to`, `subject`, `message`, optional `idempotency_key`. |
| POST | `/api/v1/admin/user-groups/{slug}/emails` | `admin:user-groups`; body email; case-insensitive license/owner match. |
| GET | `/api/v1/admin/app-versions` | `admin:versions`; status `released|all|published|staged|draft`, default released. |
| PATCH | `/api/v1/admin/app-versions/{version}/release-notes` | `admin:versions`; leading `v` normalized; `release_notes` required, null/blank clears. |

Admin tokens are created only in `/admin/api-tokens`, plain token shown once, and must carry exact ability. Keep token out of repo/logs. Email automation should set `idempotency_key` to prevent duplicate sends. [Agent manifest](https://soloterm.com/api/v1/agents)

## Recommended integration choices

- Agent controlling local Solo: MCP first. It has richer coordination, identity, timer, search, lock, todo, and scratchpad operations.
- Shell/CI/local script: CLI first; stable envelopes and exit codes avoid token plumbing.
- Editor/plugin needing structured REST: local HTTP API; bootstrap from discovery every time.
- Human handoff/navigation: deep links.
- Docs/download/update/license/feedback automation against Solo service: hosted API v1.
- Never hard-code current MCP tool availability or local HTTP port/token. Discover runtime catalog and discovery document.

## Source notes

Runtime-only evidence, queried 2026-07-15:

- **R1:** `mcp_tools_summary()` returned `tool_count: 95` and category inventory reproduced above.
- **R2:** `help()` plus every canonical topic: processes, timers, coordination, locks, scratchpads, todos, spawning, inspection, readiness, projects, docs, solo.yml.
- **R3:** Standard MCP resource listing returned cursor-paginated scratchpad/todo resources and both documented templates.
- **R4:** Solo CLI was not installed on this shell PATH; CLI inventory comes from official CLI docs, not inferred command execution.
- **R5:** Local `http-api.json` was not present, so local HTTP inventory uses official docs. Full per-install endpoint schemas remain discoverable from each running app's authenticated `/api/discovery`.

## Sources

- [Solo raw docs index](https://soloterm.com/api/v1/docs)
- [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server)
- [MCP tools overview](https://soloterm.com/api/v1/docs/mcp-tools/overview)
- [Project MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/project)
- [Process MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/process)
- [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
- [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos)
- [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)
- [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)
- [CLI overview](https://soloterm.com/api/v1/docs/cli/overview)
- [CLI JSON output and scripting](https://soloterm.com/api/v1/docs/cli/json-output-and-scripting)
- [Local HTTP API](https://soloterm.com/api/v1/docs/integrations/http-api)
- [Deep links](https://soloterm.com/api/v1/docs/integrations/deep-links)
- [`solo.yml` overview](https://soloterm.com/api/v1/docs/projects/solo-yml)
- [Command trust and security](https://soloterm.com/api/v1/docs/commands/trust-security)
- [Hosted API v1 agent manifest](https://soloterm.com/api/v1/agents)
- [Solo product site](https://soloterm.com/)

Web-search artifact: `/tmp/solo-technical-integration.json`. URL-extraction artifact: `/tmp/solo-api-v1.json`.
