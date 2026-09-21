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
- When `routing-agent-work` is installed and a selection remains, invoke it for model, effort, fallback, and reviewer selection. Otherwise, use the caller's explicit route or configured tool defaults.
- Fleet names are models, not agent tools. `list_agent_tools` returns CLI installations. Apply the route through saved defaults or `extra_args`.
- `setup_agent_integration` writes or updates Solo guidance in `CLAUDE.md` or `AGENTS.md`. Treat this as repository edit: require request, preserve local instructions, and review diff.

| CLI | Model flag | Reasoning flag | Canonical source |
|---|---|---|---|
| `claude` | `--model <alias\|id>` | `--effort <level>` | `claude --help` |
| `codex` | `-m <id>` | `-c model_reasoning_effort="<level>"` | `codex --help`, `codex exec --help` |
| `opencode` | `-m provider/model` | `--variant <provider-specific-level>` | `opencode run --help` |
| `grok` | `-m <id>` | `--reasoning-effort <level>` | `grok --help` |

Flags drift with CLI releases. Verify the route's flags against live `--help` before launch. Do not use Solo to discover or score unknown models.

Built-in subagents versus more Solo agents: when a fan-out stays within one provider, prefer the CLI's native subagents over extra Solo processes—faster, cheaper, one harness. All work headless: claude delegates via the Agent tool or description matching (`.claude/agents/*.md` or `--agents '<json>'`; per-agent `model` and `effort`); codex spawns only when the prompt asks explicitly ("spawn one agent per…")—`[features] multi_agent` is stable-on, built-ins `default`/`worker`/`explorer`, per-agent `model`/`model_reasoning_effort` in `~/.codex/agents/<name>.toml`; opencode primaries delegate through the `task` tool to `general`/`explore` or agents in `.opencode/agents/` (per-agent `model`, `reasoningEffort`/`variant`); grok spawns via `spawn_subagent` (built-ins `general-purpose`/`explore`/`plan`; custom `--agents '<json>'` with per-subagent `model`; effort inherits the session; `--no-subagents` disables). Lanes that cross providers—or need a per-subagent setting their CLI cannot pin—stay on Solo, the common case; same-CLI model and tier mixes stay built-in where the CLI pins them (claude/codex: model and effort; opencode: model and variant; grok: model only). Headless `opencode run` lanes auto-reject file access outside their cwd (`external_directory` permission); keep worker briefs and outputs inside the project, or inline them in the prompt.

Claude agent teams (gate: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings `env`) upgrade subagents to peer teammates with a shared task list and mailbox. Prose-triggered in interactive sessions only—"Spawn three teammates…", always naming each teammate's model since unnamed teammates fall back to the default teammate model, not the lead's (effort is inherited); Solo-spawned claude TUIs form real teams, while `claude -p` silently substitutes subagents. One team per session, no nesting. Use for Claude-family workers that must talk to each other; when `fan-solo` is installed, its house-style reference has more detail.

### Spawn and retask

- Route the task first. Retask an owned idle direct child only when its tool, model, effort, and context match. Start fresh when the route or review contract requires fresh context.
- Before retasking heavy context, use the CLI's own compaction command. If none exists, close after durable handoff and spawn fresh. Solo auto-summary is not compaction.
- Call `list_agent_tools`; choose returned configured installation by task fit.
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
- Close or retask each owned child in the same pass its task completes, its evidence is reviewed, and its handoff is durable—capture terminal-only findings (research, citations, excerpts) claim-level first, since closing destroys the only copy. Unreviewed or partial results keep it open; a finished agent left live or idle after the parent moves on is cruft—at every depth, one generation at a time: each parent settles only the direct children it spawned and confirms a child's subtree is settled before closing it.
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
