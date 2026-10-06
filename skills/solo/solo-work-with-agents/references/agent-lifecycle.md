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

Apply the ownership gate in `SKILL.md` to input, stop, restart, close, rename, output clearing, UI selection, and timer delivery. Record returned child IDs because later process reads do not reliably prove parentage. When authority is unclear, inspect only and ask the user before mutation.

## Spawn contract

### Tool setup and health

- `list_agent_tools` is the live list of tool types and installations. A custom Generic tool can host a terminal agent that Solo does not list.
- Solo stores command/default arguments and optional generic prompt/summarizer behavior but does not install agent CLIs.
- Health is environment-specific. Ready is launchable; Not checked remains launchable but inconclusive; Missing and Broken are not launchable; Disabled is separate.
- Refresh health explicitly. Runtime Doctor explains tool/environment launchability; MCP connection count/repair is a different diagnostic.
- Saved default flags belong in Settings. `extra_args` appends one-launch flags without changing saved defaults; verify effective launch command in current UI when flags matter.
- When `routing-agent-work` is installed and a selection remains, invoke it for model, effort, fallback, and reviewer selection. Otherwise, use the caller's explicit route or configured tool defaults.
- Fleet names are models, not agent tools. `list_agent_tools` returns CLI installations. Apply the route through saved defaults or `extra_args`.
- `setup_agent_integration` adds a `## Solo Integration` section to `CLAUDE.md` or `AGENTS.md` and leaves an existing section unchanged. Treat this as repository edit: require request, preserve local instructions, and review diff.

Set the routed model and effort explicitly on every routed spawn. When `routing-agent-work` is installed, its fleet reference owns the flag syntax. Otherwise, read the flags from the CLI's live `--help`. Do not use Solo to discover or score unknown models.

Prefer a CLI's built-in subagents when every lane stays within one CLI and that CLI can pin each lane's settings. Use Solo agents when lanes cross CLIs or need settings the CLI cannot pin. Headless `opencode run` lanes reject file access outside their working directory, so keep briefs and outputs inside the project. When `fan-solo` is installed, its house-style reference has the per-CLI subagent and Claude agent-team detail.

### Spawn and retask

- Route the task first. Retask an owned idle direct child only when its tool, model, effort, and context match. Start fresh when the route or review contract requires fresh context.
- Before retasking heavy context, use the CLI's own compaction command. If none exists, close after durable handoff and spawn fresh. Solo auto-summary is not compaction.
- Call `list_agent_tools`; choose returned configured installation by task fit. Pass `agent_tool_installation_id` when discovery returns environment-specific installations.
- Prefer `spawn_agent` for agents. Use generic `spawn_process(kind="agent")` only when generic process creation is required.
- Treat `spawn_agent` response as authoritative for `process_id`, name, and `agent_instructions`.
- Record child ID, project, tool, task, and durable work record immediately.
- Prepend `agent_instructions` to first prompt, then send through `send_input`.
- Remember spawning never changes caller identity or default scope.
- While a child owns a scope, stay read-only on it: route rework back through `send_input`, and take the scope back only after a durable handoff records the transfer and the child is stopped or released.

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
- Follow the close-or-retask rule in `SKILL.md`. Capture terminal-only findings, such as research and citations, claim-level first, because closing destroys the only copy. Settle only direct children, and confirm a child's own subtree is settled before closing it.
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
