---
name: solo-work-with-agents
description: Configure, health-check, launch, prompt, inspect, resume, summarize, follow up with, and close one Solo-managed agent session. Use for built-in or custom CLI agent setup, launchability, one-off flags, input, output, status, summaries, idle or blocked handling, and owned-agent cleanup.
---

# Work With Solo Agents

Operate one agent lifecycle through live Solo MCP discovery. Keep scope, ownership, and evidence explicit.

## Discover Before Acting

1. Call `whoami` and confirm actor, Solo process, and effective project.
2. Call `help(topic="spawning")` before spawning and `help(topic="processes")` before lifecycle or I/O actions.
3. Call `mcp_tools_summary` or inspect current tool discovery when expected tools are absent. Treat feature toggles and live schemas as authoritative.
4. Preserve effective project unless user explicitly requests another project.

Read [agent-lifecycle.md](references/agent-lifecycle.md) before spawning, routing input, targeting a timer, controlling a process, or recovering from ambiguous identity.

## Configure and Check Tools

- Configure saved agent commands/default flags in Solo Settings. Use `extra_args` only for one launch.
- Treat Solo as runtime host, not CLI installer. Repair missing CLI or shell environment outside Solo.
- Refresh installation health before diagnosing launch menus; distinguish Ready, Not checked, Missing, Broken, and Disabled.
- Use Runtime Doctor for tool/environment launchability. Keep MCP connection health as separate concern.
- Call `setup_agent_integration` only when user asks to add/update Solo guidance in `AGENTS.md` or `CLAUDE.md`; review resulting repository diff.

## Enforce Process Ownership

- Control only own Solo process and Solo descendants personally spawned during current run.
- Record every returned child `process_id` immediately with project, purpose, and related todo or scratchpad.
- Never control parent, sibling, unrelated process, YAML-backed shared process, or another agent's descendants without explicit user or runbook authority naming target.
- Never infer ownership from idle, stopped, completed, or abandoned state. State changes do not transfer authority.
- Keep root/operator responsible for Git, integration, commits, pushes, publishing, and deployment unless explicitly delegated.

## Launch One Agent

1. Inventory current project processes and capacity.
2. Call `list_agent_tools`; choose current configured, enabled, launchable installation by task fit.
3. Call `spawn_agent`; prefer returned installation IDs and live options over remembered schemas.
4. Record returned child ID before any later action.
5. Prepend returned `agent_instructions` to first prompt.
6. Send one self-contained prompt with objective, authoritative inputs, owned scope, forbidden work, acceptance checks, and handoff destination.

Do not spawn when work is tiny, sequential, or shares same edit surface with current agent. Handle it directly.

## Prompt and Observe

- Use `send_input` only for owned child or explicitly authorized target.
- Inspect status and actual rendered/raw output before follow-up.
- Use an idle timer for delayed follow-up; do not tight-poll or interrupt long TUI work.
- Treat idle and summaries as triage signals, never completion proof.
- Require changed files or artifacts, commands/tests, blockers, remaining risk, and next action in handoff.

## Resume and Summarize

- Resume only stopped supported sessions with saved session identity. Do not confuse agent-conversation resume with terminal reattach.
- Treat auto-summary and idle classification as triage only. Inspect actual output and artifacts before declaring completion.
- Remember spawned subagents may skip automatic summaries and summarizer support varies by tool/configuration.

## Finish Safely

1. Persist useful handoff in todo comment or scratchpad before cleanup.
2. Inspect output, files, diff, and checks at relevant layer.
3. Leave Git/integration decision to root/operator.
4. Cancel stale timers and release owned locks.
5. Close only owned descendant after handoff is durable and partial edits are understood.

## Stop Conditions

Stop and request authority when target ownership is unproven, project scope is wrong, action would affect shared/YAML-backed process, or user has not authorized cross-project or outward-facing work.
