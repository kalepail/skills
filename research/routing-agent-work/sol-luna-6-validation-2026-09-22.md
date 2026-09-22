# GPT-6 Sol and Luna routing validation

Validation date: 2026-09-22.
Baseline commit: `2644e12`.

## Changes

The fleet uses `gpt-6-sol` and `gpt-6-luna` for general Sol and Luna routes.
Astra at `high` remains the ordinary Codex default.
Sol precedes Terra for eligible Codex budget tasks and as the fallback for Luna extraction.
Task estimates must fit the budget.
Luna keeps narrow extraction and triage tasks, with `high` as the starting effort.
Consequential interpretation stays with the stronger routes.

Daybreak Blue remains a separate security alias with its documented `gpt-5.6-sol` base.
That base does not restore the older Sol model as a general route.
Historical research retains the names that its original sources used.

## Behavior comparison

Two fresh agent contexts applied the previous and updated policy to the same 15 prompts.
Both evaluators used `gpt-6-astra` at `high`.
Each received only its policy version and the prompts, without expected answers.
The baseline evaluator received two added prompts after its first 13 responses.
The updated evaluator received all 15 prompts together.

| Primary decision check | Previous policy | Updated policy |
|---|---:|---:|
| Model, effort, and invocation match the updated requirements | 7/15 | 15/15 |

Eight changed decisions match the updated requirements.
Seven preserved decisions still pass.
The checks cover model replacement, budget routing, extraction fallback, effort failures, and delegation limits.
They also cover the Daybreak alias, different-family review, consequential interpretation, and negative triggers.

The baseline failures show the intended policy change, not defects against the old requirements.
[Recorded prompts, responses, grades, and policy hashes](evidence/sol-luna-6-2026-09-22/routing-evals.json)

## Structural checks

- The Skill Creator validator passed.
- `git diff --check` passed.
- The eval file contains 51 unique cases with all required fields.
- Both project links and all three global links resolve to the edited skill.
- The three distribution files retain the correct unchanged skill name and path.
- Remaining old Sol references cover Daybreak or a negative test against the retired general route.
- The tested fleet snapshot matches the final edited fleet.

## Limits

These checks test routing instructions, not model performance or provider access.
They grade primary decisions, not every assertion in all 51 stored cases.
Each policy version used one context for multiple prompts.
No selected task worker ran during the evaluation.
The local catalog confirms identifiers and effort settings, not successful model inference.
The published benchmark findings appear in the [research report](sol-luna-6-research-2026-09-22.md).

No default model settings, credentials, or provider accounts changed.
The installation links expose this skill change on its next invocation.
