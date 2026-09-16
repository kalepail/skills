# Routing skill update validation

Validation date: 2026-09-16.
Baseline commit: `dea99fa`.

## Applied decisions

The user approved the review and specified a stronger preference for Astra.
The updated skill uses Astra at `high` for most Codex work.
It considers Astra at `medium` or `low` for suitable simple tasks before selecting Sol.
Sol remains available for explicit requests, unavailable Astra access, and demonstrated cost or latency advantages.
Terra and Luna retain their specific budget-sensitive roles.

Daybreak Blue covers security reviews, authorized vulnerability exploration, and patch validation.
Its route preserves target limits and checks account access.
It does not count as a different model family from other OpenAI routes.

Muse supports `max` where the selected provider exposes it.
Provider fallback preserves the required effort and accepted data terms.
Codex `ultra` requires permission for automatic delegation within the caller's limits.

Google and DeepSeek remain outside the approved fleet.
The preceding review examined their documentation and catalog entries.
No model-quality evaluation ran for them because the user expressed little interest in adding them.

## Behavior comparison

Two separate clean-context agents evaluated the previous and updated skill versions.
Both used `gpt-6-astra` at `high` and received the same 19 prompts.
Each agent received only its skill version and the prompts, without expected answers.
The sessions evaluated policy decisions using supplied host status.
They did not launch the selected workers or call model providers.

Prompt 36 initially omitted the execution host.
The fixture was clarified to name Codex and rerun in both sessions.

| Check | Previous skill | Updated skill |
|---|---:|---:|
| Primary model, effort, and trigger decisions | 11/19 | 19/19 |
| Changed decisions that match the new policy | — | 8 |
| Preserved decisions | — | 11 |

The checks cover ordinary Astra work, lower Astra effort, Sol fallback, security routing, and different-family review.
They also cover Muse provider selection, delegation limits, API effort, excluded models, and negative triggers.
GLM long-context work and Luna extraction retained their specialist routes.

Manual inspection confirmed that outputs kept unverified access checks explicit.
The outputs preserved security target limits and contributor data conditions.
Neither agent claimed that selected workers launched or task tests passed.

The previous skill produced two Muse policy ambiguities.
Its effort table stopped at `xhigh`, while a later note conditionally permitted `max`.
Its full-route rule required contributor failures without clearly handling unaccepted contributor terms.
The updated evaluator reported no policy contradictions.

[Recorded prompts, decisions, grades, and skill hashes](evidence/2026-09-16-routing-evals.json)

## Structural checks

- The official Skill Creator validator passed.
- `git diff --check` passed.
- The eval file contains 39 unique cases with the required fields.
- `SKILL.md` contains 107 lines; its fleet reference contains 96 lines.
- Relative skill references remain inside the portable skill directory.
- Both project discovery links resolve to the updated source.
- All three global installation links resolve to the updated source.
- Catalog and distribution entries still match the unchanged skill name and path.

## Limits

The comparison tests routing instructions, not model performance or provider availability.
The 19 checks do not execute every assertion in all 39 stored cases.
Each version used one fresh session containing multiple prompts, rather than one session per prompt.
Per-evaluation duration and token usage were unavailable from the native agent interface.
Provider capabilities come from the preceding live review, not these simulated host checks.

No default model settings, credentials, or provider account settings changed.
The existing installation links make the updated skill available on its next invocation.

## Publication review

Gitleaks `8.30.1` found no secrets in the working tree or scanned Git history.
The history review included fetched remote refs, the available pull-request head, and local reflogs.
A separate scan covered all 305 stored Git blobs, including unreachable objects.
The scans used the default rules with inline allow comments and local ignore files disabled.
GitHub returned no secret-scanning alerts and confirmed enabled push protection.
The publication review removed temporary local audit paths from the new research note.
These checks do not prove the absence of every possible secret or copies outside the inspected repository.
