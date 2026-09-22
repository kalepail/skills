# Fixed Agent Fleet

Use this reference only after a lane has a bounded output. It provides routing clues, not an overall model ranking.

## Codex preference

Prefer GPT-6 Astra at `high` for most Codex work.
Consider Astra at `medium` for small, well-defined tasks and `low` for trivial, readily checked tasks.
Consider those settings before choosing GPT-6 Sol to reduce cost or latency.
Keep Sol for explicit requests, unavailable Astra access, or a demonstrated task-specific cost or latency advantage.
Use Luna for narrow high-volume extraction.
For Codex-pinned budget work, consider Sol before Terra when Astra exceeds the budget and the task estimates fit.
Use Terra when Sol is unavailable or its measured task cost exceeds the budget.
Keep Astra as the default for ordinary Codex work.

Use [Sol's model page](https://developers.openai.com/api/docs/models/gpt-6-sol) and [Luna's model page](https://developers.openai.com/api/docs/models/gpt-6-luna) for API capabilities and pricing.
Their documented roles support these placements; they do not establish a benchmark ranking against the other fleet models.
Use the selected host's context limit and effort controls when they differ from API limits.

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

Use the bounded rows only for narrow work with readily checked output. Treat migrations and multi-file features as difficult implementation. Use the budget row only when the caller states a cost limit.

| Primary lane | First route | Fallbacks, in order |
|---|---|---|
| Ambiguous planning, architecture, orchestration, or synthesis | Claude with Opus 5.5 | Claude with Fable 5.1; Codex with GPT-6 Astra; GPT-6 Sol |
| Difficult implementation, refactoring, debugging, or test construction | Claude with Opus 5.5 | Claude with Fable 5.1; Codex with GPT-6 Astra; Grok 4.7; GPT-6 Sol |
| Terminal workflows, primary verification, or acting on gathered evidence | Codex with GPT-6 Astra | Claude with Opus 5.5; Claude with Fable 5.1; OpenCode with GLM-5.3 for text-only input; Grok 4.7; GPT-6 Sol |
| Bounded implementation, repository sweep, data collection, or tool calling | Codex with GPT-6 Astra | Claude with Opus 5.5 at medium; Grok 4.7; GPT-6 Sol; GPT-5.6 Terra for bounded work |
| Budget-sensitive bounded coding or repository sweeps | Claude with Opus 5.5 at medium | Grok 4.7 at high; Codex with GPT-6 Astra at medium when the budget allows it; GPT-6 Sol when task estimates fit; GPT-5.6 Terra when the caller pins Codex or no earlier route is available |
| Narrow high-volume extraction or triage | Codex with GPT-6 Luna | GPT-6 Sol; GPT-5.6 Terra |
| Security review, authorized vulnerability exploration, or patch validation | Codex with Daybreak Blue | GPT-6 Astra; Claude with Opus 5.5 for defensive review of the caller's own code; OpenCode with GLM-5.3 for text-only input |
| Precision review or quality-first technical prose | Claude with Opus 5.5 | Fable 5.1; GPT-6 Astra; Grok 4.7; GPT-6 Sol; GLM-5.3 Flash |
| Independent research, test execution, coding, or adversarial challenge | Grok 4.7 | Kimi K3 when the harness preserves full history; GLM-5.3 Flash; GPT-6 Astra; GPT-6 Sol |
| Text-only long-context coding, complex agent work, or long-horizon implementation | OpenCode with GLM-5.3 | GPT-6 Astra; GPT-6 Sol; Kimi K3 when the harness preserves full history |
| Preserved-reasoning multimodal sessions or long-horizon work | OpenCode with Kimi K3 | Muse Spark 1.3; GLM-5.3 when the input is text-only; GPT-6 Astra; GPT-6 Sol |
| General multimodal long-context or multimodal agentic knowledge work | OpenCode with Muse Spark 1.3 | Kimi K3 when the harness preserves full history; GPT-6 Astra; GPT-6 Sol |
| Cost-sensitive agentic coding, automation, multimodal review, or structured technical prose | OpenCode with GLM-5.3 Flash | Muse Spark 1.3; Grok 4.7; GPT-6 Astra; GPT-6 Sol |
| Visual implementation from screenshots, PDFs, or designs; long-horizon multimodal creation | OpenCode with Muse Spark 1.3 | GLM-5.3 Flash; GPT-6 Astra; GPT-6 Sol |

## Know each route

| Model | Worker CLI | Effort | Strong clues | Limits and keep-away clues |
|---|---|---|---|---|
| Opus 5.5 (`claude-opus-5-5`) | Claude | `low` to `max` | Default Claude route. Planning, orchestration, synthesis, difficult coding, debugging, long unattended migrations and audits, code review, knowledge work, computer use, charts and screenshots, and technical prose | Use Opus 5.5 only; do not select Opus 5. Its API default is `medium`, so set effort explicitly. Use `medium` for bounded work and `high` for meaningful work. Use `low` only for trivial, readily checked tasks. At `xhigh` and `max` it thinks much more than Opus 5 did. Use them only for the hardest lanes. It follows supplied writing rules. Give unattended runs a completion check and a stop budget. A turn that ends in text is a progress report, not proof of completion. Cyber safeguards can hand most security work to Opus 4.8, which is outside this fleet. Use Opus 5.5 only for defensive review of the caller's own code. Do not route vulnerability exploration or exploit reproducers to it. |
| Fable 5.1 | Claude | `high` to `max` | Claude fallback when Opus 5.5 is unavailable. Escalation for demanding reasoning and long-horizon autonomy when Opus 5.5 at `xhigh` or `max` falls short | It costs 2.5 times Opus 5.5 per token and runs slower. Prefer `xhigh`. Use `max` only when the failure cost justifies its much higher token use. Give it a clear completion check and stop budget. |
| GPT-6 Astra (`gpt-6-astra`) | Codex | `low` to `max`; host `ultra` mode when the host confirms it | Default Codex work, difficult coding, verification, research, computer use, and synthesis | Start at `high`. Use `medium` or `low` only for the bounded cases above. Prefer `xhigh` or `max` when difficulty warrants it. API effort stops at `max`. Confirm `ultra` on the host before use. |
| GPT-6 Sol (`gpt-6-sol`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Complex coding, agent workflows, testing, and verification fallback | Start at `high` for meaningful work. Prefer Astra first, including lower Astra effort for suitable tasks. Honor an explicit Sol request. Confirm task cost or latency before selecting Sol on those grounds. |
| GPT-5.6 Terra | Codex | `medium` to `max`; host `ultra` mode when permitted | Codex-pinned budget fallback, bounded sweeps, data collection, tool calling, and triage | Usually use `medium` or `high`. Prefer the earlier budget routes when the budget and caller pin allow them. Consider Sol before Terra when its task estimates fit. Give consequential interpretation or final action to Astra, Opus 5.5, or Fable 5.1. |
| GPT-6 Luna (`gpt-6-luna`) | Codex | `high` to `max` | Narrow, high-volume extraction and triage when cost matters | Start at `high`. Use `xhigh` or `max` only when a local task sample shows a material gain. Keep the lane small. Escalate through the listed fallbacks when recall is inadequate. Give consequential interpretation to Astra, Opus 5.5, or Fable 5.1. Use only effort values confirmed by the selected host. |
| Daybreak Blue (`gpt-daybreak-blue-latest` → `gpt-5.6-sol`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Defensive cybersecurity reviews when refusal calibration matters | Its documented base is GPT-5.6 Sol. Check the alias through the [Daybreak model page](https://developers.openai.com/api/docs/models/gpt-daybreak-blue-latest). A Sol fleet update does not change this alias. It is not a different-family reviewer of Sol, Terra, Luna, or Astra work. Select it with an approved API key. A ChatGPT-account Codex login cannot use it. Start at `high`. If access is missing, use Astra. Keep the caller's target and action limits. |
| Grok 4.7 (`grok-4.7`) | Grok | `medium` to `xhigh` | Research, tool use, coding, testing, challenge, independent review, and budget-sensitive coding | Verify factual claims and executed checks. Use Grok 4.7 only. Published terminal scores are vendor-reported. Use `grok-4.7-build-fast` only when latency matters and the host lists it. It is the same model at twice the token rate and twice the output speed. |
| GLM-5.3 | OpenCode | `high` or `max` | Text-only long-context coding, complex agents, long-horizon implementation, and defensive security analysis | It has no image input. Prefer `max` for complex coding. Prefer Kimi when vision or preserved reasoning history matters. |
| Kimi K3 | OpenCode | `high` or `max` | Multimodal long context, preserved-reasoning sessions, long-horizon knowledge work, and repository-task challenge | Start fresh. The harness must preserve its full reasoning and tool history. Prefer GLM-5.3 for text-only work when speed or cost matters. |
| GLM-5.3 Flash | OpenCode | `high` or `max` | Efficient coding, automation, tools, multimodal work, review, and prose | Prefer full GLM-5.3 for hard text-only long-horizon work. Confirm the configured route provides high or max reasoning. |
| Muse Spark 1.3 | OpenCode | `medium` to `max`, subject to provider support | Multimodal work, visual implementation, agentic workflows, and long-horizon coding | Follow the provider order above among routes that meet the task's effort and data requirements. Results depend strongly on the harness. |

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
Consult [OpenAI model documentation](https://developers.openai.com/api/docs/models) when an API surface differs from the host.

## Pair independent reviewers

- Review Astra, Sol, Terra, Luna, or Daybreak work with Opus 5.5, Fable 5.1, Grok, GLM-5.3, or GLM-5.3 Flash.
- Review Opus 5.5 or Fable 5.1 work with Astra, Grok, GLM-5.3, or GLM-5.3 Flash. Opus 5.5 and Fable 5.1 are the same family.
- Review Grok work with Astra, Opus 5.5, or Fable 5.1.
- Review Kimi, either GLM route, or Muse work with Astra, Opus 5.5, or Fable 5.1.

Daybreak Blue belongs to the same model family as the other OpenAI routes.
Use it for defensive-cyber refusal calibration on work from another family. Use GPT-6 Sol when the Codex preference permits it.

Give the reviewer the artifact and requirements. Keep the author's reasoning out of the initial review context.
