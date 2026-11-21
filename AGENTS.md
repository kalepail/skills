# kalepail skills — agent guide

Personal, opinionated AI-agent skills for Tyler van der Hoeven. This file defines the repository structure and authoring rules. It is the only agent instruction file: Claude Code and Codex read `AGENTS.md` directly, and a `CLAUDE.md` on the path takes precedence over it in Claude Code's default mode.

## What this repo is

Shipped skills live under category folders in `skills/`:

- `engineering/`: technical testing and release workflows.
- `productivity/`: general workflows that are not tied to one product.
- `solo/`: product-specific Solo and SoloTerm workflows.

Use plain task names without an author prefix. Keep a product prefix when it gives necessary scope, such as `solo-*`.

Each category has a `README.md`. It lists every skill, grouped by invocation mode.

Every skill works when installed alone. A skill can invoke another model-invoked skill when that skill is installed. It must keep a safe fallback.

All current skills are model-invoked. Each description states positive triggers and hard negative boundaries. Write the boundaries so a skill stays idle when the task needs no skill-specific choice.

`README.md` is the human-facing catalog, requirements list, and install guide.

## Where things live

| Path | What |
|---|---|
| `skills/<category>/<name>/SKILL.md` | Portable source of truth for the skill |
| `skills/<category>/<name>/references/` | Progressive-disclosure detail, linked explicitly from `SKILL.md` |
| `skills/<category>/<name>/agents/openai.yaml` | Codex UI, invocation-policy, and dependency metadata |
| `skills/<category>/<name>/evals/evals.json` | Trigger and behavior eval cases |
| `skills/<category>/README.md` | Category catalog, grouped by invocation mode |
| `.agents/skills/<name>`, `.claude/skills/<name>` | Flat project-discovery links into categorized sources |
| `skills/productivity/routing-agent-work/` | Official agent, model, effort, fallback, and reviewer selection rules |
| `skills/solo/fan-solo/references/house-style.md` | Solo-specific safety and orchestration mechanics |

### Distribution surfaces

These files control distribution:

- `skills.sh.json` and `.claude-plugin/plugin.json` enumerate every promoted skill.
- `.claude-plugin/marketplace.json` lists the Claude plugin products: the complete collection and standalone `agent-browser-webauthn`.
- `skills/engineering/agent-browser-webauthn/.claude-plugin/plugin.json` defines that standalone plugin.

Codex uses skills.sh or the flat `.agents/skills/` project surface. This repository does not ship a `.codex-plugin` manifest.

After you add, rename, move, or remove a skill, update the enumerating files. Bump the collection `version` in `.claude-plugin/plugin.json` and its marketplace entry together. Keep each marketplace `version` equal to its plugin's `plugin.json` version. Run `claude plugin validate .` and `grok plugin validate .` after you change a manifest.

## House rules

`routing-agent-work` is the official selection authority for agent CLIs, models, effort, fallbacks, and reviewers. Use it when the delegation choice can change the result.

The skill keeps a fixed, manually maintained list of model families. At launch, it resolves the selected family to the newest model in the worker CLI's own listing, so a new model version needs no edit. To add or remove a family, update `references/fleet.md` and the evals together. The skill never adds an unlisted family during a task.

`skills/solo/fan-solo/references/house-style.md` owns Solo-specific safety and orchestration mechanics. Read it before any Solo mutation, agent spawn, shared-state edit, or process control.

Solo skills invoke `routing-agent-work` when it is installed and a selection remains open. Otherwise, they use the caller's explicit route or the configured tool defaults.

## Skill authoring standard

Apply these rules on every skill change:

- Portable core: `SKILL.md` frontmatter is `name` + `description` (plus `license` and string-valued `metadata` when useful). Keep Claude-only fields out. Put Codex presentation and dependencies in `agents/openai.yaml`.
- Description is routing code: what + when + trigger cues + an explicit "Do not use for…" boundary, so sibling skills do not false-trigger on each other.
- Progressive disclosure: `SKILL.md` routes; branch detail lives in `references/`, one hop deep, and each link states when to read it. New `SKILL.md` files target under 200 lines; 500 is the ceiling.
- A skill stays useful installed alone: no required local resource links outside its own directory. Links to live official docs are fine.
- Start instruction-only. Add a script only for fragile, repeated, or mechanically verifiable operations. Execute-test it on representative success and failure inputs.
- Forward-only truth: present tense, single best current behavior, no dates, no not-this-anymore framing. Point drift-prone facts at live authorities (`--help`, model listings, live schemas, current official docs). Fix reality before you document a workaround. Discrepancy history stays in commit messages or session artifacts.
- Evals are tests, not fixtures: keep realistic positive and hard-negative trigger cases plus behavior cases in `evals/evals.json`. Update them with any description or behavior change — triggering is API surface. A JSON file alone proves nothing; prove changed behavior in clean sessions against no-skill or the prior version.

## Dogfood: use the skills to build the skills

This repository self-hosts through per-skill links in `.agents/skills/` and `.claude/skills/`. Each link points into the categorized source tree.

- Route Solo and SoloTerm work through `$fan-solo` and the `solo-*` skills, especially while you build them. Friction met in use is authoring signal: fix the skill, then continue.
- A skill edit is live on its next invocation. Instructions already loaded in the current conversation persist until the skill is invoked again.
- Machine-local dogfood wiring gives each non-Solo skill three global symlinks: `~/.agents/skills/<name>` points into this repository, and `~/.claude/skills/<name>` and `~/.codex/skills/<name>` point to the `~/.agents/skills` hub. Solo skills stay project-local through this repository's `.agents/skills` and `.claude/skills` links.
- New skill checklist: create `skills/<category>/<name>/` with `SKILL.md`, `agents/openai.yaml`, and `evals/evals.json`. Add the project links in `.agents/skills/` and `.claude/skills/`. Add the three global symlinks for a non-Solo skill. Update the category catalog, the root catalog, the README requirements, and the distribution surfaces.

## Third-party dependencies

The skills orchestrate external tools. They do not bundle or authenticate them. `README.md` lists every requirement for users. The agent-relevant details:

- **Solo MCP** (`solo`) — required by `fan-solo` and every `solo-*` skill; no fallback. Enable Solo's local MCP server: <https://soloterm.com/docs/integrations/mcp-server>
- **A fan-out vehicle** — `deep-research` uses any host that supplies isolated worker context and durable results. Without one, it runs lanes sequentially.
- **Parallel** — `deep-research` prefers `parallel-cli` for saved artifacts. Parallel Search MCP and Parallel Task MCP are fallbacks.
- **Perplexity MCP** — `deep-research` uses it as an independent challenge lane.
- **Stellar Raven MCP** — `deep-research` uses it first for Stellar-ecosystem discovery.
- **agent-browser and Node.js 22+** — `agent-browser-webauthn` drives passkey and Stellar smart-account browser tests through Chrome DevTools virtual WebAuthn authenticators.
- **ffmpeg and macOS `afconvert`** — `audio-convert` probes and converts with `ffmpeg`/`ffprobe` and `afconvert`/`afinfo`.
- **A secret scanner** — `commit-push-deploy` scans staged changes and outgoing commits with `gitleaks`, or with the repository's configured scanner, before it commits and pushes.

A missing optional provider degrades to a documented fallback, not a hard failure.

## Conventions

- Solo scratchpads and todos are **ephemeral but consumer-gated**. Promote durable conclusions to repository docs. Retire a record (archive a scratchpad, delete a todo) only after its recorded consumers have consumed the current revision. Scratchpads declare their consumers in `## Retire after`. Mid-run cruft is acceptable; lost mid-cycle context is not.
