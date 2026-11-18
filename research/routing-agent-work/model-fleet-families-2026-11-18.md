# Family routing: the record behind the version-free skill

Record date: 2026-11-18. Repository baseline: `ff7979d` (`origin/main`). Host: agentpc.

`routing-agent-work` routes by model family. At launch the router resolves the selected family to its newest model through the worker CLI's own listing. This record holds what that change moved out of the skill: how each CLI resolves a family, the claims that named one version, the version each was measured on, and the observations that shaped the rules. It is a research record, not shipped skill text.

Earlier evidence stays where it is: [2026-11-10](model-fleet-update-2026-11-10.md), [2026-10-06](model-fleet-update-2026-10-06.md), [2026-09-22](model-fleet-update-2026-09-22.md), [2026-09-16 review](model-fleet-review-2026-09-16.md), and [the Sol and Luna 6 research](sol-luna-6-research-2026-09-22.md).

## How each CLI resolves a family

Checked on agentpc from help text, offline files, and listing commands. No model call ran.

| CLI | Method | Evidence |
|---|---|---|
| Claude Code 2.1.327 | Pass the alias `opus`, `fable`, `sonnet`, or `haiku` to `--model`. | `claude --help` for `--model` says: "Use an alias for the latest model (e.g. 'fable', 'opus', or 'sonnet')". The help text names no `haiku` alias. The evidence for `haiku` is the binary's strings, which include `'fable', 'opus', 'sonnet', 'haiku') or full model ID`. |
| Codex 0.169.0 | `codex debug models` renders the catalog as JSON: `{models:[{slug, visibility, available_access_programs, supported_reasoning_levels, ...}]}`. Codex has no alias. The script takes the visible slug `gpt-<ver>-<family>` with the highest version. | `~/.codex/models_cache.json`; the four entries compared below are in [the evidence folder](evidence/fleet-2026-11-18/codex-sol-astra-entries.json). |
| Grok 1.0.88 | `grok models` prints `* grok-4.7 (default)`, `- grok-4.7-build-fast`, `- grok-4.6`, and `- grok-4.5`. The script takes the highest-version `grok-<ver>` with no suffix. | `~/.grok/models_cache.json` holds the same identifiers and their `reasoning_efforts`. |
| OpenCode 2.3.0 | `opencode models` prints one identifier per line: 511 lines, 359 under `openrouter`. The script matches the provider-prefixed pattern. | The listing is a free listing command, not a model call. |

The script is `scripts/resolve_model.py`. Its `--self-test` covers the cases below, and the live runs follow.

### Why the script

Resolution is mechanical, repeated on every non-Claude launch, and fragile when done by hand:

- Versions sort numerically (`6` < `6.1` < `6.2`), and xAI numbering breaks a pure numeric order: the OpenRouter listing has `grok-4.20` beside `grok-4.3` to `grok-4.7`, and `grok-4.20-0309` is the older model. When the integer-tuple winner and the plain-decimal winner differ, the script reports `ambiguous`.
- Speed variants and sibling tiers must drop out: `-build-fast`, `-highspeed`, `-ultraspeed`, `-flash`, `-flashx`, `-prime`, `-turbo`, and the hidden `gpt-reserve`.
- A provider order can pin a stale version. On agentpc, Cloudflare Workers AI lists `glm-4.7-flash` and OpenRouter lists `glm-5.3-flash`, so resolving each provider row alone would launch the older model. The script resolves across every row and reports the older rows as `stale`.
- DeepSeek Flash ties inside one provider: `deepseek-v4.1-flash` and `deepseek-v4.1-flash-1017` share version 4.1. The patterns require the four-digit snapshot and capture it as `s`. A second snapshot of one version on any row, or different snapshots on different rows, exits 3, and one snapshot mirrored across rows resolves in provider order. The script never sorts snapshots, because `MMDD` wraps at the year boundary.

### Decision: no OpenRouter `~vendor/<family>-latest` aliases

OpenRouter lists aliases such as `~moonshotai/kimi-latest`, `~google/gemini-pro-latest`, `~x-ai/grok-latest`, `~z-ai/glm-latest`, and `~deepseek/deepseek-flash-latest`. The skill needs the resolved identifier to pin the host, check effort variants, and record the run. A server-side alias hides the target model and can change which tier it means: `gemini-pro` does not map clearly to Carbon. The same reason covers `gpt-daybreak-blue-latest`, which earlier research found pointing at `gpt-5.6-sol` while `gpt-6-sol` existed ([the Sol and Luna 6 research](sol-luna-6-research-2026-09-22.md)).

### Live resolution on agentpc

These runs read the live listings on 2026-11-18 from `/home/tyler/code/kalepail-skills`. The direct `moonshotai/` provider is absent from agentpc's OpenCode listing, so the Kimi highspeed fixture in the self-test is synthetic and its live run reports no match.

| Family | Resolved identifier |
|---|---|
| Sol | `gpt-6.2-sol` |
| Astra | `gpt-6.2-astra` |
| Terra | `gpt-6.1-terra` |
| Luna | `gpt-6-luna` |
| Sol under Daybreak Blue (`--access-program daybreak_blue`) | `gpt-6-sol` |
| Grok | `grok-4.7` |
| Kimi | `openrouter/moonshotai/kimi-k3.1-pro` |
| Kimi highspeed | no match: the direct provider is absent |
| Gemini Carbon | `openrouter/google/gemini-4-carbon` |
| GLM | `cloudflare-workers-ai/@cf/zai-org/glm-5.3`, with `openrouter/z-ai/glm-5.3` as an alternate |
| GLM Flash | `openrouter/z-ai/glm-5.3-flash`; the Cloudflare row is stale at `glm-4.7-flash` |
| DeepSeek Flash | `cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v4.1-flash-1017`, with the OpenRouter mirror of the same snapshot as an alternate (the free row was removed afterward; see the dispositions) |
| Muse Ember | `openrouter/meta/muse-ember` |
| Muse Wonder | `openrouter/meta/muse-wonder` |
| MiMo Pro | `openrouter/xiaomi/mimo-v2.6-pro` |

## Observations

### The new Sol and Astra

The Codex catalog on agentpc lists `gpt-6.2-sol` and `gpt-6.2-astra` beside `gpt-6.1-sol` and `gpt-6-astra`. The four full entries, minus `model_messages`, are in [the evidence folder](evidence/fleet-2026-11-18/codex-sol-astra-entries.json).

Same in both versions: reasoning levels low to ultra, a 500k Sol window and a 272k Astra window (both with an 872k maximum), search-tool support, and multi-agent v2 at `xhigh`. The catalog descriptions still match the roles: "Fast, go-to model for coding and everyday work." for Sol and "Our most capable model for complex coding and professional work." for Astra.

Different:

- `gpt-6.2-sol` adds audio input. Nobody has measured it, and the skill adds no audio route for it.
- `gpt-6.2-sol` adds the `ultrafast` service tier.
- Astra's default effort changed from `medium` (`gpt-6-astra`) to `low` (`gpt-6.2-astra`). The skill sets effort explicitly, so the default does not matter.
- Astra's `supports_experimental_context` changed from true to false, and the experimental tool list changed on both. No routing rule uses either.
- The catalog descriptions of `gpt-6.1-sol` and `gpt-6-astra` read "Previous generation model for coding and everyday work." and "Previous generation model for complex coding and professional work."
- Daybreak eligibility: `gpt-6-sol` lists `daybreak_blue`, and `gpt-6.1-sol` and `gpt-6.2-sol` list only `standard`.

No routing rule depends on a property that only an older version had. The "lowest cost per task among the frontier routes" clue was measured on `gpt-6.1-sol` and moved here.

### The Daybreak alias

The catalog lists `gpt-daybreak-blue-latest`, display name "Daybreak Blue", described as "Latest frontier agentic coding model for broad defensive cybersecurity work" and limited to `daybreak_blue`. The previous `fleet.md` called the alias deprecated. No research record supports that: `rg -i deprecat` over `research/routing-agent-work/` finds nothing about the alias, and the catalog lists it as visible. The skill drops the sentence. It tells the router not to select the alias because it does not name the model it runs, and to resolve the newest Sol whose catalog entry lists `daybreak_blue`. Whether the Daybreak route should use the alias is an owner decision.

### Dead OpenCode catalog cache

`references/opencode.md` reads effort variants from `~/.cache/opencode/models.json`. Under OpenCode 2.3.0 on agentpc that directory holds only `bin`, and `opencode models` has no flag that prints variants. Under family routing, a version nobody has launched reaches the run with no way to read its variants first. The skill still carries that check. This item does not fix it.

## Effort policies the skill kept

The owner's instruction carries these effort ranges forward as family policy. Each was tuned on measurements of one version. The skill states a "because" clause only when two or more versions of the family show it. A new version may behave differently; the "Review the fleet" triggers and the effort-fallback launch step guard against that.

| Policy | Last measured on | Two versions? |
|---|---|---|
| Luna: use `max` | GPT-5.6 Luna (35.9% against 29.4% for `high`) and GPT-6 Luna (AA 37 against 32) | The direction, yes. "At a small cost" holds on GPT-6 Luna only |
| Grok: use `xhigh` | Grok 4.7 | No: bare policy |
| DeepSeek Flash: use `max` | DeepSeek V4.1 Flash (1017) | No: bare policy |
| GLM: `high`, not `max` | GLM-5.3 | No: bare policy. The `limit.output` note is a harness fact and stays |
| Muse Ember: use `max` | Muse Ember | No: bare policy |
| Sonnet: not below `xhigh` | Sonnet 5.5 | No: bare policy |
| Fable: no `max` | Fable 5.2 | No: bare policy |
| Terra: top at `xhigh` | GPT-6.1 Terra | No: bare policy |

The search covered the files in `research/routing-agent-work/` with `rg`. A version not named in a measurement there counts as not measured.

## Claims removed from the skill

Each claim below is quoted exactly from `git show origin/main:skills/productivity/routing-agent-work/references/fleet.md`, or from `SKILL.md` or `evals/evals.json` where marked. Every claim has a disposition:

- **moved to this record**: a measurement or rank tied to one version; the live text no longer states it;
- **kept as policy**: the live text keeps the routing rule as a family policy, without the number;
- **dropped as structural-duplicate**: another rule already covers it;
- **replaced**: the live text carries an identifier pattern or a new trigger in its place;
- **dropped: unsourced** or **dropped: framing**: the claim had no traceable source or only framed a list.

"Measured on" names the versions the claim was measured on.


### Know the cost basis

- Quote: "On the Vals Index, Sonnet 5.5 uses the most tokens per task. GPT-6.1 Sol and GPT-6 Astra use the fewest among the frontier routes. Treat token counts as an efficiency clue, not as a limit measure."
  - Measured on: Sonnet 5.5, GPT-6.1 Sol, GPT-6 Astra; Vals Index.
  - Disposition: moved to this record.
  - Note: Source not traced in the research records; carried as written in `fleet.md`.
- Quote: "Fable 5.2 can use at most half of that limit, and it uses the limit fastest."
  - Measured on: Policy about the Claude subscription limit; no measurement.
  - Disposition: kept as policy (Fable keeps the half-limit cap).

### Treat challenger findings as leads

- Quote: "Seven challengers trail the default routes on terminal work and on the Artificial Analysis intelligence index."
  - Measured on: GLM-5.3, GLM-5.3 Flash, DeepSeek V4.1 Flash, MiMo V2.6 Pro, Muse Ember, Muse Wonder 1.0, Grok 4.7 against the default routes; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record; the challenger list stays as policy.
- Quote: "Muse Wonder 1.0 scores slightly above GPT-6.1 Sol on the Vals Index."
  - Measured on: Muse Wonder 1.0 (64.88%) and GPT-6.1 Sol (63.94%), Vals Index read 2026-11-09; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "Kimi K3.1 Pro matches or beats GPT-6.1 Sol on terminal evaluations. It trails on composite, science, and knowledge evaluations."
  - Measured on: Kimi K3.1 Pro and GPT-6.1 Sol; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.

### Know each route: Opus

- Quote: "Default Claude route and Anthropic's recommended daily driver."
  - Measured on: Opus 5.5; vendor positioning.
  - Disposition: moved to this record (vendor claim); the default-route rule stays as policy.
- Quote: "Leads the Artificial Analysis Coding Agent Index. Ties Fable 5.2 for first on Vals Terminal-Bench. Places near the top of the LMArena text and creative-writing boards"
  - Measured on: Opus 5.5, Fable 5.2; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "Above `xhigh`, escalate to Fable 5.2: at `high`, it scores above Opus 5.5 at `max` on the Artificial Analysis index at a lower cost per task."
  - Measured on: Fable 5.2 `high` (62, $9.08) against Opus 5.5 `max` (59, $10.04), AA Intelligence Index v5; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: kept as policy ("Above `xhigh`, escalate to Fable"); the reason is moved.
- Quote: "Use Opus 5.5 only for defensive review of the caller's own code."
  - Measured on: Policy.
  - Disposition: kept as policy.

### Know each route: Fable

- Quote: "It leads the Artificial Analysis intelligence index, the Vals Index, and the Artificial Analysis HLE-Diamond and Terminal-Bench-Science runs. It ties Opus 5.5 for first on Vals Terminal-Bench."
  - Measured on: Fable 5.2; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "it leads the Artificial Analysis 3D-building board"
  - Measured on: Fable 5.2 `max` (1271 Elo); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "Anthropic recommends Opus 5.5 for everyday work."
  - Measured on: Vendor positioning, Opus 5.5.
  - Disposition: kept as policy ("Opus is the default for everyday work").
- Quote: "On the Artificial Analysis Terminal-Bench run, it ties Opus 5.5 and trails Kimi K3.1 Pro and Gemini 4 Carbon."
  - Measured on: Fable 5.2 (60%), Opus 5.5, Kimi K3.1 Pro (67%), Gemini 4 Carbon (65%); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "`max` adds 3 points over `xhigh` on the Artificial Analysis index at nearly twice the cost per task, and it scores lower than `xhigh` on ARC-AGI."
  - Measured on: Fable 5.2 `max` against `xhigh`; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record; "Do not use `max`" stays as policy.
- Quote: "Claude Code defaults it to `medium`; set the effort explicitly."
  - Measured on: Fable 5.2 in Claude Code; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: kept as policy ("Set the effort explicitly"); the default observation is moved.

### Know each route: Sonnet

- Quote: "At `max`, it is second on the Vals Index and nearly matches Opus 5.5 on terminal work"
  - Measured on: Sonnet 5.5; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "It scores far lower below `xhigh`."
  - Measured on: Sonnet 5.5; [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: kept as policy ("Do not route Sonnet below `xhigh`"); the reason is moved.
- Quote: "At `xhigh` and `max`, its quality is similar to Opus 5.5, and both use the same weekly limit."
  - Measured on: Sonnet 5.5, Opus 5.5.
  - Disposition: moved to this record for the quality claim; the shared weekly limit stays as policy.
- Quote: "It uses the most tokens per task in the fleet."
  - Measured on: Sonnet 5.5.
  - Disposition: moved to this record.
  - Note: Source not traced in the research records; carried as written in `fleet.md`.

### Know each route: Haiku

- Quote: "It trails GPT-6.1 Terra and GPT-6.1 Sol on coding and terminal evaluations. Muse Ember scores as high or higher at a lower cost per task."
  - Measured on: Haiku 5.5, GPT-6.1 Terra, GPT-6.1 Sol, Muse Ember; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.

### Know each route: Sol

- Quote: "Lowest cost per task among the frontier routes"
  - Measured on: GPT-6.1 Sol; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "`max` scores higher than `xhigh` on independent evaluations."
  - Measured on: GPT-6.1 Sol; [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: moved to this record; "Use `max` for hard lanes with a stop budget" stays as policy.
- Quote: "Opus 5.5 scores higher on independent terminal evaluations; use Opus 5.5 when terminal failure cost is high."
  - Measured on: Opus 5.5 against GPT-6.1 Sol; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: kept as policy ("Use Opus when terminal failure cost is high"); the reason is moved.

### Know each route: Astra

- Quote: "Fable 5.2 scores higher on the Artificial Analysis science runs."
  - Measured on: Fable 5.2, GPT-6 Astra; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "On coding-agent evaluations, Astra scores about the same as GPT-6.1 Sol at several times the cost."
  - Measured on: GPT-6 Astra, GPT-6.1 Sol; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: kept as policy ("Keep ordinary coding on Sol, not Astra"); the numbers are moved.

### Know each route: Terra

- Quote: "It trails GPT-6.1 Sol on coding and terminal work. In Codex, `xhigh` matches `max` on the Artificial Analysis coding-agent index."
  - Measured on: GPT-6.1 Terra, GPT-6.1 Sol; [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: moved to this record; the `medium` to `xhigh` range and "Keep difficult lanes on Sol" stay as policy.

### Know each route: Luna

- Quote: "Use `max`; it scores much higher than `high` at a small cost."
  - Measured on: GPT-5.6 Luna (35.9% against 29.4%, review 2026-09-16) and GPT-6 Luna (AA 37 against 32, sol-luna-6 research). The direction held on both versions. "At a small cost" held on GPT-6 Luna only.
  - Disposition: kept as policy ("Use `max`; it scores higher than `high`"); "much" and "at a small cost" are moved.

### Know each route: Sol under Daybreak Blue

- Quote: "The `gpt-daybreak-blue-latest` alias is deprecated."
  - Measured on: No source. `rg -i deprecat` over the research records finds nothing about the alias, and the Codex catalog lists it as visible.
  - Disposition: dropped: unsourced. The skill now says not to select the alias because it does not name the model it runs.
- Quote: "GPT-6.1 Sol and Astra get reduced refusals only with Daybreak Red approval."
  - Measured on: GPT-6.1 Sol and GPT-6 Astra.
  - Disposition: replaced by the family rule: a Sol or Astra version whose catalog entry lacks `daybreak_blue` is not a Daybreak Blue route.
- Quote: "In a headless Codex run, pass `-m gpt-6-sol -c daybreak=true` on that command."
  - Measured on: GPT-6 Sol; the `daybreak_blue` listing in the catalog.
  - Disposition: kept as policy with `-m <resolved>` in place of the identifier.

### Know each route: Grok

- Quote: "`low` and `medium` score much lower on the Vals boards."
  - Measured on: Grok 4.7; [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: kept as policy ("Use `xhigh`"); the reason stays out because only one version was measured.
- Quote: "It trails the default routes on independent coding and terminal evaluations."
  - Measured on: Grok 4.7 (28.79% on Vals TB4 at $18.09 per test); [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: moved to this record; "Do not use it as a coding fallback" stays as policy.

### Know each route: Gemini Carbon

- Quote: "It is third on the Vals Index and second on the Artificial Analysis intelligence index, at about 60% of Fable 5.2's cost per Vals test."
  - Measured on: Gemini 4 Carbon; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "It costs more per task than Kimi K3.1 Pro and the open-weight routes."
  - Measured on: Gemini 4 Carbon against Kimi K3.1 Pro; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved; "It is not a low-cost route" stays as the coarse cost tier.
- Quote: "It trails Opus 5.5 on the Artificial Analysis Coding Agent Index and on Vals Terminal-Bench."
  - Measured on: Gemini 4 Carbon, Opus 5.5; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.

### Know each route: Kimi

- Quote: "It leads the Artificial Analysis Terminal-Bench run and the open-weight models on the Artificial Analysis intelligence index"
  - Measured on: Kimi K3.1 Pro; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "It is slow and verbose. It is weak on science and hard knowledge."
  - Measured on: Kimi K3.1 Pro; [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: moved to this record; "Do not use it to review science or research" stays in the reviewer pairing.
  - Note: Source not traced in the research records; carried as written in `fleet.md`.

### Know each route: Muse Wonder

- Quote: "it leads the Vals CyberBench"
  - Measured on: Muse Wonder 1.0.
  - Disposition: moved to this record.
  - Note: Source not traced in the research records; carried as written in `fleet.md`.
- Quote: "It trails Gemini 4 Carbon on the Vals Index and Vals Terminal-Bench, at a similar or higher cost per test."
  - Measured on: Muse Wonder 1.0, Gemini 4 Carbon; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.

### Know each route: Muse Ember

- Quote: "Lowest cost per task in the fleet on the Vals boards."
  - Measured on: Muse Ember ($0.15 per Vals Index test); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved; "Low-cost route" stays as the coarse cost tier.
- Quote: "It scores above GPT-6 Luna, GLM-5.3 Flash, and DeepSeek V4.1 Flash on Vals Terminal-Bench and the Artificial Analysis intelligence index"
  - Measured on: Muse Ember; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "It trails the frontier routes by a wide margin."
  - Measured on: Muse Ember; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved; "Keep consequential interpretation on a stronger route" stays as policy.
- Quote: "Use `max`; it scores 2 points above `xhigh` on the Artificial Analysis index at a similar cost."
  - Measured on: Muse Ember `max` (36) against `xhigh` (34); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: kept as policy ("Use `max`"); the reason stays out because only one version was measured.

### Know each route: GLM

- Quote: "`high` scores higher than `max` on Vals Terminal-Bench."
  - Measured on: GLM-5.3; [2026-11-10 update](model-fleet-update-2026-11-10.md) and [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: kept as policy ("Use `high`, not `max`"); the reason stays out because only one version was measured.
- Quote: "It is slow and verbose, and it costs more per task than its token price suggests."
  - Measured on: GLM-5.3.
  - Disposition: moved to this record.
  - Note: Source not traced in the research records; carried as written in `fleet.md`.

### Know each route: GLM Flash

- Quote: "It trails DeepSeek V4.1 Flash on composite evaluations. Muse Ember scores higher on every independent board at a lower cost; use GLM-5.3 Flash when the lane needs open weights."
  - Measured on: GLM-5.3 Flash, DeepSeek V4.1 Flash, Muse Ember; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved; "Use it when the lane needs open weights" stays as policy.

### Know each route: DeepSeek Flash

- Quote: "Among the open-weight routes, it trails only Kimi K3.1 Pro on the Artificial Analysis index, and it leads GLM-5.3 on the Vals Index."
  - Measured on: DeepSeek V4.1 Flash (1017); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "Lower levels score much lower on the Vals boards."
  - Measured on: DeepSeek V4.1 Flash (1017).
  - Disposition: kept as policy ("Use `max`"); the reason stays out because only one version was measured.
  - Note: Source not traced in the research records; carried as written in `fleet.md`.
- Quote: "It trails GLM-5.3 and GLM-5.3 Flash on terminal work."
  - Measured on: DeepSeek V4.1 Flash (1017); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "DeepSeek V4.1 Flash (1017)"
  - Measured on: The snapshot `1017` named a dated release.
  - Disposition: replaced by the four-digit snapshot in the identifier pattern; a second snapshot of one version fails closed.

### Know each route: MiMo Pro

- Quote: "It is slow. It trails Kimi K3.1 Pro and the GLM routes on terminal work."
  - Measured on: MiMo V2.6 Pro; [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: moved to this record.

### Know the models outside the fleet

- Quote: "These models score well but are not routable from the four worker CLIs:"
  - Measured on: Framing sentence.
  - Disposition: dropped: framing; the skill states only that the models are not routable.
- Quote: "- Gemini 4 Argon: Gemini 4 Carbon scores higher on the Vals Index, Vals Terminal-Bench, and the Artificial Analysis index at a lower cost per task."
  - Measured on: Gemini 4 Argon (50, 69.39%, 57.58%) against Gemini 4 Carbon (60, 70.45%, 63.13%); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "- Muse Spark 1.3: Muse Ember scores higher on the Vals Index and Vals Terminal-Bench at a small fraction of the cost per task."
  - Measured on: Muse Spark 1.3, Muse Ember; [2026-10-06 update](model-fleet-update-2026-10-06.md) and [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "- Kimi K3: Kimi K3.1 Pro scores higher on every independent board at a lower price."
  - Measured on: Kimi K3, Kimi K3.1 Pro; [2026-10-06 update](model-fleet-update-2026-10-06.md).
  - Disposition: dropped as structural-duplicate: Kimi K3 is an older version of the Kimi family, and resolution never selects it.
- Quote: "- Grok 4.7 Fast: the same model at a higher price."
  - Measured on: Grok 4.7 Fast.
  - Disposition: kept as policy ("Grok fast variants and every other speed variant: the same model at a higher price").
- Quote: "- DeepSeek V4 Pro: DeepSeek V4.1 Flash scores higher at a lower cost."
  - Measured on: DeepSeek V4 Pro against DeepSeek V4.1 Flash; no later Pro version was measured.
  - Disposition: moved to this record.
- Quote: "- GLM-5.3 Prime and FlashX: no independent evaluations."
  - Measured on: GLM-5.3 Prime, GLM-5.3 FlashX.
  - Disposition: moved to this record; the identifier patterns exclude both tiers.
- Quote: "- Qwen 3.8 Max: closed weights and a high cost per task."
  - Measured on: Qwen 3.8 Max.
  - Disposition: moved to this record; closed weights alone do not exclude a family, because Muse Ember has closed weights and is listed.
- Quote: "- MiniMax M3 and M3.1 Flash: low terminal scores, and MiniMax trains on API input."
  - Measured on: MiniMax M3, M3.1 Flash.
  - Disposition: the terminal-score reason is moved; "MiniMax trains on API input" stays as the structural exclusion.
- Quote: "- Gemini 3.8 Flash: Muse Ember and GLM-5.3 Flash score higher on terminal work at a lower cost."
  - Measured on: Gemini 3.8 Flash against Muse Ember and GLM-5.3 Flash.
  - Disposition: moved to this record.
- Quote: "- Inkling 2 Small: low terminal scores at a high token use."
  - Measured on: Inkling 2 Small (12.63% on Vals Terminal-Bench 4.0); [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.
- Quote: "- Mistral Large 4: no fleet lane fits it, and it has few independent evaluations."
  - Measured on: Mistral Large 4.
  - Disposition: moved to this record.
- Quote: "- Claude Mythos 5.2: Anthropic's approved cybersecurity and life-sciences programs only."
  - Measured on: Claude Mythos 5.2.
  - Disposition: kept as policy without the version.

### Select the provider

- Quote: "`openrouter/moonshotai/kimi-k3.1-pro`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`moonshotai/kimi-k3.1-pro`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`moonshotai/kimi-k3.1-pro-highspeed`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`openrouter/google/gemini-4-carbon`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`cloudflare-workers-ai/@cf/zai-org/glm-5.3`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`openrouter/z-ai/glm-5.3`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`cloudflare-workers-ai/@cf/zai-org/glm-5.3-flash`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`openrouter/z-ai/glm-5.3-flash`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`opencode/glm-5.3-flash-free`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v4.1-flash-1017`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`openrouter/deepseek/deepseek-v4.1-flash-1017`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "3. `opencode/deepseek-v4.1-flash-free`, when the lane fits its smaller context and output limits"
  - Measured on: Provider row; no measurement.
  - Disposition: removed from the provider order. The free identifier carries no snapshot, so its snapshot identity cannot be checked against the Cloudflare and OpenRouter rows. Resolution requires the four-digit snapshot (captured as `s`) on every DeepSeek Flash row. The owner may want the row back with an identity check; see the owner questions in `EXEC.md`.
- Quote: "`openrouter/meta/muse-ember`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`openrouter/meta/muse-wonder`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").
- Quote: "`openrouter/xiaomi/mimo-v2.6-pro`"
  - Measured on: Pinned identifier; no measurement.
  - Disposition: replaced by the family's identifier pattern in `fleet.md` ("Select the provider").

### Review the fleet

- Quote: "Review the fleet when a listed model gets a successor. Also review it when a new model tops an independent board."
  - Measured on: Trigger.
  - Disposition: replaced: a successor of a listed family now routes at once, and the trigger is a new family, a family that leaves the listings, or a rejected effort value.

### Pair independent reviewers

- Quote: "- Kimi K3.1 Pro can review code and terminal work from another family. Do not use it to review science or research."
  - Measured on: Kimi K3.1 Pro.
  - Disposition: kept as policy without the version.

### SKILL.md

- Quote: "It places near the top of independent human-preference evaluations of text and writing."
  - Measured on: Opus 5.5; LMArena text and creative-writing boards; [2026-11-10 update](model-fleet-update-2026-11-10.md).
  - Disposition: moved to this record.

### Eval expectations (id 52)

- Quote: "Sonnet 5.5 scores far lower below xhigh, and at xhigh and max its quality is similar to Opus 5.5."
  - Measured on: Same measurements as the matching `fleet.md` claim.
  - Disposition: moved to this record; the case still expects the same selection.

### Eval expectations (id 54)

- Quote: "because max scores higher than xhigh on independent evaluations"
  - Measured on: Same measurements as the matching `fleet.md` claim.
  - Disposition: moved to this record; the case still expects the same selection.

### Eval expectations (id 72)

- Quote: "which uses few tokens per task"
  - Measured on: Same measurements as the matching `fleet.md` claim.
  - Disposition: moved to this record; the case still expects the same selection.

### Eval expectations (id 78)

- Quote: "Fable 5.2 at high scores above Opus 5.5 at max on the Artificial Analysis index at a lower cost per task. Set the effort explicitly, because Claude Code defaults Fable 5.2 to medium."
  - Measured on: Same measurements as the matching `fleet.md` claim.
  - Disposition: moved to this record; the case still expects the same selection.

### Eval expectations (id 80)

- Quote: "Gemini 4 Carbon scores higher on the independent boards at a lower cost per task."
  - Measured on: Same measurements as the matching `fleet.md` claim.
  - Disposition: moved to this record; the case still expects the same selection.

## Proof gap

The change was checked with the resolver's self-test, live listing runs, JSON and schema checks, a version-pin gate, a syntax check, and a frontmatter check. No behavior eval ran. The authoring standard asks for clean-session runs against the previous version. Behavior stays unproven until the owner authorizes that run.
