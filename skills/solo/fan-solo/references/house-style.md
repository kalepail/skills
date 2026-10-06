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
4. Search current official docs with `help(query="...")` or the hosted docs index for behavior and schemas.
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

`list_agent_tools` is the live list of launchable tools. Add a terminal agent that Solo does not list as a custom Generic tool before spawning it. Pass the returned `agent_tool_installation_id` when a project has environment-specific installations.

### Set model and reasoning explicitly

Every routed spawn sets the model and effort explicitly. Put standing choices in the tool's saved default flags. Pass per-lane overrides through `extra_args`.

| CLI | Model flag | Reasoning flag | Canonical source |
|---|---|---|---|
| `claude` | `--model <alias\|id>` | `--effort <level>` | `claude --help` |
| `codex` | `-m <id>` | `-c model_reasoning_effort="<level>"` | `codex --help`, `codex exec --help` |
| `opencode` | `-m provider/model` | `--variant <provider-specific-level>` | `opencode run --help` |
| `grok` | `-m <id>` | `--reasoning-effort <level>` | `grok --help` |

When `routing-agent-work` is installed, its fleet reference owns flag syntax and accepted values. Use this table only as the fallback. Verify flags against the installed CLI before launching. Do not use Solo to discover or score new models.

### Built-in subagents vs Solo workers

Prefer a CLI's built-in subagents when every lane stays within one CLI and that CLI can pin each lane's model and effort. Use Solo workers when lanes cross CLIs or need settings the parent cannot pin. Solo workers also give the lead durable IDs, timers, and output it can inspect.

Claude agent teams are a third topology: peers with a shared task list and mailbox. Use them only when Claude workers must communicate or claim shared tasks. Name each teammate's routed model explicitly. Cross-CLI work stays on Solo.

Subagent and team mechanics change often. Read the CLI's current docs or `--help` before relying on a trigger phrase, config key, or limit:

- Claude: code.claude.com/docs/en/sub-agents and code.claude.com/docs/en/agent-teams
- Codex: developers.openai.com/codex/subagents
- OpenCode: opencode.ai/docs/agents
- Grok: `grok --help` and the docs.x.ai CLI reference

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

Complete or backlog todos, promote durable conclusions as evidence lands, and cancel obsolete timers and locks. Archive or delete a record only after its consumers read the current revision, as its `## Retire after` contract records. Use backlog for real future work, not for finished or abandoned state. Shrink the live set late and with certainty, never eagerly.

## Monitor without guessing

- Use timers instead of sleep loops or tight polling.
- Use idle-any to harvest the next quiet worker. An `already_satisfied` response means a watched worker is idle now: inspect it, then reschedule for the busy remainder.
- Use idle-all only for a true barrier.
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

Harvest and closure travel together. When an owned worker's lane is complete and its evidence is reviewed, persist the handoff. Then close or retask the worker in the same pass. An idle worker left open after harvest is cruft.

- Keep a worker open while its results are unreviewed or partial. Closing never substitutes for consumption.
- Capture terminal-only results, such as research findings and citations, claim-level in the durable handoff before close. Closing destroys the only copy.
- Settle one generation at a time. Each parent settles only its direct children. It confirms a child's own subtree is settled before it closes that child.
