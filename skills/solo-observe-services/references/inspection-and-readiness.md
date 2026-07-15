# Inspection and readiness reference

Read for exact inspection tools, listener-readiness semantics, output modes, UI limits, and CLI commands.

## Structured tools

Project/process:

- `get_project_status`: project metadata plus current processes.
- `get_project_stats`: project process CPU/memory.
- `list_processes`: commands, terminals, agents, stopped entries.
- `get_process_status`: detailed one-process state, PID, uptime, agent state.
- `select_process`: attach/render target terminal in Solo UI; treat as control action requiring ownership/authority, not passive inspection.

Services:

- `services_list`: project-local detected services, readiness, URLs, ports.
- `get_process_ports`: detected ports/URLs for one process and descendants.
- `wait_for_bound_port`: wait for project/target listener; timeout returns `ready=false`, `timed_out=true`.

Output:

- `get_process_output`: rendered terminal rows; default 50, maximum 200.
- `search_output`: search rendered rows.
- `get_process_raw_output`: raw bytes/control sequences; default 50, maximum 200.
- `search_raw_output`: search raw stream.
- `clear_output`: clear saved buffer only; process/PTY keeps running.

Read-only status/output/port inspection may cover project scope. Any control action—including UI selection, rename, input, output clearing, stop/restart/close, or timer delivery—requires self/recorded-descendant ownership or exact user/runbook authority. Idle/stopped/completed state never transfers ownership.

## Status interpretation

Lifecycle states include starting, running, stopping, stopped, exited, and failed. Trust, unread output, and exhausted crash restart are separate indicators. Terminal output and sidebar status can update at slightly different times.

Running means process exists. Ready means Solo detects listening localhost port associated with tracked process/child. Healthy requires application-specific check beyond listener.

## Terminal behavior

- Retain up to 10,000 lines for current run in UI.
- Detach/reattach view without restarting running process.
- Do not treat runtime output as permanent archive across app restarts.
- Search plain text, case-insensitive; no regex.
- Search alternate screen only within active frame.
- Clear/prune removes content from later search.

Activity monitor shows project, managed process/subprocess, CPU, memory, command, ports, PID, type, parent, and kill action. Use tree view to attribute descendant listener to managed root.

## CLI inspection

```bash
solo status
solo doctor
solo projects list
solo processes list --project-id 2 --status running
solo processes get 9
solo processes output 9 --lines 200
solo processes output 9 --raw --lines 500
```

`solo --version` reports CLI binary locally; `solo version` contacts app. CLI state commands require running app and enabled HTTP API. Use `--json` for stable envelopes and exit codes.

## Reporting template

```text
Project: <name/id>
Process: <name/id/kind>
State: <state; trust separately>
Listener: <host:port/url or none>
Readiness: <listener-ready, waiting, or timed out>
Resources: <CPU/memory anomaly if relevant>
Evidence: <short rendered/raw excerpt and why mode chosen>
Limit: <what remains unproven, such as HTTP health>
```

## Sources

- https://soloterm.com/api/v1/docs/mcp-tools/services
- https://soloterm.com/api/v1/docs/mcp-tools/process
- https://soloterm.com/api/v1/docs/mcp-tools/output
- https://soloterm.com/api/v1/docs/activity/activity-monitor
- https://soloterm.com/api/v1/docs/commands/status-indicators
- https://soloterm.com/api/v1/docs/terminal/basics
- https://soloterm.com/api/v1/docs/terminal/search
- https://soloterm.com/api/v1/docs/terminal/persistent-sessions
- https://soloterm.com/api/v1/docs/cli/overview
- https://soloterm.com/api/v1/docs/cli/projects-and-processes
- https://soloterm.com/api/v1/docs/cli/json-output-and-scripting
- https://soloterm.com/changelog
