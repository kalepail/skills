# CLI and local HTTP API

Use this reference for shell automation, JSON contracts, local REST discovery, authentication, errors, pagination, and endpoint routing.

## Choose interface

Prefer `solo` CLI for shell scripts. Use direct local HTTP API when integration needs endpoint schemas, request IDs, actor attribution, or language-native REST. Both require running Solo app and enabled HTTP API. Built-in CLI help, `solo --version`, and local routine bundling work without app.

## CLI discovery and globals

Bundled CLI reads `http-api.json`, validates app PID/API version, and authenticates automatically. Use `--app-data-dir <dir>` or `SOLOTERM_APP_DATA_DIR` for non-default app data.

```text
solo --version      local CLI version
solo version        running app and API version
solo status         readiness, project/process counts, data dir, port
solo doctor         discovery, reachability, compatibility diagnosis
solo help [command]
```

Global flags: `--json`, `--app-data-dir`, `--help|-h`, `--version|-V`.

## CLI groups

```text
solo projects list|get|create|rename|delete
solo processes list|get|spawn|start|stop|restart|rename|delete|output
solo commands start-all|stop-all|restart-all
solo agents list
solo todos list|get|create|update|delete|complete|incomplete
solo scratchpads list|read|create|update|append|rename|archive|unarchive|delete
solo routine
```

Use `--project-id` for project-scoped process filters and every todo/scratchpad command. Use `--expected-revision` for scratchpad update/append/rename/delete; delete also requires `--confirm`. Use `--confirm-stop-running` when project/process deletion must stop active work.

## JSON and exit contract

Pass `--json` on every scripted command.

```json
{"ok":true,"command":"projects list","data":{}}
{"ok":false,"error":{"code":"not_found","message":"...","command":"processes get"}}
```

Success goes to stdout. Failure goes to stderr and exits nonzero. Branch on code:

| Exit | Class |
|---|---|
| 0 | success |
| 64 | usage/arguments |
| 65 | app rejected request |
| 66 | input file unreadable |
| 69 | app/discovery unavailable |
| 70 | protocol/internal |
| 74 | stdin I/O |
| 77 | permission/token/discovery |
| 78 | configuration/version mismatch |

List payloads include `totalCount`, `offset`, `limit`, `hasMore`, `nextOffset`. Continue until `hasMore=false`.

## Local HTTP discovery and authentication

Server binds `127.0.0.1` only. Default port is 24678, but Solo chooses free random port on collision. Read discovery every session and again after 401, restart, or version failure.

Default discovery file:

- macOS/Linux: `~/.config/soloterm/http-api.json`
- Windows: `%USERPROFILE%\.config\soloterm\http-api.json`
- Custom: `SOLOTERM_APP_DATA_DIR/http-api.json`

File contains `schemaVersion`, `apiVersion`, app version, URLs, port, token, PID, capabilities, and full endpoint request/response schemas. Unix mode is `0600`. Token rotates on every server start. Authenticated `GET /api/discovery` returns live catalog without file-only token/PID.

Send `Authorization: Bearer <token>` on every request, including `/api/version`. Send JSON mutations with `Content-Type: application/json`. Do not log discovery file or token.

## HTTP contract

- Routes are local `/api/...`, not hosted `/api/v1/...`.
- Success: `{ok:true, requestId, data}`.
- Failure: `{ok:false, requestId, error:{code,message,details}}`; automate against `code` and `details`.
- Body maximum: 2 MB. Bodyless endpoints reject non-empty body, including `{}`.
- Lists default 50, max 500; clamped requests set `limitClamped=true`. Workspace list is unpaginated.
- Every GET supports HEAD. OPTIONS reports published methods. Browser origins must be loopback.
- Optional `x-solo-request-id` supports log correlation. Optional `x-solo-actor-id`/`x-solo-actor-name` attribute mutations.

Stable errors: 400 `bad_request`, 401 `unauthorized`, 403 `forbidden`, 404 `not_found`, 405 `method_not_allowed`, 409 `conflict`, 412 `precondition_failed`, 413 `payload_too_large`, 415 `unsupported_media_type`, 426 `version_mismatch`, 500 `internal`, 503 `service_unavailable`.

## Endpoint families

Use the discovery document for the exact local route catalog. Route families include:

- Discovery/status: `/api/version`, `/api/status`, `/api/discovery`.
- Projects: list/create/get/patch/delete/move-to-workspace.
- Workspaces: list/create/patch/delete/reorder.
- Processes: list/get/output/delete/spawn/start/stop/restart/rename and project start-all/stop-all/restart-all.
- Todos: list/create/get/update/delete/complete and comment CRUD.
- Scratchpads: list/create/read/replace/delete/append/rename/archive/unarchive.

Use discovery document for exact installed schemas. Important constraints:

- Project create requires existing absolute path and is idempotent on canonical path.
- Process spawn permits terminal or configured agent, not arbitrary command.
- Command lifecycle honors trust and bulk results can be partial.
- Todo status and completed fields are mutually exclusive in same update.
- Scratchpad destructive writes require `expectedRevision`; handle 412 by re-read/reconcile/retry.

## Sources

- https://soloterm.com/api/v1/docs/cli/overview
- https://soloterm.com/api/v1/docs/cli/projects-and-processes
- https://soloterm.com/api/v1/docs/cli/todos-and-scratchpads
- https://soloterm.com/api/v1/docs/cli/json-output-and-scripting
- https://soloterm.com/api/v1/docs/integrations/http-api
