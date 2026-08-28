# Fan-out vehicle guide

Read before dispatching a research fan-out. This is a decision guide, not a command reference: vehicle names, flags, and tool ids drift, so confirm any vehicle against its own live listing or `--help` before dispatch.

## Contents

- What a vehicle must supply
- Detect what is present
- Vehicle families
- Write a lane brief
- Rules that hold in every vehicle

## What a vehicle must supply

Fan-out is a capability, not a product. Any host clears the bar when it supplies all four:

| Capability | Why the research needs it |
|---|---|
| Isolated worker context | Lanes stay independent; one lane's findings cannot contaminate another's search path |
| A bounded lane brief | The worker knows its question, its source policy, and when it is done |
| Completion signal | The lead knows a lane finished rather than stalled |
| Durable result surface | Findings, citations, and raw artifacts survive the worker that produced them |

A host missing any of these runs lanes sequentially instead. Sequential is a complete vehicle, not a degraded mode.

## Detect what is present

Never assume a remembered vehicle, and never install or authenticate one to obtain fan-out. Probe in this order and stop at the first that clears the bar for the lane count already planned:

1. **Host-native subagents** — read the current session's own tool list.
2. **Installed orchestrators** — check the available skill listing, then confirm the underlying tool responds to `--help` or its own status command.
3. **Sequential** — always available, needs no probe.

Prefer the simplest vehicle that clears the bar. Extra machinery costs setup, tokens, and failure modes without improving evidence quality.

## Vehicle families

Match the family to what the lanes actually need. Examples name what these families look like in practice; treat them as recognition cues, not a supported-vehicle list.

| Family | Supplies | Reach for it when |
|---|---|---|
| Host-native subagents | Isolated context and results returned into this session | Lanes are short, read-only, and belong to one model. The default choice |
| Terminal or pane managers | Separate CLI agents, each its own process and model | Lanes want genuinely different models, or a lane needs an interactive tool |
| Worktree or workspace apps | Isolated checkouts alongside separate agents | A lane reads or builds a repository at a specific revision |
| Durable orchestrators | Bounded workers plus timers, locks, and state that outlives the session | Lanes are long or expensive, or findings must survive this session |
| Sequential | Nothing beyond this session | Nothing else is present, or the question has one lane |

Two cautions. A vehicle offering worktrees does not make repository isolation necessary — most research lanes read, and a shared checkout is fine. A vehicle offering durable state does not make it the right default — reach for durability when a lane genuinely outlives the session, not because the feature exists.

When a companion skill for the chosen vehicle is installed, delegate the worker mechanics to it and keep the research method here. When none is installed, drive the vehicle directly from its own documentation.

## Write a lane brief

The brief is the contract, and it is identical across vehicles. Each lane receives:

- one research question, stated so a lane cannot silently widen it;
- its evidence angle, and the angles other lanes already cover;
- the source policy: acceptable sources, primary-source requirements, freshness date;
- the return shape: findings, exact URLs or file paths, key excerpts, source dates, contradictions, and the provider used;
- its budget and stop condition.

A lane that returns prose without citations has failed regardless of how good the prose is.

## Rules that hold in every vehicle

- **Never delegate the verdict.** Workers gather and cite. Reconciliation, adversarial cross-check, and the recommendation stay with the lead.
- **Independence is the point.** Two lanes citing the same page are one source. Assign distinct angles, not the same prompt to different engines, unless measuring provider agreement is itself the question.
- **Record the vehicle beside the provider.** A reader reproducing the research needs both.
- **Vehicle failure reroutes, it never lowers the standard.** When a vehicle dies, hangs, or was never present, run the remaining lanes sequentially with unchanged citation and verification discipline.
- **Spawning is a cost decision.** Worker fan-out spends tokens and, on some vehicles, money. Respect the same budget authority that governs paid providers.
- **Never put credentials in a lane brief.** Workers inherit their own authentication.
