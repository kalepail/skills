You are an orchestrator. You must apply ONLY the routing policy below (SKILL.md and its fleet reference) to each request in prompts. Do not use outside knowledge about models. Do not launch any worker. Treat host status statements in a prompt as true.
For each request return one JSON object: {"id": <id>, "invoke_skill": true|false, "worker_cli": "Claude|Codex|Grok|OpenCode|none", "model": "<fleet model name or Unrouted or none>", "effort": "<value or none>", "fallback": "<next route or none>", "reviewer": "<model or none>", "note": "<=25 words"}. For a request that asks for several roles (for example several challengers), put the primary route in model and list the others in note.
Write a JSON array of all objects to the file answers.json in the current directory, and nothing else.
If a request does not need this routing policy, set invoke_skill to false and model to none.

=== SKILL.md ===
---
name: routing-agent-work
description: Select an agent CLI, model, and reasoning effort for delegated work. Use when an orchestrator, parent agent, or user must assign implementation, security review, authorized vulnerability exploration, research, review, second-opinion or edge-case confirmation, synthesis, multimodal, long-context, high-volume extraction, or prose lanes across Claude, Codex, Grok, or OpenCode. Also use it to check that a headless OpenCode worker finished. Do not use for other orchestration mechanics, research provider or source selection, live model discovery, provider setup, general model comparisons, single-agent work with no delegation choice, or a lane whose worker, model, and effort are already fixed.
---

# Route Agent Work

Route only when the selection can change the result. Continue with the current agent when no delegation choice exists.

The caller owns orchestration mechanics, except the completion check for a headless OpenCode worker. Orchestration hosts include Herdr, Orca, Conductor, and Solo. Worker CLIs are Claude, Codex, Grok, and OpenCode.

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

When the caller pins only the worker CLI, apply the pinned-CLI rule in the fleet reference.

An `Unrouted` lane does not launch. Return it to the caller for an explicit constraint change or fleet update.

Treat a safeguard handoff to a model outside the fleet as an unavailable route. Use the next listed fallback.

Before launch, check only the selected route. Do not enumerate or score unrelated models.

1. Confirm the configured identifier and effort control through host status or a targeted CLI check.
2. If the identifier fails, try each provider the fleet lists for that model, then the next fallback.
3. If only the effort value fails, use a supported value that meets the lane requirement and the model's range. Otherwise, use the next fallback.
4. When a route needs a harness property, such as preserved reasoning history, confirm it through host documentation or the caller. Skip the route when nobody can confirm it.

For OpenCode routes, read [references/opencode.md](references/opencode.md). It covers the catalog refresh and the completion check. An OpenCode exit code alone does not prove that the worker finished.

## Set effort

Set the model and effort explicitly for each worker and nested worker. Never rely on an unverified default.

Choose the effort from the lane, not from the CLI default. An effort in a lane row wins. Otherwise, use these levels:

- Use `medium` for bounded, clear, low-risk work.
- Use `low` only for trivial, readily checked tasks, or for bounded work under a stated cost limit.
- Use `high` for meaningful implementation, research, review, and routine synthesis.
- Use `xhigh` for hard planning, hard debugging, multi-source synthesis, and adversarial review.
- Use `max` for the hardest quality-first work with a clear stopping condition.

Keep each value inside the selected model's range in the fleet reference. Raise it to the model's floor when the level above is lower.

Use only supported effort values. Omit an unsupported flag only when the configured route confirms the required mode.

Codex `ultra` enables automatic task delegation. Use it only when the caller's delegation limits and host support permit it.
Do not use `ultra` when the caller requires one worker or a fixed delegation structure. Keep the effort that the lane needs.

## Shape the delegation tree

Use one direct worker for one bounded lane. Use a sub-orchestrator when a lane contains several independent sublanes.

One worker layer plus one nested layer is usually sufficient. This is guidance, not a universal limit.

Ask a sub-orchestrator to load `routing-agent-work` only when it must choose child routes and can load the skill. Otherwise, pass each child route in its brief. Each child reports only to its direct parent.

The parent watches completion signals. It requests more context only when the compact report cannot support a decision.

## Add independent review

Add review when the failure cost justifies it. Give the reviewer a fresh context with the specification and artifact first.

Prefer a capable reviewer from a different model family. Treat model diversity as a clue, not proof of independence.

Require reproducible evidence. Ask for tests, paths, commands, or cited sources instead of an unsupported verdict.

Use lower-cost models from other families as extra challengers. The fleet reference explains how to treat their findings.

## Handle prose

Treat prose as a separate lane only when prose is a meaningful deliverable. Keep the existing worker when it can write the required text well.

Pass the caller's writing standard into the worker brief. Opus 5.5 is the quality-first default for technical prose. It follows supplied writing rules closely.

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

When the caller pins a worker CLI, use the lane row's first route on that CLI. If the row has none, use a route on that CLI whose strong clues fit the lane. Otherwise, mark the lane `Unrouted`. A pinned Grok CLI has no coding route.

## Route by lane

The bounded rows are the bounded implementation, budget, and extraction rows. Use them only for narrow work with readily checked output. Treat migrations and multi-file features as difficult implementation. Use the budget row only when the caller states a cost limit.
For difficult implementation under a stated cost limit, use GPT-6.1 Sol at `high` or `xhigh`, then Sonnet 5.5 at `high`. Give the lane a stop budget.
Security lanes keep the caller's target and action limits on every route and fallback.

| Primary lane | First route | Fallbacks, in order |
|---|---|---|
| Ambiguous planning, architecture, orchestration, or synthesis | Claude with Opus 5.5 | Fable 5.1; GPT-6 Astra; GPT-6.1 Sol |
| Difficult implementation, refactoring, debugging, or test construction | Claude with Opus 5.5 | Sonnet 5.5 at `xhigh`; GPT-6.1 Sol at `xhigh`; GPT-6 Astra |
| Terminal workflows, primary verification, or acting on gathered evidence | Codex with GPT-6.1 Sol | GPT-6 Astra; Opus 5.5; Sonnet 5.5 |
| Bounded implementation, repository sweep, data collection, or tool calling | Codex with GPT-6.1 Sol at `medium` | Sonnet 5.5 at `medium`; Opus 5.5 at `medium`; GLM-5.3 Flash at `max` |
| Budget-sensitive bounded coding or repository sweeps | Codex with GPT-6.1 Sol at `medium` | Sonnet 5.5 at `medium` or `high`; GLM-5.3 Flash at `max`; Opus 5.5 at `low` |
| Narrow high-volume extraction or triage | Codex with GPT-6 Luna | GPT-6.1 Sol at `low` or `medium`; GLM-5.3 Flash at `high` |
| Security review, authorized vulnerability exploration, or patch validation | Codex with Daybreak Blue | GPT-6 Astra; GPT-6.1 Sol; Opus 5.5 for defensive review of the caller's own code; GLM-5.3 for text-only input |
| Precision review or quality-first technical prose | Claude with Opus 5.5 | Sonnet 5.5; Fable 5.1; GPT-6 Astra; GPT-6.1 Sol |
| Independent challenge, second opinion, or live web and X research | Grok 4.7 | GLM-5.3; Muse Spark 1.3; Kimi K3 when the harness preserves full history |
| Edge-case discovery and confirmation across model families | OpenCode with Muse Spark 1.3 | GLM-5.3 for text-only input; Kimi K3 when the harness preserves full history; Grok 4.7; GLM-5.3 Flash |
| General multimodal, visual implementation, or long-context documents and screenshots | OpenCode with Muse Spark 1.3 | Opus 5.5; GPT-6.1 Sol; Kimi K3 when the harness preserves full history |
| Text-only long-context work that needs an open-weight model | OpenCode with GLM-5.3 | Kimi K3 when the harness preserves full history; GLM-5.3 Flash |
| Lowest-cost or open-weight automation, multimodal review, or structured prose | OpenCode with GLM-5.3 Flash | GPT-6.1 Sol at `medium`; Sonnet 5.5 at `medium`; Muse Spark 1.3 |

## Treat weaker-model findings as leads

GLM-5.3, GLM-5.3 Flash, Kimi K3, Muse Spark 1.3, and Grok 4.7 trail the default routes on independent coding and terminal evaluations.
Use them for cost, modality, open weights, or a different model family.
Treat their findings as leads, not verdicts.
Reproduce a finding with a test, command, or cited source before a stronger route acts on it.
Run two or three of them in parallel when the lane needs diverse edge cases. For one run, follow the order in the edge-case row.
Launch headless OpenCode runs as [opencode.md](opencode.md) describes. A run can end with no answer and exit code 0.
Discard a finding that no check reproduces.
When one of these models owns a lane, accept its result only after the lane's completion check passes.

## Know each route

| Model | Worker CLI | Effort | Strong clues | Limits and keep-away clues |
|---|---|---|---|---|
| Opus 5.5 (`claude-opus-5-5`) | Claude | `low` to `max` | Default Claude route. Planning, orchestration, synthesis, difficult coding, debugging, long unattended migrations, code review, knowledge work, computer use, screenshots, and technical prose | Use `max` only with a clear stop budget. Give unattended runs a completion check and a stop budget. A turn that ends in text is a progress report, not proof of completion. Cyber safeguards can hand security work to a model outside the fleet. Use Opus 5.5 only for defensive review of the caller's own code. |
| Sonnet 5.5 (`claude-sonnet-5-5`) | Claude | `low` to `high`; `xhigh` only as a fallback | Fast Claude route for well-scoped coding, bug fixes, bounded sweeps, documents, and design-sensitive work | Above `high`, Opus 5.5 gives better results at a similar task cost. Use Sonnet 5.5 above `high` only when Opus 5.5 is unavailable. Avoid `max`; it produces very high output-token counts. Cyber safeguards can hand security work to a model outside the fleet. Do not route vulnerability exploration to it. |
| Fable 5.1 (`claude-fable-5-1`) | Claude | `high` to `max` | Escalation for demanding reasoning and long-horizon autonomy when Opus 5.5 at `xhigh` falls short; planning fallback when Opus 5.5 is unavailable | It costs more per token than Opus 5.5 and runs slower. Prefer `xhigh`. Give it a clear completion check and stop budget. |
| GPT-6.1 Sol (`gpt-6.1-sol`) | Codex | `low` to `max`; host `ultra` mode when permitted | Default Codex route. Complex coding, terminal work, verification, agent workflows, computer use, and repeated long-running work | Prefer `xhigh` over `max` for coding unless a local sample shows a gain. Escalate to Astra when it falls short on the hardest end-to-end work. |
| GPT-6 Astra (`gpt-6-astra`) | Codex | `low` to `max`; host `ultra` mode when the host confirms it | Escalation for the hardest end-to-end Codex work, difficult research, and final consequential interpretation | It costs much more per task than GPT-6.1 Sol. Use `high` or `xhigh`. Use `max`, or host `ultra`, only for the hardest lanes with a stop budget. |
| GPT-6 Luna (`gpt-6-luna`) | Codex | `high` to `max` | Narrow, high-volume extraction and triage when cost matters | Start at `high`. Use `xhigh` or `max` only when a local task sample shows a material gain. Keep the lane small. Give consequential interpretation to GPT-6.1 Sol, Astra, or Opus 5.5. |
| Daybreak Blue (`gpt-daybreak-blue-latest` → `gpt-5.6-sol`) | Codex | `medium` to `max`; host `ultra` mode when permitted | Defensive cybersecurity reviews when refusal calibration matters | Check the alias through the [Daybreak model page](https://developers.openai.com/api/docs/models/gpt-daybreak-blue-latest). Its base is not a general route. It is not a different-family reviewer of other OpenAI work. Select it with an approved API key; a ChatGPT-account Codex login cannot use it. Start at `high`. If access is missing, use Astra. Keep the caller's target and action limits. |
| Grok 4.7 (`grok-4.7`) | Grok | `medium` to `xhigh` | Independent challenge from another family, research with live web and X context, and second opinions | It trails the default routes on independent coding and terminal evaluations at a higher task cost. Do not use it as a coding fallback. Verify its factual claims and executed checks. |
| GLM-5.3 | OpenCode | `high` or `max` | Open-weight text-only long-context work, defensive security analysis, and different-family challenge | It has no image input. Prefer `max`. At `max`, its reasoning can exceed OpenCode's output cap; [opencode.md](opencode.md) shows how to raise it. It is slow and verbose. |
| GLM-5.3 Flash | OpenCode | `high` or `max` | Very low-cost coding, automation, tools, multimodal review, and prose | Use `max` for coding. Confirm the configured route provides high or max reasoning. |
| Kimi K3 | OpenCode | `high` or `max` | Preserved-reasoning multimodal sessions and different-family challenge | Start each new lane in a fresh session. The harness must preserve its full reasoning and tool history; generic harnesses score poorly. Keep a session that Kimi K3 started on Kimi K3, because a model switch loses that history. It is slow and expensive for its quality. |
| Muse Spark 1.3 | OpenCode | `medium` to `max`, subject to provider support | Multimodal work, visual implementation, knowledge work, and different-family challenge | It trails on terminal-heavy agent work. Follow the provider order below among routes that meet the task's effort and data requirements. Results depend strongly on the harness. |

GLM-5.3, GLM-5.3 Flash, and Kimi K3 have open weights. Open weights do not keep data local: the selected provider still receives the input. Mark a lane `Unrouted` when its privacy limit excludes every listed provider.

Use [OpenAI's model pages](https://developers.openai.com/api/docs/models) and [Claude's models overview](https://platform.claude.com/docs/en/models/overview) for current API limits and prices.
Use the selected host's context limit and effort controls when they differ from API limits.

## Muse provider selection

Use only Muse Spark 1.3 for Muse routes. Prefer contributor routes when the caller's lane contract states acceptance of their data terms. Without that statement, treat the terms as not accepted.

Try these identifiers in order:

1. `meta/muse-spark-1.3-contributor`
2. `openrouter/meta/muse-spark-1.3-contributor`
3. `opencode/muse-spark-1.3-contributor-free`
4. `meta/muse-spark-1.3`
5. `openrouter/meta/muse-spark-1.3`

Skip contributor routes when their data terms are not accepted.
Check effort support for the selected identifier, not only the model family.
If no supported effort meets the task requirement, advance through the provider list before changing models.

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

- Review GPT-6.1 Sol, Astra, Luna, or Daybreak work with Opus 5.5, Sonnet 5.5, or Fable 5.1.
- Review Opus 5.5, Sonnet 5.5, or Fable 5.1 work with GPT-6.1 Sol or Astra. The three Claude models are one family.
- Review Grok work with GPT-6.1 Sol, Astra, or Opus 5.5.
- Review Kimi, either GLM route, or Muse work with GPT-6.1 Sol, Astra, or Opus 5.5.
- Add Grok 4.7, Muse Spark 1.3, GLM-5.3, or Kimi K3 as extra challengers. They do not replace a capable reviewer, and their findings need reproduction.

When no listed reviewer is available, mark the review lane `Unrouted`. Do not promote an extra challenger to reviewer.

Give the reviewer the artifact and requirements. Keep the author's reasoning out of the initial review context.
=== references/opencode.md ===
# Run OpenCode Workers

Read this before you launch an OpenCode route. An interactive OpenCode session in a terminal multiplexer needs only the catalog check.

## Check the catalog

Before you reject a new or recently updated identifier, refresh the model catalog once:

```bash
opencode models --refresh
opencode models <provider>
```

Check only the selected provider. Treat an identifier that is absent after the refresh as unavailable, and use the next fallback. Skip the refresh when host status already confirms the identifier.

## Launch a headless worker

`opencode run` can exit with code 0 and give no answer. Judge each run from its event stream, not from its exit code.
Use the bundled launcher. Call it by its full path, because it lives in this skill's `scripts/` folder:

```bash
python3 <skill-dir>/scripts/opencode_worker.py \
  --model <provider/model> --variant <effort> \
  --dir <work-dir> --prompt-file <brief.md> \
  --text-out <answer.md> --timeout 900
```

The launcher does these steps:

- It sends the prompt on stdin and then closes stdin. Long briefs do not hit argument-size limits.
- It turns off each MCP server that `opencode debug config` lists for the work directory. Use `--keep-mcp` when the lane needs MCP tools.
- It raises the output token cap through `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX`.
- It runs with `--pure` and turns off automatic updates.
- It stops the run after the time limit.
- It starts the run once more after a `database is locked` failure at start.
- It prints one JSON summary line. `--text-out` receives the text of the final step only. `--events-out` keeps the full stream.

| Exit code | Status | Meaning |
|---|---|---|
| 0 | `complete` | The last step ended with `stop`, and that step has answer text |
| 2 | `truncated` | The output token cap stopped the model |
| 2 | `incomplete` | The run stopped after a tool call, often a rejected permission |
| 2 | `empty` | The last step has no answer text |
| 2 | `filtered` | A content filter stopped the model |
| 2 | `unconfirmed` | The last step has text, but the provider gave no clear finish reason |
| 3 | `timeout` | The run passed the time limit |
| 4 | `error` | OpenCode, the provider, or the launcher reported an error |
| 64 | usage error | A required argument, file, or directory is missing |

Accept a result only when the status is `complete` and the lane's own completion check passes.
Treat `unconfirmed` text as a lead: read it, then confirm it with the lane's check.
Run `python3 <skill-dir>/scripts/opencode_worker.py --self-test` after you change the launcher.

## Know the failure modes

| Symptom | Cause | Control |
|---|---|---|
| The run makes no progress and never ends | `opencode run` reads stdin until it closes. An open pipe keeps it waiting | Send the prompt on stdin, or redirect stdin from `/dev/null` |
| Exit code 0, no text, last `step_finish` reason `length` | OpenCode's output cap can be lower than a reasoning model needs at `max`. The model spends the cap on reasoning | Raise `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` to the model's output limit |
| Exit code 0, no text, last reason `tool-calls` | A headless run rejects each permission request that needs approval | Put all inputs inside `--dir`. Grant only the needed permissions through `OPENCODE_PERMISSION`. Use `--auto` only in a disposable work directory |
| Many extra input tokens on each step, and slow start-up | `--pure` turns off plugins, not MCP servers. Each run loads every configured MCP server | Turn the servers off through `OPENCODE_CONFIG_CONTENT` |
| `database is locked` at start | Many OpenCode processes start at the same time on one data directory | Start the run once more. Stagger large batches |

## Run without the launcher

Apply the same controls by hand:

```bash
OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX=<model-output-limit> \
OPENCODE_CONFIG_CONTENT='{"mcp":{"<server>":{"enabled":false}}}' \
opencode run --pure --format json --dir <work-dir> \
  -m <provider/model> --variant <effort> < brief.md > events.jsonl
```

List the server names with `opencode debug config`. Add one entry for each name.
Put a time limit on the process.
Read the events after the last `step_start`: the last `step_finish` reason must be `stop`, and the step must have text.

## Read attached sessions through export

`opencode serve` with `opencode run --attach <url>` can save start-up time across many runs.
The attached client can stop its output after the first event while the server finishes the session.
Read the result with `opencode export <sessionID>`. Do not trust the stdout of an attached client.

Check flag and variable names with `opencode run --help` and the [OpenCode CLI documentation](https://opencode.ai/docs/cli).

=== prompts ===
[
 {
  "id": 1,
  "prompt": "Split this migration into implementation, testing, and independent review lanes. I was thinking Codex for both implementation and independent review. Pick agents and reasoning levels."
 },
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
  "id": 6,
  "prompt": "The deliverable is a polished README and pull request description. The implementation owner already understands the change."
 },
 {
  "id": 7,
  "prompt": "Use this new unlisted model I heard about for a review lane. Find its current variants and score it first."
 },
 {
  "id": 8,
  "prompt": "Review this pull request yourself and report the findings. Do not delegate the review."
 },
 {
  "id": 9,
  "prompt": "How does Codex multi-agent orchestration work?"
 },
 {
  "id": 11,
  "prompt": "Assign a cheap worker to extract the same five fields from thousands of small independent records. The lane needs no broad judgment."
 },
 {
  "id": 13,
  "prompt": "Assign a worker to inspect screenshots and a PDF, then build and verify a long-running visual interface change."
 },
 {
  "id": 14,
  "prompt": "Configure my OpenCode providers and API credentials so Kimi K3 can launch."
 },
 {
  "id": 15,
  "prompt": "Give me an overall ranked comparison of every frontier model and score each one from one to ten."
 },
 {
  "id": 16,
  "prompt": "Which model should replace the current model for this entire single-agent chat? I will not delegate anything."
 },
 {
  "id": 17,
  "prompt": "Launch Claude with Fable 5.1 at xhigh for this already-written planning brief."
 },
 {
  "id": 18,
  "prompt": "Update our routing skill to add a newly released model to the approved fleet."
 },
 {
  "id": 21,
  "prompt": "Assign a worker to continue a multimodal long-horizon knowledge task that Kimi K3 started. The OpenCode provider preserves complete Kimi reasoning and tool history."
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
  "id": 34,
  "prompt": "Choose a Codex model for a very hard debugging task. Only one worker is allowed, with no automatic or nested delegation. Host status confirms Astra max and ultra."
 },
 {
  "id": 40,
  "prompt": "Before I dispatch these three research lanes, tell me which search providers each lane should use: Parallel CLI, Perplexity, or Parallel Task MCP."
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
  "id": 45,
  "prompt": "Assign an Opus 5.5 worker to run a multi-part code base migration overnight without supervision. Route the lane and state its report contract."
 },
 {
  "id": 46,
  "prompt": "Route cheap bounded repository sweeps. Codex is pinned. GPT-6.1 Sol is unavailable and Astra exceeds the budget. Host status lists two older Codex models that are not in the fleet, both at medium."
 },
 {
  "id": 49,
  "prompt": "Route an ordinary Codex feature worker. GPT-6.1 Sol and Astra are both available at high. A teammate says Astra is always safer because it is the flagship. No failure-cost signal applies."
 },
 {
  "id": 52,
  "prompt": "Route a bounded bug-fix lane through Claude. The caller wants it fast and cheap. Host status confirms Sonnet 5.5 and Opus 5.5 at every effort level."
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
  "id": 58,
  "prompt": "The caller pins the Grok CLI for every worker. Route a multi-file implementation lane."
 },
 {
  "id": 59,
  "prompt": "Route a defensive review of our own service code to Opus 5.5. Host status shows that a cyber safeguard handed the request to a model outside the fleet."
 },
 {
  "id": 61,
  "prompt": "Route a multi-file migration under a strict, stated cost limit. No CLI is pinned."
 },
 {
  "id": 62,
  "prompt": "Add an independent reviewer for a finished GPT-6.1 Sol migration. The Claude provider is down, so Opus 5.5, Sonnet 5.5, and Fable 5.1 cannot run. Grok 4.7 and GLM-5.3 are available."
 },
 {
  "id": 64,
  "prompt": "Launch the selected GLM-5.3 Flash challenger as a headless OpenCode run from this orchestrator script, then collect its answer."
 },
 {
  "id": 65,
  "prompt": "I ran Muse Spark 1.3, GLM-5.3, and Kimi K3 as parallel headless challengers on our rate limiter. Muse returned three findings. GLM exited 0 with no text and reason length. Kimi failed at start with database is locked. What now?"
 },
 {
  "id": 66,
  "prompt": "my opencode tui won't start after the upgrade, it just shows a blank screen. can you figure out what broke?"
 },
 {
  "id": 67,
  "prompt": "Spawn three Herdr panes for these lanes: Codex gpt-6.1-sol high for the API, Claude claude-opus-5-5 high for the docs, OpenCode GLM-5.3 Flash max for tests."
 },
 {
  "id": 68,
  "prompt": "What is Codex's default model right now on my machine?"
 },
 {
  "id": 69,
  "prompt": "who should i hand this review to? opus wrote the patch and it touches auth"
 },
 {
  "id": 70,
  "prompt": "which model should the subagent use for a quick grep-and-report across the monorepo? nothing gets edited"
 }
]