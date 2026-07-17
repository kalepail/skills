---
name: solo-orchestrate-agents
description: Plan and coordinate multi-agent work through Solo with bounded workers, durable state, locks, timers, evidence review, and handoffs. Use for parallel research, disjoint implementation lanes, cross-model review, cross-project cohorts, or delegation through several Solo agents. Do not use for single-agent, sequential, or shared-file work, or when the deliverable is cited or comparative research synthesis (use solo-deep-research).
---

# Orchestrate Solo Agents

Run centralized lead-worker orchestration. Optimize for verified outcome, not agent count.

## Load Current Semantics

1. Call `whoami`; confirm actor, process, and effective project.
2. Call live `help` for `spawning`, `timers`, `locks`, `scratchpads`, `todos`, and `coordination` as each surface becomes relevant.
3. Use current tool discovery and `mcp_tools_summary`; never rely on remembered schemas or disabled tools.
4. Inventory processes, capacity, current todos, and exact locks before dispatch.

Read [orchestration.md](references/orchestration.md) before building todo graph, dispatching a cohort, choosing idle-any versus idle-all, or recovering stalled work.

Read [safety.md](references/safety.md) before any process control, cross-project action, shared edit, timer delivery, Git/integration action, or cleanup.

## Decide Whether to Fan Out

Keep work with lead when task is small, sequential, shares mutable state, or next step depends immediately on current result.

Fan out only when lanes are independent, have disjoint write scopes or read-only outputs, and save meaningful waiting. Use cross-model diversity for consequential independent review, then reconcile evidence centrally.

## Run Canonical Workflow

### 1. Plan

- Interview for goal, constraints, non-goals, authoritative inputs, risks, and verification.
- Write concise plan to Solo scratchpad with stable sections.
- Make lead responsible for user conversation, synthesis, integration, and final evidence.
- Keep lead writes to coordination state, final synthesis, and mechanical integration seams—a no-code lead delegates even those; assign separable artifact changes and rework to worker lanes, and require concise evidence plus artifact paths back, not whole pasted deliverables.

### 2. Build Work Graph

- Create one todo per meaningful lane plus integration/verification todos.
- Put objective, owned scope, forbidden work, acceptance checks, handoff destination, priority, and tags in each todo.
- Add blockers before dispatch. Dispatch only unblocked lanes.

### 3. Dispatch Bounded Workers

- Discover available agent tools live; choose by lane fit.
- Apply the fleet routing, explicit model/reasoning flags, extended-fleet weave, and built-in-versus-Solo topology rules in [orchestration.md](references/orchestration.md)—the single source for dispatch mechanics; discover launchable tools and verify every CLI flag live before dispatch.
- Prefer Solo's maintained `worker_bootstrap` MCP prompt when the host exposes it, then layer lane specifics, instead of hand-rewriting the whole identity/lock/state contract.
- Spawn one worker per independent lane.
- Record every returned child `process_id` with todo and project immediately.
- Prepend returned `agent_instructions` to self-contained worker prompt.
- Require worker to lock its todo and relevant shared edit area, preserve unrelated changes, avoid Git/publishing/integration, and report exact evidence.

### 4. Wait Without Polling

- Never wait with shell `sleep` or ad-hoc polling loops; Solo timers are the wait primitive.
- Schedule idle-any timer to harvest first newly quiet worker; reschedule for remaining cohort.
- Use idle-all only for true barrier after all current lanes must quiet.
- Put process/todo/scratchpad IDs and exact next action in timer body.
- Prefer Solo's `timer_followup` MCP prompt for wake handling and stale-timer cleanup when available.
- Treat timer deadline, idle, prompt delivery, and summaries as inspection triggers only.

### 5. Review Evidence

- Inspect actual worker output, files, diff/artifact, checks, and todo comment.
- Integrate one lane at time; run narrowest relevant verification after meaningful step.
- Inform still-running workers about relevant overlapping changes.
- Never accept majority vote or summary as proof; verify consequential findings independently.

### 6. Persist Handoff

- Comment changed files/artifacts, commands/tests, blockers, remaining risk, and one next action on todo.
- Update scratchpad current summary, decisions, and verification.
- Reconcile blockers and dispatch next unblocked cohort.
- Complete todo only after evidence passes.

### 7. Clean Up

- Cancel stale timers and release owned locks.
- Capture handoff before closing any worker.
- Close only descendants current actor spawned; never clean parent, sibling, unrelated, YAML-backed, or another actor's descendants without explicit authority.
- Leave Git, commits, pushes, PRs, publishing, deployment, and final integration to root/operator unless expressly delegated.

## Fail Closed

Stop mutation and ask user when identity, project, process parentage, target authority, cross-project intent, or outward-facing authority is unclear. Idle/stopped/completed state never grants control.
