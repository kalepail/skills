---
name: routing-agent-work
description: Select an agent CLI, model, and reasoning effort for delegated work. Use when an orchestrator, parent agent, or user must assign implementation, security review, authorized vulnerability exploration, research, review, second-opinion or edge-case confirmation, synthesis, multimodal, long-context, high-volume extraction, or prose lanes across Claude, Codex, Grok, or OpenCode. Also use it to check that a headless OpenCode worker finished. Do not use for other orchestration mechanics, research provider or source selection, live model discovery, provider setup, general model comparisons, single-agent work with no delegation choice, or a lane whose worker, model, and effort are already fixed.
---

# Route Agent Work

Route only when the selection can change the result. Continue with the current agent when no delegation choice exists.

The caller owns orchestration mechanics, except the completion check for a headless OpenCode worker. Orchestration hosts include Herdr, Orca, Conductor, and Solo. Worker CLIs are Claude, Codex, Grok, and OpenCode.

## Define the lane

Write one bounded contract before selecting a model:

- primary output and completion check;
- allowed files, tools, and state changes;
- required evidence or tests;
- context the worker needs;
- report destination.

Split work only when lanes can progress independently, isolate risk, or provide independent review. Do not create lanes to increase agent count.

## Select the route

Read [references/fleet.md](references/fleet.md) before choosing a model, effort, fallback, or reviewer.

Apply these decision axes in order:

1. **Lane fit**: match the model to the primary output.
2. **Failure cost**: use a stronger route or independent review when errors are expensive.
3. **Constraints**: check context length, modality, privacy, tool use, and available providers.
4. **Cost and latency**: use them as tie-breakers between routes that can meet the quality bar.

Use only the fixed fleet. Try listed fallbacks in order. If every listed route is unavailable, mark the lane `Unrouted`.

Fallbacks handle an unavailable route. Escalation handles failure cost. Escalate to a stronger route or a higher effort when errors are expensive or the first attempt falls short.

When the caller pins only the worker CLI, apply the pinned-CLI rule in the fleet reference.

An `Unrouted` lane does not launch. Return it to the caller for an explicit constraint change or fleet update.

Treat a safeguard handoff to a model outside the fleet as an unavailable route. Use the next listed fallback.

Before launch, check only the selected route. Do not enumerate or score unrelated models.

1. Confirm the configured identifier and effort control through host status or a targeted CLI check.
2. If the identifier fails, try each provider the fleet lists for that model, then the next fallback.
3. If only the effort value fails, use a supported value that meets the lane requirement and the model's range. Otherwise, use the next fallback.
4. When a route needs a harness property, such as preserved reasoning history, confirm it through host documentation or the caller. Skip the route when nobody can confirm it.

For OpenCode routes, read [references/opencode.md](references/opencode.md). It covers the catalog refresh and the completion check. An OpenCode exit code alone does not prove that the worker finished.

## Set effort

Set the model and effort explicitly for each worker and nested worker. Never rely on an unverified default.

Choose the effort from the lane, not from the CLI default. An effort in a lane row wins. Otherwise, use these levels:

- Use `medium` for bounded, clear, low-risk work.
- Use `low` only for trivial, readily checked tasks, or for bounded work under a stated cost limit.
- Use `high` for meaningful implementation, research, review, and routine synthesis.
- Use `xhigh` for hard planning, hard debugging, multi-source synthesis, and adversarial review.
- Use `max` for the hardest quality-first work with a clear stopping condition.

Keep each value inside the selected model's range in the fleet reference. Raise it to the model's floor when the level above is lower.

Use only supported effort values. Omit an unsupported flag only when the configured route confirms the required mode.

Codex `ultra` enables automatic task delegation. Use it only when the caller's delegation limits and host support permit it.
Do not use `ultra` when the caller requires one worker or a fixed delegation structure. Keep the effort that the lane needs.

## Shape the delegation tree

Use one direct worker for one bounded lane. Use a sub-orchestrator when a lane contains several independent sublanes.

One worker layer plus one nested layer is usually sufficient. This is guidance, not a universal limit.

Ask a sub-orchestrator to load `routing-agent-work` only when it must choose child routes and can load the skill. Otherwise, pass each child route in its brief. Each child reports only to its direct parent.

The parent watches completion signals. It requests more context only when the compact report cannot support a decision.

## Add independent review

Add review when the failure cost justifies it. Give the reviewer a fresh context with the specification and artifact first.

Prefer a capable reviewer from a different model family. Treat model diversity as a clue, not proof of independence.

Require reproducible evidence. Ask for tests, paths, commands, or cited sources instead of an unsupported verdict.

Use lower-cost models from other families as extra challengers. The fleet reference explains how to treat their findings.

## Handle prose

Treat prose as a separate lane only when prose is a meaningful deliverable. Keep the existing worker when it can write the required text well.

Pass the caller's writing standard into the worker brief. Opus 5.5 is the quality-first default for technical prose. It follows supplied writing rules closely.

## Return a route card

Return one compact card for each lane:

```text
Lane: <bounded output>
Worker CLI: <Claude | Codex | Grok | OpenCode | none>
Model: <fixed fleet model | Unrouted>
Effort: <explicit supported value | none>
Reason: <lane fit and failure-cost rationale>
Verified: <host status or targeted CLI check>
Fallback: <next fixed-fleet model, or none>
Reviewer: <different-family fixed-fleet model, or none>
Report contract: <result, artifact paths, checks, risks, blockers>
```

The worker returns the result, evidence paths, completed checks, unresolved risks, and blockers. It does not return a full transcript.
