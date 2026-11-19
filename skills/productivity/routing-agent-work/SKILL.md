---
name: routing-agent-work
description: Select an agent CLI, model, and effort for delegated implementation, planning, research, review, synthesis, multimodal work, extraction, or prose across Claude, Codex, Grok, OpenCode, and Antigravity (agy). Also use to verify completion of headless OpenCode or Antigravity workers. Do not use for launch mechanics alone, research source selection, provider setup, general model comparisons, or reselecting a route the caller already fixed.
---

# Route Agent Work

Route only when the selection can change the result. Continue with the current agent when no delegation choice exists.

The caller owns orchestration mechanics. It can use Herdr, Orca, Conductor, Solo, or another host that supports the selected worker.

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
4. **Cost and latency**: use them as tie-breakers between routes that can meet the quality bar. The fleet reference explains how subscription headroom and API spend count.

Use only the fixed families. Try listed fallbacks in order. If every listed route is unavailable, mark the lane `Unrouted`.

Fallbacks handle an unavailable route. Escalation handles failure cost. Escalate to a stronger route or a higher effort when errors are expensive or the first attempt falls short.

When the caller pins only the worker CLI, apply the pinned-CLI rule in the fleet reference.

A model version the caller names is a caller constraint, like a pinned CLI. Honor it and mark it `(caller-pinned)` on the card. If that version is not listed, the route is unavailable. The skill never picks a version itself.

An `Unrouted` lane does not launch. Return it to the caller for an explicit constraint change or fleet update.

Treat a safeguard handoff to a model outside the fleet as an unavailable route. Use the next listed fallback.

Before launch, check only the selected route. Do not enumerate or score unrelated models.

1. Resolve the selected family on the launch host and confirm its effort control. Claude takes an alias. For other workers, use `scripts/resolve_model.py` with the [fleet reference](references/fleet.md#resolve-the-family) patterns for routes whose data terms the lane accepts. Check a caller-pinned version directly in the listing.
2. If the resolved or pinned identifier fails, try only its same-version alternates, then the next family. When the newest version is unavailable, the family is unavailable. Do not launch an older version.
3. If only the effort value fails, use a supported value that meets the lane requirement and the model's range. Otherwise, use the next fallback.
4. When a route needs a harness property, such as preserved reasoning history, confirm it through host documentation or the caller. Skip the route when nobody can confirm it.

For OpenCode routes, read [references/opencode.md](references/opencode.md). It covers resolution, model selection, and the completion check. An OpenCode exit code alone does not prove that the worker finished.

For Antigravity routes, read [references/antigravity.md](references/antigravity.md) for effort, quota, and completion checks.

## Set effort

Set the model and effort explicitly for each worker and nested worker. Never rely on an unverified default.

Choose the effort from the lane, not from the CLI default. An effort in a lane row wins. Otherwise, use these levels:

- Use `medium` for bounded, clear, low-risk work.
- Use `low` only for trivial, readily checked tasks, or for bounded work under a stated cost limit.
- Use `high` for meaningful implementation, research, review, and routine synthesis.
- Use `xhigh` for hard planning, hard debugging, multi-source synthesis, and adversarial review.
- Use `max` for the hardest quality-first work with a clear stopping condition.

Keep each value inside the selected family's range in the fleet reference. Raise it to the family's floor when the level above is lower.

Use only supported effort values. Omit an unsupported flag only when the configured route confirms the required mode.

Codex `ultra` enables automatic task delegation. Use it only when the caller's delegation limits and host support permit it.
Do not use `ultra` when the caller requires one worker or a fixed delegation structure. Keep the effort that the lane needs.

## Shape the delegation tree

Use one direct worker for one bounded lane. Use a sub-orchestrator when a lane contains several independent sublanes.

One worker layer plus one nested layer is usually sufficient. This is guidance, not a universal limit.

Ask a sub-orchestrator to load `routing-agent-work` only when it must choose child routes and can load the skill. Otherwise, pass each child route in its brief, with its resolved identifier. Each child reports only to its direct parent.

The parent watches completion signals. It requests more context only when the compact report cannot support a decision.

## Add independent review

Add review when the failure cost justifies it. Give the reviewer a fresh context with the specification and artifact first.

Apply the fleet's family grouping before selecting a candidate when the lane requires independence. Give the reviewer fresh evidence and require its own checks.

Require reproducible evidence. Ask for tests, paths, commands, or cited sources instead of an unsupported verdict.

Use lower-cost models from other families as extra challengers. The fleet reference explains how to treat their findings.

## Handle prose

Treat prose as a separate lane only when prose is a meaningful deliverable. Keep the existing worker when it can write the required text well.

Pass the caller's writing standard into the worker brief. Opus is the quality-first default for technical prose.

## Return a route card

Return one compact card for each lane:

```text
Lane: <bounded output>
Worker CLI: <Claude | Codex | Grok | OpenCode | Antigravity | none>
Model: <fleet family> → <resolved identifier> | <fleet family> → <identifier> (caller-pinned) | Unrouted
Effort: <explicit supported value | none>
Reason: <lane fit and failure-cost rationale>
Verified: <resolution or host status check>
Fallback: <next fixed-fleet family, or none>
Reviewer: <different-family fixed-fleet family, or none>
Report contract: <result, artifact paths, checks, risks, blockers>
```

For Claude, the model line reads `Opus → alias opus`, and the worker's report states the model the session ran.

The worker returns the result, evidence paths, completed checks, unresolved risks, and blockers. It does not return a full transcript.
