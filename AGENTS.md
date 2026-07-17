# kalepail skills — agent guide

Personal, opinionated AI-agent skills for kalepail (Tyler van der Hoeven). This file is the entry point for working in this repo: what lives where, the house rules, the authoring standard, and how the repo dogfoods its own skills. `CLAUDE.md` points here.

## What this repo is

Shipped skills live under `skills/`, one directory per skill:

- `agent-browser-webauthn` — passkey and Stellar smart-account browser testing through `agent-browser` and Chrome DevTools virtual WebAuthn authenticators.
- The **Fan Solo family** — `fan-solo` routes broad Solo/SoloTerm requests to the focused `solo-*` skills covering project setup, workspace, processes, observation, troubleshooting, agents, orchestration, deep research, todos, scratchpads, close-out, prompts, and automation.

`README.md` is the human-facing catalog and install guide.

## Where things live

| Path | What |
|---|---|
| `skills/<name>/SKILL.md` | Portable source of truth for the skill |
| `skills/<name>/references/` | Progressive-disclosure detail, linked explicitly from `SKILL.md` |
| `skills/<name>/agents/openai.yaml` | skills.sh installer interface (display name, prompt, tool deps) — not an OpenAI format |
| `skills/<name>/evals/evals.json` | Trigger and behavior eval cases |
| `skills/fan-solo/references/house-style.md` | House rules — see below |
| `research/skill-best-practices.md` | The authoring standard this repo builds skills by |
| `research/fan-solo/` | Solo product research: orientation and evidence, never fresher authority than live runtime or docs |

### Distribution surfaces

Five files describe distribution: `skills.sh.json` and `.claude-plugin/plugin.json` enumerate every skill; `.claude-plugin/marketplace.json` lists the plugin products (the whole collection, plus `agent-browser-webauthn` sourced straight from its skill directory); `.codex-plugin/plugin.json` points at `./skills/`; `.agents/plugins/marketplace.json` points at the repo root. When a skill is added, renamed, or removed, inspect all five plus the README and update the ones whose contract actually changes — the enumerating files always, the root-pointing files only when their metadata is affected.

## House rules

`skills/fan-solo/references/house-style.md` is the house rulebook. Read it before any Solo mutation, agent spawn, shared-state edit, or process control — in this repo's own development too. It is the routing authority: match model and effort to the lane, never route a pure-orchestrator or reviewer model as the coder, and give consequential independent review a different model family than the implementer. The fleet table, per-CLI flags, effort tiers, subagent topologies, and extended-fleet rubric live there; verify launchable tools and flags live before dispatch. Portable skills carry standalone operational copies of routing detail in their own `references/` (they cannot depend on a sibling skill); when routing changes, update house-style.md first, then reconcile the skill-local copies.

## Build skills by the research

`research/skill-best-practices.md` is the authoring standard. Apply it on every skill change:

- Portable core: `SKILL.md` frontmatter is `name` + `description` (plus `license` and string-valued `metadata` when useful). Claude-only fields stay out; Codex presentation and dependencies go in `agents/openai.yaml`.
- Description is routing code: what + when + trigger cues + an explicit "Do not use for…" boundary so sibling skills do not false-trigger on each other.
- Progressive disclosure: `SKILL.md` routes; branch detail lives in `references/`, one hop deep, each link stating when to read it. New `SKILL.md` files target under 200 lines; 500 is the ceiling.
- A skill stays useful installed alone: no required local resource links outside its own directory. Links to live official docs are fine.
- Start instruction-only. Add a script only for fragile, repeated, or mechanically verifiable operations, and execute-test it on representative success and failure inputs.
- Forward-only truth: present tense, single best current behavior, no dates, no not-this-anymore framing. Point drift-prone facts at live authorities (`--help`, model listings, live schemas, current official docs). Fix reality before documenting a workaround; discrepancy history stays in research or session artifacts.
- Evals are tests, not fixtures: keep realistic positive and hard-negative trigger cases plus behavior cases in `evals/evals.json`, and update them with any description or behavior change — triggering is API surface. A JSON file alone proves nothing; prove changed behavior in clean sessions against no-skill or the prior version.

## Dogfood: use the skills to build the skills

This repo self-hosts for Claude Code and `.agents`-aware hosts: the committed `.claude/skills → ../skills` and `.agents/skills → ../skills` symlinks expose the live skills to sessions working in this repo.

- Route Solo/SoloTerm work through `$fan-solo` and the `solo-*` skills — especially while building them. Friction met in use is authoring signal: fix the skill, then continue.
- A skill edit is live on its next invocation; instructions already loaded in the current conversation persist until re-invoked.
- Machine-local dogfood wiring (not a distribution requirement): each skill gets three global symlinks — `~/.agents/skills/<name>` → this repo, then `~/.claude/skills/<name>` and `~/.codex/skills/<name>` → the `.agents` hub. Never copy skill directories into this wiring — copies drift. Installer-made copies elsewhere (skills.sh, manual install) are supported and fine.
- New skill checklist: create `skills/<name>/` (`SKILL.md`, `agents/openai.yaml`, `evals/evals.json`), add the three global symlinks, then update the distribution surfaces and README per "Distribution surfaces".

## Third-party dependencies

The skills orchestrate external tools; they do not bundle or authenticate them:

- **Solo MCP** (`solo`) — required by `fan-solo` and every `solo-*` skill; no fallback. Enable Solo's local MCP server: <https://soloterm.com/docs/integrations/mcp-server>
- **Parallel** — `solo-deep-research` prefers `parallel-cli` for reproducible saved artifacts, with Parallel Search / Task MCP as fallbacks.
- **Perplexity MCP** — `solo-deep-research` uses it as an independent reasoning and counter-evidence lane.
- **agent-browser** — `agent-browser-webauthn` drives passkey / Stellar smart-account browser tests via Chrome DevTools virtual WebAuthn authenticators.

Missing optional providers degrade to documented fallbacks, not hard failures.

## Conventions

- Solo scratchpads and todos are **ephemeral but consumer-gated**: promote durable conclusions to repository docs, and retire a record — archive a scratchpad, delete a todo — only after its recorded consumers have consumed the current revision (scratchpads declare this in `## Retire after`). Mid-run cruft is acceptable; lost mid-cycle context is not.
