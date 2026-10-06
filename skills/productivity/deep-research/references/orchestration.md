# Fan-out vehicle guide

Read before you dispatch a research fan-out. This guide helps you choose a vehicle. It is not a command reference. Vehicle names, flags, and tool ids drift, so confirm each vehicle against its own live listing or `--help` before dispatch.

## Contents

- What a vehicle must supply
- Detect what is present
- Vehicle families
- Write a lane brief
- Rules that hold in every vehicle

## What a vehicle must supply

Fan-out is a capability, not a product. A host clears the bar when it supplies all four capabilities:

| Capability | Why the research needs it |
|---|---|
| Isolated worker context | Lanes stay independent. The findings of one lane cannot change the search path of another |
| A bounded lane brief | The worker knows its question, its source policy, and its stop condition |
| Completion signal | The lead knows that a lane finished and did not stall |
| Durable result surface | Findings, citations, and raw artifacts survive the worker that produced them |

If a host does not supply all four, run the lanes sequentially.

## Detect what is present

Do not assume a vehicle from memory. Do not install or authenticate a vehicle to get fan-out. Probe in this order. Stop at the first vehicle that clears the bar for the planned lane count:

1. **Host-native subagents:** read the tool list of the current session.
2. **Installed orchestrators:** check the skill listing. Then confirm that the underlying tool responds to `--help` or its own status command.
3. **Sequential:** always available. It needs no probe.

Prefer the simplest vehicle that clears the bar. Extra machinery adds setup, tokens, and failure modes. It does not improve evidence quality.

## Vehicle families

Match the family to what the lanes need. The families are recognition cues, not a list of supported products.

| Family | Supplies | Use it when |
|---|---|---|
| Host-native subagents | Isolated context, with results returned to this session | Lanes are short, read-only, and use one model. This is the default |
| Terminal or pane managers | Separate CLI agents, each with its own process and model | Lanes need different models, or a lane needs an interactive tool |
| Worktree or workspace apps | Isolated checkouts with separate agents | A lane reads or builds a repository at a specific revision |
| Durable orchestrators | Bounded workers, plus timers, locks, and state that outlive the session | Lanes are long or expensive, or findings must outlive this session |
| Sequential | Nothing more than this session | No other vehicle is present, or the question has one lane |

A vehicle feature is not a reason to use it. Most research lanes only read, so a shared checkout is sufficient. Use durable state only when a lane must outlive the session.

## Write a lane brief

The brief is the contract. It is the same in each vehicle. Give each lane:

- one research question, stated so that the lane cannot silently widen it;
- its evidence angle, and the angles that other lanes cover;
- the source policy: acceptable sources, primary-source requirements, and the freshness date;
- the return shape: findings, exact URLs or file paths, key excerpts, source dates, contradictions, and the provider;
- its budget and its stop condition.

A lane that returns prose without citations failed, even if the prose is good.

## Rules that hold in every vehicle

- **Assign distinct angles.** Do not send the same prompt to different engines, unless provider agreement is the research question.
- **Record the vehicle beside the provider.** A reader who reproduces the research needs both.
- **Vehicle failure changes the route, not the standard.** When a vehicle stops, hangs, or is not present, run the remaining lanes sequentially. Keep the same citation and verification rules.
- **Spawning is a cost decision.** Worker fan-out spends tokens and, on some vehicles, money. The budget authority for paid providers also controls fan-out.
- **Do not put credentials in a lane brief.** Workers use their own authentication.
