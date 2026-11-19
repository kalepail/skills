# Antigravity workers

## Verify the route

Resolve the model family on the launch host with `agy models` and the fleet resolver. Check the effort on the resolved base model:

```bash
agy --model <resolved-base-id> --effort <effort> -p /effort --output-format json --print-timeout 15s
```

Check JSON `status`, `command.data.current`, and `command.data.available`. For a caller-pinned base version, verify that version's catalog rows before checking effort. For a caller-pinned ID that already ends in an effort suffix, match the whole ID and pass it as `--model` on its own.

Use the signed-in Antigravity subscription when the lane accepts its data terms. Check the model's group with `agy -p /usage --output-format json --print-timeout 15s` before a large run. The same account uses the same quota groups from either host. API rates, five-hour and weekly limits, and credit overages are separate. Preserve an approved zero-retention API route when the lane requires its terms.

Choose a single-model ID for a one-worker lane. Orchestrator uses a planner and a separate implementation model. Use it only when the caller selects that workflow and permits delegation. For a hard cap on nested workers, verify the harness can enforce the cap before routing to Antigravity.

## Verify the result

- Prefer an interactive worker for approvals or user review. Start it in the intended work directory, with the resolved model and effort. Use the caller's execution mode and permission scope.
- For unattended work, set `--print-timeout` and use `-p <prompt> --output-format json`. Require a successful process exit, `status: SUCCESS`, and the lane's acceptance check. Check the requested artifact, test outcome, or substantive response, depending on the lane.
- Read `denied_actions` when a result is missing. Headless mode can soft-deny tools and still report `SUCCESS`, sometimes with an empty `response`. Retry only with the specific permissions the caller authorized or switch to an interactive run. Treat partial output and timeouts as incomplete.

[Effort command](https://antigravity.google/docs/cli/commands/effort/) · [Usage](https://antigravity.google/docs/cli/commands/usage/) · [Headless mode](https://antigravity.google/docs/cli/headless/) · [Model selector and Orchestrator](https://antigravity.google/docs/models)
