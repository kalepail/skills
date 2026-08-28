# Diagnostic reference

Read for symptom-to-check mappings and authoritative Solo behavior.

## Symptom matrix

| Symptom | Check first | Likely causes | Minimal repair when authorized |
|---|---|---|---|
| Command will not start | trust + status | untrusted YAML variant, limits, unavailable profile | review/trust in UI; select available profile |
| YAML edit not applied | project sync state | unsynced hash, unreadable/oversize YAML, invalid path | inspect diff, sync; keep file under 1 MB |
| Command starts in wrong folder | saved `working_dir` + profile | stale config, invalid path, WSL mapping | fix in-root path/mapping; restart target |
| Tool not found | shell/profile environment | stale 10-minute capture, init file not login-loaded, missing shim | refresh shell environment; export shim/path; restart |
| `nvm` works only in terminal | startup definition | shell function exists but executable paths not exported | export runtime paths/shims for managed launch |
| Repeated restart/failure | rendered output + exhausted indicator | deterministic boot error, crash restart limit | fix boot error; restart target after correction |
| Restarts on unrelated edits | watch patterns | broad glob; Solo `*` crosses separators | narrow project-relative patterns |
| Running but no URL | ports + child tree | still starting, binds external/non-local, no listener, wrong process | wait for port; inspect child; fix bind config |
| Port ready but app fails | protocol health | listener initialized before dependencies/app | call health endpoint; inspect app output |
| Output/status mismatch | short wait + status/output | independent update timing, alternate screen, stale view | poll status; select/reattach process |
| CLI cannot connect | `solo doctor` | app stopped, HTTP API off, stale/missing discovery, token/version mismatch | start app/enable API; reread discovery; align versions |

## Repair authority

- Control only self and Solo descendants self spawned; rely on recorded returned child IDs.
- Require exact user/runbook authority for parent, sibling, unrelated, YAML-backed shared process, or another agent's descendants.
- Never infer ownership from idle, stopped, failed, completed, or handed-off state.
- Apply same gate to stop/restart/close, rename, input, clear output, UI selection, and timer delivery.
- Keep Git, publishing, deployment, and integration with root/operator.

## Trust and YAML

Trust fingerprint covers command, working directory, environment, `auto_start`, `auto_restart`, and normalized watch patterns. Rename alone may preserve trust. Trust is local to machine/project variant. Untrusted commands cannot start/restart through UI, MCP, or automation.

Solo watches root YAML using debounced hash comparison. Sync can add/update/rename/remove commands but never auto-starts or restarts them. Removed running command stops during sync. Invalid watch globs are ignored; unsafe working directories are rejected.

## Shell and execution environment

Unix:

1. Resolve shell from `SHELL`, passwd, then `/bin/sh`.
2. Capture with interactive login `-ilc env`.
3. Cache 10 minutes.
4. Refresh through command palette after startup-file changes.
5. Restart existing child to receive new environment.

Windows host inherits normalized app environment. WSL uses distro environment. Project profile controls shell and host/WSL target for commands, terminals, and agents. Preserve selected unavailable profile with warning until repaired/changed. Configure project/distro root mapping when host path differs inside WSL.

Solo injects `SOLO_PROCESS_ID`, `SOLO_PROJECT_ID`, and `SOLO_PROCESS_KIND`; these are context, not credentials.

## Restart and readiness

Crash auto-restart pauses after 10 restarts within 60 seconds. File-watch restart is separate, recursive, debounced, and create/modify driven. Preserve crash output before manual restart.

Solo readiness proves tracked process or descendant has listening localhost port. Timeout means no detected listener before deadline, not necessarily crash. Use application health request to prove dependency/migration/protocol readiness.

## Output and CLI

Use rendered output for normal errors. Use raw output only for escape/control/alternate-screen issues. UI keeps up to 10,000 lines for current run; output is not permanent archive across app restart. Clear removes searchable retained buffer without stopping process.

CLI checks:

```bash
solo --version  # local CLI binary
solo version    # running app/API version
solo status     # readiness, counts, data dir, API port
solo doctor     # discovery, reachability, compatibility
```

CLI control requires running app and enabled HTTP API. Discovery file contains current port/token; token changes whenever server restarts.

## Sources

- https://soloterm.com/api/v1/docs/projects/solo-yml
- https://soloterm.com/api/v1/docs/projects/yml-change-notifications
- https://soloterm.com/api/v1/docs/commands/trust-security
- https://soloterm.com/api/v1/docs/commands/auto-restart
- https://soloterm.com/api/v1/docs/commands/file-watch-auto-restart
- https://soloterm.com/api/v1/docs/commands/status-indicators
- https://soloterm.com/api/v1/docs/environment/execution-profiles
- https://soloterm.com/api/v1/docs/environment/shell-environment
- https://soloterm.com/api/v1/docs/environment/version-managers
- https://soloterm.com/api/v1/docs/mcp-tools/services
- https://soloterm.com/api/v1/docs/mcp-tools/output
- https://soloterm.com/api/v1/docs/terminal/persistent-sessions
- https://soloterm.com/api/v1/docs/cli/overview
- https://soloterm.com/api/v1/docs/integrations/http-api
- https://soloterm.com/changelog
