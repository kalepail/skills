---
name: kalepail-deep-research
description: Conduct and synthesize deep, exhaustive, comparative, or cross-checked research into a decision or contested question using independent evidence lanes, claim-level citations, contradiction resolution, and stress-tested conclusions. Use when the deliverable is a cited research synthesis or recommendation, including deep multi-source Stellar-ecosystem investigations. Do not use for a narrow lookup or single-source read — one fact, version, API signature, or docs page, even a Stellar or Soroban one; answer those directly from the authoritative source. Do not use for implementation, code review, or generic multi-agent coordination.
---

# Kalepail Deep Research

Produce a defensible, cited synthesis from independent evidence. One research method; the providers and the agent topology adapt to what is actually available in the session.

## Frame the Research

Write a concise brief containing:

- core problem, separate from any proposed solution;
- intended decision or deliverable;
- scope, geography, time horizon, and freshness date;
- must-prove claims and useful counterclaims;
- acceptable sources and primary-source requirements;
- time, cost, and output constraints.

Treat a proposed solution as a hypothesis unless the user explicitly makes it a constraint. Frame two to four concrete research questions around the underlying problem. State reasonable defaults instead of blocking; batch concise choice questions only when ambiguity would materially change scope, cost, or the recommendation.

## Discover Live Surfaces

Discover what is enabled before planning lanes; never assume remembered tool names:

- **General web:** prefer `parallel-cli` for saved artifacts, Perplexity MCP as an independent lane, Parallel Search or Task MCP as fallback or final pass. Read [providers.md](references/providers.md) before assigning providers, launching paid research, or recovering a missing backend.
- **Stellar ecosystem:** Stellar Raven MCP is the first discovery surface for any Stellar-ecosystem question. Read [stellar-raven.md](references/stellar-raven.md) before running a Stellar lane.
- **Fan-out:** Solo MCP with the `$solo-orchestrate-agents` skill, when both are present, supplies bounded-worker mechanics.

## Plan Evidence Lanes

Keep narrow lookups and simple fact checks out of this skill entirely — one search surface, one citation, done.

Fan out only when the question is deep, exhaustive, comparative, or independently verified, or has at least two separable evidence lanes. Prefer two to four distinct lanes; divide by research angle first (local code, official docs, primary evidence, landscape, dependencies, user impact, counterevidence, independent synthesis) and provider second. Duplicate prompts across engines only when measuring provider agreement is itself the point.

## Choose the Vehicle

- **Solo available and at least two independent lanes:** delegate worker mechanics — bounded lanes, timers, durable handoffs — to `$solo-orchestrate-agents`. Keep reconciliation, adversarial cross-check, and the final verdict here; never delegate the verdict.
- **Otherwise:** run the same lanes sequentially in this session with identical evidence discipline. Nothing in this skill requires Solo.

## Run the Research

1. Record the brief, research questions, lane plan, and source policy in whatever durable working state the session has (scratchpad, plan file, or the report draft itself).
2. Work each lane to a citation-ready result: findings, exact file paths or URLs, key excerpts, source dates, uncertainty, contradictions, and the provider or tool used. Preserve raw provider artifacts when available.
3. Verify consequential claims against primary sources or two genuinely independent sources. Different providers citing the same page count as one source.
4. Run targeted follow-ups only for unresolved claims, stale evidence, or disagreements — never repeat the same broad prompt.
5. If findings overturn the user's premise or expose a materially different path, pause with a short evidence summary and specific choices before committing to a recommendation.
6. Synthesize centrally. Evaluate any proposed solution explicitly and recommend a simpler alternative when it solves the underlying problem with less cost or risk.
7. Stress-test the recommendation with concrete failure modes, regressions, edge cases, user impact, and maintenance burden.

## Control Cost and Failure

- Paid processors, task creation, and credit purchases are billing actions: require an explicit budget or existing runbook authority first.
- Never place API keys in prompts, notes, logs, or repository files.
- If a provider is missing, unauthenticated, rate-limited, or out of credit, record the failure and reroute the lane; do not install, authenticate, or add funds without authority.
- Prefer saved JSON or Markdown artifacts over truncated terminal output.
- Do not claim exhaustive coverage; report search boundaries and remaining uncertainty.

## Complete with Evidence

Use only the sections that add value: **Answer**, **Evidence**, **Sources** (paths and URLs), **Related**, **Downsides & Risks**. Include key disagreements and confidence or limitations. Complete only after citations resolve and consequential claims pass verification. If implementation is next, hand the verified research context to the appropriate planning workflow instead of planning inside this skill.
