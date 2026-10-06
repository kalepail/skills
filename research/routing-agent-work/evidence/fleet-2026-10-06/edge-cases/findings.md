# Edge-case review by open challenger models

Three OpenCode models reviewed the draft routing policy for contradictions, ambiguities, gaps, and unsafe rules.
Each received only the policy text and the instruction in [prompt.md](prompt.md).
The lead checked every finding against the policy text before any edit.

| Model and route | Effort | Result | Wall time |
|---|---|---|---|
| Kimi K3 (`moonshotai/kimi-k3`) | `max` | 10 findings; 10 confirmed | 313 s |
| Muse Spark 1.3 (`openrouter/meta/muse-spark-1.3`) | `max` | 10 findings; 3 new and confirmed, 6 repeat Kimi findings, 1 already covered | 159 s |
| GLM-5.3 (`openrouter/z-ai/glm-5.3`) | `max` | Empty final message, exit code 0, no findings | 193 s |
| GLM-5.3 (`openrouter/z-ai/glm-5.3`) | `high` | 8 findings, the last one cut off mid-text; 8 confirmed | 422 s |

Raw event streams: `kimi-k3.jsonl`, `muse-1.3.jsonl`, `glm-5.3-max-empty.jsonl`, `glm-5.3-high.jsonl`.

## Harness events

- The first attempt ran all three models at once. It hung for 1h44m with no output, and the lead stopped it.
- A second parallel attempt failed at start for two models with `database is locked`.
- The direct `meta/muse-spark-1.3` route returns HTTP 402 for this account. The OpenRouter route works.
- GLM-5.3 at `max` produced an empty result. The capability probes saw the same failure once.

## Confirmed findings and fixes

| Finding | Source | Fix |
|---|---|---|
| "Use `max` when the caller requires one worker" forced `max` on trivial lanes | Kimi, Muse | The one-worker limit now only rules out `ultra` |
| "Keep other models at `medium` or above" named no models and conflicted with `low` fallbacks | Kimi, Muse | Per-model ranges govern; `low` is allowed for trivial work or under a stated cost limit |
| Lane rows had no effort, and the CLI default conflicted with the effort levels | Kimi, Muse | Effort comes from the lane; a lane-row effort wins |
| `high` and `xhigh` both named synthesis | Kimi | Routine synthesis uses `high`; multi-source synthesis uses `xhigh` |
| A pinned CLI whose default does not fit the lane, for example Grok for coding, had no outcome | Kimi, Muse | The default applies only when its clues fit; otherwise the lane is `Unrouted` |
| Grok 4.7 was both a capable reviewer and a weaker model whose findings are leads | Kimi, Muse | Grok 4.7 is an extra challenger only |
| The edge-case row listed three models with no order | Kimi | Order: Muse Spark 1.3, GLM-5.3 for text-only input, Kimi K3 |
| A difficult lane under a cost limit had no route | Kimi | GPT-6.1 Sol at `high` or `xhigh`, then Sonnet 5.5 at `high`, with a stop budget |
| No check existed for Kimi's preserved-history requirement | Kimi, Muse | Confirm harness properties through host documentation or the caller; otherwise skip the route |
| A safeguard handoff to Opus 4.8 had no defined result | Kimi | Treat it as an unavailable route and use the next fallback |
| Sonnet 5.5 at `xhigh` as a fallback conflicted with its row note | Muse | The note now allows it above `high` only when Opus 5.5 is unavailable |
| Muse provider order versus model fallback had no precedence | Muse | Try each listed provider before the next model fallback |
| Contributor-term acceptance had no record | Muse | The lane contract must state acceptance; otherwise the terms are not accepted |
| A lane owned by a leads-only model had no acceptance rule | GLM | Accept its result only after the lane's completion check passes |
| Target and action limits bound only the Daybreak row | GLM | Security lanes keep those limits on every route and fallback |
| A pinned CLI plus a cost limit on difficult work had no order | GLM | Use the first route in the cost-limit chain on that CLI |
| GLM-5.3 Flash had no effort in two rows | GLM | `max` for bounded coding, `high` for extraction |
| No reviewer remained when the Claude family was down | GLM | Mark the review lane `Unrouted`; never promote a challenger |
| Privacy limits had no route property | GLM | The fleet names the open-weight models and states that the provider still receives the input |
| "The bounded rows" had no definition | GLM | The fleet names the three bounded rows |
| A pinned CLI with a lane row that has no route on that CLI had no outcome | GLM | Use a fitting route on that CLI, otherwise `Unrouted` |

Muse also proposed removing Opus 5.5 from the security row.
The row already limits Opus 5.5 to defensive review of the caller's own code, and the new safeguard-handoff rule covers the rest.
