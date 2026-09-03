# Fixed Agent Fleet

Use this reference only after a lane has a bounded output. It provides routing clues, not an overall model ranking.

Use only Muse Spark 1.3 for Muse routes. Prefer contributor routes after explicit acceptance of their data terms.

Try these identifiers in order:

1. `meta/muse-spark-1.3-contributor`
2. `openrouter/meta/muse-spark-1.3-contributor`
3. `opencode/muse-spark-1.3-contributor-free`
4. `meta/muse-spark-1.3`
5. `openrouter/meta/muse-spark-1.3`

Use `opencode models --refresh` before rejecting a recent identifier. Advance to the next identifier when the selected route remains unavailable.

Do not select a Muse Spark 1.2 route.

## Route by lane

| Primary lane | First route | Fallbacks, in order |
|---|---|---|
| Ambiguous planning, architecture, orchestration, or synthesis | Claude with Fable 5.1 | Claude with Opus 5; Codex with GPT-5.6 Sol |
| Difficult implementation, refactoring, debugging, or test construction | Claude with Opus 5 | Codex with GPT-5.6 Sol; Claude with Fable 5.1 |
| Terminal workflows, primary verification, or acting on gathered evidence | Codex with GPT-5.6 Sol | Claude with Opus 5; Grok 4.6 |
| Bounded implementation, repository sweep, data collection, or tool calling | Codex with GPT-5.6 Terra | GPT-5.6 Sol when the result drives a consequential action; then Grok 4.6 |
| Narrow high-volume extraction or triage | Codex with GPT-5.6 Luna | GPT-5.6 Terra |
| Precision review or quality-first technical prose | Claude with Opus 5 | Fable 5.1; GPT-5.6 Sol; GLM-5.3 Flash; Grok 4.6 |
| Independent research, test execution, coding, or adversarial challenge | Grok 4.6 | Kimi K3; GLM-5.3 Flash; GPT-5.6 Sol |
| Text-only long-context coding, complex agent work, or long-horizon implementation | OpenCode with GLM-5.3 | Kimi K3; GPT-5.6 Sol |
| Preserved-reasoning multimodal sessions or long-horizon work | OpenCode with Kimi K3 | Muse Spark 1.3; GLM-5.3 when the input is text-only; GPT-5.6 Sol |
| General multimodal long-context or multimodal agentic knowledge work | OpenCode with Muse Spark 1.3 | Kimi K3 when the harness preserves full history; GPT-5.6 Sol |
| Cost-sensitive agentic coding, automation, multimodal review, or structured technical prose | OpenCode with GLM-5.3 Flash | Muse Spark 1.3; Grok 4.6; GPT-5.6 Sol |
| Visual implementation from screenshots, PDFs, or designs; long-horizon multimodal creation | OpenCode with Muse Spark 1.3 | GLM-5.3 Flash; GPT-5.6 Sol |

## Know each route

| Model | Worker CLI | Effort | Strong clues | Limits and keep-away clues |
|---|---|---|---|---|
| Fable 5.1 | Claude | `high` to `max` | Ambiguous planning, architecture, orchestration, synthesis, autonomous difficult work, and agentic knowledge work | Prefer `xhigh` for quality-first work. Use `max` only when the failure cost justifies its much higher token use. Give it a clear completion check and stop budget. |
| GPT-5.6 Sol | Codex | `medium` to `ultra` | Complex coding, refactors, testing, verification, and acting on gathered evidence | Use a fresh different-family reviewer for consequential changes. |
| GPT-5.6 Terra | Codex | `medium` to `xhigh` | Bounded coding, repository sweeps, data collection, tool calling, and triage | Give consequential interpretation or final action to Sol, Opus, or Fable 5.1. |
| GPT-5.6 Luna | Codex | `high` to `max` | Narrow, high-volume extraction and triage when cost matters | Start at `high`. Use `xhigh` or `max` only when a local task sample shows a material gain. Keep the lane small. Prefer Terra when recall or judgment matters. |
| Opus 5 | Claude | `high` to `max` | Quality-first coding, debugging, precision review, computer use, and technical prose | Prefer `xhigh` for coding. Use `max` for the hardest knowledge work. It need not own a separate prose lane. |
| Grok 4.6 | Grok | `medium` to `xhigh` | Research, tool use, coding, testing, challenge, and independent review | Verify factual claims and executed checks. Use Grok 4.6 only. |
| GLM-5.3 | OpenCode | `high` or `max` | Text-only long-context coding, complex agents, long-horizon implementation, and defensive security analysis | It has no image input. Prefer `max` for complex coding. Prefer Kimi when vision or preserved reasoning history matters. |
| Kimi K3 | OpenCode | `high` or `max` | Multimodal long context, preserved-reasoning sessions, long-horizon coding, research, and knowledge work | Start fresh. The harness must preserve its full reasoning and tool history. Prefer GLM-5.3 for text-only work when speed or cost matters. |
| GLM-5.3 Flash | OpenCode | `high` or `max` | Efficient coding, automation, tools, multimodal work, review, and prose | Prefer full GLM-5.3 for hard text-only long-horizon work. Confirm the configured route provides high or max reasoning. |
| Muse Spark 1.3 | OpenCode | `medium` to `xhigh` | Multimodal work, visual implementation, agentic workflows, and long-horizon coding | Prefer the contributor identifier order above. Use full 1.3 routes when every contributor route fails. Check access and data terms. Results depend strongly on the harness. Use `xhigh` until the provider exposes `max`. |

## Map effort to the worker CLI

Use the host's installed controls. These forms show the intended mapping:

| Worker CLI | Model control | Effort control |
|---|---|---|
| Claude | `--model <alias-or-id>` | `--effort medium|high|xhigh|max` |
| Codex | `-m <model-id>` | `-c model_reasoning_effort="medium|high|xhigh|max|ultra"` when supported |
| Grok | `-m <grok-model-id>` | `--reasoning-effort medium|high|xhigh` |
| OpenCode | `-m <provider/model>` | `--variant <provider-supported-value>` |

Do not translate effort names as equal compute across providers. Choose the level within the selected model's supported range.

## Pair independent reviewers

- Review Sol, Terra, or Luna work with Fable 5.1, Opus, Grok, GLM-5.3, or GLM-5.3 Flash.
- Review Fable 5.1 or Opus work with Sol, Grok, GLM-5.3, or GLM-5.3 Flash.
- Review Grok work with Sol, Fable 5.1, or Opus.
- Review Kimi, either GLM route, or Muse work with Sol, Fable 5.1, or Opus.

Give the reviewer the artifact and requirements. Keep the author's reasoning out of the initial review context.
