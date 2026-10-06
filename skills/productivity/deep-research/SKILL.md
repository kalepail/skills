---
name: deep-research
description: Conduct and synthesize deep, exhaustive, comparative, or cross-checked research into a decision or contested question using independent evidence lanes, claim-level citations, contradiction resolution, and stress-tested conclusions. Use when the deliverable is a cited research synthesis or recommendation, including deep multi-source Stellar-ecosystem investigations. Do not use for a narrow lookup or single-source read — one fact, version, API signature, or docs page, even a Stellar or Soroban one; answer those directly from the authoritative source. Do not use for bulk enrichment of a list or table with no synthesis, implementation, code review, or generic multi-agent coordination.
---

# Deep Research

This skill produces a defensible, cited synthesis from independent evidence. It uses one research method. The providers and the agent topology change with what the session makes available.

## Frame the Research

Write a short brief. Include these items:

- the core problem, separate from any proposed solution;
- the decision or deliverable that the research supports;
- the scope, geography, time horizon, and freshness date;
- the claims that the research must prove, and useful counterclaims;
- the acceptable sources and the primary-source requirements;
- the time, cost, and output limits.

Treat a proposed solution as a hypothesis. Treat it as a constraint only when the user says so. Write two to four concrete research questions about the underlying problem. State reasonable defaults and continue. Ask questions only when an ambiguity changes the scope, the cost, or the recommendation. Put all such questions in one short batch.

## Discover Live Surfaces

Find the enabled tools before you plan lanes. Do not use tool names from memory.

- **General web:** prefer `parallel-cli` for saved artifacts. Use Perplexity MCP as an independent lane. Use Parallel Search MCP or Parallel Task MCP as a fallback or a final pass. Read [providers.md](references/providers.md) before you assign providers, start paid research, or recover a missing provider.
- **Stellar ecosystem:** use Stellar Raven MCP first for each Stellar-ecosystem question. Read [stellar-raven.md](references/stellar-raven.md) before you run a Stellar lane.
- **Fan-out:** read the session tool list and skill listing for a vehicle that runs lanes in parallel. Read [orchestration.md](references/orchestration.md) before you dispatch a fan-out.

## Plan Evidence Lanes

Do not use this skill for a narrow lookup or a simple fact check. Use one search surface and one citation for those.

Fan out only when the question is deep, exhaustive, comparative, or independently verified. Fan out also when the question has two or more separable evidence lanes. Use two to four distinct lanes. Divide the work by research angle first and by provider second. The angles are local code, official docs, primary evidence, landscape, dependencies, user impact, counterevidence, and independent synthesis. Send the same prompt to different engines only when provider agreement is the research question.

After you define the lanes, load `routing-agent-work` through the current host when it is installed and worker selection matters. If it is not installed, use the route from the caller or the host default. Keep provider and evidence selection in this skill.

## Choose the Vehicle

Use host-native subagents when the session can start them. Use sequential lanes when no vehicle is present or the question has one lane. Sequential lanes are a complete vehicle: the citation and verification rules do not change. Read [orchestration.md](references/orchestration.md) for the capability bar, the vehicle families, and the lane brief.

Give worker mechanics to the companion skill of the vehicle when one is installed. Keep provider selection, reconciliation, the adversarial cross-check, and the final verdict in this skill. Never delegate the verdict.

## Run the Research

1. Record the brief, the research questions, the lane plan, and the source policy in durable working state. Use a scratchpad, a plan file, or the report draft.
2. Work each lane to a citation-ready result. Include findings, exact file paths or URLs, key excerpts, source dates, uncertainty, contradictions, and the provider or tool. Keep raw provider artifacts when they are available.
3. Verify each consequential claim against a primary source or two independent sources. Different providers that cite the same page give one source.
4. Run targeted follow-ups only for unresolved claims, stale evidence, or disagreements. Do not repeat the same broad prompt.
5. If the findings change the premise of the user or show a different path, stop. Give a short evidence summary and specific choices before you recommend.
6. Synthesize centrally. Evaluate each proposed solution explicitly. Recommend a simpler alternative when it solves the underlying problem with less cost or risk.
7. Stress-test the recommendation. Name concrete failure modes, regressions, edge cases, user impact, and maintenance cost.

## Control Cost and Failure

- Paid processors, task creation, and credit purchases are billing actions. Get an explicit budget or runbook authority first.
- Never put API keys in prompts, notes, logs, or repository files.
- If a provider is missing, unauthenticated, rate-limited, or out of credit, record the failure and reroute the lane. Do not install, authenticate, or add funds without authority.
- Prefer saved JSON or Markdown artifacts to truncated terminal output.
- Do not claim exhaustive coverage. Report the search boundaries and the remaining uncertainty.

## Complete with Evidence

Use only the sections that add value: **Answer**, **Evidence**, **Sources** (paths and URLs), **Related**, **Downsides & Risks**. Include key disagreements and the confidence or limits. Complete the work only after the citations resolve and the consequential claims pass verification. If implementation is next, give the verified research context to the applicable planning workflow. Do not plan inside this skill.
