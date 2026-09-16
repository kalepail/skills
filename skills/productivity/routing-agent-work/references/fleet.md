# Fixed Agent Fleet

Use this reference only after a lane has a bounded output. It provides routing clues, not an overall model ranking.

## Codex preference

Prefer GPT-6 Astra at `high` for most Codex work.
Consider Astra at `medium` for small, well-defined tasks and `low` for trivial, readily checked tasks.
Consider those settings before choosing GPT-5.6 Sol to reduce cost or latency.
Keep Sol for explicit requests, unavailable Astra access, or a demonstrated task-specific cost or latency advantage.
Use Terra or Luna when their bounded, budget-sensitive role fits. Do not make them the default for ordinary Codex work.

## Muse provider selection

Use only Muse Spark 1.3 for Muse routes. Prefer contributor routes after explicit acceptance of their data terms.

Try these identifiers in order:

1. `meta/muse-spark-1.3-contributor`
2. `openrouter/meta/muse-spark-1.3-contributor`
3. `opencode/muse-spark-1.3-contributor-free`
4. `meta/muse-spark-1.3`
5. `openrouter/meta/muse-spark-1.3`

Use `opencode models --refresh` before rejecting a recent identifier. Advance to the next identifier when the selected route remains unavailable.

Skip contributor routes when their data terms are not accepted.
Check effort support for the selected identifier, not only the model family.
If no supported effort meets the task requirement, advance through the provider list before changing models.
Full Meta 1.3 and OpenRouter 1.3 routes expose `max`; confirm the selected contributor route separately.

Do not select a Muse Spark 1.2 route.

## Route by lane

| Primary lane | First route | Fallbacks, in order |
|---|---|---|
| Ambiguous planning, architecture, orchestration, or synthesis | Claude with Fable 5.1 | Claude with Opus 5; Codex with GPT-6 Astra; GPT-5.6 Sol |
| Difficult implementation, refactoring, debugging, or test construction | Claude with Opus 5 | Codex with GPT-6 Astra; Claude with Fable 5.1; GPT-5.6 Sol |
| Terminal workflows, primary verification, or acting on gathered evidence | Codex with GPT-6 Astra | GPT-5.6 Sol; Claude with Opus 5; Grok 4.6 |
| Bounded implementation, repository sweep, data collection, or tool calling | Codex with GPT-6 Astra | GPT-5.6 Sol; GPT-5.6 Terra for bounded work; Grok 4.6 |
| Budget-sensitive bounded coding or repository sweeps | Codex with GPT-5.6 Terra | GPT-6 Astra at medium; GPT-5.6 Sol |
| Narrow high-volume extraction or triage | Codex with GPT-5.6 Luna | GPT-5.6 Terra |
| Security review, authorized vulnerability exploration, or patch validation | Codex with Daybreak Blue | GPT-6 Astra; Claude with Opus 5; OpenCode with GLM-5.3 for text-only input |
| Precision review or quality-first technical prose | Claude with Opus 5 | Fable 5.1; GPT-6 Astra; GPT-5.6 Sol; GLM-5.3 Flash; Grok 4.6 |
| Independent research, test execution, coding, or adversarial challenge | Grok 4.6 | Kimi K3; GLM-5.3 Flash; GPT-6 Astra; GPT-5.6 Sol |
| Text-only long-context coding, complex agent work, or long-horizon implementation | OpenCode with GLM-5.3 | Kimi K3; GPT-6 Astra; GPT-5.6 Sol |
| Preserved-reasoning multimodal sessions or long-horizon work | OpenCode with Kimi K3 | Muse Spark 1.3; GLM-5.3 when the input is text-only; GPT-6 Astra; GPT-5.6 Sol |
| General multimodal long-context or multimodal agentic knowledge work | OpenCode with Muse Spark 1.3 | Kimi K3 when the harness preserves full history; GPT-6 Astra; GPT-5.6 Sol |
| Cost-sensitive agentic coding, automation, multimodal review, or structured technical prose | OpenCode with GLM-5.3 Flash | Muse Spark 1.3; Grok 4.6; GPT-6 Astra; GPT-5.6 Sol |
| Visual implementation from screenshots, PDFs, or designs; long-horizon multimodal creation | OpenCode with Muse Spark 1.3 | GLM-5.3 Flash; GPT-6 Astra; GPT-5.6 Sol |

## Know each route

| Model | Worker CLI | Effort | Strong clues | Limits and keep-away clues |
|---|---|---|---|---|
| Fable 5.1 | Claude | `high` to `max` | Ambiguous planning, architecture, orchestration, synthesis, autonomous difficult work, and agentic knowledge work | Prefer `xhigh` for quality-first work. Use `max` only when the failure cost justifies its much higher token use. Give it a clear completion check and stop budget. |
| GPT-6 Astra (`gpt-6-astra`) | Codex | `low` to `max`; host `ultra` mode when permitted | Default Codex work, difficult coding, verification, research, computer use, and synthesis | Start at `high`. Use `medium` or `low` only for the bounded cases above. Prefer `xhigh` or `max` when difficulty warrants it. |
| GPT-5.6 Sol (`gpt-5.6-sol`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Retained coding, testing, and verification fallback | Prefer Astra first, including Astra at lower effort for suitable tasks. Honor an explicit Sol request. |
| GPT-5.6 Terra | Codex | `medium` to `max`; host `ultra` mode when permitted | Budget-sensitive bounded coding, repository sweeps, data collection, tool calling, and triage | Usually use `medium` or `high`. Give consequential interpretation or final action to Astra, Opus, or Fable 5.1. |
| GPT-5.6 Luna | Codex | `high` to `max` | Narrow, high-volume extraction and triage when cost matters | Start at `high`. Use `xhigh` or `max` only when a local task sample shows a material gain. Keep the lane small. Prefer Terra when recall or judgment matters. |
| Opus 5 | Claude | `high` to `max` | Quality-first coding, debugging, precision review, computer use, and technical prose | Prefer `xhigh` for coding. Use `max` for the hardest knowledge work. It need not own a separate prose lane. |
| Daybreak Blue (`gpt-daybreak-blue-latest`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Security reviews, authorized vulnerability exploration, and patch validation | Start at `high`. Confirm access for the selected host and account. Keep the caller's target and action limits. Treat its underlying OpenAI model as the same family for review. |
| Grok 4.6 | Grok | `medium` to `xhigh` | Research, tool use, coding, testing, challenge, and independent review | Verify factual claims and executed checks. Use Grok 4.6 only. |
| GLM-5.3 | OpenCode | `high` or `max` | Text-only long-context coding, complex agents, long-horizon implementation, and defensive security analysis | It has no image input. Prefer `max` for complex coding. Prefer Kimi when vision or preserved reasoning history matters. |
| Kimi K3 | OpenCode | `high` or `max` | Multimodal long context, preserved-reasoning sessions, long-horizon coding, research, and knowledge work | Start fresh. The harness must preserve its full reasoning and tool history. Prefer GLM-5.3 for text-only work when speed or cost matters. |
| GLM-5.3 Flash | OpenCode | `high` or `max` | Efficient coding, automation, tools, multimodal work, review, and prose | Prefer full GLM-5.3 for hard text-only long-horizon work. Confirm the configured route provides high or max reasoning. |
| Muse Spark 1.3 | OpenCode | `medium` to `max`, subject to provider support | Multimodal work, visual implementation, agentic workflows, and long-horizon coding | Follow the provider order above among routes that meet the task's effort and data requirements. Results depend strongly on the harness. |

## Map effort to the worker CLI

Use the host's installed controls. These forms show the intended mapping:

| Worker CLI | Model control | Effort control |
|---|---|---|
| Claude | `--model <alias-or-id>` | `--effort medium|high|xhigh|max` |
| Codex | `-m <model-id>` | `-c model_reasoning_effort="low|medium|high|xhigh|max|ultra"` within the selected route's policy |
| Grok | `-m <grok-model-id>` | `--reasoning-effort medium|high|xhigh` |
| OpenCode | `-m <provider/model>` | `--variant <provider-supported-value>` |

Do not translate effort names as equal compute across providers. Choose the level within the selected model's supported range.

Check Codex identifiers and effort controls with targeted host status or `codex debug models`.
The Codex host's `ultra` mode includes automatic delegation; it is not a portable API effort value.
Consult [OpenAI model documentation](https://developers.openai.com/api/docs/models) when an API surface differs from the host.

## Pair independent reviewers

- Review Astra, Sol, Terra, Luna, or Daybreak work with Fable 5.1, Opus, Grok, GLM-5.3, or GLM-5.3 Flash.
- Review Fable 5.1 or Opus work with Astra, Grok, GLM-5.3, or GLM-5.3 Flash.
- Review Grok work with Astra, Fable 5.1, or Opus.
- Review Kimi, either GLM route, or Muse work with Astra, Fable 5.1, or Opus.

Use Daybreak for security work when it provides the required reviewer independence. Use Sol when the Codex preference permits it.

Give the reviewer the artifact and requirements. Keep the author's reasoning out of the initial review context.
