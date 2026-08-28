---
name: solo-run-processes
description: Operate Solo-managed commands and terminals through start, stop, restart, rename, spawn, input, bulk actions, trust gates, auto-start, crash restart, and file-watch restart. Use when launching a dev stack, controlling project commands, renaming a process, opening terminals, sending input, or configuring restart behavior. Do not use for read-only status and readiness, project or solo.yml setup, or failure diagnosis.
---

# Run Solo Processes

Control existing process entries with smallest lifecycle action that achieves requested state.

## Workflow

1. Establish identity and scope.
   - Call `whoami` first when running inside Solo-managed agent.
   - Otherwise call `list_projects`, then `select_project` when multiple projects exist.
   - Use Solo process IDs from Solo tools only; never substitute OS PIDs or another orchestrator’s IDs.
2. Inspect before mutating.
   - Call `list_processes` or `get_project_status`.
   - Call `get_process_status` for target.
   - Confirm process kind, state, trust, and whether user requested one process or command batch.
3. Confirm authority and ownership.
   - Control only current process and Solo descendants this process spawned.
   - Record every returned child process ID at spawn time; do not reconstruct ownership from later process lists.
   - Require explicit user/runbook authority for parent, sibling, unrelated, YAML-backed shared process, or another agent's descendants.
   - Never infer ownership from idle, stopped, failed, completed, or handed-off state.
4. Respect trust.
   - Start/restart only trusted command processes.
   - If command is untrusted, report blocker and direct user to Solo UI review.
   - Never weaken or bypass trust to complete lifecycle request.
5. Choose exact action.
   - Call `start_process` for stopped stored entry.
   - Call `stop_process` for running entry.
   - Call `restart_process` when latest saved configuration must relaunch.
   - Use `start_all_commands`, `stop_all_commands`, or `restart_all_commands` only for explicit project-wide command request.
   - Call `spawn_process` only to create new terminal or agent; do not use spawn to duplicate configured command.
   - Record returned child ID immediately with purpose and owner.
6. Interact only when requested and authorized.
   - Call `send_input` for terminal text or control bytes.
   - Use `submit=false` to type without Enter.
   - Use bytes `3`, `4`, or `27` for Ctrl+C, Ctrl+D, or Escape.
7. Verify result.
   - Poll `get_process_status`; do not infer success from request acceptance.
   - Read short rendered output tail when startup confirmation matters.
   - Use port-readiness tools only when user needs service ready, not merely process running.
8. Report target, authority basis, action, final state, recorded child IDs, and skipped/failed entries.

## Runtime policy

- Treat `auto_start` as eligibility, not immediate launch. Project Auto Start, command flag, trust, and limits all gate startup.
- Use crash `auto_restart` only for commands expected to remain alive. Expect pause after 10 restarts in 60 seconds.
- Use `restart_when_changed` only when native watcher is insufficient. Keep globs narrow and project-root-relative.
- Keep crash restart and file-watch restart conceptually separate.
- Restart after shell environment or saved command configuration changes; existing child environment never updates in place.

## Safety

- Stop only requested scope. Project-wide actions affect commands, not terminals or agents.
- Use `close_process` only to remove terminal or agent. Use stop/restart for commands.
- Pass `confirm_self_close=true` only when user explicitly asks current process to close itself.
- Apply same ownership gate to stop, restart, close, rename, input, output clearing, UI selection, and timer delivery.
- Do not delete project or process definition when stop is enough.
- Do not clear output during lifecycle work; retained failure output supports diagnosis.
- Reuse existing dev process instead of starting duplicate service.
- Leave Git, publishing, deployment, and integration to root/operator.

## Boundary

- Hand initial repository/YAML architecture to project setup workflow.
- Hand agent setup, health, launch, resume, summaries, prompting, and cleanup to single-agent lifecycle workflow.
- Hand read-only URL, port, resource, and output inspection to service observation workflow.
- Hand repeated failure, environment mismatch, or unexplained state to troubleshooting workflow.

## Reference

Read [process lifecycle reference](references/process-lifecycle.md) before bulk actions, trust-sensitive starts, auto-restart/file-watch configuration, spawning, closing, or raw input.
