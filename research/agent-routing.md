# Agent Routing Research

This research supports `routing-agent-work`. The shipped skill keeps only durable routing clues.

Read [the current fleet update](routing-agent-work/model-fleet-update-2026-10-06.md) for measured scores, costs, latency, local probes, and runtime checks.

## Research method

The research used separate lanes for official model documentation, independent benchmarks, practitioner reports, and adversarial review. Parallel CLI saved the primary artifacts. Parallel MCP and Perplexity supplied independent searches and counterevidence. Grok supplied an X-focused practitioner lane. Fable 5 and GPT-5.6 Sol reviewed the conclusions independently.

The review rejected one overall model ranking. Benchmark results changed with the task, harness, effort, and evaluation method. The routing skill therefore uses lane fit first and cost last.

## Durable conclusions

1. Select the model for the lane's primary output.
2. Raise capability or add review when failure cost increases.
3. Treat privacy, modality, context, and provider access as route constraints.
4. Use cost and latency only between routes that meet the quality bar.
5. Set effort within the selected model's supported range.
6. Keep reviews fresh and evidence-based.
7. Use a different model family as a useful independence clue.
8. Keep child reports compact and send them to the direct parent.
9. Use a sub-orchestrator when it reduces parent context load.
10. Maintain the fleet manually. Do not add unknown models during task execution.

## Evidence by model family

OpenAI documents GPT-6 Astra, GPT-6.1 Sol, and GPT-6 Luna as separate operating points. Its Codex guidance recommends GPT-6.1 Sol for complex coding and agentic work. It keeps Astra for the hardest end-to-end work and Luna for clear, repeatable tasks. Independent measurements put GPT-6.1 Sol near Astra at about one fifth of its task cost. The routing skill therefore uses GPT-6.1 Sol as the Codex default and Astra as escalation.

- [Codex models](https://learn.chatgpt.com/docs/models)
- [GPT-6.1 Sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
- [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)

Anthropic tells users to start with Opus 5.5 for most workloads. It keeps Fable 5.1 for demanding reasoning and long-horizon agentic work. It positions Sonnet 5.5 as the faster, lower-cost complement for well-scoped work. Its effort documentation shows that effort is a provider-specific control. The research supports Opus 5.5 as the default Claude route for planning, coding, review, and technical prose. It supports Sonnet 5.5 for bounded work at `low` to `high` and Fable 5.1 as the escalation route. Opus 5.5 safeguards send most cybersecurity tasks to Opus 4.8. Sonnet 5.5 safeguards send flagged requests to Sonnet 5.

- [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)
- [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)
- [Claude models overview](https://platform.claude.com/docs/en/models/overview)
- [Claude Fable 5.1 and Claude Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)
- [Anthropic effort documentation](https://platform.claude.com/docs/en/build-with-claude/effort)

xAI documents Grok 4.7 as its model for coding, agentic tasks, and knowledge work. Independent terminal and coding evaluations put it below the Claude and Codex default routes at a higher task cost. The routing skill therefore uses Grok for independent challenge and live web and X research, not as a coding fallback. It requires reproducible evidence for its findings.

- [Introducing Grok 4.7](https://x.ai/news/grok-4-7)
- [Grok 4.7 documentation](https://docs.x.ai/developers/grok-4-7)

Z.ai positions full GLM-5.3 as its text-only flagship for complex coding and long-horizon agents. It supports a 1M-token context, 128K output, and `low`, `high`, or `max` reasoning. Z.ai recommends `max` for complex coding. Independent evaluations put GLM-5.3 and Kimi K3 below GPT-6.1 Sol at a higher task cost. Kimi K3 scores poorly in generic harnesses that drop its reasoning history. The routing skill therefore uses GLM-5.3 for open-weight text-only long-context work and both models as different-family challengers. It treats their findings as leads that a check must reproduce.

Z.ai identifies GLM-5.3 Flash as the former `ox-alpha`. Its official material emphasizes efficient agentic coding, tool use, automation, multimodal input, and low cost. It shares the 1M-token context and 128K output limits. The route uses high or max reasoning and prefers full GLM-5.3 for harder text-only long-horizon work.

- [GLM-5.3 announcement](https://z.ai/blog/glm-5.3)
- [GLM-5.3 documentation](https://docs.z.ai/guides/llm/glm-5.3)
- [GLM-5.3 Flash announcement](https://z.ai/blog/glm-5.3-flash)
- [GLM-5.3 Flash documentation](https://docs.z.ai/guides/vlm/glm-5.3-flash)
- [Z.ai model pricing](https://docs.z.ai/guides/overview/pricing)
- [Artificial Analysis: GLM-5.3 and Kimi K3](https://artificialanalysis.ai/models/comparisons/glm-5-3-vs-kimi-k3)
- [Artificial Analysis: GLM-5.3 Flash and GLM-5.3](https://artificialanalysis.ai/models/comparisons/glm-5-3-flash-vs-glm-5-3)

Moonshot documents Kimi K3 for multimodal long-context and agentic work. The model publishes interleaved reasoning behavior. The route therefore uses a fresh session and preserves its complete reasoning and tool history.

- [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3)
- [Kimi Code model configuration](https://www.kimi.com/code/docs/en/kimi-code/models.html)

Meta documents Muse Spark 1.3 for multimodal and long-horizon coding work. Independent evaluations rank it highest of the three open challengers on knowledge work, and low on terminal-heavy work. The routing skill permits only version 1.3. It prefers contributor routes after data-term acceptance. It tries direct Meta contributor first and OpenRouter contributor second.

- [Introducing Muse Spark 1.3](https://research.meta.ai/blog/introducing-muse-spark-1-3)

## Benchmark interpretation

Independent leaderboards helped identify task-specific strengths. They did not provide a stable overall order.

- [Artificial Analysis Long Context Reasoning](https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning) tests synthesis across long documents.
- [Artificial Analysis Terminal-Bench v2.1](https://artificialanalysis.ai/evaluations/terminalbench-v2-1) tests agentic terminal work.
- [Terminal-Bench 4.0](https://www.tbench.ai) tests longer terminal tasks with confidence intervals.
- [Artificial Analysis Omniscience](https://artificialanalysis.ai/evaluations/omniscience) measures knowledge and hallucination behavior.
- [CursorBench](https://cursor.com/cursorbench) measures coding-agent behavior inside a specific harness.
- [Lech Mazur writing benchmark](https://github.com/lechmazur/writing) uses pairwise judgments over constrained creative writing.

These evaluations use different prompts, tools, judges, contexts, and effort settings. A model can lead one evaluation and trail another. The skill therefore avoids fixed scores and benchmark numbers.

## Repository structure

The category structure follows Matt Pocock's repository pattern. It uses plain skill names inside broad task categories. It also separates user-invoked flows from model-invoked disciplines.

- [Matt Pocock skills repository](https://github.com/mattpocock/skills)
- [Matt Pocock repository agent rules](https://github.com/mattpocock/skills/blob/main/AGENTS.md)

This repository uses `engineering`, `productivity`, and `solo` categories. Product-specific Solo names keep their `solo-` scope. General skills do not use an author prefix.
