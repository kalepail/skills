---
name: solo-troubleshoot
description: Diagnose Solo project, command, terminal, service, CLI, shell, version-manager, trust, solo.yml sync, working-directory, execution-profile, WSL, restart-loop, output, port, and readiness failures. Use when tooling is missing, commands fail, YAML changes do not apply, status disagrees, or services never become ready. Do not use for routine status views or authorized routine start, stop, and restart.
---

# Troubleshoot Solo

Find root cause with smallest evidence set. Separate configuration, trust, lifecycle, listener readiness, and application health before changing anything.

## Workflow

1. Restate symptom and expected state.
   - Identify project, process, action, last known good state, and recent config/profile/shell change.
   - Ask only when target or desired state cannot be inferred safely.
2. Establish Solo scope.
   - Call `whoami`, `list_projects`, and `select_project` as needed.
   - Call `get_project_status`, then `get_process_status` for target.
3. Classify failure before reading broad logs.
   - Trust/config: untrusted variant, unsynced YAML, invalid `working_dir`, unknown command.
   - Launch/environment: unavailable profile, wrong WSL root, missing `PATH`, version-manager function only.
   - Runtime: failed/exited process, crash-loop exhaustion, watcher-triggered restarts.
   - Readiness: running process without listener, wrong child/port, listener without healthy application.
   - Control plane: CLI/API discovery, token, version, app startup, or MCP scope issue.
4. Gather narrow evidence.
   - Use rendered output first; search exact error text.
   - Use raw output only for control sequences/redraw issues.
   - Inspect ports and subprocesses before scraping “ready” log messages.
   - Run `solo doctor` for CLI/app discovery failures.
5. State root cause and evidence.
   - Distinguish confirmed cause from remaining hypothesis.
   - If user asked only to diagnose, stop here.
6. Confirm repair authority.
   - Control only self and recorded Solo descendants self spawned.
   - Require exact user/runbook authority for parent, sibling, unrelated, YAML-backed shared process, or another agent's descendants.
   - Do not infer ownership from idle, stopped, failed, completed, or handed-off state.
7. Apply smallest authorized repair.
   - Require UI trust review for untrusted command.
   - Sync YAML, refresh shell environment, fix profile/root/path, or restart only affected process as appropriate.
   - Preserve output until cause is understood.
   - Avoid delete/recreate when sync, path edit, or restart is sufficient.
8. Reproduce original check.
   - Confirm status transition.
   - Confirm listener with readiness tool when relevant.
   - Confirm application health separately when requested.
   - Report fixed cause, changed state, and unresolved risk.

## Diagnostic order

Follow cheapest decisive checks:

1. Scope and process identity.
2. Trust and YAML sync state.
3. Saved command and `working_dir`.
4. Execution profile/environment availability.
5. Rendered startup output.
6. Crash restart exhaustion or file-watch churn.
7. Bound ports/child ownership.
8. Application-specific health.

## Guardrails

- Never bypass trust, widen working directory outside repo, or enable broad auto-trust as quick fix.
- Never clear output before diagnosis.
- Never assume running means ready or listening means healthy.
- Never restart every project command when one target can be repaired.
- Never stop, restart, close, rename, input, clear, select, or deliver timer to process outside ownership without exact authority.
- Never edit shell startup files, `solo.yml`, or WSL mappings unless user requested repair.
- Never delete project/process state to cure stale UI without proving cheaper repair failed.
- Leave Git index, commits, pushes, publishing, deployment, and integration to root/operator.

## Boundary

- Use project setup workflow for planned new configuration rather than failure recovery.
- Use process lifecycle workflow for straightforward requested start/stop/restart with no unexplained failure.
- Use service observation workflow for read-only status/URL/log report with no diagnosis request.

## Reference

Read [diagnostic reference](references/diagnostics.md) before diagnosing trust, YAML sync, shell/version manager, execution profile/WSL, crash-loop, readiness, output retention, or CLI/API failures.
