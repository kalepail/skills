---
name: solo-automate
description: Automate and integrate Solo through MCP, CLI, local HTTP API, hosted API v1, documentation resources, prompts, and solo:// deep links. Use when scripting Solo, discovering live schemas, configuring MCP clients, consuming Solo docs programmatically, or choosing an integration surface. Do not use for normal interactive Solo work already owned by a focused skill.
---

# Automate Solo

Choose supported Solo surface, discover current contract, then perform smallest authorized action.

## Route Request

1. Use local Solo MCP for local projects, processes, output, services, agents, coordination, todos, scratchpads, prompts, and timers.
2. Use `solo` CLI for shell scripts and CI-like local automation. Require `--json`; branch on documented exit codes.
3. Use local HTTP API for editors, plugins, and programs needing REST. Read current discovery file; never hard-code port, token, capabilities, or schemas.
4. Use hosted `https://soloterm.com/api/v1/docs` for machine-readable product documentation and hosted `/api/v1` only for documented web services.
5. Use `solo://` links for human navigation and scratchpad/todo MCP resource addressing.

Do not treat local `/api` and hosted `/api/v1` as same API.

## Discover Before Acting

1. Call `whoami` to inspect identity and effective project.
2. Call `list_projects` and `select_project` only when scope remains missing or user names another project.
3. Call `help()` for capability overview, then relevant topic.
4. Call `mcp_tools_summary()` or use client tool discovery before relying on any remembered tool name, schema, feature toggle, or documented category.
5. Inspect target state before mutation. Use IDs returned by Solo, never OS PIDs or another orchestrator's IDs.

Read [MCP discovery and protocol](references/mcp.md) before using MCP tools, prompts, resources, session identity, project scope, timers, or feature catalogs.

## Execute Conservatively

1. Prefer read-only discovery and inspection when intent is ambiguous.
2. Request explicit authority before deletion, output clearing, self-close, process-wide/bulk control, cross-project mutation, agent spawning, terminal input, feedback submission, or hosted admin action.
3. Preserve command trust, optimistic revisions, lock ownership, and project boundaries.
4. Verify mutations through fresh state, not request acceptance alone.
5. Report surface used, target scope, observed result, and unresolved manual step.

Read [safety and authority](references/safety.md) before any mutation or side effect.

## Use Scriptable Interfaces

For CLI or local REST work:

1. Confirm Solo app runs and HTTP API is enabled.
2. Prefer CLI unless caller needs direct REST schemas or endpoint control.
3. Parse JSON envelopes and stable error codes; keep stderr separate.
4. Page until `hasMore` is false.
5. Re-read discovery after authentication, connection, or version failure.

Read [CLI and local HTTP API](references/cli-and-local-http.md) before writing commands, scripts, HTTP requests, retries, pagination, or error handling.

## Use Hosted Surfaces and Links

Read [hosted API, docs, and deep links](references/hosted-docs-and-links.md) before fetching docs, calling hosted `/api/v1`, handling admin abilities, generating installer/update requests, or constructing `solo://` URIs.

## Hand Off Focused Work

- Use `solo-run-processes` for straightforward start, stop, restart, spawn, input, or restart policy.
- Use `solo-observe-services` for read-only status, output, resources, ports, URLs, and readiness.
- Use `solo-set-up-projects` for import, `solo.yml`, execution profiles, and trust setup.
- Use `solo-troubleshoot` for unexplained failures or diagnosis.
- Use `solo-work-with-agents` for one agent lifecycle and `solo-orchestrate-agents` for multi-agent coordination.
- Use `solo-track-todos`, `solo-keep-scratchpads`, or `solo-save-prompts` for feature-focused work.
- Use coding, browser, GitHub, or deployment skills when Solo only hosts process context; do not turn general work into Solo orchestration.

## Stop Conditions

Stop before acting when target scope is unresolved, live tools contradict assumed contract, user has not authorized side effect, command is untrusted, revision is stale, lock belongs to another actor, or requested operation belongs to another skill.
