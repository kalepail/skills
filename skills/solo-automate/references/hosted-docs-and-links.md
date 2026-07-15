# Hosted API, docs, and deep links

Use this reference for Solo's internet-facing `/api/v1`, raw documentation, download/update/license/feedback integrations, and `solo://` navigation.

## Keep APIs separate

| Surface | Base | Authentication | Purpose |
|---|---|---|---|
| Local HTTP | dynamic `http://127.0.0.1:<port>/api` | rotating local bearer token | control running desktop app |
| Hosted API v1 | `https://soloterm.com/api/v1` | public routes none; admin routes scoped Sanctum token | docs, downloads, updates, licensing, notifications, feedback/admin automation |

Never send local Solo token to hosted service. Never use hosted API to manage local projects/processes.

## Documentation API

Start with:

```text
GET https://soloterm.com/api/v1/health
GET https://soloterm.com/api/v1/agents
GET https://soloterm.com/api/v1/docs
GET https://soloterm.com/api/v1/docs/{section}/{page}
```

`/api/v1/agents` is machine-readable manifest for current public/admin surface. `/api/v1/docs` and child paths return Markdown. Prefer these over scraping human `/docs` pages.

## Hosted public endpoints

| Method/path | Critical contract |
|---|---|
| GET `/api/v1/health` | status and timestamp |
| GET `/api/v1/agents` | current machine manifest |
| GET `/api/v1/docs[/{path}]` | Markdown index/page |
| GET `/api/v1/download/{platform}` | `darwin-universal|windows-x86_64|linux-x86_64`; redirect, not JSON; `source?` |
| GET `/api/v1/updates/manifest` | platform from `X-Platform` preferred or `platform|target`; optional license/device/current version; JSON or 204 |
| POST `/api/v1/license/validate` | device hash, license key, app version; optional device/platform/OS metadata |
| GET `/api/v1/license/status` | `X-Device-ID` and `X-App-Version`; optional `X-License-Key` |
| POST `/api/v1/license/deactivate` | device ID and license key |
| POST `/api/v1/notifications/check` | app version and licensed boolean; optional client metadata/counts/last ID |
| POST `/api/v1/feedback` | device/app/OS/arch/message; email optional |

Re-read `/api/v1/agents` before coding against request/response details.

## Hosted admin endpoints

Require Sanctum bearer token with exact ability:

- `admin:feedback`: list feedback; patch resolution/follow-up/notes.
- `admin:email`: send one transactional email; use `idempotency_key`.
- `admin:user-groups`: attach matching license emails to group.
- `admin:versions`: list version groups; patch release notes.

Create tokens only through `/admin/api-tokens`; plain token is shown once. Do not infer admin authority from user access to local Solo. Require explicit request before feedback changes, email, group membership, or changelog mutation.

## Deep links

```text
solo://proj/{projectId}
solo://proj/{projectId}/process/{slug}--{processId}
solo://proj/{projectId}/scratchpad/{slug}--{scratchpadId}
solo://proj/{projectId}/todo/{slug}--{todoId}
```

Generate slug by lowercasing, replacing non-alphanumerics with dashes, and truncating to 20 characters. Slug is readability only; numeric suffix resolves target, so rename does not break link. Prefer Solo's Copy link action when exact URI is available.

Opening link launches/focuses Solo and navigates. Links work in browsers, chat, editors, terminal output, rendered Solo Markdown, and command-palette paste. Malformed/stale links are ignored without error.

Scratchpad/todo deep-link forms are also MCP resource URIs. Resource reads are Markdown and read-only.

## Sources

- https://soloterm.com/api/v1/agents
- https://soloterm.com/api/v1/health
- https://soloterm.com/api/v1/docs
- https://soloterm.com/api/v1/docs/integrations/http-api
- https://soloterm.com/api/v1/docs/integrations/deep-links
- https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources
