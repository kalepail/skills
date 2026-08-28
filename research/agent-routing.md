# Agent Routing Research

This research supports `routing-agent-work`. The shipped skill keeps only durable routing clues.

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

OpenAI documents Sol, Terra, and Luna as separate GPT-5.6 operating points. The model guidance also describes explicit reasoning controls. These sources support different Codex routes for quality-first implementation, bounded work, and high-volume narrow work. They do not support a universal quality order across every task.

- [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning)

Anthropic documents Fable 5 and Opus 5 as high-capability models. Its effort documentation shows that effort is a provider-specific control. The research supports Fable for ambiguous planning and autonomy. It supports Opus for precision work and quality-first prose.

- [Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)
- [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)
- [Anthropic effort documentation](https://platform.claude.com/docs/en/build-with-claude/effort)

xAI documents Grok 4.6 as a reasoning and agentic model. The research supports Grok for coding, testing, research, and independent challenge. The routing skill still requires reproducible evidence for its factual findings.

- [Introducing Grok 4.6](https://x.ai/news/grok-4-6)
- [Grok 4.6 documentation](https://docs.x.ai/developers/grok-4-6)

Z.ai positions full GLM-5.3 as its text-only flagship for complex coding and long-horizon agents. It supports a 1M-token context, 128K output, and `low`, `high`, or `max` reasoning. Z.ai recommends `max` for complex coding. Artificial Analysis gives full GLM-5.3 and Kimi K3 the same rounded Intelligence Index score. Its measurements show lower cost and latency for GLM-5.3, while Kimi retains multimodal input and a preserved-reasoning contract. The route therefore uses full GLM-5.3 for quality-first text-only long-horizon work and Kimi for multimodal preserved-reasoning work.

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

Meta documents Muse Spark 1.2 with Muse Code as its co-designed harness. The model supports multimodal and long-horizon coding work. The routing skill treats harness quality and provider data terms as route constraints.

- [Introducing Muse Code and Muse Spark 1.2](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2)
- [Build with Muse Code](https://developer.meta.com/ai/resources/blog/build-with-muse-code)

## Benchmark interpretation

Independent leaderboards helped identify task-specific strengths. They did not provide a stable overall order.

- [Artificial Analysis Long Context Reasoning](https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning) tests synthesis across long documents.
- [Artificial Analysis Terminal-Bench v2.1](https://artificialanalysis.ai/evaluations/terminalbench-v2-1) tests agentic terminal work.
- [Artificial Analysis Omniscience](https://artificialanalysis.ai/evaluations/omniscience) measures knowledge and hallucination behavior.
- [CursorBench](https://cursor.com/cursorbench) measures coding-agent behavior inside a specific harness.
- [Lech Mazur writing benchmark](https://github.com/lechmazur/writing) uses pairwise judgments over constrained creative writing.

These evaluations use different prompts, tools, judges, contexts, and effort settings. A model can lead one evaluation and trail another. The skill therefore avoids fixed scores and benchmark numbers.

## Repository structure

The category structure follows Matt Pocock's repository pattern. It uses plain skill names inside broad task categories. It also separates user-invoked flows from model-invoked disciplines.

- [Matt Pocock skills repository](https://github.com/mattpocock/skills)
- [Matt Pocock repository agent rules](https://github.com/mattpocock/skills/blob/main/AGENTS.md)

This repository uses `engineering`, `productivity`, and `solo` categories. Product-specific Solo names keep their `solo-` scope. General skills do not use an author prefix.
