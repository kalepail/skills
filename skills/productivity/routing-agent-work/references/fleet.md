# Fixed Agent Fleet

Use this reference only after a lane has a bounded output. It provides routing clues, not an overall model ranking.

Every route names a model family. The router resolves the family to its newest model when it launches the route, as "Resolve the family" describes. A new version of a listed family needs no edit.

## Know the cost basis

The fleet owner pays for each worker CLI in one of two ways. Use the cost basis as the cost tie-breaker.

- **Subscription routes:** Claude, Codex, and Grok signed in with their subscriptions have weekly limits. A task costs weekly-limit headroom, not dollars.
- **API routes:** OpenCode routes bill per token from API accounts. A Codex run that signs in with an API key is also an API route.
- **API accounts:** Spend from Cloudflare first, then OpenRouter. The other API accounts have tighter limits. Use them only when the family has no Cloudflare or OpenRouter route.

Apply these rules:

- When an API route and a subscription route both meet the quality bar, use the subscription route.
- Use an API route when it gives a needed modality, model family, open weights, or quality level.
- Before a large lane, read the selected subscription's weekly headroom from host status.
- When one subscription is low, move bounded lanes to another subscription CLI first. Then use OpenCode.
- On Claude, all families share one weekly limit. Fable can use at most half of that limit, and it uses the limit fastest.
- Luna, Terra, Haiku, GLM Flash, DeepSeek Flash, and Muse Ember are the low-cost routes. Check the provider's current price before an API lane depends on a cost difference.

## Default route for each worker CLI

| Worker CLI | Default route | Escalation | Keep for |
|---|---|---|---|
| Claude | Opus at `high` | Opus at `xhigh`, then Fable at `high` or `xhigh` with a stop budget | Planning, difficult implementation, review, and prose |
| Codex | Sol at `high` | Sol at `xhigh` or `max`; Astra for science, research, and final interpretation | Implementation, terminal work, verification, and sweeps |
| Grok | Grok at `xhigh` | None | Independent challenge and live web or X research |
| OpenCode | Set by the lane table | Set by the lane table | Other model families, multimodal input, open weights, and low-cost lanes |

When the caller pins a worker CLI, use the lane row's first route on that CLI. If the row has none, use a route on that CLI whose strong clues fit the lane. Otherwise, mark the lane `Unrouted`. A pinned Grok CLI has no coding route.

## Resolve the family

Resolve only the selected route, on the host that launches the worker. Listings differ by host and account. Record the resolved identifier on the route card.

- **Claude.** Pass the alias `opus`, `fable`, `sonnet`, or `haiku` to `--model`. The alias selects the family's newest model. The worker's report states the model the session ran.
- **Codex, Grok, and OpenCode.** Run `python3 <skill-dir>/scripts/resolve_model.py --cli <codex|grok|opencode> --pattern '<regex>'`. It reads the CLI's own listing and prints one JSON line. Repeat `--pattern` once per provider row, in provider order. Pass `--dir <work-dir>` for OpenCode, because its catalog is project-specific. Run it with `--help` for the matching rules.

| Family | Worker CLI | `--pattern` |
|---|---|---|
| Sol | Codex | `gpt-(?P<v>[0-9.]+)-sol` |
| Astra | Codex | `gpt-(?P<v>[0-9.]+)-astra` |
| Terra | Codex | `gpt-(?P<v>[0-9.]+)-terra` |
| Luna | Codex | `gpt-(?P<v>[0-9.]+)-luna` |
| Sol under Daybreak Blue | Codex | The Sol pattern, with `--access-program daybreak_blue` |
| Grok | Grok | `grok-(?P<v>[0-9.]+)` |
| Each OpenCode family | OpenCode | The patterns in "Select the provider", in order |

Read the result:

- Exit 0: launch `resolved`. If that identifier fails on sign-in, billing, or a missing variant, try each identifier in `alternates`, which carry the same version on later provider rows.
- A row in `stale` carries only an older version. Never launch it.
- Exit 1 (no match) and exit 3 (ambiguous): the family is unavailable. Take the next fallback and flag the fleet for review.
- Exit 4: the listing failed or could not be parsed. Read the listing by hand with the CLI's own command, or take the next fallback.
- Exit 64: the call is wrong. Fix it.

Follow these resolution rules:

- Patterns match the whole identifier, so sibling tiers and speed variants fall out. Speed variants are a mode of their family, never a family: Grok `-build-fast`, Kimi `-highspeed`, MiMo `-ultraspeed`, and the Codex `fast` and `ultrafast` service tiers. The one fleet use is the Kimi highspeed provider row, which resolves in its own call.
- Do not use the OpenRouter `~<vendor>/<family>-latest` aliases. They hide the model they run, so the provider pin, the effort variants, and the run record cannot name it.
- Do not select `gpt-daybreak-blue-latest`. It does not name the model it runs.
- DeepSeek Flash patterns require the four-digit snapshot suffix. A second snapshot of the same version fails closed with exit 3 and triggers a fleet review.
- A family whose newest release drops its tier name no longer matches. Take the next fallback and flag the fleet for review.

## Route by lane

The bounded rows are the bounded implementation, budget, and extraction rows. Use them only for narrow work with readily checked output. Treat migrations and multi-file features as difficult implementation. Use the budget row only when the caller states a cost or headroom limit.
For difficult implementation under a stated cost limit, use Sol at `xhigh` or `max`. Give the lane a stop budget.
Security lanes keep the caller's target and action limits on every route and fallback.

| Primary lane | First route | Fallbacks, in order |
|---|---|---|
| Ambiguous planning, architecture, orchestration, or synthesis | Claude with Opus | Fable; Astra; Sol |
| Difficult implementation, refactoring, debugging, or test construction | Claude with Opus | Fable at `high`; Sonnet at `max`; Sol at `max`; Kimi at `high`; Astra |
| Terminal workflows, primary verification, or acting on gathered evidence | Codex with Sol | Opus; Sonnet at `max`; Kimi at `high`; Astra |
| Bounded implementation, repository sweep, data collection, or tool calling | Codex with Sol at `medium` | Terra at `xhigh`; Opus at `medium`; Muse Ember at `max`; DeepSeek Flash at `max` |
| Budget-sensitive bounded coding or repository sweeps | Codex with Sol at `medium` | Terra at `xhigh`; Haiku at `max`; Muse Ember at `max`; DeepSeek Flash at `max` |
| Narrow high-volume extraction or triage | Codex with Luna at `max` | Terra at `medium`; Haiku at `high`; Muse Ember at `max`; DeepSeek Flash at `max` |
| Security review, authorized vulnerability exploration, or patch validation | Codex with Sol under Daybreak Blue access | Astra; Sol; Opus for defensive review of the caller's own code; Muse Wonder or Gemini Carbon for defensive review; GLM for text-only input |
| Precision review or quality-first technical prose | Claude with Opus | Fable; Gemini Carbon at `high`; Sonnet at `max`; Astra; Sol |
| Independent challenge or second opinion | OpenCode with Gemini Carbon at `medium` | Kimi at `high`; Grok; GLM at `high`; Muse Ember at `max` |
| Live web and X research | Grok | Astra and Opus for web research only |
| Edge-case discovery and confirmation across model families | OpenCode with Kimi at `high` | Gemini Carbon at `medium`; GLM at `high` for text-only input; Grok; Muse Ember at `max`; DeepSeek Flash at `max` |
| Visual implementation, screenshots, or long-context documents | Claude with Opus | Fable at `high`; Sol; Gemini Carbon at `high`; Kimi at `high` |
| Audio or video input, or multimodal work that needs another model family | OpenCode with Gemini Carbon at `medium` | Muse Ember at `max`; MiMo Pro for open-weight input |
| Text-only long-context work that needs an open-weight model | OpenCode with GLM at `high` | DeepSeek Flash at `max`; GLM Flash at `high` |
| Open-weight automation, multimodal review, or structured prose | OpenCode with DeepSeek Flash at `max` | GLM Flash at `high`; MiMo Pro |

For an independent challenge under a tight API budget, start with Grok. It runs on a subscription.
When the Claude weekly limit makes Opus unavailable, skip the other Claude fallbacks in the row. They share that limit.
When Fable has used its half of the Claude weekly limit, treat it as unavailable. Escalate Opus to `max` with a stop budget, or use the next fallback.

## Treat challenger findings as leads

The challenger families are GLM, GLM Flash, DeepSeek Flash, MiMo Pro, Muse Ember, Muse Wonder, and Grok. They are not default routes.
Use them for cost, modality, open weights, or a different model family.
Treat their findings as leads, not verdicts.
Reproduce a finding with a test, command, or cited source before a stronger route acts on it.
Run two or three of them in parallel when the lane needs diverse edge cases. For one run, follow the order in the edge-case row.
Launch headless OpenCode runs as [opencode.md](opencode.md) describes. A run can end with no answer and exit code 0.
Discard a finding that no check reproduces.
When one of these families owns a lane, accept its result only after the lane's completion check passes.

## Know each route

| Family | Worker CLI | Effort | Strong clues | Limits and keep-away clues |
|---|---|---|---|---|
| Opus | Claude | `medium` to `xhigh`; `max` only when Fable is unavailable | Default Claude route for everyday work. Planning, orchestration, synthesis, difficult coding, debugging, long unattended migrations, code review, knowledge work, computer use, screenshots, and technical prose | `high` is the efficient choice when its quality meets the lane. Above `xhigh`, escalate to Fable. Give `max` a clear stop budget. Give unattended runs a completion check and a stop budget. A turn that ends in text is a progress report, not proof of completion. Use Opus when terminal failure cost is high. Cyber safeguards can hand security work to a model outside the fleet. Use Opus only for defensive review of the caller's own code. |
| Fable | Claude | `high` or `xhigh` | Claude escalation for the hardest planning, implementation, science, and research lanes. Prose and visual fallback | It uses the Claude weekly limit fastest, and it can use at most half of it. Opus is the default for everyday work. Do not use `max`. Set the effort explicitly; do not rely on the Claude Code default. Cyber safeguards can hand security work to a model outside the fleet. |
| Sonnet | Claude | `xhigh` or `max` | Fallback when Opus is unavailable | Do not route Sonnet below `xhigh`. It shares the Claude weekly limit with Opus. Cyber safeguards can hand security work to a model outside the fleet. Do not route vulnerability exploration to it. |
| Haiku | Claude | `high` or `max` | Low-headroom Claude route for extraction, triage, and small bounded tasks | Keep consequential interpretation on a stronger route. |
| Sol | Codex | `medium` to `max`; host `ultra` mode when permitted | Default Codex route. Complex coding, terminal work, verification, agent workflows, computer use, and repeated long-running work | Use `max` for hard lanes with a stop budget. Use Opus when terminal failure cost is high. |
| Astra | Codex | `high` to `max`; host `ultra` mode when the host confirms it | Codex escalation for science, difficult research, and final consequential interpretation. Different-family alternative to Fable for that work | Keep ordinary coding on Sol, not Astra. Use `high` or `xhigh`. Use `max`, or host `ultra`, only for the hardest lanes with a stop budget. |
| Terra | Codex | `medium` to `xhigh` | Low-cost Codex route for bounded coding, extraction, computer use, and screenshots | Keep difficult lanes on Sol. |
| Luna | Codex | `high` or `max` | Narrow, high-volume extraction and triage | Use `max`; it scores higher than `high`. Use `high` only when the cost per call dominates. Keep the lane small. Give consequential interpretation to Sol, Astra, or Opus. |
| Sol under Daybreak Blue | Codex | `medium` to `max`; host `ultra` mode when permitted | Defensive cybersecurity reviews when refusal calibration matters. Daybreak Blue gives it reduced refusals | Daybreak is an access program, not a family. Resolve the newest Sol whose catalog entry lists `daybreak_blue`. A Sol or Astra version whose catalog entry does not list `daybreak_blue` is not a Daybreak Blue route. Check the eligible models on the [Daybreak guide](https://developers.openai.com/api/docs/guides/daybreak) and the [access overview](https://help.openai.com/en/articles/20001258). The account must have Daybreak Blue approval. Model choice alone does not turn Daybreak on. In a headless Codex run, pass `-m <resolved> -c daybreak=true` on that command. In an interactive Codex session, turn it on with `/daybreak`. Do not save Daybreak as the default; it can block models without Daybreak support. Confirm the active access program in host status. On the API, send `access_programs.cyber` as `daybreak_blue`. Without approval, use Astra. It is not a general route. It is not a different-family reviewer of other OpenAI work. Start at `high`. Keep the caller's target and action limits. |
| Grok | Grok | `xhigh` | Independent challenge from another family, research with live web and X context, and second opinions. Runs on a subscription | Use `xhigh`. Do not use it as a coding fallback. Verify its factual claims and executed checks. |
| Gemini Carbon | OpenCode | `medium` or `high` | Audio, video, and PDF input. Independent challenge and review from a third model family. Use `high` for consequential review and visual coding | It is not a low-cost route. Check the provider's current price. Use it when its family or modality changes the result. |
| Kimi | OpenCode | `high`; `max` for hard lanes | Terminal-heavy challenge, edge-case discovery, long-context multimodal sessions, and different-family challenge | Start each new lane in a fresh session. The harness must pass back its full reasoning and tool history; OpenCode does this. Keep a session that Kimi started on Kimi, because a model switch loses that history. Do not use `low`. Use the highspeed route only when a person waits on the output. |
| Muse Wonder | OpenCode | `high` to `max` | Defensive cyber review from another family. Meta-family challenge | Muse Wonder Full is not routable from the fleet. |
| Muse Ember | OpenCode | `xhigh` or `max` | Low-cost route for bounded coding, extraction, triage, tool calling, and Meta-family challenge. Text, image, audio, video, and PDF input | Keep consequential interpretation on a stronger route. Use `max`. It has closed weights. |
| GLM | OpenCode | `high` | Open-weight text-only long-context work, defensive security analysis, and different-family challenge | It has no image input. Use `high`, not `max`. At `max`, its reasoning can reach the model's output limit. [opencode.md](opencode.md) shows how to raise `limit.output`. |
| GLM Flash | OpenCode | `high` or `max` | Very low-cost open-weight coding, terminal work, automation, tools, and multimodal review | Use it when the lane needs open weights. OpenCode handles its multimodal tasks less well than other harnesses. Confirm the configured route provides the selected effort. |
| DeepSeek Flash | OpenCode | `max` | Low-cost open-weight route for bounded coding and automation | Use `max`. Never route it to DeepSeek's own API. |
| MiMo Pro | OpenCode | none; pass `--no-variant` | Open-weight multimodal work with audio and video input at a low cost | The route has no effort variants. |

GLM, GLM Flash, DeepSeek Flash, and MiMo Pro have open weights. Check the model card before an open-weight lane uses Kimi. Open weights do not keep data local: the selected provider still receives the input. Mark a lane `Unrouted` when its privacy limit excludes every listed provider.

Use [OpenAI's model pages](https://developers.openai.com/api/docs/models) and [Claude's models overview](https://platform.claude.com/docs/en/models/overview) for current API limits and prices.
Use the selected host's context limit and effort controls when they differ from API limits.

### Know the models outside the fleet

A fleet review adds a family only after it beats a listed family on the independent boards. A family that the tables do not list is not a route. The identifier patterns exclude sibling tiers.

These models are not routable from the four worker CLIs:

- Muse Wonder Full: Meta's Muse Code subscription only.
- Claude Mythos: Anthropic's approved cybersecurity and life-sciences programs only.
- Copilot Fusion, Devin Fusion, and Cursor Composer: their own products only.

Check their access on the vendor pages during a fleet review.

These stay out of the fleet:

- Grok fast variants and every other speed variant: the same model at a higher price.
- MiniMax: it trains on API input.

## Select the provider

Resolve the family with every row's pattern in one call, in this order. The result is the first row that carries the newest version. Skip a row whose data terms the lane does not accept. Treat a route that fails on sign-in, billing, or a missing variant as unavailable, and try `alternates`, then the next fallback.

| Family | Provider order |
|---|---|
| Kimi | 1. `openrouter/moonshotai/kimi-k(?P<v>[0-9.]+)(-pro)?`, pinned to `moonshotai` with zero data retention. 2. `moonshotai/kimi-k(?P<v>[0-9.]+)(-pro)?`. Highspeed, in its own call and only when a person waits on the output: `moonshotai/kimi-k(?P<v>[0-9.]+)-pro-highspeed` |
| Gemini Carbon | `openrouter/google/gemini-(?P<v>[0-9.]+)-carbon`, pinned to `google-vertex` with zero data retention |
| GLM | 1. `cloudflare-workers-ai/@cf/zai-org/glm-(?P<v>[0-9.]+)`. 2. `openrouter/z-ai/glm-(?P<v>[0-9.]+)`, pinned to `cloudflare` with zero data retention |
| GLM Flash | 1. `cloudflare-workers-ai/@cf/zai-org/glm-(?P<v>[0-9.]+)-flash`. 2. `openrouter/z-ai/glm-(?P<v>[0-9.]+)-flash`, pinned to `z-ai` with zero data retention. 3. `opencode/glm-(?P<v>[0-9.]+)-flash-free`, when the lane fits its smaller context and output limits |
| DeepSeek Flash | 1. `cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v(?P<v>[0-9.]+)-flash-[0-9]{4}`. 2. `openrouter/deepseek/deepseek-v(?P<v>[0-9.]+)-flash-[0-9]{4}`, pinned to `cloudflare` with zero data retention. 3. `opencode/deepseek-v(?P<v>[0-9.]+)-flash-free`, when the lane fits its smaller context and output limits |
| Muse Ember | `openrouter/meta/muse-ember(-(?P<v>[0-9.]+))?`, pinned to `google-vertex` with zero data retention |
| Muse Wonder | `openrouter/meta/muse-wonder(-(?P<v>[0-9.]+))?`, pinned to `meta`. No zero-retention host exists |
| MiMo Pro | `openrouter/xiaomi/mimo-v(?P<v>[0-9.]+)-pro`, pinned to `deepinfra` with zero data retention |

Follow these host rules:

- Pin each OpenRouter route as the table says. Without a pin, OpenRouter can choose a low-precision host that collects data. [opencode.md](opencode.md) shows the pin.
- Require zero data retention only where the table says so. Muse Wonder has no zero-retention host. Skip it when a lane requires zero retention.
- Google Vertex output limits differ by region on OpenRouter. When a long output stops at the limit, pin a region with a larger limit, as the OpenRouter endpoint list shows.
- Cloudflare Workers AI `@cf/` routes keep no data and do not train on it. Other Cloudflare identifiers pass the request to the upstream provider under its terms.
- Cloudflare AI Gateway logs request payloads by default, as its [logging page](https://developers.cloudflare.com/ai-gateway/observability/logging/) states. Its Muse routes end streams without a finish signal; do not use them.
- Contributor routes and some free routes train on the input. Use them only when the caller's lane contract accepts their data terms. Without that statement, treat the terms as not accepted.
- NVIDIA API routes are for trial use only. Do not use them for fleet work.
- Check the selected route's effort values in the OpenCode catalog, as [opencode.md](opencode.md) shows. Values differ between providers for one family.

## Map effort to the worker CLI

Use the host's installed controls. These forms show the intended mapping:

| Worker CLI | Model control | Effort control |
|---|---|---|
| Claude | `--model <alias-or-id>` | `--effort low|medium|high|xhigh|max` within the selected route's policy |
| Codex | `-m <model-id>` | `-c model_reasoning_effort="low|medium|high|xhigh|max|ultra"` within the selected route's policy |
| Grok | `-m <grok-model-id>` | `--reasoning-effort low|medium|high|xhigh` |
| OpenCode | `-m <provider/model>` on `opencode run`; `model` in `opencode.json` or `/models` in the TUI | `#<provider-supported-value>` appended to the model, as `-m <provider/model>#<value>` |

Do not translate effort names as equal compute across providers. Choose the level within the selected family's supported range.

Check Codex effort controls with targeted host status or `codex debug models`.
The Codex host's `ultra` mode includes automatic delegation; it is not a portable API effort value.

## Pair independent reviewers

- Review OpenAI work with Opus, Fable, Sonnet, or Gemini Carbon.
- Review Opus, Sonnet, Haiku, or Fable work with Sol, Astra, or Gemini Carbon. The Claude families are one model family.
- Review Gemini Carbon work with Opus, Fable, Sol, or Astra.
- Review Grok, Kimi, GLM, DeepSeek, MiMo, or Muse work with Sol, Astra, Opus, or Gemini Carbon.
- Kimi can review code and terminal work from another family. Do not use it to review science or research.
- Use Kimi, Grok, Muse, GLM, or DeepSeek Flash as extra challengers. Their findings need reproduction.

When no listed reviewer is available, mark the review lane `Unrouted`. Do not promote an extra challenger to reviewer.

Give the reviewer the artifact and requirements. Keep the author's reasoning out of the initial review context.

## Review the fleet

Review the fleet when a new model family appears, a listed family leaves the listings, or a new family tops an independent board. Also review it when a resolved version rejects a listed effort value, or drops a modality or access program that a lane row relies on. A new version of a listed family needs no edit; it routes at once through resolution.

- Compare every model on the same independent yardsticks.
- Use the [Vals Index](https://www.vals.ai/benchmarks/vals_index) and [Vals Terminal-Bench](https://www.vals.ai/benchmarks/terminal-bench-4).
- Use the [Artificial Analysis leaderboard](https://artificialanalysis.ai/leaderboards/models) and its [coding-agent index](https://artificialanalysis.ai/agents/coding-agents).
- Use [LMArena](https://lmarena.ai/leaderboard) for human preference.
- Label vendor-reported scores as vendor claims.
- Compare the cost per task, not the token price.
- Check the score at each effort level before you set an effort range.
- Run one tool-using task on each provider route before you list it.
