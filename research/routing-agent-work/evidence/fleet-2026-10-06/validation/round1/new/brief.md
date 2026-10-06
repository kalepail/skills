You are an orchestrator. You must apply ONLY the routing policy below (SKILL.md and its fleet reference) to each request in prompts. Do not use outside knowledge about models. Do not launch any worker. Treat host status statements in a prompt as true.
For each request return one JSON object: {"id": <id>, "invoke_skill": true|false, "worker_cli": "Claude|Codex|Grok|OpenCode|none", "model": "<fleet model name or Unrouted or none>", "effort": "<value or none>", "fallback": "<next route or none>", "reviewer": "<model or none>", "note": "<=25 words"}. For a request that asks for several roles (for example several challengers), put the primary route in model and list the others in note.
Write a JSON array of all objects to the file answers.json in the current directory, and nothing else.

=== SKILL.md ===
---
name: routing-agent-work
description: Select an agent CLI, model, and reasoning effort for delegated work. Use when an orchestrator, parent agent, or user must assign implementation, security review, authorized vulnerability exploration, research, review, second-opinion or edge-case confirmation, synthesis, multimodal, long-context, high-volume extraction, or prose lanes across Claude, Codex, Grok, or OpenCode. Do not use for orchestration mechanics, research provider or source selection, live model discovery, provider setup, general model comparisons, single-agent work with no delegation choice, or a lane whose worker, model, and effort are already fixed.
---

# Route Agent Work

Route only when the selection can change the result. Continue with the current agent when no delegation choice exists.

The caller owns orchestration mechanics. Orchestration hosts include Herdr, Orca, Conductor, and Solo. Worker CLIs are Claude, Codex, Grok, and OpenCode.

## Define the lane

Write one bounded contract before selecting a model:

- primary output and completion check;
- allowed files, tools, and state changes;
- required evidence or tests;
- context the worker needs;
- report destination.

Split work only when lanes can progress independently, isolate risk, or provide independent review. Do not create lanes to increase agent count.

## Select the route

Read [references/fleet.md](references/fleet.md) before choosing a model, effort, fallback, or reviewer.

Apply these decision axes in order:

1. **Lane fit**: match the model to the primary output.
2. **Failure cost**: use a stronger route or independent review when errors are expensive.
3. **Constraints**: check context length, modality, privacy, tool use, and available providers.
4. **Cost and latency**: use them as tie-breakers between routes that can meet the quality bar.

Use only the fixed fleet. Try listed fallbacks in order. If every listed route is unavailable, mark the lane `Unrouted`.

Fallbacks handle an unavailable route. Escalation handles failure cost. Escalate to a stronger route or a higher effort when errors are expensive or the first attempt falls short.

When the caller pins only the worker CLI, use that CLI's default route or a more specific fleet route on it. Mark the lane `Unrouted` when none fits.

An `Unrouted` lane does not launch. Return it to the caller for an explicit constraint change or fleet update.

Before launch, confirm only the selected configured identifier and effort control through host status or a targeted CLI check. If the identifier fails, try the next fallback. If only the effort value fails, use a supported value that meets the lane requirement and model floor. If none fits, try the next fallback. Do not enumerate or score unrelated models.

Before rejecting a new or recently updated OpenCode identifier, refresh its model catalog once:

```bash
opencode models --refresh
```

Then use `opencode models <provider>` to check only the selected provider. Treat an identifier absent after refresh as unavailable, then use the listed fallback. Skip the refresh when host status already confirms the identifier.

## Set effort

Set the model and effort explicitly for each worker and nested worker. Never rely on an unverified default.

- Use each worker CLI's default route and effort from the fleet reference.
- Use `medium` for bounded, clear, low-risk work. Routes whose range starts at `low` permit it only for trivial, readily checked tasks.
- Use `high` for meaningful implementation, research, review, and synthesis.
- Use `xhigh` for hard planning, debugging, synthesis, and adversarial review.
- Use `max` for the hardest quality-first work with a clear stopping condition.
- Keep other models at `medium` or above. Apply each model's range and floor from the fleet reference.

Use only supported effort values. Omit an unsupported flag only when the configured route confirms the required mode.

Codex `ultra` enables automatic task delegation. Use it only when the caller's delegation limits and host support permit it.
Use `max` when the caller requires one worker or a fixed delegation structure.

## Shape the delegation tree

Use one direct worker for one bounded lane. Use a sub-orchestrator when a lane contains several independent sublanes.

One worker layer plus one nested layer is usually sufficient. This is guidance, not a universal limit.

Ask a sub-orchestrator to load `routing-agent-work` only when it must choose child routes and can load the skill. Otherwise, pass each child route in its brief. Each child reports only to its direct parent.

The parent watches completion signals. It requests more context only when the compact report cannot support a decision.

## Add independent review

Add review when the failure cost justifies it. Give the reviewer a fresh context with the specification and artifact first.

Prefer a capable reviewer from a different model family. Treat model diversity as a clue, not proof of independence.

Require reproducible evidence. Ask for tests, paths, commands, or cited sources instead of an unsupported verdict.

Use lower-cost models from other families to find edge cases and confirm results. Treat their findings as leads. Reproduce each finding before a stronger route acts on it.

## Handle prose

Treat prose as a separate lane only when prose is a meaningful deliverable. Keep the existing worker when it can write the required text well.

Use ASD-STE100 for comments, documentation, reviews, pull request text, and user-facing explanations. Opus 5.5 is the quality-first default for technical prose. It follows supplied writing rules closely.

## Return a route card

Return one compact card for each lane:

```text
Lane: <bounded output>
Worker CLI: <Claude | Codex | Grok | OpenCode | none>
Model: <fixed fleet model | Unrouted>
Effort: <explicit supported value | none>
Reason: <lane fit and failure-cost rationale>
Verified: <host status or targeted CLI check>
Fallback: <next fixed-fleet model, or none>
Reviewer: <different-family fixed-fleet model, or none>
Report contract: <result, artifact paths, checks, risks, blockers>
```

The worker returns the result, evidence paths, completed checks, unresolved risks, and blockers. It does not return a full transcript.

=== references/fleet.md ===
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

=== prompts ===
[
 {
  "id": 2,
  "prompt": "I need five agents to inspect separate packages and report the affected files. The parent should not consume their full transcripts. Two child orchestrators cannot load local skills."
 },
 {
  "id": 3,
  "prompt": "Route an ambiguous planning lane. Host status says the Opus 5.5 identifier is unavailable. Fable 5.1 is available at xhigh."
 },
 {
  "id": 4,
  "prompt": "Assign a worker to read a very large text-only design archive and trace its decisions into a long-running implementation."
 },
 {
  "id": 5,
  "prompt": "Pick a low-cost model for multimodal tool use and a second model to challenge its findings."
 },
 {
  "id": 11,
  "prompt": "Assign a cheap worker to extract the same five fields from thousands of small independent records. The lane needs no broad judgment."
 },
 {
  "id": 12,
  "prompt": "Assign an independent worker to research an API claim, exercise the code path, and challenge the implementer's result."
 },
 {
  "id": 20,
  "prompt": "Route a bounded repository sweep. The host pins Claude for every worker. Targeted checks show that Opus 5.5, Sonnet 5.5, and Fable 5.1 are unavailable. Opus 5 still appears in the host catalog."
 },
 {
  "id": 21,
  "prompt": "Assign a worker to continue a multimodal long-horizon knowledge task that Kimi K3 started. The OpenCode provider preserves complete Kimi reasoning and tool history."
 },
 {
  "id": 22,
  "prompt": "Assign a worker to analyze a very large set of screenshots and documents. The task does not need preserved reasoning history."
 },
 {
  "id": 24,
  "prompt": "Route a Codex worker to implement a feature and run its integration checks. The host confirms all approved Codex models and effort levels. No budget constraint applies."
 },
 {
  "id": 25,
  "prompt": "Pick a Codex worker for a small, well-defined file rename and import update. Existing checks cover every changed reference. Keep latency modest. Host status confirms GPT-6.1 Sol and Astra at low, medium, and high."
 },
 {
  "id": 26,
  "prompt": "Pick a Codex worker to alphabetize ten supplied labels and verify the exact output against a provided list. This is a trivial isolated task. Host status confirms GPT-6.1 Sol at low and medium."
 },
 {
  "id": 27,
  "prompt": "Route a Codex worker to implement a feature. Host status confirms GPT-6.1 Sol is unavailable and Astra supports high. Other CLIs are excluded."
 },
 {
  "id": 28,
  "prompt": "Route a Codex worker for cheap bounded repository sweeps under a strict budget. The caller pins Codex. Host status confirms GPT-6.1 Sol and GPT-5.6 Terra at medium. Astra exceeds this budget. Grok is outside the pin."
 },
 {
  "id": 29,
  "prompt": "Select a worker to review our authentication service for vulnerabilities and validate patches. Testing stays in our isolated checkout. Host status confirms Daybreak Blue access and high effort."
 },
 {
  "id": 31,
  "prompt": "Select an independent security reviewer for code written by GPT-6.1 Sol. Daybreak Blue and Opus 5.5 are available. A different model family is required."
 },
 {
  "id": 41,
  "prompt": "Route cheap bounded repository sweeps. No CLI is pinned. Host status confirms GPT-6.1 Sol at medium, Sonnet 5.5 at medium, Opus 5.5 at medium, and Grok 4.7 at high."
 },
 {
  "id": 44,
  "prompt": "Choose a worker to explore vulnerabilities in our owned parser and build local exploit reproducers. The host pins Claude. Host status confirms Opus 5.5 at high. No external targets are allowed."
 },
 {
  "id": 46,
  "prompt": "Route cheap bounded repository sweeps. Codex is pinned. GPT-6.1 Sol is unavailable and Astra exceeds the budget. Host status confirms GPT-6 Sol and GPT-5.6 Terra at medium."
 },
 {
  "id": 47,
  "prompt": "Choose an effort for a GPT-6 Luna extraction worker. The task is narrow. The host confirms high, xhigh, and max. A colleague suggests ultra. No local sample supports higher effort."
 },
 {
  "id": 49,
  "prompt": "Route an ordinary Codex feature worker. GPT-6.1 Sol and Astra are both available at high. A teammate says Astra is always safer because it is the flagship. No failure-cost signal applies."
 },
 {
  "id": 50,
  "prompt": "Route a narrow extraction lane. GPT-6 Luna is unavailable. GPT-6.1 Sol and GPT-5.6 Terra support low and medium and meet the budget."
 },
 {
  "id": 52,
  "prompt": "Route a bounded bug-fix lane through Claude. The caller wants it fast and cheap. Host status confirms Sonnet 5.5 and Opus 5.5 at every effort level."
 },
 {
  "id": 53,
  "prompt": "Route a very hard Claude debugging lane. A colleague suggests Sonnet 5.5 at max because it is cheaper per token. Opus 5.5 is available at xhigh."
 },
 {
  "id": 54,
  "prompt": "Route a hard multi-file Codex refactor. Host status confirms GPT-6.1 Sol at high, xhigh, and max. The caller asks for the best effort setting."
 },
 {
  "id": 55,
  "prompt": "Route a lane that asks Kimi K3, GLM-5.3, and Muse Spark 1.3 to find edge cases in our new rate limiter. The implementer is Opus 5.5."
 },
 {
  "id": 56,
  "prompt": "Use Grok 4.7 as the fallback for a difficult implementation lane because Opus 5.5 is unavailable."
 },
 {
  "id": 57,
  "prompt": "Route a Codex worker to review authentication code for vulnerabilities. Host status lists gpt-6.1-sol, gpt-6-astra, and gpt-daybreak-blue-latest. The Daybreak key is approved."
 }
]