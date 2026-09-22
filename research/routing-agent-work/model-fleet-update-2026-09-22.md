# Opus 5.5 fleet update

Update date: 2026-09-22.
Repository baseline: `1c1131a`.

## Recommendation

Replace Opus 5 with Opus 5.5 (`claude-opus-5-5`) in every route.
Make Opus 5.5 the default Claude route.
Put it first for planning, difficult implementation, precision review, technical prose, and budget-sensitive coding.
Rank it above Grok 4.7 wherever both routes appear.
Keep Fable 5.1 as the Claude escalation route.
Keep Astra first for terminal work, primary verification, and bounded Codex work.
Remove Opus 5 from the fleet.

## Facts from Anthropic

Anthropic released Opus 5.5 on September 22, 2026.
The models overview now tells users to start with Opus 5.5 for most workloads.
It recommends Fable 5.1 for demanding reasoning and long-horizon agentic work.
It also recommends Fable 5.1 when Opus 5.5 at higher effort still falls short.
Opus 5 is now a legacy model.
[Models overview](https://platform.claude.com/docs/en/models/overview)

| Item | Opus 5.5 | Opus 5 | Fable 5.1 |
|---|---|---|---|
| Price per million tokens, input / output | $4 / $20 | $5 / $25 | $10 / $50 |
| Cache read per million tokens | $0.20 | $0.50 | 2.5% of input |
| Context / max output | 1M / 128K | 1M / 128K | 1M / 128K |
| API default effort | `medium` | `high` | `high` |
| Effort levels | `low` to `max` | `low` to `max` | `low` to `max` |
| Thinking | Always on | Can be disabled at `high` or below | Always on |
| Comparative latency | Moderate | Moderate | Slower |

[Opus 5.5 model page](https://platform.claude.com/docs/en/models/opus-5-5/overview)
[What's new in Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)
[Effort](https://platform.claude.com/docs/en/build-with-claude/effort)

Anthropic reports these behavior facts:

- Opus 5.5 at `medium` matches or beats Opus 5 at `high` on coding and knowledge-work evaluations.
- At the same effort value, it thinks more per turn than Opus 5, most of all at `xhigh` and `max`.
- It generates output more than 30% faster than Opus 5.
- At default settings, typical workloads cost about 40% less than on Opus 5.
- It sustains long unattended migrations and audits, and it delegates to subagents well.
- An unattended run can end a turn with a progress report before the task is complete.
- It reads charts, diagrams, and screenshots more precisely, and it is more reliable at computer use.
- It follows supplied writing rules and puts the most important information first.

[Prompting Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
[Announcement](https://www.anthropic.com/claude-opus-5-5)

### Safeguards

Opus 5.5 is the first Opus model with Fable 5.1-class safeguards for cybersecurity, biology, and distillation.
Users can find and fix bugs in their own code.
Most other cybersecurity tasks go to Opus 4.8 through a transparent fallback.
A Cyber Verification Program for Opus 5.5 is not yet available.
This limit changes the security route.
[Announcement, Safeguards section](https://www.anthropic.com/claude-opus-5-5)

## Benchmarks

### Vendor-reported

Anthropic reports these results. Opus 5.5 uses `max` effort unless the note says otherwise.

| Benchmark | Opus 5.5 | Fable 5.1 | Opus 5 | GPT-6 Astra | GPT-5.6 Sol |
|---|---|---|---|---|---|
| Terminal-Bench 4.0 (Opus 5.5 at `xhigh`) | 66.4% | 55.8% | 52.3% | 57.9% | 37.3% |
| FrontierCode v1.1 main | 54.4% | 50.3% | 48.0% | 53.3% | 47.5% |
| CursorBench 4.0 | 57.8% | 51.8% | 46.6% | — | 41.7% |
| GDPval-AA v2.1 Elo | 1846 | 1735 | 1708 | 1542 | 1588 |
| AutomationBench | 40.0% | 31.4% | 26.9% | 41.4% | 28.8% |
| Terminal-Bench-Science 0.1 | 58.7% | 52.6% | 29.0% | 64.6% | 22.4% |
| OSWorld 2.0 (partial) | 81.8% | 80.7% | 74.0% | — | — |

The Terminal-Bench 4.0 standard error is ±2.6 points for Opus 5.5.
The GPT-6 Astra and Sol figures are as reported by OpenAI.
Anthropic says the real gap between Opus 5.5 and Fable 5.1 is narrower than these scores suggest.

Anthropic also reports these default-effort (`medium`) results:

- CursorBench 4.0: 52.5% at about one third of Sol `max` cost per task.
- FrontierCode: 54.6%, above Astra's best score at about one fifth of the cost per task.
- Terminal-Bench 4.0: Opus 5.5 at default effort beats Opus 5 at `max` for about one fifth of the cost.

### Independent

Artificial Analysis Intelligence Index v4.3.2:

| Model and effort | Index |
|---|---|
| Opus 5.5 `max` | 58 |
| Fable 5.1 `max` | 53 |
| GPT-6 Astra `max` | 53 |
| Opus 5 `max` | 51 |
| Grok 4.7 `xhigh` | 46 |

Artificial Analysis also reports high token use for Opus 5.5 at `max`: 260M output tokens against a 91M median.
Its Opus 5.5 cost per task was not yet published.
[Opus 5.5](https://artificialanalysis.ai/models/claude-opus-5-5)
[Leaderboard](https://artificialanalysis.ai/leaderboards/models)

Terminal-Bench 4.0 independent runs have no Opus 5.5 row yet.
The public leaderboard gives Astra `max` 58.2% and Fable 5.1 `max` 57.9%.
Artificial Analysis gives Astra `xhigh` 59.6% and Fable 5.1 `xhigh` 55.1%.
Vals gives Astra 57.07%, Fable 5.1 49.49%, and Opus 5 45.45%.
[Terminal-Bench](https://www.tbench.ai)
[Artificial Analysis Terminal-Bench 4.0](https://artificialanalysis.ai/evaluations/terminalbench-4-0)
[Vals Terminal-Bench 4.0](https://www.vals.ai/benchmarks/terminal-bench-4)

CursorBench 4.0 has no Opus 5.5 row yet.
Its Grok 4.7 rows are `xhigh` 46.3% at $6.01 and `high` 43.9% at $4.69 per task.
[CursorBench](https://cursor.com/cursorbench)

## Route decisions

| Lane | Change | Basis |
|---|---|---|
| Ambiguous planning, architecture, orchestration, synthesis | Opus 5.5 first; Fable 5.1 first fallback | Anthropic's model guidance, the independent index lead, and subagent delegation reports |
| Difficult implementation, debugging, test construction | Opus 5.5 first; Fable 5.1 first fallback | Vendor coding results and the independent index lead at 40% of Fable 5.1's token price |
| Terminal work, primary verification | Astra stays first; Opus 5.5 is the first fallback | Astra has the independent Terminal-Bench lead. Opus 5.5 has only a vendor result. Verification also benefits from a family other than the usual Opus author. |
| Bounded implementation, sweeps, data collection | Astra stays first; Opus 5.5 at `medium` goes above Grok 4.7 | This keeps the user's Codex preference and puts Opus 5.5 above Grok. |
| Budget-sensitive bounded coding | Opus 5.5 at `medium` first; Grok 4.7 at `high` second | The vendor CursorBench result at `medium` is above Grok 4.7 `xhigh` at lower reported cost. Confirm with the CursorBench row when it appears. |
| Security review and vulnerability exploration | Opus 5.5 stays third, for defensive review of the caller's own code only | Safeguards send most cybersecurity tasks to Opus 4.8. |
| Precision review and technical prose | Opus 5.5 first | Better code review with fewer false alarms, and it follows writing rules |

## Retired Opus 5 notions

| Old notion | Current finding |
|---|---|
| Fable 5.1 and Astra lead the coding-agent benchmarks; use Opus only when its quality is enough at a lower price. | Opus 5.5 leads the vendor coding results and the independent index. It is the default, not the budget choice. |
| Prefer `xhigh` for Opus coding. | Start at `medium` for bounded work and `high` for meaningful work. `xhigh` and `max` now think much more per turn. |
| Opus effort range is `high` to `max`. | `low` is useful for trivial, readily checked tasks. Customer reports show `low` beating Opus 5 at `high` on code review and finance tasks. |
| Opus review is verbose and produces many low-value nitpicks. | Early testers report more bugs caught and fewer false alarms. One reports 72% of known bugs at `low`, against 56% for Opus 5 at `high`. |
| Opus need not own a separate prose lane. | It still need not, but it is now clearly the prose default. It follows supplied writing rules, such as ASD-STE100. |
| Opus is a general security-review fallback. | Only for defensive review of the caller's own code. Other security work can go to Opus 4.8. |
| An Opus request without an effort value runs at `high`. | The Opus 5.5 API default is `medium`. Always set effort explicitly. |

## Open checks

- Add the independent Terminal-Bench 4.0 and CursorBench 4.0 rows for Opus 5.5 when they appear.
- Recheck the terminal lane if Opus 5.5 leads Astra in an independent Terminal-Bench run.
- Recheck the security lane when the Cyber Verification Program covers Opus 5.5.
- Measure the budget lane's per-task cost for Opus 5.5 at `medium` against Grok 4.7 at `high`.

## Local evidence

Checked versions: Claude Code `2.1.280`, Codex `0.155.1`, Grok `1.0.40`, OpenCode `1.18.32`.
`claude --help` lists `--effort` values `low`, `medium`, `high`, `xhigh`, and `max`.
The `opus` alias resolves to the latest Opus model.

## Validation

Clean-context evaluators applied each skill version to the same 18 prompts.
They received only the skill text and the prompts, without expected answers.
They did not launch workers or call model providers.

| Check | Previous skill | Updated skill |
|---|---:|---:|
| Primary model, effort, and trigger decisions that match the new policy | 7/18 | 17/18 |

The previous skill used Opus 5 or Fable 5.1 where the new policy uses Opus 5.5.
It treated an Opus 5.5 lane as `Unrouted`, because Opus 5.5 was not in its fleet.
The preserved decisions were Luna extraction, GLM-5.3 long context, Grok challenge, Astra Codex work, and Daybreak security review.

The first updated run found five unclear rules.
The fixes separate bounded and difficult implementation, and they require a stated cost limit for the budget row.
They also name Fable 5.1 as the Claude fallback and mark Opus 4.8 as outside the fleet.
The final run used the fixed text.
Its only miss was P18: the unattended-run card had no stop budget.
The Opus 5.5 row then got a stop-budget rule. No run tested that last edit.

A Claude evaluator stopped during the first updated run.
A safety classifier ended its response while it wrote route cards for the security prompts.
This shows that the new cyber safeguards can affect routing-policy work that mentions exploit reproducers.
The security prompts and the final run then used Codex with `gpt-6-astra` at `high`.

Structural checks:

- The Skill Creator validator passed.
- `git diff --check` passed.
- The eval file contains 45 unique cases with the required fields.
- `SKILL.md` contains 107 lines; its fleet reference contains 98 lines.
- The project and global installation links resolve to the updated source.

Limits:

- The comparison tests routing instructions, not model performance.
- Each version ran all prompts in one session, not one session for each prompt.
- The 18 prompts do not execute every assertion in all 45 stored cases.
