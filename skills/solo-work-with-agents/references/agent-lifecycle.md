# Agent lifecycle and ownership reference

Read this reference before spawning, prompting, inspecting, timing, stopping, restarting, renaming, selecting, clearing output, or closing a Solo agent.

## Live discovery sequence

1. Call `whoami` to inspect actor, process, and effective project.
2. Call `help(topic="spawning")` for current spawn workflow.
3. Call `help(topic="processes")` for current lifecycle, input, and output workflow.
4. Call `help(topic="timers")` before scheduling follow-up.
5. Use `mcp_tools_summary` or live tool discovery for enabled names and schemas. Disabled feature tools disappear from discovery; do not guess them.

Solo-managed agents normally auto-identify. If detection fails, assert only caller's own `SOLO_PROCESS_ID`; never pass another process ID to impersonate or target it. Use `project_id` for scope and `delivery_process_id` for timer routing.

## Process authority

Apply recursive, non-transferable ownership:

- Control self and descendants this actor spawned.
- Record returned child IDs because later process reads do not reliably prove parentage.
- Treat parent, sibling, unrelated, YAML-backed shared process, and another actor's descendants as unauthorized unless user/runbook explicitly names target and action.
- Apply same gate to input, stop, restart, close, rename, output clearing, UI selection, and timer delivery.
- Do not infer authority from idle, stopped, completed, failed, or apparently abandoned state.

When authority is unclear, inspect only. Ask user before mutation.

## Spawn contract

### Tool setup and health

- Built-in tool types include Claude, Codex, Amp, Gemini, OpenCode, Copilot, and Kimi; custom Generic tools can host other terminal agents.
- Solo stores command/default arguments and optional generic prompt/summarizer behavior but does not install agent CLIs.
- Health is environment-specific. Ready is launchable; Not checked remains launchable but inconclusive; Missing and Broken are not launchable; Disabled is separate.
- Refresh health explicitly. Runtime Doctor explains tool/environment launchability; MCP connection count/repair is a different diagnostic.
- Saved default flags belong in Settings. `extra_args` appends one-launch flags without changing saved defaults; verify effective launch command in current UI when flags matter.
- `setup_agent_integration` writes or updates Solo guidance in `CLAUDE.md` or `AGENTS.md`. Treat this as repository edit: require request, preserve local instructions, and review diff.

- Call `list_agent_tools`; choose returned configured installation by task fit.
- Prefer `spawn_agent` for agents. Use generic `spawn_process(kind="agent")` only when generic process creation is required.
- Treat `spawn_agent` response as authoritative for `process_id`, name, and `agent_instructions`.
- Record child ID, project, tool, task, and durable work record immediately.
- Prepend `agent_instructions` to first prompt, then send through `send_input`.
- Remember spawning never changes caller identity or default scope.

Use one bounded worker prompt:

```text
Objective: <one outcome>
Authoritative inputs: <paths, todo, scratchpad section>
Ownership: <files or read-only surface>
Forbidden: <non-goals, Git/publishing/integration>
Acceptance: <checks and evidence>
Handoff: <destination plus changed files, tests, blockers, risk, next action>
```

## Observation and follow-up

- Use status plus actual output. Search raw output only when rendered rows lose needed detail.
- Use idle timer instead of sleep or tight polling. Timer body must be self-contained and trusted.
- Treat idle as quiet, not done. Treat auto-summary as triage, not evidence.
- Use `wait_for_bound_port` for listener readiness; do not infer readiness from quiet output.
- Avoid interrupting active TUI work. Send follow-up only when evidence shows input is needed.

## Resume and summaries

- Resume last or chosen saved session only for supported stopped agents. Resume restores agent conversation identity, not PTY screen history or a restartable command slot.
- Auto-summarization requires configured summarizer and quiet/activity cadence. Spawned subagents may skip it; support differs by agent tool.
- Treat summary, idle, permission-wait, thinking, working, and error classifications as heuristics. Reopen output and artifacts for proof.

## Cleanup

- Persist handoff before close; closing removes session but does not revert filesystem edits.
- Inspect partial changes before closing mid-task child.
- Cancel owned stale timers and release owned locks.
- Close only owned descendant. Self-close requires explicit user request and current live confirmation semantics.
- Leave Git index, commits, pushes, PRs, publishing, deployment, and final integration to root/operator unless explicitly delegated.

## Sources

- https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal
- https://soloterm.com/api/v1/docs/mcp-tools/process
- https://soloterm.com/api/v1/docs/mcp-tools/output
- https://soloterm.com/api/v1/docs/mcp-tools/timers
- https://soloterm.com/api/v1/docs/agents/idle-detection
- https://soloterm.com/api/v1/docs/agents/setting-up-tools
- https://soloterm.com/api/v1/docs/agents/installation-health
- https://soloterm.com/api/v1/docs/agents/auto-summarization
- https://soloterm.com/api/v1/docs/agents/closing-agents
- https://soloterm.com/api/v1/docs/terminal/persistent-sessions
- https://soloterm.com/api/v1/docs/workflows/agents-spawning-agents
- https://soloterm.com/api/v1/docs/integrations/mcp-server
- https://x.com/aarondfrancis/status/2075571055041675691
