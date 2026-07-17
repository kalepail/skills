---
name: solo-deep-research
description: Conduct and synthesize deep research on any topic before planning or implementation by fanning out bounded Solo research lanes across the codebase, official docs, available Parallel CLI or MCP tools, and Perplexity MCP. Use for deep, exhaustive, current, comparative, proposed-solution, or cross-checked research that benefits from multiple agents, cited evidence, contradiction resolution, recommendation stress-testing, and a durable research handoff. Do not use for narrow lookups (a single fact, version, or API signature) or general implementation and review orchestration.
---

# Conduct Deep Research with Solo

Use Solo as the lead-worker shell around research providers. Optimize for independent evidence and a defensible synthesis, not query or agent count.

## Establish Live Scope

1. Call Solo `whoami`; confirm actor, process, and effective project.
2. Load live Solo help for spawning, timers, scratchpads, todos, and coordination as needed.
3. Discover enabled agent tools and research surfaces. Check for `parallel-cli` first, then Perplexity MCP and Parallel Search or Task MCP; never assume remembered tool names are enabled.
4. Apply `$solo-orchestrate-agents` for ownership, dispatch, timers, locks, and evidence review.

Read [providers.md](references/providers.md) before assigning providers, launching paid research, or recovering a missing backend.

## Frame the Research

Write a concise brief containing:

- core problem, separate from any proposed solution;
- intended decision or deliverable;
- scope, geography, time horizon, and freshness date;
- must-prove claims and useful counterclaims;
- acceptable sources and primary-source requirements;
- time, cost, and output constraints.

Treat a proposed solution as a hypothesis unless the user explicitly makes it a constraint. Frame two to four concrete research questions around the underlying problem.

State reasonable defaults instead of blocking. Before dispatch, batch concise choice questions only when ambiguity would materially change scope, provider cost, or the recommendation. Explain each choice's practical tradeoff in plain language.

## Decide Whether to Fan Out

Keep narrow lookups and simple fact checks with one search surface.

Fan out when the user asks for deep, exhaustive, comparative, or independently verified research, or when the question has at least two separable evidence lanes. Match worker count to complexity and prefer two to four distinct lanes. Divide by research angle first and provider second; duplicate prompts across engines only when measuring provider agreement is itself useful.

Route discovery and tool-calling lanes to launchable research models and keep central synthesis, adversarial cross-check, and final judgment with the lead—it owns reconciliation and never delegates the verdict. The current fleet rubric, including which models earn research lanes and which fabricate, lives in fan-solo's house-style reference; verify routes against live listings before dispatch.

## Prefer This Provider Flow

Use this as a strong default, not a rigid pipeline:

1. Prefer `parallel-cli` for primary discovery, extraction, and deep research because it produces reproducible saved artifacts.
2. Use Perplexity MCP as the secondary independent lane for alternative discovery, counterevidence, deep research, or reasoning over collected evidence.
3. Use Parallel Search MCP as a fallback when a worker lacks shell access or the CLI is unavailable, and for lightweight in-loop search or fetch.
4. Use Parallel Task MCP selectively as a final deep-verification or cited-report lane after initial evidence reveals the remaining questions.

Depart from this order when authentication, budget, latency, worker capabilities, or the question's shape makes another surface clearly better. The Solo lead always owns reconciliation and the final answer.

## Run the Research

1. Create a scratchpad for the brief, research questions, lane matrix, source policy, findings, contradictions, and synthesis.
2. Create one todo per independent lane plus verification and synthesis todos. Give each lane one question, one provider preference, source requirements, and a citation-ready handoff format.
3. Follow the preferred provider flow where useful: CLI for primary saved artifacts, Perplexity for a distinct challenge, Search MCP as fallback, and Task MCP for a warranted final deep pass.
4. Dispatch only relevant local-code, official-docs, discovery, dependency, user-impact, counterevidence, or independent-analysis lanes to bounded workers. Record every child process ID.
5. Require each worker to return findings, exact file paths or URLs, key snippets or excerpts, source dates, uncertainty, contradictions, and provider/tool used. Preserve raw provider artifacts when available.
6. Verify important claims against primary sources or two genuinely independent sources. Different providers citing the same page count as one source.
7. Run targeted follow-up searches only for unresolved claims, stale evidence, or disagreements. Use Solo timers for asynchronous tasks; never infer completion from elapsed time.
8. If findings overturn the user's premise or expose a materially different path, pause with a short evidence summary and specific choices before committing to a recommendation. Otherwise continue.
9. Synthesize centrally and evaluate any proposed solution explicitly. Recommend a simpler alternative when it solves the underlying problem with less cost or risk.
10. Stress-test the recommendation with concrete failure modes, regressions, edge cases, user impact, and maintenance burden.

## Control Cost and Failure

- Treat paid processors, task creation, credit purchase, and balance top-ups as billing actions. Require an explicit budget or existing runbook authority before use.
- Never place API keys in prompts, todos, scratchpads, logs, or repository files.
- If a provider is missing, unauthenticated, rate-limited, or out of credit, record the failure and reroute the lane. Do not install, authenticate, or add funds without authority.
- Prefer saved JSON or Markdown artifacts over truncated terminal output.
- Do not claim exhaustive coverage; report search boundaries and remaining uncertainty.

## Complete with Evidence

Use only the sections that add value:

- **Answer:** direct finding or recommendation.
- **Evidence:** decisive snippets, data, or claim-level support.
- **Sources:** file paths and URLs.
- **Related:** worthwhile adjacent findings or alternatives.
- **Downsides & Risks:** specific breakage, regressions, user impact, or maintenance cost.

Include key disagreements and confidence or limitations. Update the scratchpad with the final synthesis and artifact paths, then complete todos only after citations resolve and consequential claims pass verification. If implementation is next, hand the verified research context to the appropriate planning workflow instead of planning inside this skill.
