# Fan Solo house style

Apply before any Solo mutation, agent spawn, shared-state edit, or process control.

## Contents

- Source and scope
- Prefer one agent
- Apply an external route
- Respect recursive process ownership
- Store state once
- Monitor without guessing
- Mutate safely
- Prove completion

## Source and scope

1. Honor current user decision.
2. Call `whoami`; confirm actor, Solo process, and effective project.
3. Read `help()` and required topic help. Discover enabled tools.
4. Consult live Solo Docs MCP/current official docs for behavior and schemas.
5. Treat bundled research as orientation and evidence, not current runtime authority.

Keep current project unless cross-project work is explicit. Project scope and caller identity are separate.

## Prefer one agent

Keep work single-agent when steps are sequential, touch shared state, need one coherent design judgment, or fan-out overhead exceeds lane work.

Orchestrate only independent lanes with clear ownership and integration value. Before spawning, define:

- objective and authoritative inputs;
- owned files/surface and forbidden neighbors;
- acceptance checks;
- todo/scratchpad destination;
- handoff format;
- exact lock, if collision risk exists.

Route the lane first. Retask an owned idle direct child only when its tool, model, effort, and context match. Start fresh when the route or review contract requires fresh context.

Lead owns plan, dependencies, integration, Git, publishing, and final completion. Worker owns one bounded lane.

Any agent that parents workers spends its context on orchestration, evidence review, integration judgment, and synthesis. Assign each separable artifact change to one end-to-end worker lane. Return rework to its owning lane. Transfer a failed lane whole to a fresh worker. Once only trivial follow-through remains, continue with one agent. The parent authors coordination state, user-facing synthesis, final evidence, and tightly coupled integration edits. Give other integration changes to one worker. Require concise reports and artifact paths. Open full artifacts only when judgment requires them. Git, publishing, and final verification stay with the root lead.

## Apply an external route

When `routing-agent-work` is installed and a selection remains, invoke it before selecting an agent CLI, model, effort, fallback, or reviewer. Treat its route card as the selection authority.

When the skill is absent, use an explicit route from the user or caller. Otherwise, use the selected Solo tool's configured defaults. Do not invent a fleet rule inside Solo.

Fleet names are models, not Solo agent tools. Discover live launchable tools with `list_agent_tools`. Apply the route through the selected tool's saved defaults or `extra_args`.

Solo's built-in tool types are Claude, Codex, Amp, Gemini, OpenCode, Copilot, and Kimi. Add any other terminal agent, such as Grok, as a custom Generic tool before spawning it. This list states intent; it does not prove a given tool is installed and enabled.

### Set model and reasoning explicitly

Every routed spawn sets the model and effort explicitly. Put standing choices in the tool's saved default flags. Pass per-lane overrides through `extra_args`.

| CLI | Model flag | Reasoning flag | Canonical source |
|---|---|---|---|
| `claude` | `--model <alias\|id>` | `--effort <level>` | `claude --help` |
| `codex` | `-m <id>` | `-c model_reasoning_effort="<level>"` | `codex --help`, `codex exec --help` |
| `opencode` | `-m provider/model` | `--variant <provider-specific-level>` | `opencode run --help` |
| `grok` | `-m <id>` | `--reasoning-effort <level>` | `grok --help` |

Verify flags and accepted values against the installed CLI before launching. Do not use Solo to discover or score new models.

### Built-in subagents vs Solo workers

Prefer a CLI's built-in subagents when every lane stays within one CLI. Use Solo workers when lanes cross CLIs or require settings the parent cannot pin.

All four trigger routes work headless; re-run a route live before relying on it:

| CLI | How to trigger | Definitions and per-subagent settings |
|---|---|---|
| `claude` | Auto-delegation from agent `description`, "use the X subagent", or the Agent tool; works under `claude -p` | `.claude/agents/*.md` or `--agents '<json>'`; per-agent `model` (`sonnet`/`opus`/`haiku`/`fable`/id/`inherit`) and `effort` (`low…max`); `--forward-subagent-text` exposes child transcripts in stream-json. Source: code.claude.com/docs/en/sub-agents |
| `codex` | Conversational only—ask explicitly ("spawn one agent per…") or name custom agents in prose ("Have `pr_explorer` map the affected paths"); `AGENTS.md` standing instructions; `spawn_agents_on_csv` for batch; works under `codex exec` | `[features] multi_agent` stable-on; built-ins `default`/`worker`/`explorer`; per-agent `model` + `model_reasoning_effort` in `~/.codex/agents/<name>.toml` or `.codex/agents/`; `[agents] max_threads=6`, `max_depth=1`. Source: developers.openai.com/codex/subagents |
| `opencode` | Primary agent auto-delegates via the `task` tool from agent descriptions; `@name` in TUI; works under `opencode run` | Built-in subagents such as `general`/`explore` (the set varies by version); custom in `.opencode/agents/*.md`, `~/.config/opencode/agents/`, or `opencode.json` `agent` key; per-agent `model` and `reasoningEffort`/`variant`; gate with `permission.task`. Source: opencode.ai/docs/agents |
| `grok` | Model-driven `spawn_subagent`—steer by naming a type ("use the explore subagent"); `--no-subagents` disables; works under `--single` | Built-ins `general-purpose`/`explore`/`plan`; custom via `--agents '<json>'` or `--agent <file>` (Claude-compatible schema with per-subagent `model`); effort inherits session `--reasoning-effort`; `--best-of-n <N>` runs N headless attempts plus judge. Source: docs.x.ai/build CLI reference |

Claude agent teams are a third topology. They provide peers with a shared task list and mailbox. Enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Always name each teammate's routed model. Teammates inherit effort but not the lead's model. Use teams only when Claude workers must communicate or claim shared tasks. Cross-CLI work stays on Solo. Source: code.claude.com/docs/en/agent-teams

## Respect recursive process ownership

Control only self and recorded descendants. Parent, sibling, unrelated, YAML-backed shared process, or another agent's descendants remain outside authority unless user or runbook explicitly names exact target and action.

Idleness, stopped state, finished handoff, or “clean up” does not transfer ownership. Record returned child IDs because names and live reads do not prove parentage.

This gate applies to input, stop/restart/close, rename, clear output, UI selection, and timer delivery.

## Store state once

| State | Store |
|---|---|
| Shared plan, findings, decisions, evidence, current summary | Scratchpad |
| Owned action, acceptance, status, blockers | Todo |
| Task progress, changed files, checks, risks, next action | Todo comment |
| Small temporary JSON status/pointer/heartbeat | KV |
| Short collision avoidance | General or todo lock |
| Wake-up after time/idle | Timer |
| Reusable cross-agent text | Prompt template |
| Reconciled project behavior/architecture | Repository docs |

Do not duplicate scratchpad narrative into todos. Point todo to relevant scratchpad section. KV has no compare-and-swap; protect competing read-modify-write or avoid it. Scratchpad edits use revision and smallest targeted mutation.

Complete or backlog todos, promote durable conclusions as evidence lands, and cancel obsolete timers and locks. Retirement—archive or delete—waits for consumption at the current revision under the item's `## Retire after` contract. Backlog is for real future work, not finished or abandoned state; reach the small honest live set late and certain, never eagerly.

## Monitor without guessing

- Use timers instead of sleep loops or tight polling.
- Use idle-any to harvest next newly quiet worker; idle-all only for true barrier.
- Treat idle as quiet heuristic, not completion.
- Use service/port readiness for listener state, not agent idle.
- Inspect actual output and artifacts after timer fires.
- Cancel obsolete timers when phase changes.

Timer body becomes fresh user turn. Keep it lead-authored, self-contained, and limited to IDs, expected evidence, and next action; do not inject raw untrusted content.

## Mutate safely

- Review repo-defined commands before trust/start. Never bypass Solo trust.
- Treat locks as advisory leases, not authorization or correctness.
- Acquire smallest stable lock immediately before collision-prone work; release after durable handoff.
- Ask before destructive, credentialed, public, production, billing, or self-close action unless exact authority already exists.
- Preserve unrelated dirty files and concurrent changes. Workers do not own Git/index unless delegated.
- Keep credentials in host configuration; never put secrets in prompts, scratchpads, todos, logs, or repo.

## Prove completion

Require evidence at actual boundary:

- process status plus relevant rendered/raw output;
- bound port/service readiness when starting service;
- artifact, file diff, or command result;
- smallest relevant test/check, then broader risk-based checks;
- todo comment or scratchpad handoff with files, checks, blockers, remaining risk, next action.

Before closing an owned child, capture context, reconcile output, complete/release owned todo/locks, and cancel timers. Closing process never undoes filesystem edits.

Harvest and closure travel together: once an owned worker's lane is complete—quiet with final output, acceptance evidence reviewed—persist the handoff and close or retask it in the same pass. Unreviewed or partial results keep a worker open; closing never substitutes for consumption. Terminal-only results (research findings, citations, excerpts) exist nowhere but the session: capture them claim-level in the durable handoff before close, and that record stays consumer-gated for upstream consumers per retirement conventions even after the process closes. An owned worker left live or idle after harvest is cruft. This holds at every depth, one generation at a time: each parent settles only the direct children it spawned, confirms a child's own subtree is settled before closing it, and never settles anyone else's.
