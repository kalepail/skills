---
name: solo-observe-services
description: Inspect Solo-managed service status, terminal output, resource use, subprocesses, bound ports, localhost URLs, and startup readiness. Use when checking what is running, whether a server is ready, recent logs, stale status, URLs, ports, CPU, or memory without changing runtime. Do not use to change process lifecycle, edit configuration, or repair failures.
---

# Observe Solo Services

Gather structured runtime evidence before interpreting logs. Treat process running, port listening, and application healthy as separate states.

## Workflow

1. Establish project scope.
   - Call `whoami` when session may already belong to Solo project.
   - Otherwise call `list_projects` and `select_project` as needed.
2. Build project snapshot.
   - Call `get_project_status` for process inventory and states.
   - Call `get_project_stats` for CPU/memory overview.
   - Call `list_processes` for complete project entry list; filter returned rows client-side when needed.
3. Choose narrow target.
   - Call `get_process_status` for detailed state, PID, uptime, and agent state.
   - Use process ID/name returned by Solo, not OS PID guessed from logs.
   - Keep observation read-only across parent, sibling, shared, and unrelated processes; inspection does not grant control authority.
4. Inspect services and readiness.
   - Call `services_list` for project-wide discovered services.
   - Call `get_process_ports` when target process is known.
   - Call `wait_for_bound_port` when startup may still be in progress.
   - Use detected URL/port instead of hard-coded framework default.
5. Inspect output at right fidelity.
   - Use `get_process_output` for rendered diagnostic rows.
   - Use `search_output` for ordinary text lookup.
   - Use raw variants only when escape sequences, redraws, or terminal protocol behavior matter.
   - Request smallest useful line count.
6. Correlate evidence.
   - Distinguish trust from lifecycle status.
   - Distinguish root process from child listener.
   - Distinguish bound port from protocol/application health.
   - Note brief terminal/sidebar timing skew before declaring inconsistency.
7. Report concise snapshot: project, process/kind, state, PID/uptime when useful, ports/URLs, readiness meaning, resource anomalies, and relevant output lines.

## Readiness rules

- Treat Solo readiness as detected listening localhost port associated with tracked process.
- Treat timeout as `ready=false` plus `timed_out=true`, not proof process crashed.
- Perform explicit HTTP/protocol health request only when user asks for application health and target endpoint is known.
- Prefer `services_list` for discovery, `get_process_ports` for known target, and `wait_for_bound_port` for startup wait.

## Output rules

- Prefer rendered output for ordinary logs.
- Prefer raw output only for control-sequence or alternate-screen diagnosis.
- Remember retained terminal history is operational scrollback, not durable archive.
- Never clear output during observation. Call `clear_output` only after explicit user request and warn that search history disappears while process continues.
- Before any explicit clear request, verify target is self/recorded descendant or user/runbook names exact authorized target; idle/stopped state does not transfer ownership.

## Boundary

- Do not start, stop, restart, spawn, close, kill, or send input while observing.
- Do not select another process in UI, rename it, clear its output, or deliver timers without ownership/authority.
- Do not edit `solo.yml` or execution profile.
- Hand remediation request to lifecycle or troubleshooting workflow after presenting evidence.
- Leave Git, publishing, deployment, and integration to root/operator.

## Reference

Read [inspection and readiness reference](references/inspection-and-readiness.md) before selecting output mode, waiting for ports, interpreting status indicators, using CLI inspection, or explaining retention limits.
