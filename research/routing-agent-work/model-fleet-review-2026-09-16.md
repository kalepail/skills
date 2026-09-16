# Model fleet review

Review date: 2026-09-16.
Repository baseline: `dea99fa`.

## Recommendation

Add GPT-6 Astra for the hardest Codex tasks.
Update Muse Spark 1.3 effort limits by provider.
Separate Codex `ultra` from ordinary reasoning effort.
Evaluate DeepSeek V4.1 Flash before adding another general worker.
Keep the existing models until task tests justify removal.

This review changes no shipped skill or model setting.
Catalog checks confirm listed capabilities, not successful inference or task quality.
No model generation tests ran during this review.

## Changes with strong evidence

### 1. Add GPT-6 Astra

The current fleet omits Astra from every route and reviewer list.
OpenAI recommends Astra for demanding reasoning, coding, research, computer use, and document creation.
It has a 1,050,000-token context window and a 128,000-token output limit.
Base API prices are $10 input and $50 output per million tokens.
[Source](https://developers.openai.com/api/docs/models/gpt-6-astra)

The local Codex catalog lists `gpt-6-astra`.
It exposes `medium`, `high`, `xhigh`, `max`, and `ultra`, plus `low`.
The skill's existing minimum excludes `low`.
The API documentation lists effort through `max`; it does not list `ultra`.
[API source](https://developers.openai.com/api/docs/models/gpt-6-astra)

Terminal-Bench 4.0 reports these results:

| Model and effort | Agent | Resolution rate | Reported run cost |
|---|---|---|---|
| GPT-6 Astra `max` | Codex | 58.2% ± 2.8% | $3.3k |
| Fable 5.1 `max` | Claude Code | 57.9% ± 3.8% | $6.2k |
| Opus 5 `max` | Claude Code | 51.8% ± 3.4% | $6.0k |
| GPT-5.6 Sol `max` | Codex | 37.3% ± 3.8% | $2.5k |

The intervals are 95% confidence intervals.
Costs cover the reported benchmark runs, not individual tasks.
[Source](https://www.tbench.ai)

Recommended route changes are an inference from these results and provider guidance:

- Use Astra first for difficult Codex implementation, debugging, verification, and computer use.
- Add Astra as a planning and synthesis alternative to Fable 5.1.
- Add Astra as a reviewer for work from other model families.
- Keep Sol for routine work and as a cheaper fallback.
- Keep Fable 5.1 and Opus 5 as independent alternatives.

Astra and Fable have overlapping intervals.
These results do not establish a universal winner between them.
Keep the distinction between model performance and agent implementation.

### 2. Update Muse effort by provider

The fleet limits Muse Spark 1.3 to `xhigh`.
Meta now states that `max` is available through Muse Code and Meta Model API.
[Source](https://research.meta.ai/blog/introducing-muse-spark-1-3)

The refreshed local OpenCode catalog shows:

| Identifier | Highest listed variant |
|---|---|
| `meta/muse-spark-1.3` | `max` |
| `meta/muse-spark-1.3-contributor` | `xhigh` |
| `openrouter/meta/muse-spark-1.3` | `max` |
| `openrouter/meta/muse-spark-1.3-contributor` | `max` |

The direct Meta 1.3 identifiers now appear in the catalog.
Their absence in the September 3 review is historical evidence.
This review did not repeat their generation or tool tests.

Recommend `medium` through `max`, subject to the selected provider's supported variants.
Keep contributor access conditional on accepted data terms.
If the task requires `max`, skip a contributor route that only exposes `xhigh`.
Do not silently lower the task requirement to preserve provider order.

### 3. Treat `ultra` as a host mode

The current skill groups `max` and `ultra` as effort choices.
The local Codex catalog describes `ultra` as automatic task delegation.
That distinction affects worker counts, cost, and the caller's control of delegation.

Recommend a separate rule for `ultra`:

- Use it only when the host and task permit automatic delegation.
- Prefer `max` when the caller needs one worker or a fixed delegation structure.
- Do not send `ultra` to an API that only supports effort through `max`.

The local Terra catalog also exposes `max` and `ultra`.
The fleet currently stops Terra at `xhigh`.
Distinguish a deliberate routing limit from a model capability limit.
Do not raise Terra's default merely because higher settings exist.

### 4. Refresh benchmark references

Cursor released CursorBench 4.0 on September 10.
The September 3 review used the previous task set.
Do not compare its scores directly with the new scores.
[Source](https://cursor.com/cursorbench)

Current examples show why effort and task cost need separate treatment:

| Model and effort | CursorBench 4.0 score | Cost per task |
|---|---|---|
| Fable 5.1 `xhigh` | 51.6% | $13.01 |
| Fable 5.1 `max` | 51.8% | $17.28 |
| Opus 5 `xhigh` | 46.1% | $11.43 |
| GPT-5.6 Sol `max` | 41.7% | $8.23 |
| Muse Spark 1.3 `max` | 41.6% | $2.64 |
| GPT-5.6 Terra `max` | 41.3% | $5.14 |
| GPT-5.6 Luna `high` | 29.4% | $0.25 |
| GPT-5.6 Luna `max` | 35.9% | $1.03 |

Cursor warns that small score differences can reflect variance.
Astra has no row in the captured CursorBench table.
These coding scores do not directly validate extraction or prose routes.
[Source](https://cursor.com/cursorbench)

## Candidates to evaluate

### DeepSeek V4.1 Flash: first priority

DeepSeek released V4.1 Flash on September 10.
It supports image and text input, tools, and a 1M context window.
The direct API identifier is `deepseek-flash`.
The local OpenCode catalog lists `openrouter/deepseek/deepseek-v4.1-flash`.
[Announcement](https://api-docs.deepseek.com/news/news260910/)
[Model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)

Direct API peak prices are $0.30 input and $1.20 output per million tokens.
Off-peak prices are $0.15 input and $0.60 output.
These prices do not establish OpenRouter billing.
[Pricing](https://api-docs.deepseek.com/quick_start/pricing)

Evaluate it against GLM-5.3 Flash, Luna, and Muse for bounded coding and image-based extraction.
Do not replace those routes from vendor benchmark claims alone.

Its model card describes numerical effort from 1 to 100.
The hosted API documents named effort values and mappings.
OpenCode currently exposes `low`, `high`, and `max` for the OpenRouter route.
Use the selected provider's controls; do not infer a numerical mapping.
[Model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)
[Hosted effort controls](https://api-docs.deepseek.com/guides/thinking_mode)

DeepSeek's release notice announced a V4 Pro retirement.
The current pricing page explicitly reverses that decision and keeps V4 Pro available.
Use the current pricing page for that availability claim.
The retired V4 Flash identifiers now route to V4.1 Flash on the direct API.
[Current pricing and compatibility notice](https://api-docs.deepseek.com/quick_start/pricing)

### Gemini 3.8 Flash: retain as an evaluation candidate

Google lists Gemini 3.8 Flash as generally available.
It supports text, images, audio, video, and PDF input.
It exposes `low`, `medium`, and `high` thinking levels.
[Model specification](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)

The local catalog lists `openrouter/google/gemini-3.8-flash` with those three variants.
Evaluate audio, video, PDF extraction, and latency-sensitive workflows through OpenCode.
This requires no return to Gemini CLI or Antigravity.

Introductory pricing ends on December 31, 2026.
Do not put a temporary price into permanent routing guidance.
[Source](https://ai.google.dev/gemini-api/docs/latest-model)

### Daybreak Blue: optional defensive security route

The local Codex catalog lists `gpt-daybreak-blue-latest`.
OpenAI describes it as an alias with safeguards calibrated for defensive cybersecurity.
It requires separate approval and provisioning.
The current model page maps it to GPT-5.6 Sol.
[Source](https://developers.openai.com/api/docs/models/gpt-daybreak-blue-latest)

Consider it for authorized security review and patch validation when account access works.
Do not treat it as a distinct model family for independent review.
Do not add Daybreak Red or Mythos merely because their names appear in provider materials.

### Qwen3.8: lower evaluation priority

Qwen describes Qwen3.8-Max as its strongest model for coding and extended tasks.
The local catalog lists `openrouter/qwen/qwen3.8-max-0902`.
[Official overview](https://qwen.ai/blog?id=qwen3.8)

The overview alone does not establish the September 2 variant's advantage over this fleet.
Keep it on the evaluation list until a concrete task requires it.

## Keep or drop

| Current model | Recommendation |
|---|---|
| Fable 5.1 | Keep for difficult planning and synthesis. |
| Opus 5 | Keep for coding, review, and prose. |
| GPT-5.6 Sol | Keep for routine Codex work; add Astra above it for the hardest tasks. |
| GPT-5.6 Terra | Keep for bounded work; measure its value before any removal. |
| GPT-5.6 Luna | Keep for narrow extraction; retain the current `high` starting policy. |
| Grok 4.6 | Keep as a different-family research and review option. |
| GLM-5.3 | Keep for text-only extended implementation. |
| GLM-5.3 Flash | Keep pending comparison with DeepSeek V4.1 Flash. |
| Kimi K3 | Keep its preserved-history specialist role. |
| Muse Spark 1.3 | Keep; update provider effort limits. |

These are routing recommendations, not claims of measured local superiority.
The reviewed provider sources still support the existing specialist distinctions.
[Claude](https://platform.claude.com/docs/en/models/overview)
[Grok](https://docs.x.ai/developers/models)
[GLM](https://docs.z.ai/guides/llm/glm-5.3)
[GLM Flash](https://docs.z.ai/guides/llm/glm-5.3-flash)
[Kimi](https://www.kimi.com/blog/kimi-k3)

No current fleet member has a verified retirement in this review.
Drop outdated claims before dropping useful models.
Exclude old Muse 1.2 and Fable 5 routes as the skill already does.
Do not add speculative GPT-6 Sol or an untested moving alias.

## Concrete skill update scope

Update `references/fleet.md`, the effort rules in `SKILL.md`, and `evals/evals.json` together.
Keep live discovery outside normal routing.
Add cases for Astra selection, provider-specific Muse effort, and prohibited automatic delegation.
Retain hard-negative cases for model research and unknown models.

Before promotion, run clean-session comparisons against the current skill.
Include an unavailable Astra route, a Muse `max` requirement, and a task that permits only one worker.
For new models, test a bounded code fix, structured extraction, and a visual task where supported.
Measure correctness, tool failures, elapsed time, and cost on the same tasks.
Catalog presence and a successful greeting do not establish task quality.

## Local evidence

Checked versions: Codex `0.154.0`, OpenCode `1.18.30`, Claude Code `2.1.273`.
`grok models` returned `grok-4.6` as the default and also listed `grok-4.5`.

Commands used:

```text
codex debug models
grok models
opencode models --pure --refresh
opencode models meta --pure --verbose
opencode models openrouter --pure --verbose
claude --help
grok --help
```

The OpenCode refresh updated its model cache.
No provider credentials, account settings, or default models changed.
OpenCode catalog metadata does not prove provider acceptance of a request.

Search and catalog captures remain temporary local audit artifacts.
The source links above preserve the review basis.
The [validation report](model-fleet-validation-2026-09-16.md) records the implemented decisions and durable evaluation evidence.
