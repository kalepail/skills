# kalepail skills — agent guide

Personal, opinionated AI-agent skills for Tyler van der Hoeven. This file defines the repository structure and authoring rules. `CLAUDE.md` points here.

## What this repo is

Shipped skills live under category folders in `skills/`:

- `engineering/`: technical testing skills.
- `productivity/`: general workflows that are not tied to one product.
- `solo/`: product-specific Solo and SoloTerm workflows.

Use plain task names without an author prefix. Keep a product prefix when it gives necessary scope, such as `solo-*`.

Each category has a `README.md`. It lists every skill and groups them by invocation mode.

Every skill works when installed alone. A skill can invoke another model-invoked skill when available. It must keep a safe fallback.

All current skills are model-invoked. Their descriptions include positive triggers and hard negative boundaries. Avoid automatic invocation when no skill-specific choice exists.

`README.md` is the human-facing catalog and install guide.

## Where things live

| Path | What |
|---|---|
| `skills/<category>/<name>/SKILL.md` | Portable source of truth for the skill |
| `skills/<category>/<name>/references/` | Progressive-disclosure detail, linked explicitly from `SKILL.md` |
| `skills/<category>/<name>/agents/openai.yaml` | skills.sh installer interface for Codex presentation and dependencies |
| `skills/<category>/<name>/evals/evals.json` | Trigger and behavior eval cases |
| `skills/<category>/README.md` | Category catalog, grouped by invocation mode |
| `.agents/skills/<name>`, `.claude/skills/<name>` | Flat project-discovery links into categorized sources |
| `skills/productivity/routing-agent-work/` | Official agent, model, effort, fallback, and reviewer selection rules |
| `skills/solo/fan-solo/references/house-style.md` | Solo-specific safety and orchestration mechanics |
| `research/skill-best-practices.md` | The authoring standard this repo builds skills by |
| `research/fan-solo/` | Solo product research: orientation and evidence, never fresher authority than live runtime or docs |

### Distribution surfaces

Three files describe distribution. `skills.sh.json` and `.claude-plugin/plugin.json` enumerate every promoted skill. `.claude-plugin/marketplace.json` lists the Claude plugin products.

Codex uses skills.sh or the flat `.agents/skills/` project surface. This repository does not ship a native Codex plugin. Native Codex plugins require real, flat skill directories and reject this repository's categorized source layout.

Inspect all three files after adding, renaming, moving, or removing a skill. Always update enumerating files. Update marketplace metadata when its contract changes.

## House rules

`routing-agent-work` is the official selection authority for agent CLIs, models, effort, fallbacks, and reviewers. Use it when delegation selection can change the result.

The skill uses a fixed, manually maintained fleet. It does not discover unknown models or update itself. Update its fleet reference and evals together.

`skills/solo/fan-solo/references/house-style.md` owns Solo-specific safety and orchestration mechanics. Read it before any Solo mutation, agent spawn, shared-state edit, or process control.

Solo skills invoke `routing-agent-work` when it is installed and a selection remains. Otherwise, they use the caller's explicit route or the configured tool defaults.

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

This repository self-hosts through direct per-skill links under `.agents/skills/` and `.claude/skills/`. The flat links point into the categorized source tree.

- Route Solo/SoloTerm work through `$fan-solo` and the `solo-*` skills — especially while building them. Friction met in use is authoring signal: fix the skill, then continue.
- A skill edit is live on its next invocation; instructions already loaded in the current conversation persist until re-invoked.
- Machine-local dogfood wiring gives each non-Solo skill three global symlinks. `~/.agents/skills/<name>` points into this repository. Claude and Codex links point to the `.agents` hub. Solo skills stay available through this project's `.agents/skills` and `.claude/skills` links.
- New skill checklist: create `skills/<category>/<name>/` with `SKILL.md`, `agents/openai.yaml`, and `evals/evals.json`. Add three global symlinks for a non-Solo skill. Update the category catalog, root catalog, and distribution surfaces.

## Third-party dependencies

The skills orchestrate external tools; they do not bundle or authenticate them:

- **Solo MCP** (`solo`) — required by `fan-solo` and every `solo-*` skill; no fallback. Enable Solo's local MCP server: <https://soloterm.com/docs/integrations/mcp-server>
- **A fan-out vehicle** — `deep-research` uses any host that supplies isolated worker context and durable results. It runs lanes sequentially when none exists.
- **Parallel** — `deep-research` prefers `parallel-cli` for saved artifacts. Parallel Search and Task MCP are fallbacks.
- **Perplexity MCP** — `deep-research` uses it as an independent challenge lane.
- **Stellar Raven MCP** (`stellar-raven`) — `deep-research` uses it first for Stellar-ecosystem discovery.
- **agent-browser** — `agent-browser-webauthn` drives passkey / Stellar smart-account browser tests via Chrome DevTools virtual WebAuthn authenticators.

Missing optional providers degrade to documented fallbacks, not hard failures.

## Conventions

- Solo scratchpads and todos are **ephemeral but consumer-gated**: promote durable conclusions to repository docs, and retire a record — archive a scratchpad, delete a todo — only after its recorded consumers have consumed the current revision (scratchpads declare this in `## Retire after`). Mid-run cruft is acceptable; lost mid-cycle context is not.
