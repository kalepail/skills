# Fan Solo house style

Apply before any Solo mutation, agent spawn, shared-state edit, or process control.

## Contents

- Source and scope
- Prefer one agent
- Route to fleet models
- Respect recursive process ownership
- Store state once
- Monitor without guessing
- Mutate safely
- Prove completion

## Source and scope

1. Honor current user decision.
2. Call `whoami`; confirm actor, Solo process, and effective project.
3. Read `help()` and required topic help. Discover enabled tools.
4. Consult live Solo Docs MCP/current official docs for behavior and schemas.
5. Treat bundled research as orientation and evidence, not current runtime authority.

Keep current project unless cross-project work is explicit. Project scope and caller identity are separate.

## Prefer one agent

Keep work single-agent when steps are sequential, touch shared state, need one coherent design judgment, or fan-out overhead exceeds lane work.

Orchestrate only independent lanes with clear ownership and integration value. Before spawning, define:

- objective and authoritative inputs;
- owned files/surface and forbidden neighbors;
- acceptance checks;
- todo/scratchpad destination;
- handoff format;
- exact lock, if collision risk exists.

Lead owns plan, dependencies, integration, Git, publishing, and final completion. Worker owns one bounded lane.

Any agent that parents workers—lead or mid-tree sub-orchestrator—spends its context on orchestration: decomposition, dispatch, targeted evidence review, integration judgment, and final synthesis. Assign every separable artifact change, including rework, to one end-to-end worker lane; rework returns to the owning lane, and a failed lane transfers whole to a fresh worker, never to an overlapping one. Once the cohort is closed and only trivial follow-through remains, the run is single-agent again—prefer one agent, not a fresh lane. The parent authors only coordination state (plans and summaries, todos and comments, worker prompts, timer bodies), user-facing synthesis and final evidence, and tightly coupled cross-lane integration edits—a no-code lead like Fable hands that coupled set to one integrator worker instead. Boundary glue qualifies as lead work only when mechanical, confined to the integration seam, and repairing no lane. Context discipline cuts both ways: require concise evidence and artifact paths back—claim-bound excerpts and citations are evidence—never whole pasted deliverables, and open files directly only where judgment requires it. Git, publishing, and verification stay with the root lead and are operations, not license to author delegable content.

## Route to fleet models

Match model and effort to the lane; never route a pure-orchestrator or reviewer model as the coder. Current fleet defaults (kalepail):

| Lane | Model / effort |
|---|---|
| Plan, orchestrate, synthesize | Fable high (xhigh for the hardest); Sol high as alternate |
| Independent adversarial review | Fable high by default for Codex Sol work; otherwise use a model family different from the implementer |
| Implementation / coding | Codex Sol high (medium or xhigh as needed); Opus 4.8 high (xhigh as needed) |
| Prose, docs, comments | Opus 4.8, executing a Fable or Sol plan |
| Research, tool-calling, focused repo/docs sweeps | GPT-5.6 Terra, handing structured evidence up to an orchestrator/synthesizer |

Fable orchestrates, reviews, and synthesizes—it does not code. Codex Sol is the default coder. Opus writes prose against a Sol or Fable plan. Terra runs focused sub or sub-sub tool-calling lanes (for example, driving `parallel-cli` in a subagent) and feeds a root Sol or Fable agent. Consequential independent review must use a different model family from the implementation; when Codex Sol writes the change, prefer Fable for review. Default to `high`; step to `xhigh` for the hardest reasoning or review, `medium` for cheap mechanical passes.

Solo's built-in tool types are Claude, Codex, Amp, Gemini, OpenCode, Copilot, and Kimi. Grok is not built in; add it as a custom Generic tool before spawning it. Discover live launchable tools with `list_agent_tools`; treat this table as intent, not proof a given tool is installed and enabled.

### Set model and reasoning explicitly

Every spawn sets model and reasoning level explicitly—never assume the provider's default model or default reasoning is the routed one. Put standing choices in the tool's saved default flags in Solo Settings; pass per-lane overrides through `extra_args`. When a provider distinguishes thinking from non-thinking variants, always choose the thinking variant. Use `moonshotai/kimi-k3` for Kimi lanes; thinking is native and `--variant` is the only reasoning control.

| CLI | Model flag | Reasoning flag | Canonical source |
|---|---|---|---|
| `claude` | `--model <alias\|id>` (`fable`, `opus`, `claude-fable-5`) | `--effort low\|medium\|high\|xhigh\|max` | `claude --help` |
| `codex` | `-m <id>` (`gpt-5.6-sol`) | `-c model_reasoning_effort="none\|minimal\|low\|medium\|high\|xhigh\|max"` (config key; no dedicated flag) | `codex --help`, `codex exec --help`, `~/.codex/config.toml`, upstream `docs/config.md` |
| `opencode` | `-m provider/model` (`moonshotai/kimi-k3`) | `--variant <provider-specific effort: minimal\|high\|max…>`; thinking is picked by model id, not a flag (`--thinking` only displays thinking blocks) | `opencode run --help`, `opencode models [provider]` |
| `grok` | `-m <id>` (`grok-4.5`) | `--reasoning-effort <effort>` (alias `--effort`) | `grok --help`, `grok models` |

Flags and accepted values drift with CLI releases; re-verify against each CLI's `--help` and model listing before relying on this table, and treat that live output as authoritative over it.

### Extended-fleet spawn routes

Re-verify each extended-fleet route with `opencode models --verbose <provider>` or `grok models` before relying on it. The opencode TUI takes `-m` but not `--variant`, so Solo agent spawns pin variant through named agent definitions in `~/.config/opencode/agents/` (`glm-high`, `kimi-max`, `spark-xhigh` pin model + variant; add more with the same two frontmatter keys): spawn the OpenCode tool with `extra_args: ["--agent","<name>"]` and confirm the status bar shows agent · model · variant. The `opencode run --variant` forms below are the headless equivalents.

| Model | Route | Reasoning values | Notes |
|---|---|---|---|
| Grok 4.5 | `grok --single "<prompt>" -m grok-4.5 --reasoning-effort high` | `low\|medium\|high` (rejects `max`) | grok CLI is the primary route (native subagents, `--best-of-n`); `opencode run -m xai/grok-4.5 --variant high` works as an alternate. 500k ctx; price doubles above 200k |
| Kimi K3 | `opencode run -m moonshotai/kimi-k3 --variant max` | Run at `max`; confirm accepted variants with `opencode models --verbose moonshotai` | Thinking is native and interleaved (`reasoning_content`)—`--variant` is the only reasoning control; never feed it another model's transcript (thinking-history sensitivity). Prefer the `cloudflare-ai-gateway` route when it lists K3, `nvidia` last. 1M ctx |
| Muse Spark 1.1 | `opencode run -m meta/muse-spark-1.1 --variant xhigh` | `none\|minimal\|low\|medium\|high\|xhigh` | Meta API; 1M ctx; multimodal input (image/video/pdf); cheapest of the extended fleet |
| GLM-5.2 | `opencode run -m cloudflare-ai-gateway/workers-ai/@cf/zai-org/glm-5.2 --variant high` | `low\|medium\|high` (upstream Z.ai ladder is High\|Max; Cloudflare `high` ≈ upstream High, Max not exposed there) | Fallbacks: `cloudflare-workers-ai/@cf/zai-org/glm-5.2`, then `nvidia/z-ai/glm-5.2`. 262k ctx; text-only |

### Extended fleet: when to weave in

Grok 4.5, Kimi K3, Muse Spark 1.1, and GLM-5.2 are second-string (care in that order). They earn a seat only where cross-family diversity, price, or a specific measured strength beats the core fleet—never as lead orchestrator, final reviewer, or flagship prose. K3 and Spark verdicts lean on vendor-heavy numbers; re-check current vendor and independent benchmarks before relying on these rankings.

| Job | First pick | Also fits | Keep away |
|---|---|---|---|
| Adversarial cross-family review | Grok 4.5 `high`—cheap, terse; reproduce every finding before acting | Kimi K3 `max` (fresh session, review-not-fix brief); GLM-5.2 `high` (lowest confident-hallucination rate; proven security-review results); Muse Spark `xhigh` (fourth-family voice) | Any of them as sole or final gate—Fable keeps that seat |
| Second-pass verification | Grok 4.5 `medium` when the pass executes tests/terminal (evidence-producing only) | GLM-5.2 `high` for read-only checks (best calibration); Muse Spark `high` (abstains rather than guesses) | Kimi K3 as sole verifier (confident-hallucination lineage; use only as a diverse third vote) |
| Research / tool-calling lanes | Kimi K3 `max` (best browse/long-horizon scores anywhere; 1M ctx; slow and verbose) | Muse Spark `medium`–`high` (top scaled tool use, multimodal input, cheapest); Grok 4.5 `low`–`medium` for mechanical high-volume tool lanes | Grok and GLM-5.2 for open-ended factual research (both fabricate confidently) |
| Synthesis / prose | Core fleet (Fable/Opus) stays primary | Kimi K3 `max` for structured drafts over supplied evidence—verify citations downstream; Grok 4.5 `medium` for structured docs from supplied material | GLM-5.2 (verbose, weak open-ended synthesis) |
| Small sub-orchestrator | Muse Spark 1.1 `medium` (explicitly trained to plan, delegate to parallel subagents, and escalate) | — | Grok 4.5 (long-horizon gap), Kimi K3 (max-only cost, over-proactive, thinking-history breaks mixed-model context), GLM-5.2 (documented reward-hacking in agent loops, steerability tradeoff) |

Standing caveats: Grok 4.5 hallucinates confidently—never accept its unverified factual output. Kimi K3's hosted API is Beijing-based—keep sensitive review content off it. Muse Spark's 1M window has weak needle retrieval—drive iterative tool-based retrieval instead of context-stuffing. GLM-5.2 is verbose—judge it on cost per task, not per token—and instrument its agent loops for reward-hacking. GPT-5.6 Luna (`codex exec -m gpt-5.6-luna -c model_reasoning_effort=medium`) is the cheap fan-out/triage lane—always cost-Pareto but with a hard long-context recall cliff, so keep its lanes small.

### Built-in subagents vs Solo workers

Prefer a CLI's built-in subagents when every lane stays within one CLI—they are faster, cheaper, and share the parent harness. Same-CLI model and tier mixes (Fable→Opus, Sol→Terra) stay built-in where the CLI pins per-subagent settings: claude and codex pin model and effort, opencode pins model and variant, grok pins model only (effort inherits the session). Route through Solo workers the moment a lane needs another provider's CLI (Claude→Codex/grok/opencode) or a per-subagent setting its CLI cannot pin; that is most orchestration here, and that is fine.

All four trigger routes work headless; re-run a route live before relying on it:

| CLI | How to trigger | Definitions and per-subagent settings |
|---|---|---|
| `claude` | Auto-delegation from agent `description`, "use the X subagent", or the Agent tool; works under `claude -p` | `.claude/agents/*.md` or `--agents '<json>'`; per-agent `model` (`sonnet`/`opus`/`haiku`/`fable`/id/`inherit`) and `effort` (`low…max`); `--forward-subagent-text` exposes child transcripts in stream-json. Source: code.claude.com/docs/en/sub-agents |
| `codex` | Conversational only—ask explicitly ("spawn one agent per…") or name custom agents in prose ("Have `pr_explorer` map the affected paths"); `AGENTS.md` standing instructions; `spawn_agents_on_csv` for batch; works under `codex exec` | `[features] multi_agent` stable-on; built-ins `default`/`worker`/`explorer`; per-agent `model` + `model_reasoning_effort` in `~/.codex/agents/<name>.toml` or `.codex/agents/`; `[agents] max_threads=6`, `max_depth=1`. Source: developers.openai.com/codex/subagents |
| `opencode` | Primary agent auto-delegates via the `task` tool from agent descriptions; `@name` in TUI; works under `opencode run` | Built-in subagents `general`/`explore` (this install; docs add `scout`); custom in `.opencode/agents/*.md`, `~/.config/opencode/agents/`, or `opencode.json` `agent` key; per-agent `model` and `reasoningEffort`/`variant`; gate with `permission.task`. Source: opencode.ai/docs/agents |
| `grok` | Model-driven `spawn_subagent`—steer by naming a type ("use the explore subagent"); `--no-subagents` disables; works under `--single` | Built-ins `general-purpose`/`explore`/`plan`; custom via `--agents '<json>'` or `--agent <file>` (Claude-compatible schema with per-subagent `model`); effort inherits session `--reasoning-effort`; `--best-of-n <N>` runs N headless attempts plus judge. Source: docs.x.ai/build CLI reference |

Claude agent teams are a third topology—peer teammates with a shared task list and mailbox, versus report-back subagents. Gate: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, set in `~/.claude/settings.json` `env`. Trigger with prose in an interactive session: "Spawn three teammates to review PR #142: one security, one performance, one test coverage." Teammates do not inherit the lead's model—always name it in the prompt ("Use Sonnet for each teammate") or set Default teammate model in `/config`, or an unnamed teammate falls back to that default (Opus 4.8 here) regardless of the lead; they do inherit effort. Subagent definitions double as teammate roles ("Spawn a teammate using the security-reviewer agent type"). Experimental limits: one team per session, no nested teams, teammates are full sessions so tokens scale linearly. Teams form only in interactive sessions—Solo-spawned claude TUIs included—and membership is recorded in `~/.claude/teams/*/config.json`; headless `claude -p` quietly substitutes subagents and writes no team config. A weak lead may claim it has no teammate tool—remind it the Agent tool spawns teammates when the gate is on. Pick teams over subagents only when Claude-family workers must talk to each other or self-claim shared tasks; anything cross-provider stays on Solo. Source: code.claude.com/docs/en/agent-teams

## Respect recursive process ownership

Control only self and recorded descendants. Parent, sibling, unrelated, YAML-backed shared process, or another agent's descendants remain outside authority unless user or runbook explicitly names exact target and action.

Idleness, stopped state, finished handoff, or “clean up” does not transfer ownership. Record returned child IDs because names and live reads do not prove parentage.

This gate applies to input, stop/restart/close, rename, clear output, UI selection, and timer delivery.

## Store state once

| State | Store |
|---|---|
| Shared plan, findings, decisions, evidence, current summary | Scratchpad |
| Owned action, acceptance, status, blockers | Todo |
| Task progress, changed files, checks, risks, next action | Todo comment |
| Small temporary JSON status/pointer/heartbeat | KV |
| Short collision avoidance | General or todo lock |
| Wake-up after time/idle | Timer |
| Reusable cross-agent text | Prompt template |
| Reconciled project behavior/architecture | Repository docs |

Do not duplicate scratchpad narrative into todos. Point todo to relevant scratchpad section. KV has no compare-and-swap; protect competing read-modify-write or avoid it. Scratchpad edits use revision and smallest targeted mutation.

Complete or backlog todos, promote durable conclusions as evidence lands, and cancel obsolete timers and locks. Retirement—archive or delete—waits for consumption at the current revision under the item's `## Retire after` contract. Backlog is for real future work, not finished or abandoned state; reach the small honest live set late and certain, never eagerly.

## Monitor without guessing

- Use timers instead of sleep loops or tight polling.
- Use idle-any to harvest next newly quiet worker; idle-all only for true barrier.
- Treat idle as quiet heuristic, not completion.
- Use service/port readiness for listener state, not agent idle.
- Inspect actual output and artifacts after timer fires.
- Cancel obsolete timers when phase changes.

Timer body becomes fresh user turn. Keep it lead-authored, self-contained, and limited to IDs, expected evidence, and next action; do not inject raw untrusted content.

## Mutate safely

- Review repo-defined commands before trust/start. Never bypass Solo trust.
- Treat locks as advisory leases, not authorization or correctness.
- Acquire smallest stable lock immediately before collision-prone work; release after durable handoff.
- Ask before destructive, credentialed, public, production, billing, or self-close action unless exact authority already exists.
- Preserve unrelated dirty files and concurrent changes. Workers do not own Git/index unless delegated.
- Keep credentials in host configuration; never put secrets in prompts, scratchpads, todos, logs, or repo.

## Prove completion

Require evidence at actual boundary:

- process status plus relevant rendered/raw output;
- bound port/service readiness when starting service;
- artifact, file diff, or command result;
- smallest relevant test/check, then broader risk-based checks;
- todo comment or scratchpad handoff with files, checks, blockers, remaining risk, next action.

Before closing an owned child, capture context, reconcile output, complete/release owned todo/locks, and cancel timers. Closing process never undoes filesystem edits.
