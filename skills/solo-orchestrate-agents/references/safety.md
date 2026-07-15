# Orchestration safety reference

Read this reference before controlling processes, dispatching across projects, writing shared state, routing timer turns, integrating worker output, or cleaning up.

## Recursive process authority

Apply strict default:

- Actor may control itself and Solo descendants it personally spawned.
- Record every returned child ID; later process listing or state does not prove ancestry.
- Parent, sibling, unrelated process, YAML-backed shared process, and another actor's descendants require explicit user/runbook authority naming target and action.
- Idle, stopped, completed, failed, handed-off, or apparently abandoned state never transfers ownership.
- Apply gate to input, stop, restart, close, rename, clear output, UI selection, and timer delivery.
- Project scope is not process authority. A cross-project descendant may be owned only when cross-project spawn was authorized and recorded.

When parentage or authority is uncertain, inspect only and ask user before mutation.

## Scope and identity

- Confirm `whoami` before project-scoped mutation and after restart, reconnect, or project switch.
- Assert only own `SOLO_PROCESS_ID` if auto-identification fails.
- Use `project_id` for explicit scope and `delivery_process_id` for authorized timer recipient.
- Do not re-identify to impersonate or target another process.

## Shared-state safety

- Treat general locks as advisory, expiring, non-blocking leases—not security or correctness proof.
- Use stable, smallest collision-domain keys; acquire shortly before mutation and release promptly.
- Use todo lock for active task claim and general lock for shared file/logical area. One does not imply other.
- Protect competing KV read-modify-write with general lock because KV has no compare-and-swap field.
- Read scratchpad revision, apply smallest section/line/tag mutation, and reread/merge on conflict.
- Treat todo transfer as destructive to source blockers and locks; rebuild target graph explicitly.

## Timer and prompt safety

- Timer body is injected verbatim as fresh user turn. Put only trusted, self-contained next action in body.
- Store raw issue/web text in scratchpad and reference ID/section instead of embedding it in timer.
- Treat idle and summary as triage. Inspect output, files, diff/artifact, checks, and comments before completion.
- Never let prompt delivery imply authority, success, or ownership.

## Repository and outward-action boundary

- Keep root/operator responsible for user conversation, synthesis, final integration, Git index, commits, pushes, branches, tags, PRs, publishing, deployment, and production actions.
- Let workers edit only declared scopes and run declared checks. Require explicit delegation before any Git or outward-facing mutation.
- Preserve dirty trees and unrelated changes. Never revert work another actor owns.
- Keep secrets out of prompts, scratchpads, todo comments, timer bodies, logs, templates, and public artifacts.
- Require explicit authority for production, mainnet, public launch, credentials, OTP, uploads, or disclosure.

## Cleanup checklist

- Persist handoff before close.
- Verify files and partial edits.
- Cancel owned timers.
- Release owned locks.
- Close only recorded descendants.
- Leave shared/YAML-backed processes alone unless exact cleanup authority exists.
- Return evidence and integration decision to root/operator.

## Sources

- https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal
- https://soloterm.com/api/v1/docs/mcp-tools/coordination
- https://soloterm.com/api/v1/docs/mcp-tools/timers
- https://soloterm.com/api/v1/docs/mcp-tools/todos
- https://soloterm.com/api/v1/docs/mcp-tools/scratchpads
- https://soloterm.com/api/v1/docs/commands/trust-security
- https://soloterm.com/api/v1/docs/agents/closing-agents
- https://soloterm.com/api/v1/docs/workflows/agent-orchestration
