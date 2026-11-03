# Fixed Agent Fleet

Use this reference only after a lane has a bounded output. It provides routing clues, not an overall model ranking.

## Know the cost basis

The fleet owner pays for each worker CLI in one of two ways. Use the cost basis as the cost tie-breaker.

- **Subscription routes:** Claude, Codex, and Grok signed in with their subscriptions have weekly limits. A task costs weekly-limit headroom, not dollars.
- **API routes:** OpenCode routes bill per token from API accounts. A Codex run that signs in with an API key is also an API route.
- **API accounts:** Spend from Cloudflare first, then OpenRouter. The other API accounts have tighter limits. Use them only when the model has no Cloudflare or OpenRouter route.

Apply these rules:

- When an API route and a subscription route both meet the quality bar, use the subscription route.
- Use an API route when it gives a needed modality, model family, open weights, or quality level.
- Before a large lane, read the selected subscription's weekly headroom from host status.
- When one subscription is low, move bounded lanes to another subscription CLI first. Then use OpenCode.
- On Claude, all models share one weekly limit. Fable 5.1 can use at most half of that limit, and it uses the limit fastest.
- On the Vals Index, Sonnet 5.5 uses the most tokens per task. GPT-6.1 Sol and GPT-6 Astra use the fewest among the frontier routes. Treat token counts as an efficiency clue, not as a limit measure.

## Default route for each worker CLI

| Worker CLI | Default route | Escalation | Keep for |
|---|---|---|---|
| Claude | Opus 5.5 at `high` | Opus 5.5 at `xhigh`, then `max` with a stop budget | Planning, difficult implementation, review, and prose |
| Codex | GPT-6.1 Sol at `high` | GPT-6.1 Sol at `xhigh` or `max`; GPT-6 Astra for science, research, and final interpretation | Implementation, terminal work, verification, and sweeps |
| Grok | Grok 4.7 at `xhigh` | None | Independent challenge and live web or X research |
| OpenCode | Set by the lane table | Set by the lane table | Other model families, multimodal input, open weights, and low-cost lanes |

When the caller pins a worker CLI, use the lane row's first route on that CLI. If the row has none, use a route on that CLI whose strong clues fit the lane. Otherwise, mark the lane `Unrouted`. A pinned Grok CLI has no coding route.

## Route by lane

The bounded rows are the bounded implementation, budget, and extraction rows. Use them only for narrow work with readily checked output. Treat migrations and multi-file features as difficult implementation. Use the budget row only when the caller states a cost or headroom limit.
For difficult implementation under a stated cost limit, use GPT-6.1 Sol at `xhigh` or `max`. Give the lane a stop budget.
Security lanes keep the caller's target and action limits on every route and fallback.

| Primary lane | First route | Fallbacks, in order |
|---|---|---|
| Ambiguous planning, architecture, orchestration, or synthesis | Claude with Opus 5.5 | GPT-6 Astra; GPT-6.1 Sol; Fable 5.1 |
| Difficult implementation, refactoring, debugging, or test construction | Claude with Opus 5.5 | Sonnet 5.5 at `max`; GPT-6.1 Sol at `max`; Kimi K3.1 Pro at `high`; GPT-6 Astra |
| Terminal workflows, primary verification, or acting on gathered evidence | Codex with GPT-6.1 Sol | Opus 5.5; Sonnet 5.5 at `max`; Kimi K3.1 Pro at `high`; GPT-6 Astra |
| Bounded implementation, repository sweep, data collection, or tool calling | Codex with GPT-6.1 Sol at `medium` | GPT-6.1 Terra at `xhigh`; Opus 5.5 at `medium`; DeepSeek V4.1 Flash at `max`; GLM-5.3 Flash at `high` |
| Budget-sensitive bounded coding or repository sweeps | Codex with GPT-6.1 Sol at `medium` | GPT-6.1 Terra at `xhigh`; Haiku 5.5 at `max`; DeepSeek V4.1 Flash at `max`; GLM-5.3 Flash at `high` |
| Narrow high-volume extraction or triage | Codex with GPT-6 Luna at `max` | GPT-6.1 Terra at `medium`; Haiku 5.5 at `high`; GLM-5.3 Flash at `high`; DeepSeek V4.1 Flash at `max` |
| Security review, authorized vulnerability exploration, or patch validation | Codex with GPT-6 Sol under Daybreak Blue access | GPT-6 Astra; GPT-6.1 Sol; Opus 5.5 for defensive review of the caller's own code; Muse Wonder 1.0 or Gemini 4 Argon for defensive review; GLM-5.3 for text-only input |
| Precision review or quality-first technical prose | Claude with Opus 5.5 | Fable 5.1; Gemini 4 Argon at `high`; Sonnet 5.5 at `max`; GPT-6 Astra; GPT-6.1 Sol |
| Independent challenge or second opinion | OpenCode with Gemini 4 Argon at `medium` | Kimi K3.1 Pro at `high`; Grok 4.7; GLM-5.3 at `high`; Muse Spark 1.3 at `high` |
| Live web and X research | Grok 4.7 | GPT-6 Astra and Opus 5.5 for web research only |
| Edge-case discovery and confirmation across model families | OpenCode with Kimi K3.1 Pro at `high` | Gemini 4 Argon at `medium`; GLM-5.3 at `high` for text-only input; Grok 4.7; Muse Spark 1.3 at `high`; DeepSeek V4.1 Flash at `max` |
| Visual implementation, screenshots, or long-context documents | Claude with Opus 5.5 | GPT-6.1 Sol; Gemini 4 Argon at `high`; Kimi K3.1 Pro at `high`; Muse Spark 1.3 at `high` |
| Audio or video input, or multimodal work that needs another model family | OpenCode with Gemini 4 Argon at `medium` | Muse Spark 1.3 at `high`; MiMo V2.6 Pro for open-weight input |
| Text-only long-context work that needs an open-weight model | OpenCode with GLM-5.3 at `high` | DeepSeek V4.1 Flash at `max`; GLM-5.3 Flash at `high` |
| Open-weight automation, multimodal review, or structured prose | OpenCode with DeepSeek V4.1 Flash at `max` | GLM-5.3 Flash at `high`; MiMo V2.6 Pro |

For an independent challenge under a tight API budget, start with Grok 4.7. It runs on a subscription.
When the Claude weekly limit makes Opus 5.5 unavailable, skip the other Claude fallbacks in the row. They share that limit.

## Treat challenger findings as leads

Seven challengers trail the default routes on terminal work and on the Artificial Analysis intelligence index.
They are GLM-5.3, GLM-5.3 Flash, DeepSeek V4.1 Flash, MiMo V2.6 Pro, Muse Spark 1.3, Muse Wonder 1.0, and Grok 4.7.
Muse Wonder 1.0 scores slightly above GPT-6.1 Sol on the Vals Index.
Kimi K3.1 Pro matches or beats GPT-6.1 Sol on terminal evaluations. It trails on composite, science, and knowledge evaluations.
Use these models for cost, modality, open weights, or a different model family.
Treat their findings as leads, not verdicts.
Reproduce a finding with a test, command, or cited source before a stronger route acts on it.
Run two or three of them in parallel when the lane needs diverse edge cases. For one run, follow the order in the edge-case row.
Launch headless OpenCode runs as [opencode.md](opencode.md) describes. A run can end with no answer and exit code 0.
Discard a finding that no check reproduces.
When one of these models owns a lane, accept its result only after the lane's completion check passes.

## Know each route

| Model | Worker CLI | Effort | Strong clues | Limits and keep-away clues |
|---|---|---|---|---|
| Opus 5.5 (`claude-opus-5-5`) | Claude | `medium` to `max` | Default Claude route. Planning, orchestration, synthesis, difficult coding, debugging, long unattended migrations, code review, knowledge work, computer use, screenshots, and technical prose. Leads the Artificial Analysis coding-agent and cyber indexes, Vals Terminal-Bench, and the LMArena writing and instruction-following boards | `max` adds little over `xhigh` at much higher token use. `high` is the efficient choice when its quality meets the lane. Use `max` only with a clear stop budget. Give unattended runs a completion check and a stop budget. A turn that ends in text is a progress report, not proof of completion. Cyber safeguards can hand security work to a model outside the fleet. Use Opus 5.5 only for defensive review of the caller's own code. |
| Sonnet 5.5 (`claude-sonnet-5-5`) | Claude | `xhigh` or `max` | Fallback when Opus 5.5 is unavailable. At `max`, it leads the Vals Index and nearly matches Opus 5.5 on terminal work | It scores far lower below `xhigh`. At `xhigh` and `max`, its quality is similar to Opus 5.5, and both use the same weekly limit. It uses the most tokens per task in the fleet. Cyber safeguards can hand security work to a model outside the fleet. Do not route vulnerability exploration to it. |
| Haiku 5.5 (`claude-haiku-5-5`) | Claude | `high` or `max` | Low-headroom Claude route for extraction, triage, and small bounded tasks | It trails GPT-6.1 Terra and GPT-6.1 Sol on coding and terminal evaluations. Keep consequential interpretation on a stronger route. |
| Fable 5.1 (`claude-fable-5-1`) | Claude | `high` or `xhigh` | Prose fallback; it leads Opus 5.5 on the AI-judged EQ-Bench creative-writing board. Planning fallback when Opus 5.5 is unavailable | It trails Opus 5.5 and Gemini 4 Argon on the LMArena creative-writing board. It trails Opus 5.5 on coding, terminal, and composite evaluations. It uses the Claude weekly limit fastest, and it can use at most half of it. On the Artificial Analysis index, `max` gives no gain over `xhigh`. |
| GPT-6.1 Sol (`gpt-6.1-sol`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Default Codex route. Complex coding, terminal work, verification, agent workflows, computer use, and repeated long-running work. Lowest cost per task among the frontier routes | `max` scores higher than `xhigh` on independent evaluations. Use `max` for hard lanes with a stop budget. Opus 5.5 scores higher on independent terminal evaluations; use Opus 5.5 when terminal failure cost is high. |
| GPT-6 Astra (`gpt-6-astra`) | Codex | `high` to `max`; host `ultra` mode when the host confirms it | Escalation for science, difficult research, and final consequential interpretation. It leads Scale's HLE-Diamond board | On coding-agent evaluations, it scores about the same as GPT-6.1 Sol at several times the cost. Use `high` or `xhigh`. Use `max`, or host `ultra`, only for the hardest lanes with a stop budget. |
| GPT-6.1 Terra (`gpt-6.1-terra`) | Codex | `medium` to `xhigh` | Low-cost Codex route for bounded coding, extraction, computer use, and screenshots | It trails GPT-6.1 Sol on coding and terminal work. In Codex, `xhigh` matches `max` on the Artificial Analysis coding-agent index. Keep difficult lanes on GPT-6.1 Sol. |
| GPT-6 Luna (`gpt-6-luna`) | Codex | `high` or `max` | Narrow, high-volume extraction and triage | Use `max`; it scores much higher than `high` at a small cost. Use `high` only when the cost per call dominates. Keep the lane small. Give consequential interpretation to GPT-6.1 Sol, Astra, or Opus 5.5. |
| GPT-6 Sol under Daybreak Blue (`gpt-6-sol`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Defensive cybersecurity reviews when refusal calibration matters. Daybreak Blue gives it reduced refusals | Daybreak is an access program, not a model. The `gpt-daybreak-blue-latest` alias is deprecated. Check the eligible models on the [Daybreak guide](https://developers.openai.com/api/docs/guides/daybreak) and the [access overview](https://help.openai.com/en/articles/20001258). The account must have Daybreak Blue approval. Model choice alone does not turn Daybreak on. In a headless Codex run, pass `-m gpt-6-sol -c daybreak=true` on that command. In an interactive Codex session, turn it on with `/daybreak`. Do not save Daybreak as the default; it can block models without Daybreak support. Confirm the active access program in host status. On the API, send `access_programs.cyber` as `daybreak_blue`. GPT-6.1 Sol and Astra get reduced refusals only with Daybreak Red approval. Without approval, use Astra. It is not a general route. It is not a different-family reviewer of other OpenAI work. Start at `high`. Keep the caller's target and action limits. |
| Grok 4.7 (`grok-4.7`) | Grok | `xhigh` | Independent challenge from another family, research with live web and X context, and second opinions. Runs on a subscription | Use `xhigh`. `low` and `medium` score much lower on the Vals boards. It trails the default routes on independent coding and terminal evaluations. Do not use it as a coding fallback. Verify its factual claims and executed checks. |
| Gemini 4 Argon | OpenCode | `medium` or `high` | Audio, video, and PDF input. Independent challenge and review from a third model family. It is close to Opus 5.5 on the Vals Index and human-preference writing. Use `high` for consequential review and visual coding | It costs the most per task among the OpenCode routes. It trails GPT-6.1 Sol on the Artificial Analysis intelligence index. It leads GPT-6.1 Sol on the Vals Index and on LMArena text. It trails Opus 5.5 on screenshot coding. Check the provider's current price. Use it when its family or modality changes the result. |
| Kimi K3.1 Pro | OpenCode | `high`; `max` for hard lanes | Terminal-heavy challenge, edge-case discovery, long-context multimodal sessions, and different-family challenge | Start each new lane in a fresh session. The harness must pass back its full reasoning and tool history; OpenCode does this. Keep a session that Kimi started on Kimi, because a model switch loses that history. It is slow and verbose. It is weak on science and hard knowledge. Do not use `low`. Use the highspeed route only when a person waits on the output. |
| Muse Wonder 1.0 | OpenCode | `high` to `max` | Defensive cyber review from another family; it leads the Vals CyberBench. Meta-family challenge | It trails Gemini 4 Argon on the Vals Index and Vals Terminal-Bench. Its cost per test is lower, but its token price is higher. Muse Wonder Full is not routable from the fleet. |
| Muse Spark 1.3 | OpenCode | `high` | Multimodal work, visual implementation, knowledge work, and different-family challenge at a moderate cost | It trails on terminal-heavy agent work. On Vals Terminal-Bench, `xhigh` scores lower than `high`. Its native Muse Code harness scores higher than other harnesses. |
| GLM-5.3 | OpenCode | `high` | Open-weight text-only long-context work, defensive security analysis, and different-family challenge | It has no image input. `high` scores higher than `max` on Vals Terminal-Bench. It is slow and verbose, and it costs more per task than its token price suggests. At `max`, its reasoning can reach the model's output limit. [opencode.md](opencode.md) shows how to raise `limit.output`. |
| GLM-5.3 Flash | OpenCode | `high` or `max` | Very low-cost coding, terminal work, automation, tools, and multimodal review | It trails DeepSeek V4.1 Flash on composite evaluations. OpenCode handles its multimodal tasks less well than other harnesses. Confirm the configured route provides the selected effort. |
| DeepSeek V4.1 Flash (1017) | OpenCode | `max` | It ties GLM-5.3 for the top open-weight score on the Artificial Analysis index. It leads GLM-5.3 on the Vals Index. Lowest cost per task for bounded coding and automation | Lower levels score much lower on the Vals boards. It trails GLM-5.3 and GLM-5.3 Flash on terminal work. Never route it to DeepSeek's own API. |
| MiMo V2.6 Pro | OpenCode | none; pass `--no-variant` | Open-weight multimodal work with audio and video input at a low cost | The route has no effort variants. It is slow. It trails Kimi K3.1 Pro and the GLM routes on terminal work. |

GLM-5.3, GLM-5.3 Flash, DeepSeek V4.1 Flash, and MiMo V2.6 Pro have open weights. Check the model card before an open-weight lane uses Kimi K3.1 Pro. Open weights do not keep data local: the selected provider still receives the input. Mark a lane `Unrouted` when its privacy limit excludes every listed provider.

Use [OpenAI's model pages](https://developers.openai.com/api/docs/models) and [Claude's models overview](https://platform.claude.com/docs/en/models/overview) for current API limits and prices.
Use the selected host's context limit and effort controls when they differ from API limits.

### Know the models outside the fleet

These models score well but are not routable from the four worker CLIs:

- Gemini 4 Carbon: restricted access.
- Muse Wonder Full: Meta's Muse Code subscription only.
- Claude Mythos 5.1: approved security programs only.
- Copilot Fusion, Devin Fusion, and Cursor Composer: their own products only.

Check their access on the vendor pages during a fleet review.

These models stay out of the fleet:

- Kimi K3: Kimi K3.1 Pro scores higher on every independent board at a lower price.
- Grok 4.7 Fast: the same model at a higher price.
- DeepSeek V4 Pro: DeepSeek V4.1 Flash scores higher at a lower cost.
- GLM-5.3 Prime and FlashX: no independent evaluations.
- Qwen 3.8 Max: closed weights and a high cost per task.
- MiniMax M3 and M3.1 Flash: low terminal scores, and MiniMax trains on API input.
- Gemini 3.8 Flash: it scores higher on composite evaluations, but GLM-5.3 Flash costs less and scores higher on terminal work.
- Mistral Large 4: no fleet lane fits it, and it has few independent evaluations.

## Select the provider

Try the identifiers for the selected model in order. Skip a route whose data terms the lane does not accept. Treat a route that fails on sign-in, billing, or a missing variant as unavailable, and try the next one.

| Model | Provider order |
|---|---|
| Kimi K3.1 Pro | 1. `openrouter/moonshotai/kimi-k3.1-pro`, pinned to `moonshotai` with zero data retention. 2. `moonshotai/kimi-k3.1-pro`. 3. `moonshotai/kimi-k3.1-pro-highspeed`, only when a person waits on the output |
| Gemini 4 Argon | 1. `cloudflare-ai-gateway/google/gemini-4-argon`, when the output fits its 65,536-token limit and the lane accepts Google API terms and gateway logs. 2. `openrouter/google/gemini-4-argon`, pinned to `google-vertex` with zero data retention |
| GLM-5.3 | 1. `cloudflare-workers-ai/@cf/zai-org/glm-5.3`. 2. `openrouter/z-ai/glm-5.3`, pinned to `cloudflare` with zero data retention |
| GLM-5.3 Flash | 1. `cloudflare-workers-ai/@cf/zai-org/glm-5.3-flash`. 2. `openrouter/z-ai/glm-5.3-flash`, pinned to `z-ai` with zero data retention. 3. `opencode/glm-5.3-flash-free`, when the lane fits its smaller context and output limits |
| DeepSeek V4.1 Flash | 1. `cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v4.1-flash-1017`. 2. `openrouter/deepseek/deepseek-v4.1-flash-1017`, pinned to `cloudflare` with zero data retention. 3. `opencode/deepseek-v4.1-flash-free`, when the lane fits its smaller context and output limits |
| Muse Spark 1.3 | 1. `openrouter/meta/muse-spark-1.3-contributor`, only when contributor terms are accepted. 2. `openrouter/meta/muse-spark-1.3`. Pin both to `meta`; no zero-retention host exists |
| Muse Wonder 1.0 | `openrouter/meta/muse-wonder`, pinned to `meta`. No zero-retention host exists |
| MiMo V2.6 Pro | `openrouter/xiaomi/mimo-v2.6-pro`, pinned to `deepinfra` with zero data retention |

Follow these host rules:

- Pin each OpenRouter route as the table says. Without a pin, OpenRouter can choose a low-precision host that collects data. [opencode.md](opencode.md) shows the pin.
- Require zero data retention only where the table says so. Muse routes have no zero-retention host. Skip them when a lane requires zero retention.
- Cloudflare Workers AI `@cf/` routes keep no data and do not train on it. Other Cloudflare identifiers pass the request to the upstream provider under its terms.
- Cloudflare AI Gateway logs request payloads by default, as its [logging page](https://developers.cloudflare.com/ai-gateway/observability/logging/) states. Its Muse routes end streams without a finish signal; do not use them.
- Contributor routes and some free routes train on the input. Use them only when the caller's lane contract accepts their data terms. Without that statement, treat the terms as not accepted.
- NVIDIA API routes are for trial use only. Do not use them for fleet work.
- Check the selected route's effort values in the OpenCode catalog, as [opencode.md](opencode.md) shows. Values differ between providers for one model.

## Map effort to the worker CLI

Use the host's installed controls. These forms show the intended mapping:

| Worker CLI | Model control | Effort control |
|---|---|---|
| Claude | `--model <alias-or-id>` | `--effort low|medium|high|xhigh|max` within the selected route's policy |
| Codex | `-m <model-id>` | `-c model_reasoning_effort="low|medium|high|xhigh|max|ultra"` within the selected route's policy |
| Grok | `-m <grok-model-id>` | `--reasoning-effort low|medium|high|xhigh` |
| OpenCode | `-m <provider/model>` on `opencode run`; `model` in `opencode.json` or `/models` in the TUI | `#<provider-supported-value>` appended to the model, as `-m <provider/model>#<value>` |

Do not translate effort names as equal compute across providers. Choose the level within the selected model's supported range.

Check Codex identifiers and effort controls with targeted host status or `codex debug models`.
The Codex host's `ultra` mode includes automatic delegation; it is not a portable API effort value.

## Pair independent reviewers

- Review OpenAI work with Opus 5.5, Fable 5.1, Sonnet 5.5, or Gemini 4 Argon.
- Review Opus 5.5, Sonnet 5.5, Haiku 5.5, or Fable 5.1 work with GPT-6.1 Sol, Astra, or Gemini 4 Argon. The Claude models are one family.
- Review Gemini 4 Argon work with Opus 5.5, GPT-6.1 Sol, or Astra.
- Review Grok, Kimi, GLM, DeepSeek, MiMo, or Muse work with GPT-6.1 Sol, Astra, Opus 5.5, or Gemini 4 Argon.
- Kimi K3.1 Pro can review code and terminal work from another family. Do not use it to review science or research.
- Use Kimi K3.1 Pro, Grok 4.7, Muse, GLM-5.3, or DeepSeek V4.1 Flash as extra challengers. Their findings need reproduction.

When no listed reviewer is available, mark the review lane `Unrouted`. Do not promote an extra challenger to reviewer.

Give the reviewer the artifact and requirements. Keep the author's reasoning out of the initial review context.

## Review the fleet

Review the fleet when a listed model gets a successor. Also review it when a new model tops an independent board.

- Compare every model on the same independent yardsticks.
- Use the [Vals Index](https://www.vals.ai/benchmarks/vals_index) and [Vals Terminal-Bench](https://www.vals.ai/benchmarks/terminal-bench-4).
- Use the [Artificial Analysis leaderboard](https://artificialanalysis.ai/leaderboards/models) and its [coding-agent index](https://artificialanalysis.ai/agents/coding-agents).
- Use [LMArena](https://lmarena.ai/leaderboard) for human preference.
- Label vendor-reported scores as vendor claims.
- Compare the cost per task, not the token price.
- Check the score at each effort level before you set an effort range.
- Run one tool-using task on each provider route before you list it.
