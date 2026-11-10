# Fleet update: Fable 5.2, Gemini 4 Carbon, and Muse Ember

Update date: 2026-11-10.
Repository baseline: `0e3b7fb`.

## Recommendation

- Add Claude Fable 5.2 (`claude-fable-5-2`) at `high` or `xhigh` as the Claude escalation above Opus 5.5 at `xhigh`. It replaces Opus 5.5 at `max` as the escalation step, and it replaces Fable 5.1.
- Keep Opus 5.5 at `high` as the Claude default. Anthropic still recommends it as the daily driver, Fable 5.2 is capped at half of the Claude weekly limit, and Opus 5.5 leads the Artificial Analysis Coding Agent Index.
- Replace Gemini 4 Argon with Gemini 4 Carbon in every row. Carbon scores higher on every composite and terminal board, at a lower cost per task.
- Replace Muse Spark 1.3 with Muse Ember. Add Ember to the bounded, budget, and extraction rows ahead of DeepSeek V4.1 Flash, and in place of GLM-5.3 Flash. Keep GLM-5.3 Flash for the open-weight rows.
- Move Claude Mythos 5.2 into the outside-the-fleet list. It is limited to Anthropic's approved security and life-sciences programs.

The user asked about "Gemini Falcon 4". No such model exists. The new Gemini model is Gemini 4 Carbon.

## What changed since 2026-11-03

| Date | Event | Source |
|---|---|---|
| 2026-10-28 | Google announced Gemini 4 Carbon. Access was limited to vetted cyber defenders | [Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) |
| 2026-10-27 | Artificial Analysis Intelligence Index v5 replaced v4. Scores do not compare across versions | [the-decoder](https://the-decoder.com/claude-fable-5-2-and-mythos-5-2-cement-anthropics-ai-lead-just-before-its-ipo/), [DeepLearning.AI](https://www.deeplearning.ai/the-batch/gemini-leads-the-pack-again) |
| 2026-11-09 | Anthropic released Fable 5.2 and Mythos 5.2 at $8 / $40 per million tokens, down from $10 / $50 | [Anthropic](https://www.anthropic.com/claude-fable-and-mythos-5-2), [VentureBeat](https://venturebeat.com/technology/anthropic-releases-claude-fable-5-2-and-mythos-5-2-pairing-new-record-high-benchmarks-with-20-api-cost-reduction) |
| 2026-11-09 | Meta released Muse Ember at $0.10 / $0.50 per million tokens | [Meta](https://research.meta.ai/blog/muse-ember), [OpenRouter](https://openrouter.ai/meta/muse-ember) |
| 2026-11-10 | Gemini 4 Carbon became generally available on the paid Gemini API as `gemini-4-carbon`. Its introductory price is $2 / $10, and the standard price is $4 / $20 | [Gemini API changelog](https://aistudio.google.com/docs/changelog), [Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available) |

Other releases in this window were not language-model fleet candidates: Gemini Omni 1.2 Flash, GPT Image 2.6, and Ripple-65B. Inkling 2 Small scores 12.63% on Vals Terminal-Bench 4.0 and stays out. [ArtificialWatch](https://artificialwatch.com/releases/2026-11)

Fable 5.2 on subscriptions: it shares the Claude weekly limit and can use at most half of it, as Fable 5.1 could. Claude Code defaults it to `medium`. It supports `low` through `max`. Opus 5.5 API pricing did not change. [Claude support](https://support.claude.com/en/articles/17506494-claude-fable-5-2-launch-offers), [Claude Code model config](https://code.claude.com/docs/en/model-config)

## Independent measurements

Boards were read on 2026-11-10.

### Artificial Analysis Intelligence Index v5.0.1

| Model and effort | Index | USD per task |
|---|---:|---:|
| Fable 5.2 `max` | 65 | $26.54 |
| Fable 5.2 `xhigh` | 62 | $14.83 |
| Fable 5.2 `high` | 62 | $9.08 |
| Gemini 4 Carbon `high` | 60 | $7.76 |
| Opus 5.5 `max` | 59 | $10.04 |
| Gemini 4 Carbon `medium` | 58 | $6.59 |
| Opus 5.5 `xhigh` | 57 | $6.05 |
| GPT-6 Astra `max` | 57 | $6.24 |
| Fable 5.2 `medium` | 56 | $3.80 |
| GPT-6.1 Sol `max` | 55 | $1.27 |
| Sonnet 5.5 `max` | 55 | $10.02 |
| Opus 5.5 `high` | 52 | $3.46 |
| Gemini 4 Argon `high` | 50 | $9.95 |
| GPT-6.1 Sol `high` | 50 | $0.59 |
| Kimi K3.1 Pro | 46 | $3.68 |
| Haiku 5.5 `max` | 36 | $0.41 |
| Muse Ember `max` | 36 | $0.14 |
| Muse Ember `xhigh` | 34 | $0.12 |
| DeepSeek V4.1 Flash 1017 `max` | 33 | $0.60 |
| GLM-5.3 `max` | 32 | $5.01 |
| GPT-6 Luna `max` | 28 | $0.15 |
| GLM-5.3 Flash | 28 | $0.58 |

Source: [Artificial Analysis leaderboard](https://artificialanalysis.ai/leaderboards/models).
Fable 5.2 leads 5 of the 9 component evaluations, including HLE-Diamond (80%) and Terminal-Bench-Science (73%). On the Artificial Analysis Terminal-Bench 4.0 run, it scores 60%, which ties Opus 5.5. Kimi K3.1 Pro scores 67%, Carbon 65%, and Sonnet 5.5 64%. [the-decoder](https://the-decoder.com/claude-fable-5-2-and-mythos-5-2-cement-anthropics-ai-lead-just-before-its-ipo/)
On the Coding Agent Index v2.0, Opus 5.5 in Claude Code scores 62 and Carbon in Antigravity scores 59. Fable 5.2 has no row yet. [DeepLearning.AI](https://www.deeplearning.ai/the-batch/gemini-leads-the-pack-again), [kie.ai](https://kie.ai/blog/gemini-4-carbon-vs-claude-opus-5-5)

### Vals Index (2026-11-09)

| Model | Accuracy | USD per test |
|---|---:|---:|
| Fable 5.2 | 71.31% | $17.94 |
| Sonnet 5.5 | 70.85% | $16.18 |
| Gemini 4 Carbon | 70.45% | $10.51 |
| Opus 5.5 | 70.14% | $24.77 |
| Gemini 4 Argon | 69.39% | $13.37 |
| GPT-6 Astra | 65.02% | $21.28 |
| Muse Wonder 1.0 | 64.88% | $10.65 |
| GPT-6.1 Sol | 63.94% | $3.61 |
| Kimi K3.1 Pro | 62.52% | $6.44 |
| DeepSeek V4.1 Flash 1017 | 61.26% | $0.66 |
| GPT-6.1 Terra | 60.54% | $2.94 |
| Muse Ember | 60.48% | $0.15 |
| GLM-5.3 | 59.85% | $8.52 |
| Haiku 5.5 | 58.73% | $3.17 |
| Grok 4.7 | 58.62% | $11.63 |
| MiMo V2.6 Pro | 57.81% | $0.43 |
| GPT-6 Luna | 52.32% | $0.45 |
| GLM-5.3 Flash | 50.86% | $2.05 |

Source: [Vals Index](https://www.vals.ai/benchmarks/vals_index).

### Vals Terminal-Bench 4.0 (Mini-SWE-agent)

| Model | Score | USD per test |
|---|---:|---:|
| Fable 5.2 | 65.15% | $14.56 |
| Opus 5.5 | 65.15% | $12.04 |
| Sonnet 5.5 | 64.14% | $10.75 |
| Kimi K3.1 Pro | 63.64% | $4.57 |
| Gemini 4 Carbon | 63.13% | $7.45 |
| GPT-6 Astra | 59.60% | $9.58 |
| Gemini 4 Argon | 57.58% | $17.64 |
| GPT-6.1 Sol | 55.05% | $1.72 |
| Muse Wonder 1.0 | 49.49% | $14.66 |
| Muse Ember | 39.39% | $0.22 |
| GLM-5.3 | 38.89% | $9.37 |
| GLM-5.3 Flash | 37.37% | $1.22 |
| GPT-6 Luna | 13.64% | $0.35 |
| Inkling 2 Small | 12.63% | $8.22 |

Source: [Vals Terminal-Bench 4.0](https://www.vals.ai/benchmarks/terminal-bench-4). DeepSeek V4.1 Flash 1017 scores 31.8% on the Vals Index's Terminal-Bench column.

### Other independent signals

- LMArena text: Carbon is first (1528, preliminary) and Argon is second (1520). Opus 5.5 is third, and Fable 5.2 has no row yet. A secondary report puts Argon first and Opus 5.5 second on creative writing. [LMArena](https://lmarena.ai/leaderboard/text), [aimodelrace](https://aimodelrace.com/news/2026-11-06-writing-creative-gemini-4-argon-takes-1/)
- LMArena agent board: Opus 5.5 `max` is first (20.14%) and Carbon `high` is second (16.72%) at $1.65 per task. [LMArena](https://lmarena.ai/leaderboard)
- ARC-AGI: Fable 5.2 at `xhigh` beats `max` on v1, v2, and v3. [ARC Prize](https://arcprize.org/results/anthropic-claude-fable-5-2)
- Epoch ECI: Fable 5.2 scores 174 and Astra scores 169, from Epoch's pre-launch testing. [FourWeekMBA summary](https://fourweekmba.com/ai-epoch-claude-fable-5-2-sets-eci-record-at-174-astra-at-169/)
- AA-3D: Fable 5.2 `max` scores 1271 Elo. Sonnet 5.5 scores 1204 and Opus 5.5 scores 1202. [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2119953570430881946)
- Some domain boards moved down. On DualEntry's accounting benchmark, Fable 5.2 scores 81.2%, below Fable 5.1 at 85.1%. Plotly gave Fable 5.2 a perfect score at $35.74 per run, and GPT-6.1 Sol got the same score at $2.61. [DualEntry](https://www.dualentry.com/blog/claude-fable-5-2-scored-lower-than-fable-5-1), [Plotly](https://plotly.com/blog/claude-fable-5-2-plotly-data-analytics-bench/)

Vendor claims (Anthropic): FrontierCode 2.0 49.1% at `xhigh`, compared with Opus 5.5 at 45.5%. At `high`, Fable 5.2 roughly matches Opus 5.5's best score for about half the cost per task.

## Consensus

- **Fable 5.2** is the strongest general model on every composite board (AA, Vals Index, Epoch ECI). It ties Opus 5.5 on Vals Terminal-Bench and trails Kimi K3.1 Pro and Carbon on the AA terminal run. Anthropic and early reviewers keep Opus 5.5 as the daily driver and use Fable 5.2 for the hardest open-ended work. At `high`, Fable 5.2 beats Opus 5.5 at `max` on the AA index at a lower cost per task. That makes it the right escalation above Opus 5.5 at `xhigh`. Use `high` or `xhigh`: `max` gains 3 AA points at 1.8 times the cost, and it loses to `xhigh` on ARC-AGI.
- **Gemini 4 Carbon** beats Argon on the AA index (60 vs 50), the Vals Index (70.45 vs 69.39), and Vals Terminal-Bench (63.13 vs 57.58). Its cost per task is lower on all three. Every Argon role moves to Carbon. Carbon trails Opus 5.5 on the AA Coding Agent Index and on Vals Terminal-Bench.
- **Muse Ember** has the lowest cost per task on both Vals boards. It beats GLM-5.3 Flash on all three boards, and GPT-6 Luna and DeepSeek V4.1 Flash on Vals Terminal-Bench and the AA index. It roughly ties DeepSeek V4.1 Flash on the Vals Index and Haiku 5.5 on the AA index. It has closed weights, so GLM-5.3 Flash and DeepSeek V4.1 Flash keep the open-weight rows.

## Route checks

The local OpenCode catalog cache predated Carbon and Ember. It was refreshed from `models.dev/api.json`, with a backup kept in the session scratchpad. OpenRouter's live endpoint list shows zero-retention Google Vertex endpoints for both `google/gemini-4-carbon` and `meta/muse-ember`. The Cloudflare AI Gateway Carbon route was not listed. Its Ember route is a Muse route, which the fleet already excludes.

One tool-using probe ran on each new route. The task: read a CSV, sum a column, write `sum.txt`, and reply `DONE <sum>` ([brief](evidence/fleet-2026-11-10/probe-brief.md)).

| Route | Status | Seconds | Result |
|---|---|---:|---|
| `openrouter/google/gemini-4-carbon#high`, pinned `google-vertex`, ZDR | complete | 22.0 | `sum.txt` = 23 |
| `openrouter/meta/muse-ember#high`, pinned `google-vertex`, ZDR | complete | 11.4 | `sum.txt` = 23 |
| Claude `claude-fable-5-2 --effort high` | complete | 4.9 | `sum.txt` = 23, $0.70 |

## Validation

A clean Codex GPT-6.1 Sol `high` session read the updated skill and answered 10 eval scenarios: 3, 11, 13, 52, 62, 71, 78, 79, 80, and 81 ([brief](evidence/fleet-2026-11-10/validation-brief.md), [answers](evidence/fleet-2026-11-10/validation-answers-gpt-6.1-sol.md)). All answers match the routes the skill states. Scenario 80 asks for Gemini 4 Argon by name. It returned `Unrouted` and named Carbon as the fleet route, which follows the skill's rule for a pinned model outside the fleet. The eval now expects that answer.

Limits: the boards are less than two days old for Fable 5.2 and Carbon. LMArena category rows and the AA Coding Agent Index row for Fable 5.2 are not yet published. Re-check those rows at the next review.
