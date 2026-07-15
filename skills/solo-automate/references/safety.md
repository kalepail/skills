# Safety and authority

Use this reference before any Solo mutation, process input, cross-project action, destructive call, timer delivery, file import/export, feedback, or hosted admin operation.

## Authority rules

- Treat inspection as allowed when relevant; do not infer mutation authority from read request.
- Require explicit target and authority for start/stop/restart, bulk control, spawn, input, output clear, close, delete, cross-project move, timer delivery to another agent, feedback submission, or hosted admin mutation.
- Prefer narrowest target. Never widen one-process request to project-wide action.
- Verify ownership of locks and agent descendants. Idle/stopped/abandoned state does not transfer ownership.
- Stop when project/process identity is ambiguous or live schema differs materially from requested action.

## Commands and trust

Untrusted `solo.yml` command cannot manual-start, auto-start, restart, crash-restart, or file-watch restart. Trust is local and scoped to exact project/variant. Command, working directory, environment, auto settings, or watch patterns can invalidate trust. Require UI review; never bypass or weaken trust.

## Destructive and irreversible actions

- `delete_project`: require `confirm_delete=true`; require `confirm_stop_running=true` when active processes exist. Explain Solo-owned state removed and disk files preserved. Choose prompt-template policy deliberately.
- `close_process`: use only for terminal/agent. Pass `confirm_self_close=true` only after explicit self-close request.
- `clear_output`: removes saved/searchable output but not PTY/process. Require explicit request and warn diagnostic history disappears.
- Todo/scratchpad/comment deletion: require named object and explicit deletion intent.
- Prefer stop over close/delete; archive over delete; targeted edit over full overwrite.

## Concurrency and ownership

- Read scratchpad revision before edit/rename/delete; pass `expected_revision`/`expectedRevision`. On mismatch, re-read, reconcile, retry only when authorized.
- Treat coordination locks as advisory leases, not authorization. Release owned locks after work. Never release another actor's lock.
- Todo completion normally releases caller's lock. Todo transfer clears locks/blockers; confirm move scope.
- Prefer slim write receipts; fetch fresh state to verify.

## Process input and timers

- Send text/control bytes only to explicitly authorized Solo target. Bytes override text in MCP `send_input`.
- Timer `body` is injected verbatim as fresh user turn. Make it self-contained, plain, scoped, and free of hidden instructions.
- Keep timer watch list separate from `delivery_process_id`. Use readiness tools for ports; idle timers only for worker quiet.
- Cancel obsolete timers.

## Files and secrets

- Keep scratchpad relative import/export inside project; reject `..` or symlink escape. Treat absolute path as explicit wider access requiring authority.
- Do not place secrets in `solo.yml`, prompt templates, todos, scratchpads, timer bodies, deep links, logs, actor headers, or command arguments.
- Do not print local `http-api.json` token or hosted Sanctum token. Re-read local discovery privately after restart/401.

## Hosted side effects

- Public docs/health/manifest reads are safe.
- Installer/update/license calls can affect attribution, activation, or device state; use only for requested workflow.
- MCP `submit_solo_feedback` opens draft for human review; hosted `POST /api/v1/feedback` submits. Distinguish them.
- Require exact admin ability and explicit outward-action authority for email, feedback mutation, user-group mutation, or release-note update. Use email idempotency keys.

## Verification

After mutation:

1. Re-read target through same authoritative surface.
2. Confirm desired state, not only accepted request.
3. Report partial failures, skipped entries, remaining locks/timers, and manual trust/UI steps.

## Sources

- https://soloterm.com/api/v1/docs/commands/trust-security
- https://soloterm.com/api/v1/docs/mcp-tools/project
- https://soloterm.com/api/v1/docs/mcp-tools/process
- https://soloterm.com/api/v1/docs/mcp-tools/scratchpads
- https://soloterm.com/api/v1/docs/mcp-tools/todos
- https://soloterm.com/api/v1/docs/mcp-tools/timers
- https://soloterm.com/api/v1/docs/integrations/http-api
- https://soloterm.com/api/v1/agents
