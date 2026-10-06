# Fixed Agent Fleet

Use this reference only after a lane has a bounded output. It provides routing clues, not an overall model ranking.

## Default route for each worker CLI

| Worker CLI | Default route | Escalation | Keep for |
|---|---|---|---|
| Claude | Opus 5.5 at `high` | Opus 5.5 at `xhigh`, then Fable 5.1 | Planning, difficult implementation, review, and prose |
| Codex | GPT-6.1 Sol at `high` | GPT-6.1 Sol at `xhigh`, then GPT-6 Astra | Implementation, terminal work, verification, and sweeps |
| Grok | Grok 4.7 at `high` | Grok 4.7 at `xhigh` | Independent challenge and live web or X research |
| OpenCode | Set by the lane table | Set by the lane table | Open-weight, multimodal, and low-cost lanes |

Use the default when the caller pins a worker CLI and the lane has no more specific row.

## Route by lane

Use the bounded rows only for narrow work with readily checked output. Treat migrations and multi-file features as difficult implementation. Use the budget row only when the caller states a cost limit.

| Primary lane | First route | Fallbacks, in order |
|---|---|---|
| Ambiguous planning, architecture, orchestration, or synthesis | Claude with Opus 5.5 | Fable 5.1; GPT-6 Astra; GPT-6.1 Sol |
| Difficult implementation, refactoring, debugging, or test construction | Claude with Opus 5.5 | Sonnet 5.5 at `xhigh`; GPT-6 Astra; GPT-6.1 Sol at `xhigh` |
| Terminal workflows, primary verification, or acting on gathered evidence | Codex with GPT-6.1 Sol | GPT-6 Astra; Opus 5.5; Sonnet 5.5 |
| Bounded implementation, repository sweep, data collection, or tool calling | Codex with GPT-6.1 Sol at `medium` | Sonnet 5.5 at `medium`; Opus 5.5 at `medium`; GLM-5.3 Flash |
| Budget-sensitive bounded coding or repository sweeps | Codex with GPT-6.1 Sol at `medium` | Sonnet 5.5 at `medium` or `high`; GLM-5.3 Flash at `max`; Opus 5.5 at `low` |
| Narrow high-volume extraction or triage | Codex with GPT-6 Luna | GPT-6.1 Sol at `low` or `medium`; GLM-5.3 Flash |
| Security review, authorized vulnerability exploration, or patch validation | Codex with Daybreak Blue | GPT-6 Astra; GPT-6.1 Sol; Opus 5.5 for defensive review of the caller's own code; GLM-5.3 for text-only input |
| Precision review or quality-first technical prose | Claude with Opus 5.5 | Sonnet 5.5; Fable 5.1; GPT-6 Astra; GPT-6.1 Sol |
| Independent challenge, second opinion, or live web and X research | Grok 4.7 | GLM-5.3; Muse Spark 1.3; Kimi K3 when the harness preserves full history |
| Edge-case discovery and confirmation across model families | OpenCode with GLM-5.3, Muse Spark 1.3, or Kimi K3 | Grok 4.7; GLM-5.3 Flash |
| General multimodal, visual implementation, or long-context documents and screenshots | OpenCode with Muse Spark 1.3 | Opus 5.5; GPT-6.1 Sol; Kimi K3 when the harness preserves full history |
| Text-only long-context work that needs an open-weight model | OpenCode with GLM-5.3 | Kimi K3 when the harness preserves full history; GLM-5.3 Flash |
| Cost-sensitive agentic coding, automation, multimodal review, or structured technical prose | OpenCode with GLM-5.3 Flash | GPT-6.1 Sol at `medium`; Sonnet 5.5 at `medium`; Muse Spark 1.3 |

## Treat weaker-model findings as leads

GLM-5.3, GLM-5.3 Flash, Kimi K3, Muse Spark 1.3, and Grok 4.7 trail the default routes on independent coding and terminal evaluations.
Use them for cost, modality, open weights, or a different model family.
Treat their findings as leads, not verdicts.
Reproduce a finding with a test, command, or cited source before a stronger route acts on it.
Run two or three of them in parallel when the lane needs diverse edge cases.
Give each run a time limit. OpenCode runs on these models sometimes stop without a completion record.
Check that each expected output file exists and is not empty. A run can end with an empty message and exit code 0.
Parallel OpenCode runs can fail at start with `database is locked`. Retry such a run once; it is a harness failure, not a model result.
Discard a finding that no check reproduces.

## Know each route

| Model | Worker CLI | Effort | Strong clues | Limits and keep-away clues |
|---|---|---|---|---|
| Opus 5.5 (`claude-opus-5-5`) | Claude | `low` to `max` | Default Claude route. Planning, orchestration, synthesis, difficult coding, debugging, long unattended migrations, code review, knowledge work, computer use, screenshots, and technical prose | Its API default is `medium`; set effort explicitly. Use `medium` for bounded work, `high` for meaningful work, and `xhigh` for the hardest lanes. Use `max` only with a clear stop budget. Use `low` only for trivial, readily checked tasks. Give unattended runs a completion check and a stop budget. A turn that ends in text is a progress report, not proof of completion. Cyber safeguards send most security work to Opus 4.8, which is outside this fleet. Use Opus 5.5 only for defensive review of the caller's own code. |
| Sonnet 5.5 (`claude-sonnet-5-5`) | Claude | `low` to `high`; `xhigh` only as a fallback | Fast Claude route for well-scoped coding, bug fixes, bounded sweeps, documents, and design-sensitive work | Its Claude Code default is `medium` and its API default is `high`; set effort explicitly. Above `high`, it costs about as much as Opus 5.5 at lower quality, so prefer Opus 5.5. Avoid `max`; it produces very high output-token counts. Cyber safeguards send flagged security work to Sonnet 5. Do not route vulnerability exploration to it. |
| Fable 5.1 (`claude-fable-5-1`) | Claude | `high` to `max` | Escalation for demanding reasoning and long-horizon autonomy when Opus 5.5 at `xhigh` falls short; planning fallback when Opus 5.5 is unavailable | It costs 2.5 times Opus 5.5 per token and runs slower. Prefer `xhigh`. Give it a clear completion check and stop budget. |
| GPT-6.1 Sol (`gpt-6.1-sol`) | Codex | `low` to `max`; host `ultra` mode when permitted | Default Codex route. Complex coding, terminal work, verification, agent workflows, computer use, and repeated long-running work | Its Codex default is `low`; set effort explicitly. Use `high` for meaningful work, `xhigh` for hard coding, and `medium` for bounded work. Prefer `xhigh` over `max` for coding unless a local sample shows a gain. Escalate to Astra when it falls short on the hardest end-to-end work. |
| GPT-6 Astra (`gpt-6-astra`) | Codex | `low` to `max`; host `ultra` mode when the host confirms it | Escalation for the hardest end-to-end Codex work, difficult research, and final consequential interpretation | It costs about five times GPT-6.1 Sol per token. Use `high` or `xhigh`. API effort stops at `max`. Confirm `ultra` on the host before use. |
| GPT-6 Luna (`gpt-6-luna`) | Codex | `high` to `max` | Narrow, high-volume extraction and triage when cost matters | Start at `high`. Use `xhigh` or `max` only when a local task sample shows a material gain. Keep the lane small. Give consequential interpretation to GPT-6.1 Sol, Astra, or Opus 5.5. |
| Daybreak Blue (`gpt-daybreak-blue-latest` → `gpt-5.6-sol`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Defensive cybersecurity reviews when refusal calibration matters | Check the alias through the [Daybreak model page](https://developers.openai.com/api/docs/models/gpt-daybreak-blue-latest). Its base is not a general route. It is not a different-family reviewer of other OpenAI work. Select it with an approved API key; a ChatGPT-account Codex login cannot use it. Start at `high`. If access is missing, use Astra. Keep the caller's target and action limits. |
| Grok 4.7 (`grok-4.7`) | Grok | `medium` to `xhigh` | Independent challenge from another family, research with live web and X context, and second opinions | It trails the default routes on independent coding and terminal evaluations at a higher task cost. Do not use it as a coding fallback. Verify its factual claims and executed checks. Use `grok-4.7-build-fast` only when latency matters and the host lists it. |
| GLM-5.3 | OpenCode | `high` or `max` | Open-weight text-only long-context work, defensive security analysis, and different-family challenge | It has no image input. Prefer `max`. It is slow and verbose. GLM-5.3 Prime is the same model on a faster, more expensive tier. |
| GLM-5.3 Flash | OpenCode | `high` or `max` | Very low-cost coding, automation, tools, multimodal review, and prose | Use `max` for coding. Confirm the configured route provides high or max reasoning. GLM-5.3 FlashX is the same model on a faster tier. |
| Kimi K3 | OpenCode | `high` or `max` | Preserved-reasoning multimodal sessions and different-family challenge | Start each new lane in a fresh session. The harness must preserve its full reasoning and tool history; generic harnesses score poorly. Keep a session that Kimi K3 started on Kimi K3, because a model switch loses that history. It is slow and expensive for its quality. |
| Muse Spark 1.3 | OpenCode | `medium` to `max`, subject to provider support | Multimodal work, visual implementation, knowledge work, and different-family challenge | It trails on terminal-heavy agent work. Follow the provider order below among routes that meet the task's effort and data requirements. Results depend strongly on the harness. |

Use [OpenAI's model pages](https://developers.openai.com/api/docs/models) and [Claude's models overview](https://platform.claude.com/docs/en/models/overview) for current API limits and prices.
Use the selected host's context limit and effort controls when they differ from API limits.

## Muse provider selection

Use only Muse Spark 1.3 for Muse routes. Prefer contributor routes after explicit acceptance of their data terms.

Try these identifiers in order:

1. `meta/muse-spark-1.3-contributor`
2. `openrouter/meta/muse-spark-1.3-contributor`
3. `opencode/muse-spark-1.3-contributor-free`
4. `meta/muse-spark-1.3`
5. `openrouter/meta/muse-spark-1.3`

Skip contributor routes when their data terms are not accepted.
Check effort support for the selected identifier, not only the model family.
If no supported effort meets the task requirement, advance through the provider list before changing models.
Full Meta 1.3 and OpenRouter 1.3 routes expose `max`; confirm the selected contributor route separately.

## Map effort to the worker CLI

Use the host's installed controls. These forms show the intended mapping:

| Worker CLI | Model control | Effort control |
|---|---|---|
| Claude | `--model <alias-or-id>` | `--effort low|medium|high|xhigh|max` within the selected route's policy |
| Codex | `-m <model-id>` | `-c model_reasoning_effort="low|medium|high|xhigh|max|ultra"` within the selected route's policy |
| Grok | `-m <grok-model-id>` | `--reasoning-effort medium|high|xhigh` |
| OpenCode | `-m <provider/model>` | `--variant <provider-supported-value>` |

Do not translate effort names as equal compute across providers. Choose the level within the selected model's supported range.

Check Codex identifiers and effort controls with targeted host status or `codex debug models`.
The Codex host's `ultra` mode includes automatic delegation; it is not a portable API effort value.

## Pair independent reviewers

- Review GPT-6.1 Sol, Astra, Luna, or Daybreak work with Opus 5.5, Sonnet 5.5, Fable 5.1, or Grok 4.7.
- Review Opus 5.5, Sonnet 5.5, or Fable 5.1 work with GPT-6.1 Sol, Astra, or Grok 4.7. The three Claude models are one family.
- Review Grok work with GPT-6.1 Sol, Astra, or Opus 5.5.
- Review Kimi, either GLM route, or Muse work with GPT-6.1 Sol, Astra, or Opus 5.5.
- Add GLM-5.3, Muse Spark 1.3, or Kimi K3 as extra challengers for edge cases. Do not let them replace a capable reviewer.

Daybreak Blue belongs to the same model family as the other OpenAI routes.

Give the reviewer the artifact and requirements. Keep the author's reasoning out of the initial review context.
