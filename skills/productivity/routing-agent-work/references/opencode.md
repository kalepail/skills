# Run OpenCode Workers

Read this before you launch an OpenCode route. An interactive OpenCode session in a terminal multiplexer needs only the catalog check.

## Check the catalog

Before you reject a new or recently updated identifier, refresh the model catalog once:

```bash
opencode models --refresh
opencode models <provider>
```

Check only the selected provider. Treat an identifier that is absent after the refresh as unavailable, and use the next fallback. Skip the refresh when host status already confirms the identifier.

## Launch a headless worker

`opencode run` can exit with code 0 and give no answer. Judge each run from its event stream, not from its exit code.
Use the bundled launcher. Call it by its full path, because it lives in this skill's `scripts/` folder:

```bash
python3 <skill-dir>/scripts/opencode_worker.py \
  --model <provider/model> --variant <effort> \
  --dir <work-dir> --prompt-file <brief.md> \
  --text-out <answer.md> --timeout 900
```

The launcher does these steps:

- It sends the prompt on stdin and then closes stdin. Long briefs do not hit argument-size limits.
- It turns off each MCP server that `opencode debug config` lists for the work directory. Use `--keep-mcp` when the lane needs MCP tools.
- It raises the output token cap through `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX`.
- It runs with `--pure` and turns off automatic updates.
- It stops the run after the time limit.
- It starts the run once more after a `database is locked` failure at start.
- It prints one JSON summary line. `--text-out` receives the text of the final step only. `--events-out` keeps the full stream.

| Exit code | Status | Meaning |
|---|---|---|
| 0 | `complete` | The last step ended with `stop`, and that step has answer text |
| 2 | `truncated` | The output token cap stopped the model |
| 2 | `incomplete` | The run stopped after a tool call, often a rejected permission |
| 2 | `empty` | The last step has no answer text |
| 2 | `filtered` | A content filter stopped the model |
| 2 | `unconfirmed` | The last step has text, but the provider gave no clear finish reason |
| 3 | `timeout` | The run passed the time limit |
| 4 | `error` | OpenCode, the provider, or the launcher reported an error |
| 64 | usage error | A required argument, file, or directory is missing |

Accept a result only when the status is `complete` and the lane's own completion check passes.
Treat `unconfirmed` text as a lead: read it, then confirm it with the lane's check.
Run `python3 <skill-dir>/scripts/opencode_worker.py --self-test` after you change the launcher.

## Know the failure modes

| Symptom | Cause | Control |
|---|---|---|
| The run makes no progress and never ends | `opencode run` reads stdin until it closes. An open pipe keeps it waiting | Send the prompt on stdin, or redirect stdin from `/dev/null` |
| Exit code 0, no text, last `step_finish` reason `length` | OpenCode's output cap can be lower than a reasoning model needs at `max`. The model spends the cap on reasoning | Raise `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` to the model's output limit |
| Exit code 0, no text, last reason `tool-calls` | A headless run rejects each permission request that needs approval | Put all inputs inside `--dir`. Grant only the needed permissions through `OPENCODE_PERMISSION`. Use `--auto` only in a disposable work directory |
| Many extra input tokens on each step, and slow start-up | `--pure` turns off plugins, not MCP servers. Each run loads every configured MCP server | Turn the servers off through `OPENCODE_CONFIG_CONTENT` |
| `database is locked` at start | Many OpenCode processes start at the same time on one data directory | Start the run once more. Stagger large batches |

## Run without the launcher

Apply the same controls by hand:

```bash
OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX=<model-output-limit> \
OPENCODE_CONFIG_CONTENT='{"mcp":{"<server>":{"enabled":false}}}' \
opencode run --pure --format json --dir <work-dir> \
  -m <provider/model> --variant <effort> < brief.md > events.jsonl
```

List the server names with `opencode debug config`. Add one entry for each name.
Put a time limit on the process.
Read the events after the last `step_start`: the last `step_finish` reason must be `stop`, and the step must have text.

## Read attached sessions through export

`opencode serve` with `opencode run --attach <url>` can save start-up time across many runs.
The attached client can stop its output after the first event while the server finishes the session.
Read the result with `opencode export <sessionID>`. Do not trust the stdout of an attached client.

Check flag and variable names with `opencode run --help` and the [OpenCode CLI documentation](https://opencode.ai/docs/cli).
