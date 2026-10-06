# OpenCode headless reliability tests

Test date: 2026-10-06. OpenCode version: 1.18.34.
Each test used `opencode run --pure --format json` on a cheap route unless the row says otherwise.

| Test | Setup | Result | File |
|---|---|---|---|
| Global MCP load | 13 global MCP servers on | 106,383 input tokens, 9 s | `baseline-mcp-on.jsonl` |
| MCP servers off | `OPENCODE_CONFIG_CONTENT` turns each server off, plus `OPENCODE_DISABLE_CLAUDE_CODE=1` | 17,067 input tokens, 2 s, same answer | `isolated-mcp-off.jsonl` |
| Split of the saving | MCP off only / `.claude` loading off only | 19,373 / 104,133 input tokens | — |
| Open stdin | Prompt as an argument, stdin an open pipe | No progress; the 30 s alarm stopped it | — |
| Closed stdin | Same run with `< /dev/null` | Complete in 4 s | — |
| Parallel start | 6 runs at once, MCP on and MCP off | 6/6 complete in each mode, no lock | — |
| Parallel start beside hung peers | 2 runs stuck on open stdin, then 3 more runs | 3/3 complete, no lock | — |
| Permission request | Read `/etc/hosts` without `--auto` | Auto-rejected; exit 0; last reason `tool-calls`; no text | `permission-rejected.jsonl` |
| GLM-5.3 `max`, default cap | The edge-review prompt that failed earlier | This run completed with 28,505 reasoning tokens | `glm-max-default-cap.jsonl` |
| GLM-5.3 `max`, cap 128000 | Same prompt | Complete with 38,323 reasoning tokens, more than the default cap | `glm-max-128k-cap.jsonl` |
| Cap enforcement | `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX=64` | Reason `length`, no text | — |
| Attached client | `opencode serve`, then 6 parallel `run --attach` | Every client exited 0 after one `step_start` event; the server finished each session; `opencode export` returned the answers | `attach-client-stream.jsonl` |
| Bad model | Unknown model ID | `error` event, exit code 1 | `bad-model-error.jsonl` |

The two earlier GLM-5.3 failures both ended with reason `length` at 32,000 or more reasoning tokens.
The binary sets a default output cap of 32000. `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` overrides it.
GLM-5.3 at `max` used from 28,505 to 38,323 reasoning tokens on one prompt, so the default cap fails at random.

The earlier 1h44m hang matches the open-stdin result. Those three runs logged `init` and then nothing more.

The earlier `database is locked` failures came when about nine OpenCode processes started together on a 2.8 GB database. No later test reproduced the lock.

## Launcher checks

`skills/productivity/routing-agent-work/scripts/opencode_worker.py` passed these checks:

| Case | Status | Exit code |
|---|---|---|
| Offline self-test (8 classifier cases) | passed | 0 |
| GLM-5.3 Flash short answer | `complete` | 0 |
| GLM-5.3 with output cap 64 | `truncated` | 2 |
| Read outside the work directory without `--auto` | `incomplete`, rejected tool `read` | 2 |
| Time limit of 2 s | `timeout` | 3 |
| Unknown model | `error` | 4 |
| Missing arguments | usage error | 64 |
| Kimi K3 `high`, Muse Spark 1.3 `high`, GLM-5.3 `max` from `--prompt-file` | `complete`, about 19K input tokens each | 0 |

## Guidance check

Two fresh evaluators answered eval cases 64 and 65 from the skill text alone.

- GPT-6.1 Sol with the previous skill text could not give a launch command. It called the `length` result "no usable result" but did not identify the output cap. See `guidance-check-old-gpt-6.1-sol.txt`.
- Claude Sonnet 5.5 with the new text gave the launcher command, judged completion from the status and the answer file, and identified `length` as truncation by the output cap. See `guidance-check-new-sonnet.txt`.
