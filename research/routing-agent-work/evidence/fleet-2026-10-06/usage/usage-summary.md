# Local agent usage since 2026-09-01

Generated 2026-10-06T14:27:19+00:00 by `local_usage_metrics.py` and `render_usage_md.py` (run with `python3 -I`). Total turns: 11,313. The data is aggregate metadata only. No prompt or message content is included.

Column key: Input M and Output M are millions of tokens. Cache hit = cached input / total input. Wall p50 and p90 are seconds per completed turn. Aborted, Error, and No end are shares of turns. Tool fail is the share of tool calls that failed. The Caveats section defines each metric.

## Per CLI and model

| CLI | Model | Threads | Turns | API calls | Input M | Cache hit | Output M | Reasoning M | Wall p50 s | Wall p90 s | Aborted | Error | No end | Tool fail | First | Last | Logged cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grok | `grok-4.7` | 3258 | 3,610 | 14,250 | 1,363.6 | 82.6% | 30.4 | 25.7 | 82 | 252 | 0.3% | 0.0% | 1.3% | 7.3% | 2026-09-21 | 2026-10-06 | 652.85 (ticks/1e10) |
| codex | `codex-auto-review` | 303 (303 guardian) | 2,954 | 2,938 | 216.8 | 87.6% | 0.3 | 0.1 | 3 | 6 | 0.1% | 0.0% | 0.1% | 0.0% | 2026-09-01 | 2026-10-06 | - |
| codex | `gpt-6-astra` | 301 (200 primary, 101 subagent) | 1,592 | 38,180 | 4,874.5 | 97.0% | 21.3 | 6.7 | 236 | 1,324 | 0.6% | 0.0% | 0.1% | 7.8% | 2026-09-04 | 2026-10-06 | - |
| codex | `gpt-5.6-sol` | 243 (122 primary, 121 subagent) | 734 | 36,993 | 4,783.4 | 97.7% | 15.1 | 6.1 | 372 | 1,480 | 0.8% | 0.0% | 0.8% | 8.7% | 2026-09-01 | 2026-09-21 | - |
| claude | `claude-opus-5-5` | 80 (51 primary, 29 subagent) | 599 | 11,482 | 4,005.8 | 99.0% | 9.9 | - | 106 | 809 | 0.3% | 0.0% | 0.0% | 2.9% | 2026-09-29 | 2026-10-06 | - |
| claude | `claude-sonnet-5` | 407 | 407 | 722 | 27.9 | 76.6% | 0.7 | - | 16 | 43 | 0.0% | 0.0% | 0.0% | 1.0% | 2026-10-01 | 2026-10-02 | - |
| grok | `grok-4.6` | 94 | 324 | 2,137 | 450.0 | 93.0% | 2.4 | 1.8 | 188 | 717 | 3.1% | 0.6% | 4.6% | 2.0% | 2026-09-01 | 2026-09-21 | 121.77 (ticks/1e10) |
| claude | `claude-fable-5-1` | 186 (14 primary, 172 subagent) | 281 | 3,586 | 794.0 | 97.0% | 5.4 | - | 157 | 608 | 0.4% | 0.7% | 0.0% | 2.5% | 2026-09-06 | 2026-10-06 | - |
| codex | `gpt-5.6-terra` | 55 (36 primary, 19 subagent) | 165 | 5,819 | 654.2 | 97.2% | 1.8 | 0.6 | 196 | 632 | 0.0% | 0.0% | 3.0% | 7.3% | 2026-09-01 | 2026-09-19 | - |
| codex | `gpt-6.1-sol` | 52 (44 primary, 8 subagent) | 152 | 2,397 | 277.0 | 95.0% | 1.4 | 0.4 | 247 | 1,305 | 0.7% | 0.0% | 0.7% | 6.8% | 2026-09-29 | 2026-10-06 | - |
| codex | `gpt-6-sol` | 38 (36 primary, 2 subagent) | 106 | 2,884 | 343.1 | 97.8% | 1.2 | 0.4 | 193 | 1,001 | 2.8% | 0.0% | 0.9% | 6.2% | 2026-09-22 | 2026-09-29 | - |
| opencode | `meta/muse-spark-1.3-contributor` | 34 (29 primary, 5 subagent) | 95 | 2,725 | 611.0 | 87.7% | 0.7 | 1.6 | 164 | 1,893 | 1.1% | 3.2% | 0.0% | - | 2026-09-03 | 2026-10-02 | $9.04 |
| codex | `gpt-daybreak-blue-latest` | 31 | 39 | 1,225 | 128.7 | 96.1% | 0.8 | 0.4 | 395 | 974 | 2.6% | 0.0% | 0.0% | 6.7% | 2026-09-14 | 2026-09-27 | - |
| opencode | `muse-spark-1.3` | 35 | 39 | 270 | 28.1 | 89.0% | 0.1 | 0.2 | 28 | 457 | 0.0% | 2.6% | 0.0% | - | 2026-09-04 | 2026-10-06 | $8.79 |
| claude | `claude-sonnet-5-5` | 8 | 35 | 450 | 108.9 | 98.7% | 0.4 | - | 55 | 417 | 0.0% | 0.0% | 0.0% | 4.0% | 2026-09-29 | 2026-10-06 | - |
| opencode | `z-ai/glm-5.3-flash` | 6 | 34 | 422 | 81.6 | 95.3% | 0.1 | 0.3 | 311 | 822 | 0.0% | 0.0% | 2.9% | - | 2026-09-01 | 2026-10-06 | $2.03 |
| opencode | `muse-spark-1.2` | 19 | 24 | 593 | 65.6 | 92.2% | 0.2 | 0.1 | 400 | 1,598 | 0.0% | 20.8% | 4.2% | - | 2026-09-01 | 2026-09-08 | $16.54 |
| opencode | `z-ai/glm-5.3` | 21 | 21 | 457 | 63.4 | 91.3% | 0.2 | 0.4 | 481 | 1,595 | 4.8% | 0.0% | 14.3% | - | 2026-09-01 | 2026-10-06 | $19.20 |
| opencode | `moonshotai/kimi-k3` | 19 | 20 | 577 | 78.0 | 96.9% | 0.2 | 0.3 | 536 | 4,162 | 0.0% | 0.0% | 0.0% | - | 2026-09-01 | 2026-09-21 | $33.69 |
| opencode | `meta/muse-spark-1.3` | 16 (13 primary, 3 subagent) | 18 | 65 | 6.0 | 68.0% | 0.0 | 0.0 | 22 | 156 | 0.0% | 11.1% | 5.6% | - | 2026-09-03 | 2026-10-06 | $3.30 |
| opencode | `meta/muse-glimmer-30b` | 2 | 10 | 39 | 2.8 | 85.0% | 0.0 | 0.0 | 29 | 271 | 0.0% | 0.0% | 0.0% | - | 2026-09-08 | 2026-09-08 | $0.24 |
| opencode | `@cf/zai-org/glm-5.3-flash` | 5 | 9 | 73 | 10.6 | 90.8% | 0.2 | 0.0 | 639 | 1,043 | 0.0% | 0.0% | 0.0% | - | 2026-09-01 | 2026-09-01 | $0.55 |
| codex | `gpt-6-luna` | 2 | 7 | 266 | 32.2 | 96.6% | 0.1 | 0.1 | 498 | 727 | 28.6% | 0.0% | 0.0% | 14.7% | 2026-09-28 | 2026-09-29 | - |
| opencode | `@cf/zai-org/glm-5.3` | 7 | 7 | 559 | 91.1 | 96.9% | 0.5 | 0.0 | 2,746 | 6,302 | 0.0% | 0.0% | 28.6% | - | 2026-09-03 | 2026-09-24 | $29.02 |
| opencode | `kimi-k3` | 7 | 7 | 338 | 43.6 | 97.6% | 0.1 | 0.1 | 1,354 | 2,458 | 0.0% | 0.0% | 0.0% | - | 2026-09-17 | 2026-10-06 | $19.50 |
| opencode | `muse-spark-1.3-contributor` | 4 | 6 | 120 | 15.8 | 96.8% | 0.0 | 0.0 | 103 | 603 | 0.0% | 33.3% | 16.7% | - | 2026-09-04 | 2026-10-02 | $0.09 |
| grok | `grok-4.5` | 6 | 6 | 41 | 3.2 | 78.3% | 0.0 | 0.0 | 168 | 379 | 0.0% | 0.0% | 0.0% | 1.2% | 2026-09-02 | 2026-09-18 | 0.89 (ticks/1e10) |
| opencode | `muse-spark-1.3-contributor-free` | 4 | 4 | 6 | 0.4 | 33.6% | 0.0 | 0.0 | 5 | 18 | 0.0% | 0.0% | 0.0% | - | 2026-09-03 | 2026-09-03 | - |
| opencode | `x-ai/grok-4.6` | 3 | 3 | 29 | 3.8 | 83.4% | 0.0 | 0.0 | 300 | 650 | 0.0% | 0.0% | 0.0% | - | 2026-09-07 | 2026-09-08 | $3.02 |
| opencode | `deepseek/deepseek-v4.1-flash` | 2 | 2 | 12 | 1.4 | 83.7% | 0.0 | 0.0 | 20 | 20 | 0.0% | 0.0% | 0.0% | - | 2026-10-06 | 2026-10-06 | $0.04 |
| codex | `unknown` | 1 (1 guardian) | 1 | 0 | 0.0 | - | 0.0 | 0.0 | - | - | 0.0% | 0.0% | 0.0% | 0.0% | 2026-09-01 | 2026-09-01 | - |
| opencode | `grok-4.6` | 1 | 1 | 12 | 1.8 | 76.3% | 0.0 | 0.0 | 422 | 422 | 0.0% | 0.0% | 0.0% | - | 2026-09-01 | 2026-09-01 | $1.73 |
| grok | `grok-4.7-build-fast` | 1 | 1 | 1 | 0.0 | 7.2% | 0.0 | 0.0 | 6 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 2026-09-21 | 2026-09-21 | 0.10 (ticks/1e10) |

## Per CLI, model, and effort (top 25 by turns)

| CLI | Model | Effort | Threads | Turns | API calls | Input M | Cache hit | Output M | Reasoning M | Wall p50 s | Wall p90 s | Aborted | Error | No end | Tool fail | First | Last | Logged cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grok | `grok-4.7` | high | 3241 | 3,592 | 14,109 | 1,314.8 | 82.5% | 29.5 | 25.1 | 81 | 247 | 0.3% | 0.0% | 1.3% | 7.4% | 2026-09-21 | 2026-10-06 | 550.43 (ticks/1e10) |
| codex | `codex-auto-review` | low | 303 (303 guardian) | 2,954 | 2,938 | 216.8 | 87.6% | 0.3 | 0.1 | 3 | 6 | 0.1% | 0.0% | 0.1% | 0.0% | 2026-09-01 | 2026-10-06 | - |
| codex | `gpt-6-astra` | high | 188 (112 primary, 76 subagent) | 1,179 | 28,077 | 3,632.9 | 97.1% | 16.0 | 4.9 | 261 | 1,297 | 0.5% | 0.0% | 0.1% | 7.4% | 2026-09-04 | 2026-10-06 | - |
| codex | `gpt-5.6-sol` | high | 157 (93 primary, 64 subagent) | 477 | 19,439 | 2,462.8 | 97.5% | 8.9 | 3.5 | 359 | 1,387 | 0.8% | 0.0% | 1.3% | 7.3% | 2026-09-01 | 2026-09-21 | - |
| claude | `claude-sonnet-5` | high | 407 | 407 | 722 | 27.9 | 76.6% | 0.7 | - | 16 | 43 | 0.0% | 0.0% | 0.0% | 1.0% | 2026-10-01 | 2026-10-02 | - |
| claude | `claude-opus-5-5` | xhigh | 46 (25 primary, 21 subagent) | 347 | 7,260 | 2,677.0 | 99.1% | 6.7 | - | 93 | 864 | 0.3% | 0.0% | 0.0% | 2.9% | 2026-09-29 | 2026-10-02 | - |
| codex | `gpt-6-astra` | medium | 70 (47 primary, 23 subagent) | 287 | 6,627 | 823.3 | 97.2% | 3.1 | 1.0 | 102 | 1,236 | 1.1% | 0.0% | 0.0% | 9.9% | 2026-09-04 | 2026-09-25 | - |
| grok | `grok-4.6` | high | 84 | 262 | 1,391 | 281.9 | 92.1% | 1.8 | 1.3 | 192 | 694 | 3.4% | 0.8% | 5.0% | 1.8% | 2026-09-01 | 2026-09-21 | 91.15 (ticks/1e10) |
| codex | `gpt-5.6-sol` | xhigh | 84 (27 primary, 57 subagent) | 253 | 17,389 | 2,298.8 | 97.9% | 6.0 | 2.5 | 414 | 1,738 | 0.8% | 0.0% | 0.0% | 10.5% | 2026-09-01 | 2026-09-09 | - |
| claude | `claude-opus-5-5` | high | 33 (25 primary, 8 subagent) | 235 | 4,063 | 1,308.1 | 98.9% | 3.2 | - | 140 | 686 | 0.4% | 0.0% | 0.0% | 2.9% | 2026-09-29 | 2026-10-06 | - |
| claude | `claude-fable-5-1` | xhigh | 174 (2 primary, 172 subagent) | 178 | 2,114 | 240.5 | 93.5% | 3.7 | - | 172 | 582 | 0.0% | 1.1% | 0.0% | 2.4% | 2026-09-06 | 2026-09-30 | - |
| codex | `gpt-5.6-terra` | high | 54 (35 primary, 19 subagent) | 164 | 5,817 | 654.1 | 97.2% | 1.8 | 0.6 | 196 | 650 | 0.0% | 0.0% | 3.0% | 7.3% | 2026-09-01 | 2026-09-16 | - |
| codex | `gpt-6.1-sol` | high | 48 (40 primary, 8 subagent) | 144 | 2,201 | 252.7 | 95.0% | 1.3 | 0.4 | 233 | 1,236 | 0.7% | 0.0% | 0.7% | 6.6% | 2026-09-29 | 2026-10-06 | - |
| claude | `claude-fable-5-1` | high | 12 | 103 | 1,472 | 553.4 | 98.6% | 1.7 | - | 112 | 615 | 1.0% | 0.0% | 0.0% | 2.8% | 2026-09-17 | 2026-10-06 | - |
| codex | `gpt-6-astra` | xhigh | 46 (44 primary, 2 subagent) | 83 | 2,891 | 357.4 | 96.8% | 2.0 | 0.8 | 496 | 2,127 | 0.0% | 0.0% | 0.0% | 6.7% | 2026-09-08 | 2026-10-01 | - |
| codex | `gpt-6-sol` | high | 25 (23 primary, 2 subagent) | 77 | 2,074 | 252.6 | 97.7% | 0.9 | 0.3 | 215 | 1,001 | 2.6% | 0.0% | 1.3% | 5.9% | 2026-09-25 | 2026-09-29 | - |
| opencode | `meta/muse-spark-1.3-contributor` | high | 19 | 70 | 1,804 | 331.5 | 87.0% | 0.4 | 0.7 | 163 | 1,013 | 1.4% | 0.0% | 0.0% | - | 2026-09-03 | 2026-10-02 | $5.12 |
| grok | `grok-4.6` | xhigh | 9 | 61 | 730 | 167.1 | 94.6% | 0.6 | 0.5 | 164 | 1,056 | 1.6% | 0.0% | 3.3% | 2.7% | 2026-09-03 | 2026-09-11 | 30.46 (ticks/1e10) |
| codex | `gpt-6-astra` | low | 16 | 43 | 585 | 60.9 | 95.7% | 0.2 | 0.1 | 103 | 345 | 2.3% | 0.0% | 0.0% | 8.0% | 2026-09-07 | 2026-10-06 | - |
| opencode | `z-ai/glm-5.3-flash` | max | 6 | 34 | 422 | 81.6 | 95.3% | 0.1 | 0.3 | 311 | 822 | 0.0% | 0.0% | 2.9% | - | 2026-09-01 | 2026-10-06 | $2.03 |
| opencode | `muse-spark-1.3` | unspecified | 27 | 31 | 222 | 22.6 | 89.8% | 0.1 | 0.1 | 16 | 457 | 0.0% | 0.0% | 0.0% | - | 2026-09-04 | 2026-09-24 | $6.49 |
| codex | `gpt-daybreak-blue-latest` | xhigh | 29 | 30 | 1,103 | 114.7 | 95.9% | 0.7 | 0.3 | 438 | 974 | 0.0% | 0.0% | 0.0% | 6.2% | 2026-09-27 | 2026-09-27 | - |
| claude | `claude-sonnet-5-5` | high | 4 | 27 | 351 | 95.9 | 98.9% | 0.4 | - | 55 | 675 | 0.0% | 0.0% | 0.0% | 4.0% | 2026-09-29 | 2026-10-03 | - |
| codex | `gpt-6-sol` | medium | 8 | 24 | 758 | 87.2 | 98.3% | 0.3 | 0.1 | 65 | 1,153 | 4.2% | 0.0% | 0.0% | 7.3% | 2026-09-22 | 2026-09-27 | - |
| opencode | `meta/muse-spark-1.3-contributor` | xhigh | 14 (9 primary, 5 subagent) | 21 | 917 | 279.5 | 88.6% | 0.3 | 0.9 | 473 | 3,741 | 0.0% | 4.8% | 0.0% | - | 2026-09-03 | 2026-09-08 | $3.91 |

## Weekly turns (week starts Monday, UTC; rows with 5 or more turns)

| CLI/model | 2026-08-31 | 2026-09-07 | 2026-09-14 | 2026-09-21 | 2026-09-28 | 2026-10-05 | Total |
|---|---|---|---|---|---|---|---|
| `grok/grok-4.7` | 0 | 0 | 0 | 3481 | 126 | 3 | 3610 |
| `codex/codex-auto-review` | 1009 | 516 | 292 | 721 | 407 | 9 | 2954 |
| `codex/gpt-6-astra` | 147 | 273 | 237 | 692 | 235 | 8 | 1592 |
| `codex/gpt-5.6-sol` | 545 | 148 | 39 | 2 | 0 | 0 | 734 |
| `claude/claude-opus-5-5` | 0 | 0 | 0 | 0 | 531 | 68 | 599 |
| `claude/claude-sonnet-5` | 0 | 0 | 0 | 0 | 407 | 0 | 407 |
| `grok/grok-4.6` | 120 | 101 | 91 | 12 | 0 | 0 | 324 |
| `claude/claude-fable-5-1` | 8 | 168 | 4 | 0 | 98 | 3 | 281 |
| `codex/gpt-5.6-terra` | 107 | 45 | 13 | 0 | 0 | 0 | 165 |
| `codex/gpt-6.1-sol` | 0 | 0 | 0 | 0 | 151 | 1 | 152 |
| `codex/gpt-6-sol` | 0 | 0 | 0 | 102 | 4 | 0 | 106 |
| `opencode/meta/muse-spark-1.3-contributor` | 62 | 32 | 0 | 0 | 1 | 0 | 95 |
| `codex/gpt-daybreak-blue-latest` | 0 | 0 | 8 | 31 | 0 | 0 | 39 |
| `opencode/muse-spark-1.3` | 3 | 2 | 5 | 28 | 0 | 1 | 39 |
| `claude/claude-sonnet-5-5` | 0 | 0 | 0 | 0 | 27 | 8 | 35 |
| `opencode/z-ai/glm-5.3-flash` | 24 | 8 | 0 | 0 | 0 | 2 | 34 |
| `opencode/muse-spark-1.2` | 20 | 4 | 0 | 0 | 0 | 0 | 24 |
| `opencode/z-ai/glm-5.3` | 3 | 3 | 11 | 2 | 0 | 2 | 21 |
| `opencode/moonshotai/kimi-k3` | 8 | 5 | 5 | 2 | 0 | 0 | 20 |
| `opencode/meta/muse-spark-1.3` | 7 | 9 | 0 | 0 | 0 | 2 | 18 |
| `opencode/meta/muse-glimmer-30b` | 0 | 10 | 0 | 0 | 0 | 0 | 10 |
| `opencode/@cf/zai-org/glm-5.3-flash` | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| `codex/gpt-6-luna` | 0 | 0 | 0 | 0 | 7 | 0 | 7 |
| `opencode/@cf/zai-org/glm-5.3` | 1 | 0 | 4 | 2 | 0 | 0 | 7 |
| `opencode/kimi-k3` | 0 | 0 | 4 | 2 | 0 | 1 | 7 |
| `opencode/muse-spark-1.3-contributor` | 1 | 3 | 1 | 0 | 1 | 0 | 6 |
| `grok/grok-4.5` | 2 | 0 | 4 | 0 | 0 | 0 | 6 |

## Daily turns around the model changes (from 2026-09-20)

| CLI/model | 09-20 | 09-21 | 09-22 | 09-23 | 09-24 | 09-25 | 09-26 | 09-27 | 09-28 | 09-29 | 09-30 | 10-01 | 10-02 | 10-03 | 10-05 | 10-06 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `codex/gpt-6-astra` | 15 | 58 | 173 | 244 | 43 | 80 | 44 | 50 | 18 | 49 | 37 | 74 | 57 | 0 | 0 | 8 |
| `codex/gpt-6-sol` | 0 | 0 | 1 | 0 | 4 | 26 | 37 | 34 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| `codex/gpt-6.1-sol` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 22 | 62 | 52 | 7 | 0 | 1 |
| `codex/gpt-6-luna` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| `claude/claude-opus-5-5` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 134 | 42 | 272 | 80 | 3 | 29 | 39 |
| `claude/claude-fable-5-1` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 17 | 19 | 50 | 0 | 0 | 3 |
| `claude/claude-sonnet-5` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 270 | 137 | 0 | 0 | 0 |
| `claude/claude-sonnet-5-5` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 0 | 1 | 0 | 13 | 4 | 4 |

## Source notes

```json
{
 "codex": {
  "files": 1038,
  "threads": 1038,
  "token_records_without_owned_turn": {}
 },
 "claude": {
  "files": 686,
  "turns_with_no_model_call_by_origin": {
   "other": 47,
   "sdk": 2,
   "human": 2,
   "task-notification": 1
  },
  "api_error_messages_outside_turn": 2,
  "api_error_retry": 1
 },
 "opencode": {
  "user_messages": 305,
  "assistant_messages_without_user_in_window": 0
 },
 "grok": {
  "session_dirs": 3366,
  "sessions_usage_turncount_mismatch": 10,
  "session_cwd_class": {
   "experiment_work_dir": 823,
   "other": 625,
   "tmp_or_scratchpad": 1918
  }
 }
}
```

## Caveats

- **Window.** Turns start on or after 2026-09-01 00:00 UTC. The snapshot time is in `usage-summary.json` (`generated_at`). Live sessions, including this audit, still write logs, so a rerun gives slightly different numbers.
- **Claude Code retention.** `~/.claude/settings.json` sets `cleanupPeriodDays: 7`. Claude Code deletes older transcripts, so Claude rows cover about 2026-09-29 onward. Only a few long-lived files reach back to 2026-09-06. The `claude-opus-5` to `claude-opus-5-5` change on 2026-09-22 is not derivable from these logs: no `claude-opus-5` call survives.
- **Turn definitions differ by CLI.** Codex: one `turn_id` (deduplicated across forked thread files). Claude: one non-tool-result user entry that gets one or more model calls; it includes harness-injected task notifications (see `turns_by_origin`). OpenCode: one user message with one or more assistant replies. Grok: one `turn_started` event. Compare turn counts across CLIs with care.
- **Threads.** Codex `subagent` = `thread_spawn` children; `guardian` = `codex-auto-review` approval reviewers (a harness feature, not a routed lane). Claude `subagent` = files under `subagents/` (Agent tool and workflow agents). OpenCode `subagent` = sessions with a `parent_id`. Grok logs mark every session `primary`, but most Grok sessions run in agent scratchpads or experiment work directories (see `source_notes.grok.session_cwd_class`), so they are delegated or batch runs.
- **Batch runs inflate counts.** Grok `grok-4.7` (3,481 turns in the week of 2026-09-21) and Claude `claude-sonnet-5` (407 one-turn `sdk` sessions on 2026-10-01 and 2026-10-02) are mostly scripted runs. Turn counts measure volume, not interactive preference.
- **Tokens.** Input M includes cache reads and cache writes for every CLI. Totals include orchestration overhead: system prompts, tool schemas, subagent context, and compaction. Codex reasoning tokens are a subset of output tokens. Claude logs do not report reasoning tokens. OpenCode input is stored net of cache, and the script adds the cache back. Codex files from CLI 0.152.x and older have no `token_usage_record`; the script uses deduplicated `token_count` events for them.
- **Wall time.** Medians and p90 use completed turns only. Codex uses `task_complete.duration_ms`. Claude uses prompt time to the last assistant entry, so it excludes trailing tool time. OpenCode uses user message creation to the last assistant completion. Grok uses `turn_started` to `turn_ended`. Long values often include user approval waits and subagent waits.
- **Error and abort rates are harness events, not task success.** Aborted = user interrupt or cancel (Codex `turn_aborted`, Claude interrupt marker, OpenCode `MessageAbortedError`, Grok `cancelled`). Error = an API error surfaced in the log (Claude `isApiErrorMessage`, OpenCode `APIError`, Grok outcome `error`). Codex logs have no API-error event type, so the Codex error rate is 0 by construction. No end = a turn start without a completion record (crash, kill, still running). A completed turn can still be a wrong answer.
- **Tool failure rate** counts failed tool items: Codex `item_completed` status `failed`, Claude `tool_result` `is_error`, Grok `tool_completed` outcome other than `success`. A failed shell command (for example a failing test) counts as a failure, so this is a noisy signal. It is not computed for OpenCode.
- **Cost.** OpenCode cost is the `cost` field that OpenCode logged per message (provider-reported or OpenCode-priced). Grok cost is the logged `costUsdTicks`; the USD column assumes 10^10 ticks per USD, which this audit did not verify. Codex and Claude logs carry no cost, so cost is not derivable for them. No prices were invented.
- **Effort.** Codex: `turn_context.effort`. Claude: the per-entry `effort` field. OpenCode: the message `variant` (`unspecified` when absent). Grok: the session-level `summary.json` `reasoning_effort`, which is the last value set in the session.
- **Not covered.** Cloud or web sessions, other machines, and API calls that do not write these local logs. The Codex `archived_sessions` folder is included. OpenCode legacy `storage/` JSON has no files newer than 2026-09-01.
