# AI agent skill best practices

Research current through **2026-07-15**. Scope: reusable filesystem-based Agent Skills for OpenAI Codex and Anthropic Claude, plus current structures in `coreyhaines31/marketingskills` and `mattpocock/skills`. Repository observations use immutable commits listed below.

## Executive conclusions

1. **Portable core is small.** Use one directory per skill, required `SKILL.md`, and only common frontmatter: `name` and `description`; add `license` and string-valued `metadata` only when useful. Both vendors build on Agent Skills, whose specification defines `scripts/`, `references/`, and `assets/` as optional and recommends a sub-500-line `SKILL.md` with direct, one-level-deep references ([Agent Skills specification](https://agentskills.io/specification.md)).
2. **Description is routing code.** State what skill does and when it applies; front-load distinguishing intent and natural user language. Include nearby non-goals when overlap exists. Codex uses `description` for implicit matching and may shorten descriptions when its skill-list budget is exceeded; Claude also preloads descriptions and caps each listing entry, so exhaustive synonym dumps waste scarce always-on context ([OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills.md), [Anthropic: Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills)).
3. **Progressive disclosure is three-tier architecture:** metadata always loaded; `SKILL.md` loaded after selection; references/scripts/assets touched only when needed. Main file should route execution, not become encyclopedia ([Anthropic engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [OpenAI skill creator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md)).
4. **Scripts buy determinism, not prestige.** Prefer instructions for judgment-heavy work. Bundle script only for fragile, repetitive, or mechanically verifiable operations; make it self-contained, handle failures, document requirements, and execute-test it ([OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills.md), [Anthropic authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).
5. **Test triggering separately from output quality.** Use hard positive and negative trigger prompts, then behavior cases run in clean sessions both with and without skill. Keep human review for subjective output. Anthropic currently documents this much more completely than OpenAI ([Anthropic: Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills), [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)).
6. **Ship state of truth, not test residue.** Skills record how things work now, in present tense. Verification narration ("spawn-tested", "verified live against the API", test-run stories) stays in session artifacts and commit messages; at most one dated freshness stamp per drift-prone table ("last verified YYYY-MM-DD"), paired with a pointer to the live authority (`--help`, model listing) that overrides the table.
7. **Strict portability excludes Claude-only frontmatter.** Claude Code adds `disable-model-invocation`, `user-invocable`, `context`, `agent`, hooks, and dynamic injection. Current OpenAI official validator rejects unknown top-level fields, including `disable-model-invocation` ([Claude Code frontmatter](https://docs.anthropic.com/en/docs/claude-code/skills), [OpenAI validator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/quick_validate.py)). Keep canonical `SKILL.md` on common subset; put Codex UI/policy/dependencies in `agents/openai.yaml`.

## Official guidance: common ground and differences

| Concern | OpenAI Codex | Anthropic Claude | Portable rule |
|---|---|---|---|
| Required unit | Directory with `SKILL.md`; `name` and `description` required | Directory with `SKILL.md`; Claude Code is more permissive, but open standard requires same pair | Follow strict open specification, not permissive runtime behavior |
| Invocation | Explicit `$skill`/skill picker or implicit description match | Explicit `/skill-name` or implicit description match | Design implicit matching from `description`; document explicit name |
| Initial context | Name, description, path; initial skill list budget is at most 2% of context or 8,000 chars when window unknown | Name and description; Claude Code current listing budget defaults to 1% of context and each description plus `when_to_use` is capped | Front-load signal; avoid long synonym inventories |
| Main instructions | Full `SKILL.md` read only after selection | Full rendered `SKILL.md` enters conversation after invocation and persists | Put common workflow and routing only in main file |
| Supporting content | Optional scripts, references, assets; load/run as needed | Optional sibling docs, examples, scripts, templates; load/run as needed | Direct paths, explicit read/run conditions, one level deep |
| Product adapter | `agents/openai.yaml` supplies UI, implicit-invocation policy, and MCP dependencies | Claude-only frontmatter controls invocation, tools, subagents, hooks, arguments, and dynamic context | Keep product behavior outside common core where possible |
| Distribution | Local/repo skills; native Codex plugin uses `.codex-plugin/plugin.json` and one `skills` path | Local/project skills; Claude plugin uses `.claude-plugin/plugin.json` and may list skill paths | Flat shipped `skills/` tree supports both manifests |
| Validation/evals | Official creator validates schema, tests scripts, and recommends real trigger prompts/iteration; official catalog has some `evaluations/` fixtures | Official docs recommend eval-first development, fresh with/without-skill baselines, at least three cases, human review, and model matrix | Run structural checks on every change; behavior evals for changed skills and releases |

OpenAI explicitly says one skill should do one job, instructions should precede scripts, steps should have explicit inputs/outputs, and trigger prompts should test description quality ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)). Its creator adds two important implementation rules: keep detailed facts out of `SKILL.md`, avoid duplicated content between main file and references, and test every added script by running it ([OpenAI skill creator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md)). Codex-specific presentation and dependencies belong in `agents/openai.yaml`, including human-facing labels/icons/default prompt and MCP declarations ([OpenAI YAML reference](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references/openai_yaml.md)).

Anthropic adds useful prompt-design detail. Set degree of freedom to task fragility: prose for judgment, parameterized patterns for preferred approaches, exact scripts for fragile operations. Write descriptions in third person, use concrete examples, give workflows checkable feedback loops, and test every model intended for use ([Anthropic authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)). Claude Code extensions are valuable but product-specific: manual-only or model-only invocation, allowed/disallowed tools, forked subagent execution, hooks, argument substitution, and shell-backed dynamic context injection ([Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills)).

### Progressive disclosure rules

- **Tier 1 — metadata:** roughly 100-token discovery card. `description` must contain all information needed to decide whether to load skill; “When to use” section hidden in body cannot help selection ([Agent Skills specification](https://agentskills.io/specification.md), [OpenAI skill creator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md)).
- **Tier 2 — `SKILL.md`:** target well below 500 lines and about 5,000 tokens. Include workflow, branch conditions, completion criteria, output contract, safety boundaries, and navigation to resources ([Agent Skills specification](https://agentskills.io/specification.md), [Anthropic authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).
- **Tier 3 — resources:** move branch-specific domain detail to focused references; executable determinism to scripts; output inputs such as templates, fonts, images, and starter files to assets. Say **when to read**, **when to run**, and expected result. Never make agent chase chains of references ([Anthropic engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Agent Skills specification](https://agentskills.io/specification.md)).

Use `references/` for knowledge agent reads. Use `scripts/` for code agent executes. Use `assets/` for files copied, rendered, or transformed into output. Example outputs may live under `examples/` when they teach format; this is common runtime practice but not a required standard directory ([Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills)).

## Testing and evaluation

Minimum credible test stack:

1. **Static validation:** validate every skill against Agent Skills schema and naming rules. Also run Codex official validator if strict Codex compatibility matters, because its accepted top-level field set is narrower than current Claude Code extensions ([Agent Skills validation](https://agentskills.io/specification.md), [OpenAI validator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/quick_validate.py)).
2. **Script checks:** syntax-check and execute bundled scripts against smallest representative fixture, including failure path. This is ordinary software testing, not LLM evaluation.
3. **Trigger evals:** collect realistic should-trigger prompts and difficult adjacent should-not-trigger prompts. Measure false negatives and false positives independently. Anthropic official skill creator recommends about 20 balanced, realistic queries and repeated runs on held-out cases when optimizing description ([Anthropic skill creator](https://github.com/anthropics/skills/blob/9d2f1ae187231d8199c64b5b762e1bdf2244733d/skills/skill-creator/SKILL.md)).
4. **Behavior evals:** start with three representative user tasks. Run each in clean context with skill and without skill, or against previous version. Grade objective assertions programmatically; review subjective artifacts blind when practical. Record quality, tool errors, duration, and tokens ([Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)).
5. **Model and harness matrix:** test models and hosts actually supported. Skill effectiveness depends on underlying model, and host extensions differ ([Anthropic authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).

Do not confuse fixture presence with evaluation execution. JSON cases without runner, baseline, or recorded result document intent but do not prove improvement.

## Case study: `coreyhaines31/marketingskills`

Snapshot: commit [`286d3718d9bd068071792e1e4275388056419928`](https://github.com/coreyhaines31/marketingskills/tree/286d3718d9bd068071792e1e4275388056419928), 2026-07-15.

Measured structure: **47 skills**, **14,267 `SKILL.md` lines** (mean 303.6; range 107–497), **45 `evals/evals.json` files**, **40 skills with `references/`**, **0 skill-local `scripts/`**, and **1 skill-local `assets/` directory**. Collection uses strict common frontmatter (`name`, detailed `description`, `metadata.version`), Claude plugin manifests, standard installation, schema CI, and extensive domain references ([repository](https://github.com/coreyhaines31/marketingskills/tree/286d3718d9bd068071792e1e4275388056419928), [authoring rules](https://github.com/coreyhaines31/marketingskills/blob/286d3718d9bd068071792e1e4275388056419928/AGENTS.md)).

What works:

- Broad domain is split into independently discoverable jobs with explicit neighboring-skill boundaries. Rich descriptions optimize recall and route ambiguous marketing tasks ([copywriting example](https://github.com/coreyhaines31/marketingskills/blob/286d3718d9bd068071792e1e4275388056419928/skills/copywriting/SKILL.md)).
- Every skill checks one shared product-marketing context convention; 44 of 47 include explicit “Related Skills” section. This creates coherent collection behavior.
- Progressive disclosure improved materially: most skills now move frameworks, templates, benchmarks, or playbooks into `references/` rather than crossing 500-line cap.
- Eval coverage is unusually broad. Cases include prompt, expected output, assertions, files, and near-miss routing behavior ([copywriting evals](https://github.com/coreyhaines31/marketingskills/blob/286d3718d9bd068071792e1e4275388056419928/skills/copywriting/evals/evals.json)).
- CI validates changed skill shape; separate scripts support local and official Agent Skills validation ([workflow](https://github.com/coreyhaines31/marketingskills/blob/286d3718d9bd068071792e1e4275388056419928/.github/workflows/validate-skill.yml), [official-validator wrapper](https://github.com/coreyhaines31/marketingskills/blob/286d3718d9bd068071792e1e4275388056419928/validate-skills-official.sh)).

Risks and lessons:

- Descriptions often spend most 1,024-character allowance on synonyms. This favors recall but consumes always-on context and can blur boundaries. Fan Solo should keep only distinct intent branches plus hard near-misses, then prove wording with trigger evals.
- Main files average 304 lines and several sit at 487–497. They comply numerically but leave little growth margin. New material should default to references.
- Eval fixtures are not run by shown validation workflow; CI proves schema, not output quality.
- Twenty-five skill/reference files link outside skill directories into root `tools/`. Individual-skill installers may omit those dependencies, weakening self-contained portability. Fan Solo should keep required resource inside skill or declare/install external dependency explicitly ([ads example](https://github.com/coreyhaines31/marketingskills/blob/286d3718d9bd068071792e1e4275388056419928/skills/ads/SKILL.md)).

## Case study: `mattpocock/skills`

Snapshot: commit [`e9fcdf95b402d360f90f1db8d776d5dd450f9234`](https://github.com/mattpocock/skills/tree/e9fcdf95b402d360f90f1db8d776d5dd450f9234), 2026-07-14. GitHub search found this as Matt Pocock’s relevant first-party skills repository.

Measured structure: **40 skills**, **2,810 `SKILL.md` lines** (mean 70.3; range 7–140), **40 `agents/openai.yaml` adapters**, **23 `disable-model-invocation` skills**, **0 eval fixtures**, **2 script directories**, and numerous directly linked sibling reference files. Promoted engineering/productivity skills are curated through Claude plugin manifest; other buckets remain personal, in-progress, misc, or deprecated ([repository](https://github.com/mattpocock/skills/tree/e9fcdf95b402d360f90f1db8d776d5dd450f9234), [plugin manifest](https://github.com/mattpocock/skills/blob/e9fcdf95b402d360f90f1db8d776d5dd450f9234/.claude-plugin/plugin.json)).

What works:

- Bodies are exceptionally lean. Small orchestrators call reusable model-invoked disciplines; references sit beside owner skill and are disclosed by direct pointers.
- Explicit taxonomy separates human-invoked orchestration from model-invoked reusable discipline. User-invoked skills use a router so humans need not remember entire catalog ([invocation design](https://github.com/mattpocock/skills/blob/e9fcdf95b402d360f90f1db8d776d5dd450f9234/.agents/invocation.md), [router](https://github.com/mattpocock/skills/blob/e9fcdf95b402d360f90f1db8d776d5dd450f9234/skills/engineering/ask-matt/SKILL.md)).
- Every skill has Codex presentation metadata; manual-only intent is mirrored with `policy.allow_implicit_invocation: false` ([Ask Matt adapter](https://github.com/mattpocock/skills/blob/e9fcdf95b402d360f90f1db8d776d5dd450f9234/skills/engineering/ask-matt/agents/openai.yaml)).
- Collection’s own writing skill articulates strong information hierarchy: inline common steps, disclose branch-specific reference, co-locate concepts, avoid duplicate truth, and prune no-op prose ([Writing Great Skills](https://github.com/mattpocock/skills/blob/e9fcdf95b402d360f90f1db8d776d5dd450f9234/skills/productivity/writing-great-skills/SKILL.md)).

Risks and lessons:

- Dual-harness behavior is pragmatic, not strictly spec-clean. Running current OpenAI official validator against `ask-matt` fails because `disable-model-invocation` is unexpected; model-invoked `research` passes. Fan Solo should not copy Claude-only top-level fields into canonical portable files.
- No behavior evals and no validation CI beyond release workflow were present at snapshot. Lean prompts need tests as much as long prompts; composition creates hidden routing risk.
- Bucketed layout forced repository to defer native Codex plugin: Codex manifest accepts one skills path while Claude manifest can enumerate promoted directories. Flat shipped tree avoids this packaging problem ([distribution ADR](https://github.com/mattpocock/skills/blob/e9fcdf95b402d360f90f1db8d776d5dd450f9234/.agents/adr/0002-ship-as-a-claude-code-plugin.md)).

## Recommended Fan Solo architecture

Use one source tree, strict portable core, thin platform adapters, and no generated duplicate skill bodies:

```text
fan-solo/
├── README.md
├── LICENSE
├── .codex-plugin/
│   └── plugin.json                 # when native Codex distribution is needed
├── .claude-plugin/
│   └── plugin.json                 # when native Claude distribution is needed
├── skills/                         # only shipped skills; flat, no draft buckets
│   └── skill-name/
│       ├── SKILL.md                # portable source of truth
│       ├── agents/
│       │   └── openai.yaml         # Codex UI/policy/dependencies
│       ├── references/             # optional, focused, directly linked
│       ├── scripts/                # optional, deterministic helpers only
│       ├── assets/                 # optional, output resources only
│       └── evals/
│           └── evals.json          # portable test intent; runtime-neutral
└── tests/
    └── validate-skills.sh          # one structural/script check entrypoint
```

Keep drafts outside `skills/`, for example `incubator/`, so native plugin can safely point at `./skills/`. Do not create category directories unless manifests on both hosts can select same shipped subset.

Canonical frontmatter:

```yaml
---
name: skill-name
description: Does specific job. Use when user asks for X or provides Y. Do not use for adjacent Z; use z-skill instead.
license: MIT
metadata:
  author: fan-solo
  version: "1.0.0"
---
```

Rules:

- Omit `compatibility`, Claude-only invocation fields, dynamic shell injection, and host-specific tool names from canonical frontmatter. Put genuine runtime requirements in concise `Requirements` section or product adapter.
- Default skills to model- and user-invocable on both hosts. For manual-only high-side-effect workflows, combine explicit confirmation in body with Codex `policy.allow_implicit_invocation: false`; tell Claude users to apply `skillOverrides: "user-invocable-only"` locally. Add Claude-specific source variant only if collection must enforce that policy centrally; do not silently sacrifice strict Codex validation.
- Keep description around 1–3 sentences. Optimize for discriminating intent, not keyword count. Store 8–10 positive and 8–10 hard-negative trigger cases.
- Aim for **under 200 lines** in new `SKILL.md`; 500 is ceiling, not target. Every conditional branch whose detail is unnecessary elsewhere goes to focused reference.
- Keep resource links one level deep and relative to skill root. Skill must remain useful when installed alone. No required `../../shared` or repository-root links.
- Start instruction-only. Add script after repeated runs show same code being regenerated or operation needs deterministic validation. Add smallest fixture and executable check beside test entrypoint.
- Use assets only when output needs template, image, font, schema, or starter file. Do not store documentation in assets.
- Store at least three behavior cases for each nontrivial skill. On pull requests, run schema plus script checks. On changed-skill release/nightly jobs, run fresh with/without-skill behavior evals on Codex and Claude models actually supported. Require human review for subjective Fan Solo outputs.
- Version skill behavior in `metadata.version`; version plugin separately. Record behavior-changing description edits because triggering is API surface.

### Recommended acceptance gate

A Fan Solo skill ships only when:

- strict common frontmatter validates in Agent Skills and Codex validator;
- name matches directory; description has positive trigger and adjacent boundary;
- main file stays self-contained and routes every optional reference/script/asset explicitly;
- every bundled script runs successfully on representative fixture and fails helpfully on bad input;
- trigger set covers positive, hard negative, casual phrasing, and overlap with neighboring skill;
- three behavior cases beat no-skill or previous-version baseline in clean sessions, without unacceptable token/time regression;
- plugin installation exposes exactly shipped skills in both target hosts.

This combines Marketing Skills’ domain coverage, references, and per-skill eval artifacts with Matt Pocock’s lean composition, invocation taxonomy, and Codex adapters—while removing their main portability weaknesses: root-relative dependencies, unexecuted evals, bucketed packaging, and Claude-only fields in canonical frontmatter.

## Sources

### OpenAI and common specification

- [OpenAI Codex manual: Build skills](https://learn.chatgpt.com/docs/build-skills.md) (retrieved 2026-07-15)
- [OpenAI Codex: Save workflows as skills](https://developers.openai.com/codex/use-cases/reusable-codex-skills) (retrieved 2026-07-15)
- [OpenAI skills repository, commit 49f948f](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431) (2026-06-23)
- [Agent Skills specification](https://agentskills.io/specification.md) (retrieved 2026-07-15)

### Anthropic

- [Claude Code: Extend Claude with skills](https://docs.anthropic.com/en/docs/claude-code/skills) (page dated 2026-07-09; retrieved 2026-07-15)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (retrieved 2026-07-15)
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (retrieved 2026-07-15)
- [Anthropic skills repository, commit 9d2f1ae](https://github.com/anthropics/skills/tree/9d2f1ae187231d8199c64b5b762e1bdf2244733d) (2026-07-01)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) (retrieved 2026-07-15)
- [Anthropic: Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) (retrieved 2026-07-15)

### Ecosystem repositories

- [Corey Haines Marketing Skills, commit 286d371](https://github.com/coreyhaines31/marketingskills/tree/286d3718d9bd068071792e1e4275388056419928) (2026-07-15)
- [Matt Pocock Skills, commit e9fcdf9](https://github.com/mattpocock/skills/tree/e9fcdf95b402d360f90f1db8d776d5dd450f9234) (2026-07-14)
