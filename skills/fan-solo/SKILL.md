---
name: fan-solo
description: Route broad or mixed Solo and SoloTerm requests across focused project, process, agent, durable-state, and automation skills. Use when choosing among Solo skills, learning Solo, or handling several Solo capabilities in one task. Do not use for non-Solo work, or when one clearly scoped Solo action already maps to a single focused skill.
---

# Fan Solo

Treat Solo as a native workspace around existing CLI agents, terminals, and project commands—not as an IDE, agent provider, container manager, or proof that work completed.

## Enforce process authority first

Before any input, stop, restart, close, rename, output clear, UI selection, or timer delivery, prove target is current process or a recorded descendant spawned by current actor. Project membership, process name, idle/stopped/completed state, and cleanup intent never prove ownership. For parent, sibling, unrelated, YAML-backed shared process, or another actor's descendant, require explicit user or runbook authority naming exact target and action.

## Establish live context

Use sources in this order before acting:

1. Call Solo `whoami`; confirm actor, Solo process, and effective project.
2. Call `help()` for current overview, then `help(topic=...)` for relevant workflow. Use `help(topic="docs")` when documentation lookup is needed.
3. Consult live Solo Docs MCP or current official docs when behavior, schema, availability, or version matters.
4. Use bundled references for routing and house style, never as fresher authority than live runtime or docs.

Do not assume every documented tool is enabled. Discover current surface.

## Route intent

| User intent | Use |
|---|---|
| Choose among Solo capabilities or plan mixed Solo work | Stay in `$fan-solo` |
| Configure repository, `solo.yml`, commands, or shared project setup | `$solo-set-up-projects` |
| Tune workspace, navigation, settings, appearance, or notifications | `$solo-customize-workspace` |
| Start, stop, restart, rename, or manage process lifecycle | `$solo-run-processes` |
| Inspect status, output, logs, ports, or readiness without changing runtime | `$solo-observe-services` |
| Diagnose Solo configuration, discovery, trust, or runtime failure | `$solo-troubleshoot` |
| Launch and manage one bounded owned agent | `$solo-work-with-agents` |
| Coordinate multiple independent agents and integrate their work | `$solo-orchestrate-agents` |
| Conduct deep, comparative, or cross-checked research across Parallel and Perplexity surfaces | `$solo-deep-research` |
| Create actionable shared work, blockers, locks, comments, or handoffs | `$solo-track-todos` |
| Preserve plans, research, decisions, or durable project context | `$solo-keep-scratchpads` |
| Close out a finished run: promote durable conclusions to repo docs, then archive or complete the ephemeral state | `$solo-close-out-work` |
| Create reusable cross-agent prompt templates | `$solo-save-prompts` |
| Use Solo MCP, CLI, local HTTP API, hosted API, or deep links in automation | `$solo-automate` |

For ambiguous or multi-surface requests, read [capability map](references/capability-map.md) before selecting skills. Use fewest skills that fully cover task.

## Choose agent mode

Default to one agent for sequential work, shared-state edits, or one coherent judgment loop. Use `$solo-work-with-agents` for that lifecycle.

Use `$solo-orchestrate-agents` only when at least two lanes are independent enough to own separately. Lead owns decomposition, boundaries, integration, and final verification. Workers own bounded lanes—not whole goal.

Use `$solo-deep-research` when those lanes are evidence-gathering work across research providers. It owns provider selection, source independence, citation discipline, contradiction resolution, and research synthesis; `$solo-orchestrate-agents` still supplies the process mechanics.

Match model and effort to the lane, never the reverse: Fable to orchestrate and synthesize (never to code); Codex Sol to implement; Opus for prose against a plan; GPT-5.6 Terra for research and tool-calling lanes; independent review by a family different from the implementer (Fable when Codex Sol implemented). See [house style](references/house-style.md) for the current fleet.

## Choose durable state

- Scratchpad: plans, findings, decisions, evidence, handoff context.
- Todo: actionable owned lane, acceptance criteria, blockers, status, comments.
- Todo comment: task-local progress and final handoff.
- KV: small temporary/discoverable JSON, never prose or completion proof.
- Lock: short-lived collision signal, never authorization or permanent ownership.
- Timer: wake-up/resumption, never proof worker or service finished.
- Prompt template: reusable dispatch text, never current project truth.
- Repository docs: reconciled durable project behavior and decisions.

Keep the live set ephemeral. Scratchpads and todos exist to guide active work and legitimately backlogged work—nothing else. As a lane finishes, complete or backlog its todo, fold durable conclusions into repository docs, archive the scratchpad once its run goes cold, and cancel obsolete timers and locks. Stale todos and orphaned scratchpads are noise the next agent must re-litigate. When a whole run ends and its residue spans several surfaces, route the reconciliation to `$solo-close-out-work`—it promotes durable content first, then retires the ephemeral copy without losing incomplete work.

Read [house style](references/house-style.md) before spawning agents, mutating shared state, or controlling processes.

## Protect ownership and safety

- Manage only current process and descendants it spawned. Never infer authority over parent, sibling, unrelated, or shared YAML-backed process from idleness, stopped state, or cleanup intent.
- Use explicit project and process IDs when scope is ambiguous. Record returned child IDs.
- Treat command trust, locks, and identity as separate gates. Never bypass trust or treat lock as permission.
- Ask before destructive or externally visible action unless user already authorized exact target and effect.
- Preserve unrelated files, processes, todos, scratchpads, and concurrent work.

## Complete with evidence

Verify at task's real boundary: process output/status, bound port or service readiness, changed artifact or diff, relevant tests/checks, and durable todo/scratchpad handoff as applicable. Idle, prompt delivery, agent summary, successful tool call, or lock ownership alone is insufficient.

Before closing owned descendants: capture useful output, update todo/comment or scratchpad, cancel stale timers, release owned locks, and confirm acceptance checks. Close only when requested or clearly part of authorized workflow.

Use [sources](references/sources.md) when resolving provenance, product boundaries, or changing behavior.
