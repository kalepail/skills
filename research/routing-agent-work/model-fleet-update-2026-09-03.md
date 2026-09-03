# Routing Agent Fleet Model Update Review

Evidence collected on 2026-09-03.

## Decision summary

Make these changes now.

1. Replace every Fable 5 route with Fable 5.1.
2. Promote Muse Spark 1.3 and exclude every Muse Spark 1.2 route.
3. Put Opus 5 before GPT-5.6 Sol for difficult implementation.
4. Split general multimodal work from Kimi's preserved-reasoning use case.
5. Start Luna at High effort for cost-sensitive extraction.

Keep the other fixed-fleet models for their current specialist roles.

Evaluate Gemini 3.8 Flash before any fleet addition.

## High-confidence findings

### Replace Fable 5 with Fable 5.1

Anthropic now marks Fable 5 as legacy. It recommends Fable 5.1 for improved performance. [Source](https://platform.claude.com/docs/en/models/fable-5/overview)

Fable 5.1 keeps a 1M context window and a 128K output limit.
Its base price stays at $10 input and $50 output per million tokens.
Cache reads now cost $0.25 per million tokens. [Source](https://platform.claude.com/docs/en/models/fable-5-1/overview)

The current Terminal-Bench 4.0 leaderboard gives Fable 5.1 a 57.9% resolution rate.
Fable 5 has 44.5%, and the confidence intervals do not overlap. [Source](https://www.tbench.ai)

CursorBench gives Fable 5.1 Max a 73.4% score at $9.64 per task.
Fable 5 Max has 70.5% at $17.32 per task. [Source](https://cursor.com/cursorbench)

Artificial Analysis gives Fable 5.1 Max an Intelligence Index score of 66.
It gives Opus 5 Max 63, Fable 5 Max 62, and Sol Max 61. [Source](https://artificialanalysis.ai/articles/claude-fable-5-1)

The replacement needs three warnings.
Forced tool use returns an error.
Earlier Claude models cannot read Fable 5.1 thinking blocks.
Editing earlier turns invalidates those thinking blocks. [Source](https://platform.claude.com/docs/en/models/fable-5-1/overview)

### Promote Muse Spark 1.3

Meta released Muse Spark 1.3 on 2026-09-02.
Meta now serves it through Muse Code and the Meta Model API. [Source](https://research.meta.ai/blog/introducing-muse-spark-1-3)

Artificial Analysis gives Muse Spark 1.3 xhigh an Intelligence Index score of 61.
Muse Spark 1.2 xhigh scores 57.
The new score matches Sol Max and Grok 4.6 High. [Source](https://artificialanalysis.ai/articles/muse-spark-1-3)

Muse Spark 1.3 xhigh costs $0.55 per Intelligence Index task.
Sol Max costs $0.95, and Grok 4.6 High costs $0.94. [Source](https://artificialanalysis.ai/articles/muse-spark-1-3)

The model accepts text, images, and video.
It retains a 1M context window.
Its price remains $1.25 input and $4.25 output per million tokens. [Source](https://artificialanalysis.ai/articles/muse-spark-1-3)

OpenRouter exposes `meta/muse-spark-1.3` with one provider.
Its current P50 values show 86 tokens per second and 3.90-second latency.
The same page shows 99.98% uptime but 90.16% availability over three days. [Source](https://openrouter.ai/meta/muse-spark-1.3)

These OpenRouter values change with traffic and provider health.
Treat them as operational signals, not durable specifications.

### Reorder difficult implementation

Artificial Analysis Coding Agent Index v1.4 gives Opus 5 xhigh a score of 68.
GPT-5.6 Sol Max scores 65. [Source](https://artificialanalysis.ai/agents/coding-agents)

The index covers 326 tasks across three benchmark families.
It gives equal weight to DeepSWE, Terminal-Bench 2.1, and SWE-Atlas-QnA.
Each task gets three attempts. [Source](https://artificialanalysis.ai/methodology/coding-agents-benchmarking)

Terminal-Bench 4.0 gives Opus 5 Max a 51.8% resolution rate.
Sol Max has 37.3%, with no confidence-interval overlap. [Source](https://www.tbench.ai)

CursorBench gives Opus 5 Max a 70.0% score.
Sol Max has 67.2%. [Source](https://cursor.com/cursorbench)

Anthropic also describes Opus 5 as the model for complex agentic coding.
It costs half as much per token as Fable 5.1.
It has moderate latency, while Fable 5.1 has slower latency. [Source](https://platform.claude.com/docs/en/models/opus-5/overview)

Use Opus 5 first for difficult implementation.
Keep Sol as the efficient different-family fallback.
Keep Fable 5.1 for the highest failure cost and longest work.

### Split the multimodal route

The current route combines preserved reasoning with general multimodal work.
These needs now point to different models.

Keep Kimi K3 first when the harness preserves its complete reasoning history.
Kimi warns that missing history can make output quality unstable. [Source](https://www.kimi.com/blog/kimi-k3)

Use Muse Spark 1.3 first for general multimodal agentic work.
It scores 61 at $0.55 per task on the Intelligence Index.
Kimi K3 scores 60 at $0.84 per task. [Muse source](https://artificialanalysis.ai/articles/muse-spark-1-3) [Kimi source](https://artificialanalysis.ai/models/kimi-k3)

Keep GLM-5.3 first for difficult text-only long-context work.
It has a 1M context window but no image input. [Source](https://artificialanalysis.ai/models/glm-5-3)

Keep GLM-5.3 Flash first for low-cost multimodal automation.
It scores 57 at $0.09 per Intelligence Index task. [Source](https://artificialanalysis.ai/models/glm-5-3-flash)

## Recommended fleet changes

### Direct changes

- Change `Fable 5` to `Fable 5.1` in every route and reviewer list.
- Use only `Muse Spark 1.3` in general and visual multimodal routes.
- Prefer contributor routes after explicit data-term acceptance.
- Try `meta/muse-spark-1.3-contributor` first.
- Use `openrouter/meta/muse-spark-1.3-contributor` after the direct route fails.
- Use the OpenCode free contributor route before the full 1.3 routes.
- Add the Muse Spark 1.3 provider-access warning.

### Route changes

Use this order for difficult implementation:

1. Claude with Opus 5.
2. Codex with GPT-5.6 Sol.
3. Claude with Fable 5.1 for the highest failure cost.

Keep Fable 5.1 first for difficult planning and synthesis.
Use Opus 5 first when cost or latency matters.

Split the current Kimi route into two routes:

- Preserved-reasoning multimodal sessions: Kimi K3 first.
- General multimodal long-context work: Muse Spark 1.3 first.

For cost-sensitive multimodal work, keep GLM-5.3 Flash first.
Put Muse Spark 1.3 before Grok 4.6.
Normal route verification checks contributor identifiers before full 1.3 identifiers.

### Keep, but clarify

Keep GPT-5.6 Sol for efficient difficult coding and independent review.
The current coding index gap from Opus 5 is only three points. [Source](https://artificialanalysis.ai/agents/coding-agents)

Keep Grok 4.6 for independent challenge work.
CursorBench shows 70.8% at $2.81 per task for xhigh.
Terminal-Bench 4.0 shows only 20.3% for High. [Cursor](https://cursor.com/cursorbench) [Terminal](https://www.tbench.ai)

Keep GLM-5.3 for text-only long-horizon work.
Its Terminal-Bench 4.0 score is 41.8%, versus Sol's 37.3%.
Their confidence intervals overlap. [Source](https://www.tbench.ai)

Keep Terra for bounded Codex work.
Do not describe it as the universal cost leader.
Artificial Analysis found Sol and Luna on the cost-quality frontier instead. [Source](https://artificialanalysis.ai/articles/gpt-5-6-has-landed)

Keep Luna for narrow, cheap work.
CursorBench shows High at 56.8% and $0.16 per task.
Xhigh reaches 57.7% at $0.23 per task.
Max reaches 61.1% at $0.39 per task. [Source](https://cursor.com/cursorbench)

Prefer Luna High when cost controls the decision.
Use Xhigh or Max only when a local extraction test shows a material gain.

## Addition candidate

Gemini 3.8 Flash is a strong evaluation candidate.
Google released it as a production model on 2026-09-02.
It supports a 1M context window and 64K output.
It accepts text, images, audio, and video. [Source](https://ai.google.dev/gemini-api/docs/latest-model)

Artificial Analysis gives its High mode a score of 59 at $0.58 per task.
It reports about 300 output tokens per second. [Source](https://artificialanalysis.ai/articles/gemini-3-8-flash)

Its Terminal-Bench 4.0 score is only 19.1% with mini-SWE-agent. [Source](https://www.tbench.ai)

Do not add it as a difficult coding route yet.
Test it for low-latency multimodal extraction and tool workflows.

Its $0.75 input and $3.75 output prices expire after 2026-12-31.
Standard prices then become $1.50 input and $7.50 output. [Source](https://ai.google.dev/gemini-api/docs/latest-model)

Do not add Sonnet 5 for agentic coding now.
Terminal-Bench gives it 12.4%, and CursorBench gives it 61.5% at Max. [Terminal](https://www.tbench.ai) [Cursor](https://cursor.com/cursorbench)

## Local runtime evidence

The Claude CLI accepted the new Fable identifier.

```bash
claude -p "Reply with exactly: fable-5.1-ready" --model claude-fable-5-1 --effort medium --output-format text --tools ""
```

The command exited with status 0 and returned `fable-5.1-ready`.

OpenCode has working direct Meta credentials.

The direct Meta provider currently lists these Muse routes:

```text
meta/muse-spark-1.1
meta/muse-spark-1.2
meta/muse-spark-1.2-contributor
```

This command refreshed the local catalog before the provider check:

```bash
opencode models --refresh
```

After the refresh, the direct Meta list stayed unchanged.
The general catalog added OpenRouter 1.3 and OpenCode's free contributor route.
This result separates a stale cache from a missing direct Meta route.

The direct `meta/muse-spark-1.2` route completed an earlier live response.
The current routing policy excludes that version.

The direct `meta/muse-spark-1.3` route returned a provider server error.

OpenCode also resolved the new Muse model through OpenRouter.

```bash
opencode run --pure --model openrouter/meta/muse-spark-1.3 --variant xhigh "Reply with exactly: muse-1.3-ready"
```

The full OpenRouter route completed after the user confirmed the 18+ setting.
It returned the required marker with `xhigh` effort.
It also used the shell tool and returned the expected working directory.

The OpenRouter contributor route did not complete.
The account privacy policy blocks its paid model-training requirement.

After the user changed the privacy settings, the OpenRouter contributor route completed.
It passed both generation and shell-tool tests with `xhigh` effort.

The OpenCode free contributor route also passed both tests with `xhigh` effort.
The direct Meta contributor route returned a provider server error.

Prefer direct Meta access because the user has a Meta subscription.
Prefer the working OpenRouter contributor route while the direct contributor remains unavailable.
Use the OpenCode free contributor route as the next contributor fallback.
Use full 1.3 routes after every contributor route fails.
Do not use any Muse Spark 1.2 route.

## Evidence limits

- Benchmark results include the model and its agent harness.
- Cross-harness differences do not prove a pure model difference.
- Cursor warns that small score differences can be statistical noise. [Source](https://cursor.com/cursorbench)
- Fable 5.1 used server fallback for about 4% of measured output tokens. [Source](https://artificialanalysis.ai/articles/claude-fable-5-1)
- Muse Spark 1.3 lacks current CursorBench and Terminal-Bench 4.0 results.
- Muse Spark 1.3 Max remains a limited preview. [Source](https://artificialanalysis.ai/articles/muse-spark-1-3)
- The OpenRouter age and privacy gates are account-specific.
- The OpenRouter health values cover only the latest three days. [Source](https://openrouter.ai/meta/muse-spark-1.3)
- Vendor internal benchmarks remain weaker than benchmark-owner results.
- No local repository task set tested these proposed route changes.

## Parallel CLI commands

The investigation used `parallel-cli search` for discovery.
It used `parallel-cli extract` for full source capture.

Representative discovery commands:

```bash
parallel-cli search "Find current official model announcements and API specifications for the fixed fleet." -q "Fable 5.1" -q "Muse Spark 1.3" --json --max-results 20 -o /tmp/fleet-official-a.json

parallel-cli search "Find current independent benchmark results for agentic coding models as of September 2026." -q "Terminal Bench 4.0" -q "CursorBench 3.2" -q "SWE-rebench" --json --max-results 30 -o /tmp/agentic-coding-benchmarks.json

parallel-cli search "Find the current Artificial Analysis Coding Agent Index v1.4 leaderboard." -q "Opus 5 xhigh GPT-5.6 Sol max" --json --max-results 20 -o /tmp/aa-coding-agent-v14.json
```

Representative extraction commands:

```bash
parallel-cli extract "https://cursor.com/cursorbench" "https://www.tbench.ai" "https://swe-rebench.com/" --objective "Extract current leaderboard results, harnesses, effort, cost, and methodology." --json --full-content -o /tmp/benchmark-owner-extract.json

parallel-cli extract "https://www.anthropic.com/claude-fable-and-mythos-5-1" "https://platform.claude.com/docs/en/models/fable-5-1/overview" "https://platform.claude.com/docs/en/models/opus-5/overview" --objective "Extract routing facts and benchmark comparisons." --json --full-content -o /tmp/anthropic-current-extract.json

parallel-cli extract "https://research.meta.ai/blog/introducing-muse-spark-1-3" "https://artificialanalysis.ai/articles/muse-spark-1-3" "https://openrouter.ai/meta/muse-spark-1.3" --objective "Extract Muse Spark 1.3 routing, cost, performance, and availability facts." --json --full-content -o /tmp/muse-current-extract.json
```

The complete saved result files remain under `/tmp`.

## Sources

- [Claude Fable 5 overview](https://platform.claude.com/docs/en/models/fable-5/overview)
- [Claude Fable 5.1 overview](https://platform.claude.com/docs/en/models/fable-5-1/overview)
- [Claude Opus 5 overview](https://platform.claude.com/docs/en/models/opus-5/overview)
- [Muse Spark 1.3 announcement](https://research.meta.ai/blog/introducing-muse-spark-1-3)
- [Gemini 3.8 Flash guide](https://ai.google.dev/gemini-api/docs/latest-model)
- [Kimi K3 technical blog](https://www.kimi.com/blog/kimi-k3)
- [Terminal-Bench 4.0](https://www.tbench.ai)
- [CursorBench 3.2](https://cursor.com/cursorbench)
- [Coding Agent Index](https://artificialanalysis.ai/agents/coding-agents)
- [Coding Agent Index methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking)
- [Fable 5.1 analysis](https://artificialanalysis.ai/articles/claude-fable-5-1)
- [Muse Spark 1.3 analysis](https://artificialanalysis.ai/articles/muse-spark-1-3)
- [Gemini 3.8 Flash analysis](https://artificialanalysis.ai/articles/gemini-3-8-flash)
- [GPT-5.6 analysis](https://artificialanalysis.ai/articles/gpt-5-6-has-landed)
- [GLM-5.3 analysis](https://artificialanalysis.ai/models/glm-5-3)
- [GLM-5.3 Flash analysis](https://artificialanalysis.ai/models/glm-5-3-flash)
- [Kimi K3 analysis](https://artificialanalysis.ai/models/kimi-k3)
- [OpenRouter Muse Spark 1.3](https://openrouter.ai/meta/muse-spark-1.3)
