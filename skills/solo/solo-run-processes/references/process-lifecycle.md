# Process lifecycle reference

Read for exact process kinds, lifecycle tools, trust gates, restart policy, input, and CLI equivalents.

## Process kinds

| Kind | Stored command config | Auto-start/restart/watch | Close semantics |
|---|---|---|---|
| `command` | Local or `solo.yml` | Supported when trusted | Stop/restart; do not close |
| `terminal` | Local process row | Unsupported | Close removes row |
| `agent` | Local process row/session | Unsupported | Close removes row |

Use `start_process`/`restart_process` for an existing stored entry. Use `spawn_process` for a new terminal or agent.

## Authority and ownership

- Control only self and Solo descendants self spawned.
- Record returned child process IDs immediately; Solo reads do not reliably prove parentage later.
- Require explicit user/runbook authority for parent, sibling, unrelated, YAML-backed shared process, or another agent's descendants.
- Do not transfer ownership because process is idle, stopped, failed, completed, or handed off.
- Apply ownership gate to stop, restart, close, rename, input, clear output, UI selection, and timer delivery.
- Keep root/operator responsible for Git, publishing, deployment, and integration.

## Lifecycle tools

- `list_processes`: list commands, terminals, agents, stopped entries.
- `get_process_status`: inspect kind, status, PID, uptime, and agent state.
- `start_process`: start existing entry; command requires trust.
- `stop_process`: gracefully stop running entry.
- `restart_process`: stop/start existing entry with latest saved config.
- `start_all_commands`: start trusted project commands.
- `stop_all_commands`: stop project commands.
- `restart_all_commands`: restart project commands.
- `spawn_process`: create/start terminal or agent.
- `send_input`: send text or bytes; submit appends Enter by default.
- `close_process`: remove terminal/agent; self-close needs explicit confirmation.

Bulk operations affect commands only. Start/restart reports may include started, skipped, and failed entries.
Bulk request still needs exact user/runbook authority over shared YAML commands.

## Trust and startup

Untrusted YAML command blocks manual start, auto-start, restart, crash restart, and file-watch restart. Trust exact variant in UI. Variant includes command, working directory, environment, auto settings, and watch patterns.

Automatic startup requires command kind, project Auto Start for app/project-load launch, command `auto_start`, trust, and allowed license/project limits. Manual **Start auto-start** can run eligible subset even when project startup toggle is off. **Start all** ignores per-command `auto_start` but still requires trust.

## Restart mechanisms

Crash restart:

- Set `auto_restart: true` for persistent commands.
- Preserve crash output and add restart banner.
- Pause after 10 restarts in 60 seconds.
- Disable during app shutdown.

File-watch restart:

- Set `restart_when_changed` to project-relative glob list.
- Watch recursive create/modify events, debounce, coalesce, then full restart.
- Treat `*` as capable of crossing path separators; prefer explicit patterns.
- Ignore invalid globs; empty/all-invalid list creates no watcher.

## Input bytes

| Intent | `send_input` bytes |
|---|---|
| Ctrl+C | `[3]` |
| Ctrl+D | `[4]` |
| Escape | `[27]` |

Use `wait_ms` when rendered tail in same response helps confirm interaction.

For `sudo` or other credential prompts, keep credential entry human-in-the-loop in attached terminal. Never request, store, echo, or send passwords through MCP, prompts, scratchpads, todos, or logs.

After spawning, persist child ID with purpose/owner in active handoff or task state. Do not spawn duplicate service when project already has suitable running process.

## CLI equivalents

```bash
solo processes list --project-id 2
solo processes get 9
solo processes start 9
solo processes stop 9
solo processes restart 9
solo commands start-all --project-id 2
solo commands stop-all --project-id 2
solo commands restart-all --project-id 2
```

CLI requires running app and enabled HTTP API. Every command accepts `--json`.

## Sources

- https://soloterm.com/api/v1/docs/commands/trust-security
- https://soloterm.com/api/v1/docs/commands/auto-start
- https://soloterm.com/api/v1/docs/commands/auto-restart
- https://soloterm.com/api/v1/docs/commands/file-watch-auto-restart
- https://soloterm.com/api/v1/docs/commands/start-stop-restart
- https://soloterm.com/api/v1/docs/mcp-tools/process
- https://soloterm.com/api/v1/docs/cli/projects-and-processes
- https://soloterm.com/api/v1/docs/cli/json-output-and-scripting
- https://x.com/aarondfrancis/status/2058610122197274684
