# Orchestration workflow reference

Read this reference when planning multi-agent work, mapping dependencies, dispatching workers, choosing timers, reviewing evidence, or recovering a cohort.

## Contents

- Bootstrap
- State placement
- Plan and graph
- Dispatch contract
- Timers and monitoring
- Evidence and integration
- Recovery
- Sources

## Bootstrap

1. Call `whoami`; preserve effective project unless cross-project work is explicit.
2. Call live `help(topic=...)` for each active surface: `spawning`, `timers`, `locks`, `scratchpads`, `todos`, `coordination`.
3. Inspect enabled tools through current discovery or `mcp_tools_summary`. Feature toggles remove tools; never guess absent schemas.
4. Inventory processes, current capacity, todos, blockers, todo locks, and general locks.
5. Read repository instructions and current canonical plan before creating Solo state.

## State placement

| State | Primitive |
|---|---|
| Goal, assumptions, decisions, evidence, plan, current summary | Scratchpad |
| Owned action, acceptance, status, priority, blockers, handoff | Todo |
| Task-local progress and final report | Todo comment |
| Small structured phase/process-to-todo pointer | KV |
| Active task claim | Todo lock |
| Shared file/logical-area exclusion | General lease lock |
| Resume after delay/idle | Timer |
| Reusable prompt shape | Prompt template |

Keep each fact in narrowest authoritative primitive. Do not duplicate full plan into todos or store prose/logs in KV.

## Plan and graph

Write scratchpad sections for goal, scope/non-goals, project and any relevant branch/worktree, constraints, risky files, lanes/ownership, dependencies, decisions, verification, open questions, current summary, and handoffs. Worktrees are optional isolation, not required by Solo.

Create todos only for actionable lanes. Include:

```text
Objective
Authoritative inputs and scratchpad section
Owned files/surface
Forbidden work
Acceptance checks and evidence format
Priority/tags
Blockers
Handoff destination
```

Use explicit blockers. Verification depends on implementation; integration depends on required handoffs. Avoid cycles. Dispatch only unblocked independent lanes.

## Dispatch contract

Call `list_agent_tools` and choose a launchable installation by task fit. Spawn one worker per lane. Immediately record returned child ID, project, tool, todo, and ownership. Prepend returned `agent_instructions`.

Require worker prompt to state:

```text
Objective: <one outcome>
Context: scratchpad <id>, section <heading>; todo <id>
Ownership: <disjoint files or read-only surface>
Do not: <non-goals; unrelated edits; Git/publish/integrate>
Coordination: lock owned todo and named shared area
Acceptance: <commands, tests, citations, artifacts>
Handoff: changed files/artifacts, checks, blockers, risk, next action
```

Keep coupled edits with lead. Use different model families for consequential independent review; reconcile by evidence, not vote. Route by fleet defaults: Fable orchestrates, synthesizes, and reviews (not codes); Codex Sol implements; Opus 4.8 writes prose against a plan; GPT-5.6 Terra runs research and tool-calling lanes. Grok is not a Solo built-in; add it as a custom Generic tool first.

Set model and reasoning explicitly on every dispatch through saved default flags or `extra_args`—never assume the provider default—and prefer thinking variants where a provider offers them (`claude --model/--effort`; `codex -m` + `-c model_reasoning_effort=...`; `opencode -m provider/model --variant`, thinking via model id such as `kimi-k2-thinking`; `grok -m --reasoning-effort`). Each CLI's `--help` and model listing are canonical.

Prefer built-in subagents over Solo workers when a fan-out stays within one provider (all work headless): claude delegates via the Agent tool or description matching (`.claude/agents/*.md` or `--agents '<json>'`, per-agent `model` and `effort`); codex spawns only when the prompt asks explicitly ("spawn one agent per…")—`[features] multi_agent` is stable-on, per-agent `model`/`model_reasoning_effort` in `~/.codex/agents/<name>.toml`; opencode primaries delegate through the `task` tool to `general`/`explore` or custom agents; grok spawns via `spawn_subagent` (steer by naming a type; `--no-subagents` disables). Lanes that cross provider, model family, or reasoning tier route through Solo workers instead—the common case—except same-provider mixed tiers on claude/codex, which pin per-subagent model and effort natively. For Claude-family workers that must message each other or self-claim shared tasks, interactive claude sessions can form agent teams—prose-triggered, gated by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; Solo-spawned claude TUIs form real teams while `claude -p` silently substitutes subagents; always name each teammate's model; rubric in fan-solo's house-style reference.

Extended-fleet lanes (second-string; full rubric and tested spawn routes in fan-solo's house-style reference): Grok 4.5 `--reasoning-effort high` for cross-family adversarial review and `medium` for test-executing verification; Kimi K3 `--variant max` for research/tool-calling lanes and diverse third-vote review, fresh session only; Muse Spark 1.1 `--variant medium` for small sub-orchestration, `xhigh` for review; GLM-5.2 `--variant high` for cheap calibrated verification and security-flavored review. Keep all four away from lead orchestration, final review gates, open-ended factual research (Grok, GLM), and flagship prose.

Keep the worker tree shallow. Each nesting level pays a self-contained-prompt and context-loss tax and dilutes lead authority over integration. Let a worker spawn its own sub-workers only when its lane genuinely decomposes into independent sub-lanes it must own and reconcile itself; otherwise flatten and keep the lane with the lead.

## Timers and monitoring

- Solo timers replace software waits entirely: no shell `sleep`, no polling loops, no in-process timeouts for scheduling. If the wait outlives one tool call, it belongs in a Solo timer.
- `timer_fire_when_idle_any`: ignore already-idle members at scheduling and wait for a new idle transition or deadline. Use to harvest first newly quiet worker, then reschedule.
- `timer_fire_when_idle_all`: count already-idle members as satisfied; if all are already idle, expect already-satisfied response and no pending timer. Use only for true barrier.
- `timer_set`: use bounded delayed or periodic checkpoint, then cancel when phase ends.
- Keep watch set separate from `delivery_process_id`. Never re-identify session to reroute timer.
- Write trusted, self-contained timer body with process IDs, todo/scratchpad IDs, evidence to inspect, and reschedule/cancel rule.
- Use `wait_for_bound_port` for service readiness. Idle does not prove listener readiness or task completion.

On wake: re-check scope, inspect status and actual output, persist progress/blocker, review artifacts, remove finished child from watch set, and reschedule for remainder.

## Evidence and integration

Require real evidence at correct layer:

1. Worker output and durable todo comment.
2. Actual files, diff, artifact, or cited research.
3. Narrowest relevant command/test first.
4. Broader risk-appropriate checks.
5. Independent verification for consequential findings.

Integrate one lane at time. Root/operator owns Git index, commits, pushes, PRs, releases, publishing, deployment, and final synthesis unless explicitly delegated. Workers preserve dirty trees and never revert unrelated changes.

## Recovery

- Spawn unavailable: refresh live agent tools; keep lane with lead or choose launchable alternative.
- Worker quiet: inspect output/status; send bounded follow-up only if needed.
- Worker blocked: comment exact blocker, update graph, ask user only for missing authority/decision.
- Lock contention: inspect owner, avoid overlap, schedule bounded retry.
- Scratchpad conflict: reread, merge, retry smallest targeted edit.
- Timer deadline: treat as checkpoint, not success.
- Todo transfer: rebuild blockers and locks in target project.
- Solo restart: re-check identity/scope and durable state before writes.
- Closed worker: inspect filesystem before further integration; closing does not roll back edits.

## Sources

- https://soloterm.com/api/v1/docs/workflows/agent-orchestration
- https://soloterm.com/api/v1/docs/workflows/agents-spawning-agents
- https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos
- https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal
- https://soloterm.com/api/v1/docs/mcp-tools/timers
- https://soloterm.com/api/v1/docs/mcp-tools/coordination
- https://soloterm.com/api/v1/docs/mcp-tools/key-value
- https://soloterm.com/api/v1/docs/mcp-tools/scratchpads
- https://soloterm.com/api/v1/docs/mcp-tools/todos
- https://soloterm.com/api/v1/docs/agents/idle-detection
- https://x.com/aarondfrancis/status/2075213903332581379
- https://x.com/aarondfrancis/status/2075571055041675691
