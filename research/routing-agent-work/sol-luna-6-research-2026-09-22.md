# GPT-6 Sol and Luna: routing evidence

Research date: 2026-09-22.

This report separates provider claims, independent benchmark results, local availability, and routing judgment.
No model benchmark calls ran during this research.

## Recommendation

Keep Astra High as the preferred Codex route.
Replace general GPT-5.6 Sol and Luna routes with their GPT-6 counterparts.
Use Sol before Terra when a Codex task needs more capability than Luna.

This placement is a routing judgment.
Sol has Terra's input price, a lower output price, and stronger published aggregate results.
Actual task cost still depends on token use and corrections.

Keep other providers in their existing order.
This research does not establish a controlled Sol-versus-Grok comparison for the repository's coding tasks.

## Published model facts

| Model | API input | Cached input | Output | API context | Maximum output |
| --- | ---: | ---: | ---: | ---: | ---: |
| GPT-6 Astra | $10 | $1 | $50 | 1,050,000 | 128,000 |
| GPT-6 Sol | $2 | $0.20 | $10 | 1,050,000 | 128,000 |
| GPT-5.6 Sol | $4 | $0.40 | $20 | 1,050,000 | 128,000 |
| GPT-5.6 Terra | $2 | $0.20 | $12 | 1,050,000 | 128,000 |
| GPT-6 Luna | $0.10 | $0.01 | $0.50 | 1,050,000 | 128,000 |
| GPT-5.6 Luna | $0.20 | $0.02 | $1.20 | 1,050,000 | 128,000 |

Context and output limits come from each model page.
See [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [Sol](https://developers.openai.com/api/docs/models/gpt-6-sol), and [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna).
See also [previous Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra), and [previous Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna).

Prices cover one million tokens under Standard processing, with at most 272K input tokens.
Longer requests cost twice the input rates and 1.5 times the output rates.
The higher rates apply to the full request.
Cache writes cost 1.25 times the input rate.
These prices exclude tool fees. [OpenAI pricing](https://developers.openai.com/api/docs/pricing)

Sol cuts both listed input and output prices by 50%.
Luna cuts input prices by 50% and output prices by approximately 58.3%.
These percentages compare token rates, not completed task costs. [OpenAI pricing](https://developers.openai.com/api/docs/pricing)

Both new models accept text and images and produce text.
Their API effort values are `none`, `low`, `medium`, `high`, `xhigh`, and `max`.
The API default is `medium`.
Their maximum input is 922,000 tokens.
Sol's knowledge cutoff is April 20, 2026.
Luna's cutoff is May 18, 2026. [Sol model](https://developers.openai.com/api/docs/models/gpt-6-sol), [Luna model](https://developers.openai.com/api/docs/models/gpt-6-luna)

Use Responses for reasoning with tools.
Chat Completions supports their function calls only with `reasoning_effort: "none"`.
Astra supports `low` through `max`, without `none`. [Sol model](https://developers.openai.com/api/docs/models/gpt-6-sol), [Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra)

## Codex availability and effort

OpenAI positions Sol for complex coding and agent workflows.
It positions Luna for focused coding, extraction, summarization, and repeated tasks.
Astra remains its most capable option.
Availability depends on the account, client, workspace, and rollout. [Codex models](https://learn.chatgpt.com/docs/models)

Codex Ultra uses automatic delegation.
It is not an API reasoning value.
Luna supports Max but excludes Ultra. [Codex models](https://learn.chatgpt.com/docs/models)

The parent agent captured the local `codex debug models` catalog.
I inspected only approved metadata fields.

| Local model | Default effort | Available effort | Configured context |
| --- | --- | --- | ---: |
| `gpt-6-astra` | medium | low, medium, high, xhigh, max, ultra | 272000 |
| `gpt-6-sol` | medium | low, medium, high, xhigh, max, ultra | 272000 |
| `gpt-6-luna` | medium | low, medium, high, xhigh, max | 272000 |

This local catalog establishes configured availability, not successful task execution.
Its context value differs from the API maximum.
The catalog reports an effective context percentage of 95.
See [selected local metadata](evidence/sol-luna-6-2026-09-22/codex-model-metadata.json).

## OpenAI benchmark claims

OpenAI reports these results in its launch article:

| Evaluation | Model and effort | Reported result |
| --- | --- | --- |
| AutomationBench 1.0.6 | Sol xhigh | 33.2%; $0.27 per task |
| AutomationBench 1.0.6 | Astra low | 30.3%; 3.9 times Sol's task cost |
| Agents' Last Exam V1 | Sol max | 56.4% |
| DeepSWE 1.1 | Sol max | 68.8% |
| DeepSWE 1.1 | Luna max | 66.6% |
| OSWorld 2.0 offline | Sol xhigh | 60.5% |

OpenAI reports better FrontierCode results than GPT-5.6 Sol.
It reports roughly half as many Sol factual errors in its internal evaluation.
That evaluation uses conversations where users flagged previous errors.
It does not represent typical usage.

OpenAI ran GPT evaluations in its research environment or API.
It obtained competitor results from public reports.
These results do not prove universal improvement or identical production behavior.
Astra remains OpenAI's recommended model for its strongest results. [OpenAI launch report](https://openai.com/index/introducing-gpt-6-sol-and-luna/)

Cognition confirms that FrontierCode added both models on September 22.
Its benchmark grades correctness, test quality, scope, style, and repository standards.
Its fetched page did not expose numeric leaderboard rows. [FrontierCode](https://cognition.com/frontiercode)

DeepSWE's fetched leaderboard showed older model rows despite its September 22 update label.
Therefore, the new DeepSWE numbers above remain explicitly OpenAI-reported.
I did not treat the benchmark owner's missing rows as independent confirmation. [DeepSWE](https://deepswe.datacurve.ai/)

## Independent Artificial Analysis results

All rows use Intelligence Index v4.3.2.
The table preserves the displayed rounded values.

| Model | Effort | Index | USD per index task | Source |
| --- | --- | ---: | ---: | --- |
| GPT-6 Astra | max | 53 | $3.26 | [AA Astra](https://artificialanalysis.ai/models/gpt-6-astra) |
| GPT-6 Sol | max | 48 | $1.06 | [AA Sol](https://artificialanalysis.ai/models/gpt-6-sol) |
| GPT-5.6 Sol | max | 47 | $1.99 | [AA previous Sol](https://artificialanalysis.ai/models/gpt-5-6-sol) |
| GPT-6 Sol | xhigh | 44 | $0.53 | [AA Sol xhigh](https://artificialanalysis.ai/models/gpt-6-sol-xhigh) |
| GPT-6 Sol | high | 43 | $0.37 | [AA Sol high](https://artificialanalysis.ai/models/gpt-6-sol-high) |
| GPT-5.6 Terra | max | 42 | $1.40 | [AA Terra](https://artificialanalysis.ai/models/gpt-5-6-terra) |
| GPT-6 Luna | max | 37 | $0.07 | [AA Luna](https://artificialanalysis.ai/models/gpt-6-luna) |
| GPT-5.6 Luna | max | 37 | $0.18 | [AA previous Luna](https://artificialanalysis.ai/models/gpt-5-6-luna) |
| GPT-6 Luna | high | 32 | $0.03 | [AA Luna high](https://artificialanalysis.ai/models/gpt-6-luna-high) |

The index combines ten evaluations.
Its task cost is a weighted benchmark cost.
It is not the price of an arbitrary coding task.
Equal effort names do not imply equal compute budgets. [AA methodology context](https://artificialanalysis.ai/models/gpt-6-astra)

The results support a cost-efficiency improvement.
They do not show a rounded index increase for Luna.
Sol High exceeds Terra Max's rounded index at lower measured index cost.
That comparison supports the proposed budget placement.
It does not guarantee better results on every task.

AA reports no output-speed measurement for the new models.
Do not claim a measured speed advantage from these pages.
AA lists Sol's context as 872k.
OpenAI's model page lists 1,050,000 total tokens and 922,000 maximum input.
Use OpenAI's limits for API configuration.
The AA discrepancy remains unresolved. [AA Sol](https://artificialanalysis.ai/models/gpt-6-sol), [OpenAI Sol](https://developers.openai.com/api/docs/models/gpt-6-sol)

## Daybreak Blue

The current API alias remains `gpt-daybreak-blue-latest` → `gpt-5.6-sol`.
OpenAI's model page, pricing page, and cybersecurity guide independently agree.
Do not change this mapping when updating general Sol routes.
Daybreak requires the relevant account and project approval. [Daybreak Blue](https://developers.openai.com/api/docs/models/gpt-daybreak-blue-latest), [Cybersecurity guide](https://developers.openai.com/api/docs/guides/safety-checks/cybersecurity), [Pricing](https://developers.openai.com/api/docs/pricing)

## Evidence and limits

The [evidence directory](evidence/sol-luna-6-2026-09-22/) contains official model text and extracted AA text.
It also contains [parsed benchmark values](evidence/sol-luna-6-2026-09-22/benchmark-values.json) with source URLs and text hashes.
The [raw HTML manifest](evidence/sol-luna-6-2026-09-22/raw-html-manifest.json) records original hashes and external archive paths.
Large raw responses remain under `/tmp/sol-luna-6-research-2026-09-22-raw/`.
This temporary archive is not a durable repository artifact.

Search indexing lagged behind the direct pages.
Some web retrieval calls failed while ordinary HTTPS downloads succeeded.
The evidence preserves those distinctions.
No unverified search snippets support the numerical conclusions.

This report does not validate the repository's complete workload matrix.
It does not establish a new cross-provider fallback order.
The routing tests must check the updated IDs, effort limits, budget placement, and unchanged Daybreak exception.
