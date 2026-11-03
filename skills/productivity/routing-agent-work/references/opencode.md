# Run OpenCode Workers

Read this before you launch an OpenCode route. An interactive OpenCode session in a terminal multiplexer needs only the catalog check and a model selection.

## Check the catalog

Model availability is project-specific. Confirm the identifier from the work directory:

```bash
cd <work-dir> && opencode models | grep '^<provider>/'
```

Check only the selected provider. Treat an identifier that is absent as unavailable, and use the next fallback. Skip the check when host status already confirms the identifier.

Effort values differ between providers for one model. OpenCode caches the catalog, so read the route's values there:

```bash
python3 -c 'import json,os,sys; d=json.load(open(os.path.expanduser("~/.cache/opencode/models.json"))); print(d[sys.argv[1]]["models"][sys.argv[2]].get("reasoning_options"))' <provider> <model>
```

A `toggle` entry with no `effort` list means the route has no effort variants. A run with a missing variant stops at once with `Variant unavailable`.

## Select the model for an interactive session

Start the TUI in the work directory with `opencode <work-dir>`, so it loads that project's config. The TUI takes no model flag. Set `model` in the work directory's `opencode.json`, or pick the model with `/models` after launch. The config `model` sets the model only; choose the variant in the session.

## Launch a headless worker

`opencode run` can exit with code 0 and give no answer. Judge each run from its event stream, not from its exit code.
Use the bundled launcher. Call it by its full path, because it lives in this skill's `scripts/` folder:

```bash
python3 <skill-dir>/scripts/opencode_worker.py \
  --model <provider/model> --variant <effort> \
  --dir <work-dir> --prompt-file <brief.md> \
  --text-out <answer.md> --timeout 900
```

Use `--no-variant` in place of `--variant` for a route without effort variants. The route's default mode then applies.

The launcher does these steps:

- It runs a private `--standalone` server, so the per-run config reaches the worker.
- It runs in the `--dir` work directory and sets `PWD` to that path. OpenCode takes its project directory from `PWD`.
- It sends the prompt on stdin and then closes stdin. A long brief stays inside the argument-size limit.
- It turns off each MCP server that `opencode debug config --standalone` lists for the work directory. Use `--keep-mcp` when the lane needs MCP tools.
- It adds `--permission` rules, a JSON array in the `permissions` format, after the existing rules. The last matching rule wins.
- It clears multiplexer pane variables, so pane-reporting plugins stay silent. Configured plugins still load.
- It turns off automatic updates.
- It stops the run after the time limit.
- It starts the run once more after a `database is locked` failure at start.
- It prints one JSON summary line. `--text-out` receives the text of the final step only. `--events-out` keeps the full stream.

| Exit code | Status | Meaning |
|---|---|---|
| 0 | `complete` | The last step ended with `stop`, and that step has answer text |
| 2 | `truncated` | The output token limit stopped the model |
| 2 | `incomplete` | The last step has no finish, or it stopped after a tool call, often a rejected permission |
| 2 | `empty` | The last step has no answer text |
| 2 | `filtered` | A content filter stopped the model |
| 2 | `unconfirmed` | The last step has text, but the provider gave no clear finish reason |
| 3 | `timeout` | The run passed the time limit |
| 4 | `error` | OpenCode, the provider, or the launcher reported an error, or the last step ended with `error` |
| 64 | usage error | A required argument, file, or directory is missing |

Accept a result only when the status is `complete` and the lane's own completion check passes. A worker that lacks a tool can still end with `complete` and explain that it could not do the task.
Treat `unconfirmed` text as a lead: read it, then confirm it with the lane's check.
Run `python3 <skill-dir>/scripts/opencode_worker.py --self-test` after you change the launcher.

## Set the permission boundary

The default rules allow every action, including access to paths outside the work directory. A headless run rejects only an action that a rule sets to `ask`. The work directory is not an access boundary by itself.

Pass a deny rule for each action that the lane must not do. This rule blocks access outside the work directory and its project worktree:

```json
[{"action": "external_directory", "resource": "*", "effect": "deny"}]
```

Paths elsewhere in the same worktree stay open. A narrower lane needs explicit file-action rules. Shell commands need their own narrow `shell` rules. Use `--auto` only in a disposable work directory. See the [permissions documentation](https://opencode.ai/v2/docs/permissions/).

## Pin an OpenRouter route

OpenRouter picks an upstream host for each request. Without a pin, it can choose a low-precision host that collects data.
Pin the host in the model's request body. Add `"zdr": true` when the fleet reference lists zero data retention for that route. Pass the pin in `OPENCODE_CONFIG_CONTENT`; the launcher keeps it:

```bash
OPENCODE_CONFIG_CONTENT='{"providers":{"openrouter":{"models":{"moonshotai/kimi-k3.1-pro":{"body":{"provider":{"order":["moonshotai"],"allow_fallbacks":false,"zdr":true}}}}}}}' \
python3 <skill-dir>/scripts/opencode_worker.py --model openrouter/moonshotai/kimi-k3.1-pro --variant high ...
```

The same `providers` entry can go in the work directory's `opencode.json`. The fleet reference names the host for each route.
A pin that no host matches stops at once with `No endpoints found`. Treat that route as unavailable, and use the next provider.

## Know the failure modes

| Symptom | Cause | Control |
|---|---|---|
| The run makes no progress and never ends | `opencode run` reads stdin until it closes. An open pipe keeps it waiting | Send the prompt on stdin, or redirect stdin from `/dev/null` |
| The worker cannot find files that exist in the work directory | `PWD` still names the caller's directory | `cd` into the work directory, so `PWD` and the process directory agree |
| Per-run config or environment has no effect | The command used the shared background service, which keeps its own config | Pass `--standalone` |
| Exit code 0, no text, last `step_finish` reason `length` | The model spent its output limit, often on reasoning at `max` | Raise the model's `limit.output` in the provider config, or lower the variant |
| Exit code 0, no text, last reason `tool-calls` | A headless run rejects each permission request that a rule sets to `ask` | Allow only the actions the lane needs. See the permission boundary above |
| `database is locked` at start | Many OpenCode processes start at the same time on one data directory | Start the run once more. Stagger large batches |

## Run without the launcher

Apply the same controls by hand. Run each command from the work directory:

```bash
cd <work-dir>
opencode debug config --standalone
env -u TMUX -u TMUX_PANE -u HERDR_ENV -u HERDR_PANE_ID -u HC_TERMINAL_ID \
  OPENCODE_DISABLE_AUTOUPDATE=1 \
  OPENCODE_CONFIG_CONTENT='{"mcp":{"servers":{"<server>":{<its config>,"disabled":true}}}}' \
  opencode run --standalone --format json \
  -m '<provider/model>#<effort>' < brief.md > events.jsonl
```

For a route without effort variants, pass `-m '<provider/model>'` with no `#` suffix.
`opencode debug config --standalone` lists the servers. A config entry replaces the whole server entry, so copy each entry and add `"disabled": true`.
Unset every other multiplexer pane variable in the environment, such as other `HERDR_*`, `HC_*`, and `ZELLIJ*` names.
Put a time limit on the process.
Read the events after the last `step_start`. That step must end with a `step_finish` reason of `stop` and must have text.

## Reuse one server across runs

`opencode serve` with `opencode run --server <url>` saves start-up time across many runs.
When the client output ends early, read the result with `opencode session export --server <url> <sessionID>`.

Check flag and variable names with `opencode run --help` and the [OpenCode CLI documentation](https://opencode.ai/v2/docs/cli/commands/).
