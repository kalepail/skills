# Fleet update: GPT-6.1 Sol, Sonnet 5.5, and measured roles

Update date: 2026-10-06.
Repository baseline: `36f3dd2`.

## Recommendation

Make GPT-6.1 Sol at `high` the default Codex route.
Keep GPT-6 Astra as the Codex escalation route for the hardest and highest-stakes work.
Add Claude Sonnet 5.5 for fast, bounded Claude work at `low` to `high`.
Remove GPT-6 Sol and GPT-5.6 Terra from the fleet.
Remove Grok 4.7 from coding fallbacks.
Keep Grok 4.7 for independent challenge and live web and X research.
Give GLM-5.3, Kimi K3, and Muse Spark 1.3 an explicit confirmation and edge-case role.
Treat their findings as leads that a check must reproduce.
Keep Opus 5.5 as the default Claude route and the first route for planning, difficult implementation, review, and prose.

## What changed since 2026-09-22

| Date | Event | Source |
|---|---|---|
| 2026-09-28 | Anthropic released Claude Sonnet 5.5 (`claude-sonnet-5-5`), $2 / $10 per million tokens. | [Announcement](https://www.anthropic.com/claude-sonnet-5-5) |
| 2026-09-28 | OpenAI cancelled the GPT-6.1 Astra launch after internal safety tests. | [Reuters](https://www.reuters.com/business/openai-shelves-new-ai-model-after-internal-safety-tests-wsj-reports-2026-09-28/) |
| 2026-09-29 | OpenAI released GPT-6.1 Sol (`gpt-6.1-sol`), $2 / $10 per million tokens, $0.10 cached input. | [Announcement](https://openai.com/index/introducing-gpt-6-1-sol/), [model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol) |
| 2026-09-30 | Artificial Analysis published Gemini 4 Argon results. The model is not publicly available. | [AA article](https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs) |
| 2026-10-01 | Vals published Terminal-Bench 4.0 rows for Opus 5.5, Sonnet 5.5, and GPT-6.1 Sol. | [Vals TB4](https://www.vals.ai/benchmarks/terminal-bench-4) |

OpenAI's Codex guidance now says: "For complex coding and agentic workflows, use GPT-6.1 Sol when available."
It keeps Astra "for the hardest end-to-end work."
[Codex models](https://learn.chatgpt.com/docs/models)
The local Codex catalog gives `gpt-6.1-sol` priority 1 and describes `gpt-6-sol` as "Previous generation workhorse model."
The user's own `~/.codex/config.toml` already selects `gpt-6.1-sol` at `high`.

## Independent measurements

All values come from the [compiled evidence file](evidence/fleet-2026-10-06/benchmark-values.json).
Each value names its source and access date there.

### Artificial Analysis Intelligence Index v4.3.2

| Model and effort | Index | USD per index task |
|---|---:|---:|
| Opus 5.5 `max` | 58 | $5.98 |
| Sonnet 5.5 `max` | 56 | $7.67 |
| GPT-6 Astra `max` | 53 | $3.26 |
| Gemini 4 Argon `high` (not public) | 53 | $1.99 |
| GPT-6.1 Sol `max` | 52 | $0.72 |
| GPT-6.1 Sol `xhigh` / `high` / `medium` | 51 / 50 / 48 | — |
| Muse Spark 1.3 `max` | 48 | $1.60 |
| Sonnet 5.5 `high` / `medium` | 47 / 41 | — |
| Grok 4.7 `xhigh` | 46 | $3.74 |
| GLM-5.3 `max` | 45 | $2.01 |
| Kimi K3 `max` | 44 | $2.00 |
| GLM-5.3 Flash | 42 | $0.25 |
| DeepSeek V4.1 Flash `max` | 39 | $0.27 |
| GPT-6 Luna `max` | 38 | — |

On the AA Coding Agent Index, GPT-6.1 Sol at `xhigh` scores 1 point above Astra at less than 15% of its task cost.
GPT-6.1 Sol at `xhigh` also scores 3 points above its own `max` setting.
[AA GPT-6.1 Sol article](https://artificialanalysis.ai/articles/gpt-6-1-sol-replaces-gpt-6-sol-after-just-7-days-with-near-astra-intelligence)

### Vals Terminal-Bench 4.0 (one harness for every model)

| Model | Score | USD per test | Duration |
|---|---:|---:|---|
| Opus 5.5 | 65.15% | $13.20 | 1h04m |
| Sonnet 5.5 | 64.14% | $16.51 | 1h22m |
| GPT-6 Astra | 59.60% | $9.58 | 35m42s |
| Fable 5.1 | 58.08% | $17.18 | 1h00m |
| GPT-6.1 Sol | 55.05% | $1.72 | 45m12s |
| GPT-6 Sol | 44.44% | $5.79 | 34m56s |
| GLM-5.3 | 38.89% | $9.37 | 1h23m |
| Grok 4.7 | 28.79% | $18.09 | 50m21s |
| Muse Spark 1.3 `max` | 24.75% | $6.65 | 52m56s |
| GPT-5.6 Terra | 22.73% | $5.60 | 31m29s |
| Kimi K3 | 17.17% | $12.02 | 3h09m |
| GPT-6 Luna | 13.64% | $0.35 | 32m46s |

The Vals harness is Mini-SWE-agent.
Kimi K3 needs a harness that preserves its reasoning history, so this harness can understate it.
The public tbench.ai board has no Opus 5.5, Sonnet 5.5, or GPT-6.1 Sol submission.

### CursorBench 4.0

| Model and effort | Score | USD per task |
|---|---:|---:|
| Opus 5.5 `max` | 57.8% | $13.43 |
| Opus 5.5 `high` | 56.0% | $3.97 |
| Sonnet 5.5 `max` | 55.5% | $9.67 |
| Sonnet 5.5 `xhigh` | 53.1% | $3.88 |
| Opus 5.5 `medium` | 52.5% | $2.91 |
| Fable 5.1 `max` | 51.8% | $17.28 |
| Sonnet 5.5 `high` | 47.8% | $1.67 |
| Grok 4.7 `xhigh` | 46.3% | $6.01 |
| Grok 4.7 `high` | 43.9% | $4.69 |
| Opus 5.5 `low` | 43.7% | $1.17 |
| GLM-5.3 `max` | 42.6% | $5.05 |
| Muse Spark 1.3 `max` | 41.6% | $2.64 |
| Sonnet 5.5 `medium` | 39.2% | $0.70 |
| GLM-5.3 Flash `max` | 36.8% | $0.39 |

CursorBench lists no GPT-6 family rows.

### Vals Index

| Model | Accuracy | USD per test |
|---|---:|---:|
| Gemini 4 Argon | 68.90% | $15.68 |
| Sonnet 5.5 | 67.04% | $21.34 |
| Opus 5.5 | 66.97% | $32.14 |
| Fable 5.1 | 65.83% | $28.71 |
| GPT-6 Astra | 63.13% | $18.46 |
| GPT-6.1 Sol | 61.15% | $3.24 |
| Muse Spark 1.3 `max` | 58.16% | $3.79 |
| Grok 4.7 | 54.95% | $12.12 |
| GLM-5.3 | 53.51% | $7.25 |
| DeepSeek V4.1 Flash | 51.32% | $0.33 |
| GPT-6 Luna | 51.22% | $0.43 |
| Kimi K3 | 50.30% | $6.38 |

### Public usage

Public usage share measures adoption, not task quality.
On OpenCode, the top models for the seven days to October 5 were a stealth model, DeepSeek V4.1 Flash, and the free Muse Spark 1.3 contributor tier.
[OpenCode data](https://opencode.ai/data)
On OpenRouter, GLM-5.3 Flash processed 55T tokens in 30 days. Opus 5.5 processed 3.5T.
[Tokenmaxxing OpenRouter rankings](https://tokenmaxxing.com/openrouter-rankings)
Low price and free tiers drive these volumes.
They support the low-cost roles of GLM-5.3 Flash and Muse Spark 1.3. They do not support a quality ranking.

### Local usage

A read-only script aggregated local Codex, Claude Code, OpenCode, and Grok session logs from September 1 to October 6.
It recorded metadata only.
See the [usage summary](evidence/fleet-2026-10-06/usage/usage-summary.md) and its [script](evidence/fleet-2026-10-06/usage/local_usage_metrics.py).

| CLI and model | Turns | Wall p50 / p90 (s) | Abort | Seen |
|---|---:|---|---:|---|
| Grok `grok-4.7` | 3,610 | 82 / 252 | 0.3% | 09-21 to 10-06 |
| Codex `gpt-6-astra` | 1,592 | 236 / 1,324 | 0.6% | 09-04 to 10-06 |
| Codex `gpt-5.6-sol` | 734 | 372 / 1,480 | 0.8% | 09-01 to 09-21 |
| Claude `claude-opus-5-5` | 599 | 106 / 809 | 0.3% | 09-29 to 10-06 |
| Claude `claude-fable-5-1` | 281 | 157 / 608 | 0.4% | 09-06 to 10-06 |
| Codex `gpt-5.6-terra` | 165 | 196 / 632 | 0.0% | 09-01 to 09-19 |
| Codex `gpt-6.1-sol` | 152 | 247 / 1,305 | 0.7% | 09-29 to 10-06 |
| Codex `gpt-6-sol` | 106 | 193 / 1,001 | 2.8% | 09-22 to 09-29 |
| OpenCode `muse-spark-1.3-contributor` | 95 | 164 / 1,893 | 1.1% | $9.04 logged |
| Codex `gpt-daybreak-blue-latest` | 39 | 395 / 974 | 2.6% | 09-14 to 09-27 |
| Claude `claude-sonnet-5-5` | 35 | 55 / 417 | 0.0% | 09-29 to 10-06 |

Findings:

- Grok 4.7 has the most turns. Most are scripted batch runs in scratch and experiment directories. The new Grok role keeps that challenge and research work.
- Astra stayed in heavy use after GPT-6.1 Sol arrived. GPT-6.1 Sol has only 152 turns, so local data cannot yet compare their task success.
- Luna has 7 turns, and Terra stopped on September 19. Removing Terra affects no current local workflow.
- OpenCode open-model runs show harness instability: 14.3% of GLM-5.3 turns and 28.6% of Cloudflare GLM-5.3 turns have no end record.
- Claude Code keeps 7 days of logs, so these Claude rows start on September 29.

These rates are harness events, not task success. Turn definitions differ by CLI.

### Local probes

A clean-context agent ran 98 code-graded probe runs on 14 model and effort configurations through the four worker CLIs.
The five tasks were a three-bug fix with hidden tests, a 40-record extraction with decoys, a missing-input honesty trap, a constrained prose rewrite, and a six-case routing policy with three traps.
See the [probe results](evidence/fleet-2026-10-06/probes/results.md), [runner](evidence/fleet-2026-10-06/probes/runner.py), and [raw runs](evidence/fleet-2026-10-06/probes/raw/).

| Configuration | Pass | Median wall (s) | Reported cost |
|---|---:|---:|---:|
| GPT-6.1 Sol `high` | 7/7 | 42 | not reported |
| GPT-6.1 Sol `xhigh` | 7/7 | 75 | not reported |
| GPT-6 Astra `high` | 7/7 | 32 | not reported |
| GPT-6 Luna `high` | 7/7 | 16 | not reported |
| Opus 5.5 `medium` | 7/7 | 17 | $0.63 |
| Opus 5.5 `high` | 7/7 | 20 | $0.70 |
| Sonnet 5.5 `medium` | 6/7 | 11 | $0.30 |
| Sonnet 5.5 `high` | 7/7 | 14 | $0.30 |
| Grok 4.7 `high` | 7/7 | 72 | $0.64 |
| GLM-5.3 `max` | 6/7 | 93 | $0.64 |
| GLM-5.3 Flash `max` | 7/7 | 56 | $0.28 |
| Kimi K3 `max` | 7/7 | 83 | $2.03 |
| Muse Spark 1.3 `xhigh` | 7/7 | 50 | $2.33 |
| DeepSeek V4.1 Flash `max` | 7/7 | 15 | $0.12 |

Findings:

- The probes hit a ceiling. Small, bounded, checkable tasks do not separate these models. They do not contradict the harder independent benchmarks.
- The ceiling supports the bounded rows: low-cost routes complete narrow, checkable work.
- GPT-6.1 Sol at `xhigh` added no passes over `high` and took about twice as long. Use `medium` or `high` for bounded work.
- Sonnet 5.5 at `high` matched Opus 5.5 at about 45% of its cost. At `medium`, it wrote one 21-word sentence against a 20-word limit.
- GLM-5.3 at `max` spent 32,018 reasoning tokens over 369 seconds, then stopped with an empty message and no output file. OpenCode exited 0. The fleet now requires a check that each expected output exists.
- `meta/muse-spark-1.3` returned HTTP 402 "Billing verification failed." The OpenRouter route worked. The provider order already covers this account-specific failure.
- OpenCode with `--pure` still loaded about 108K tokens of global context on its first step. This raises the cost of the Kimi and Muse runs.

Limits: one or two runs for each task, synthetic tasks, different permission models for each CLI, CLI-reported costs, and a one-day snapshot.

## Route decisions

| Lane or route | Decision | Basis |
|---|---|---|
| Codex default | GPT-6.1 Sol at `high` replaces Astra at `high` | AA index 52 against 53 at 22% of task cost; AA Coding Agent Index above Astra at `xhigh`; Vals TB4 4.6 points lower at 18% of task cost; OpenAI's Codex guidance; the user's own Codex configuration |
| Codex escalation | Astra at `high` or `xhigh` | Astra still leads GPT-6.1 Sol on Vals TB4, the Vals Index, and AA by small margins |
| GPT-6.1 Sol effort | `high` default, `xhigh` for hard coding, `medium` for bounded work | AA reports `xhigh` above `max` on coding; the Codex default is `low`, so set effort explicitly |
| GPT-6 Sol and GPT-5.6 Terra | Remove | GPT-6.1 Sol beats both on every independent measure at the same or lower token price |
| Sonnet 5.5 | Add for bounded Claude work at `low` to `high`; first fallback for difficult implementation at `xhigh` | Sonnet 5.5 `high` is on the CursorBench cost frontier. Above `high`, Opus 5.5 gives a higher score at a similar cost. Sonnet 5.5 beats Fable 5.1 on Vals TB4, the Vals Index, CursorBench, and AA at a quarter of its token price |
| Fable 5.1 | Keep as planning fallback and escalation only | Opus 5.5 and Sonnet 5.5 lead it on every independent coding measure. Anthropic still recommends it when Opus 5.5 at higher effort falls short |
| Terminal and verification | GPT-6.1 Sol first, Astra second, then Opus 5.5 | Opus 5.5 leads on Vals TB4, but AA ties it with Astra. A Codex route also keeps verification in a different family from the usual Opus author |
| Budget coding | GPT-6.1 Sol at `medium`, then Sonnet 5.5, GLM-5.3 Flash, and Opus 5.5 at `low` | Measured task costs: GPT-6.1 Sol $1.72 per Vals TB4 test; Sonnet 5.5 `high` $1.67 and GLM-5.3 Flash `max` $0.39 per CursorBench task. Grok 4.7 `high` costs $4.69 for a lower score |
| Grok 4.7 | Remove from coding fallbacks and from the reviewer pairs; keep for independent challenge and live web and X research | 28.79% on Vals TB4 at $18.09 per test; below GPT-6.1 Sol on AA and the Vals Index at a higher cost. The edge-case review found that a reviewer whose findings need reproduction cannot also give the verdict |
| GLM-5.3 | Narrow to open-weight long-context work, security analysis, and challenge | GPT-6.1 Sol leads it on every measure at lower cost. Its open weights and different family remain useful |
| Kimi K3 | Fallback and challenger; keep a session it started | Lowest AA score of the three open challengers. It is slow, and generic harnesses understate it |
| Muse Spark 1.3 | Keep first for general multimodal work; add challenger role | Highest AA and Vals Index scores of the open challengers, at low cost. It is weak on terminal-heavy work |
| Security | Daybreak Blue, then Astra, then GPT-6.1 Sol | Opus 5.5 and Sonnet 5.5 have cyber safeguards. The Cyber Verification Program does not cover them yet. Sonnet 5.5 sends flagged requests to Sonnet 5 |

## Rejected candidates

| Candidate | Reason |
|---|---|
| Gemini 4 Argon | Not publicly available. No route in the fleet's worker CLIs. Recheck when OpenCode lists it. |
| DeepSeek V4.1 Flash | Near GPT-6 Luna on AA and the Vals Index. It passed all 7 local probes for $0.12, as Luna did. It adds no lane that Luna and GLM-5.3 Flash do not cover. |
| GLM-5.3 Prime, GLM-5.3 FlashX | Faster, more expensive serving tiers of existing models, not new models. |
| Grok Build 0.1 | Older coding model with no shared independent benchmark rows. |
| Qwen 3.8 Max, MiniMax M3 | Below the fleet on Vals TB4 (34.34% and 1.01%). |
| Haiku 5.5 | Announced, not released. |

## Open checks

- Recheck the terminal lane if an independent run with a Codex harness puts Opus 5.5 clearly above GPT-6.1 Sol and Astra.
- Recheck the security lane when the Cyber Verification Program covers Opus 5.5 and Sonnet 5.5.
- Recheck the Daybreak alias if OpenAI moves it to a GPT-6 model.
- Add GPT-6.1 Sol Ultrafast only after the Codex host lists it.
- Recheck Gemini 4 Argon when it becomes public and a fleet CLI lists it.

## Edge-case review

Kimi K3, Muse Spark 1.3, and GLM-5.3 reviewed the draft policy through OpenCode.
They received only the policy text.
The lead checked each finding against the text before any edit.

- Kimi K3 at `max` reported 10 findings. All 10 reproduced.
- Muse Spark 1.3 at `max` reported 3 new findings that reproduced. Six more repeated Kimi findings.
- GLM-5.3 at `max` returned an empty result with exit code 0. At `high`, it reported 8 findings, and all 8 reproduced; its output stopped mid-text.

The 21 fixes cover pinned-CLI outcomes, effort precedence, the one-worker rule, the Grok reviewer role, safeguard handoffs, harness-property checks, cost-limited difficult work, security limits on every fallback, an unavailable reviewer family, open-weight privacy, and the Muse provider order.
The weaker models found real defects at low cost. Their high verified-finding rate supports the challenger role, with reproduction before action.
See the [edge-case findings](evidence/fleet-2026-10-06/edge-cases/findings.md).

Harness events during this review:

- Three OpenCode runs started at the same time hung for 1h44m with no output.
- A second parallel start failed for two models with `database is locked`.
- Sequential runs with a 10-minute limit succeeded.

A later investigation found the causes. See [OpenCode reliability](#opencode-reliability).

## OpenCode reliability

A follow-up test found a cause for each OpenCode failure in this update.
See the [test results](evidence/fleet-2026-10-06/opencode/results.md).

| Failure seen | Cause | Control |
|---|---|---|
| Three runs hung for 1h44m after `init` | `opencode run` waits for the end of stdin, and the launching shell kept stdin open | Close stdin |
| GLM-5.3 at `max` ended twice with no text and exit code 0 | OpenCode's default output cap of 32000 tokens. GLM-5.3 at `max` used 28,505 to 38,323 reasoning tokens on one prompt, so the cap fails at random | Set `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` to 128000 |
| About 108K input tokens on the first step | `--pure` keeps the 13 global MCP servers; they add about 85K tokens | Turn the servers off through `OPENCODE_CONFIG_CONTENT`; a short run drops from 106,383 to 17,067 input tokens |
| `database is locked` at start | About nine processes started together on a 2.8 GB database; no later test reproduced it | Retry once and stagger large batches |

The test also found two more silent failures:

- A headless run rejects each permission request that needs approval. It then exits 0 with no text.
- An attached `run --attach` client stops its output after the first event, but the server finishes the session.

The routing skill now has a [headless OpenCode reference](../../skills/productivity/routing-agent-work/references/opencode.md) and a tested launcher, `scripts/opencode_worker.py`.
The launcher applies these controls and reports `complete`, `truncated`, `incomplete`, `empty`, `timeout`, or `error`.
It passed its offline self-test and live checks on GLM-5.3, GLM-5.3 Flash, Kimi K3, and Muse Spark 1.3.

These causes change the reading of two earlier results:

- The GLM-5.3 probe failure and the empty GLM-5.3 edge review were harness truncation, not model refusals.
- The Kimi K3 and Muse Spark 1.3 probe costs include about 85K tokens of MCP tool definitions on each step. Isolated runs cost much less.

## Validation

Fresh evaluators applied either the previous policy (`36f3dd2`) or the new policy to the same 34 eval prompts.
They received only the policy text and the prompts, without expected answers.
They did not launch workers.
A script graded the primary model and effort against a fixed key.
See the [prompts, briefs, answers, and grader](evidence/fleet-2026-10-06/validation/).

| Evaluator | Previous policy | New policy |
|---|---:|---:|
| Claude Sonnet 5.5 at `high` | 16/34 | 34/34 |
| GPT-6.1 Sol at `high` | 16/34 | 34/34 |

Every previous-policy miss is an intended change.
Examples are Astra or Terra where the new policy uses GPT-6.1 Sol, and Grok 4.7 where the new policy returns `Unrouted`.

The validation rounds found two defects in the new text, and both are fixed:

- The difficult-implementation row listed Astra before GPT-6.1 Sol. A Codex-pinned evaluator therefore chose Astra for a hard refactor. The row now lists GPT-6.1 Sol at `xhigh` first, which matches the Codex escalation order.
- An earlier round had GPT-6.1 Sol treat eval 2 as orchestration mechanics and decline to route it. That case predates this change. The other evaluator routed it correctly.

Structural checks:

- The Skill Creator validator passes for all 16 skills.
- Every eval file is valid JSON, and `git diff --check` passes.
- After the audit below, the routing eval file contains 40 cases: 28 positive and 12 hard-negative trigger cases, each marked with `should_trigger`.
- The project and global installation links resolve to the edited sources.

Limits:

- The evaluation tests routing instructions, not model performance.
- Each evaluator answered all prompts in one context.
- The key grades the primary model and effort, not every assertion in all 63 cases.

## Skill audit

Three fresh-context auditors reviewed the changed skills for overfitting and cleanliness.
The auditors applied the skill-creator principles: generalize from incidents, keep the text lean, explain the reason, and avoid drift-prone facts.

Changes to `routing-agent-work`:

- Removed facts that drift: provider effort defaults, price ratios, named safeguard targets, speed-tier aliases, and one account's provider effort support.
- Kept one copy of the pinned-CLI rule, the weaker-model rule, and the Daybreak family note.
- Turned the launch check into a numbered list and moved the OpenCode catalog refresh into `references/opencode.md`.
- Replaced the hard-coded ASD-STE100 rule with "pass the caller's writing standard into the worker brief".
- Stated in the description that the skill also checks whether a headless OpenCode worker finished.
- Fixed the launcher: it sends the prompt on stdin, reads only the final step's text, sums tokens across steps, adds `filtered` and `unconfirmed` statuses, checks MCP servers in the work directory, and returns a JSON error instead of a traceback. It passed 11 offline cases, a 180 KB prompt, and a live two-step tool run.
- Cut the evals from 65 to 40. The cut removed near-duplicates and cases that restated one sentence, and it added three hard negatives and two casual-phrasing positives.

A regression round on the 40 cases compared the committed version with the audited version.
See [round 4](evidence/fleet-2026-10-06/validation/round4/).

| Evaluator | Committed version | Audited version |
|---|---:|---:|
| Claude Sonnet 5.5 at `high` | 39/40 | 40/40 |
| GPT-6.1 Sol at `high` | 38/40 | 39/40 |

The committed version missed the headless OpenCode case, because it had no launch guidance.
The remaining miss is eval 7: the evaluator rejected the unlisted model but offered a fleet reviewer.

The deep-research, agent-browser-webauthn, and Solo audits removed version-specific lists, hard-coded shortcuts and limits, duplicated rules, and evals fitted to one incident.
They kept every safety rule. Each Solo skill still states its own ownership and trust gates, because each skill must work when installed alone.

