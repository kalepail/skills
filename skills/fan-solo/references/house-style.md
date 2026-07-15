# Fan Solo house style

Apply before any Solo mutation, agent spawn, shared-state edit, or process control.

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

Lead owns plan, dependencies, integration, Git, publishing, and final completion. Worker owns one bounded lane.

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
