# Fan Solo capability map

Use this map when request spans capabilities or adjacent skills could both match. Route to fewest focused skills. Run router only for selection and shared safety model.

## Focused skills

| Skill | Owns | Route elsewhere when |
|---|---|---|
| `$solo-set-up-projects` | Add/configure Solo projects; audit or write shareable `solo.yml`; define commands and safe defaults | User wants personal workspace UI/settings rather than repo setup |
| `$solo-customize-workspace` | Workspaces, project placement, navigation, appearance, notifications, hotkeys, sidebar behavior | Change belongs in repository or `solo.yml` |
| `$solo-run-processes` | Mutating command/terminal lifecycle: start, stop, restart, rename, close, bulk command control | Request is read-only status/readiness, failure diagnosis, or a single agent session's launch/prompt/close (→ `$solo-work-with-agents`) |
| `$solo-observe-services` | Read-only command/terminal status/output, ports, URLs, service readiness, activity evidence | User asks to change lifecycle, repair failure, or inspect one owned agent session (→ `$solo-work-with-agents`) |
| `$solo-troubleshoot` | Diagnose MCP discovery, identity, project scope, trust, command config, API/CLI, or runtime failures | User only needs normal status view or authorized restart |
| `$solo-work-with-agents` | Launch, prompt, inspect, wake, hand off, and close one owned agent | Two or more independent worker lanes need lead integration |
| `$solo-orchestrate-agents` | Decompose independent lanes—implementation, review, or evidence-gathering—spawn bounded workers, coordinate state/timers/locks, reconcile output | Work is sequential, shares same files, or needs one judgment loop |
| `$solo-track-todos` | Actionable work records, blockers, priorities, claims, locks, comments, completion handoffs | Material is narrative context rather than owned action |
| `$solo-keep-scratchpads` | Working (persistent-but-non-canonical) Markdown plans, research, decisions, evidence, summaries, and handoffs | Item needs assignee/status/blockers or reusable prompt behavior |
| `$solo-close-out-work` | Multi-surface reconciliation of a finished run: promote durable content to repo docs, then archive/complete/backlog the ephemeral scratchpads, todos, timers, and owned locks/KV | Single-surface edit owned by the state skill, active work, or any process control |
| `$solo-save-prompts` | Cross-agent reusable prompt templates with placeholders and insert/send/copy flow | Content is current task truth or durable project decision |
| `$solo-automate` | Select and use Solo MCP, CLI, local HTTP, hosted API, or deep links; compose repeatable integrations | Request is normal interactive use already owned by focused workflow skill |

## Integration surface selection

| Caller/goal | Prefer | Why |
|---|---|---|
| Agent controlling local Solo | MCP | Richest identity, process, coordination, todo, scratchpad, timer, and lock surface |
| Shell script or local CI | `solo` CLI | Stable JSON envelopes and exit codes; CLI handles local API discovery/token |
| Editor or local structured integration | Local HTTP API | Loopback REST; bootstrap from live discovery file every run |
| Human navigation/handoff | `solo://` deep link | Opens exact project, process, todo, or scratchpad in Solo |
| Public docs/download/update/license/feedback service | Hosted API v1 | Internet-facing service; distinct from local loopback `/api` |

Do not hard-code local API port/token, agent tool IDs, enabled MCP groups, or docs-only tools. Discover runtime catalog.

## Solo mental model

```text
Solo app
└── Workspace
    └── Project (filesystem folder)
        ├── Todos
        ├── Agents       ┐
        ├── Terminals    ├─ processes
        ├── Commands     ┘
        └── Scratchpads
```

- Workspace organizes projects and windows; switching workspace does not stop processes.
- Project is filesystem scope, not security sandbox or hard orchestration boundary.
- For related repositories, a parent folder may be its own "Solo Parent" project while authorized workers spawn into child projects. Record cross-project child IDs and keep one active work lane per repository.
- Process means command, agent, or terminal.
- Command is reusable managed shell process; agent is real configured CLI agent; terminal is ad hoc shell.
- Todo and scratchpad are project-scoped working records — persistent across sessions but non-canonical, promoted to repo docs at closeout — not processes.

## Common routing sequences

- **Set up and run project:** `$solo-set-up-projects` → `$solo-run-processes` → `$solo-observe-services`.
- **Single agent task:** `$solo-work-with-agents`; add `$solo-track-todos` or `$solo-keep-scratchpads` only when work needs durable state.
- **Multi-agent task:** `$solo-orchestrate-agents` owns lead loop; use todos for lanes, scratchpad for shared plan/evidence, timers for wakeups.
- **Research fan-out:** `$solo-orchestrate-agents` supplies bounded workers, timers, and handoffs for independent evidence lanes; provider selection and citation discipline come from the session's own research method or skill, not from Solo.
- **Multi-repository task:** keep each repository as its own project, optionally add parent folder as overview project, and require explicit cross-project spawn scope.
- **Failure:** `$solo-troubleshoot` diagnoses; hand authorized lifecycle change to `$solo-run-processes`.
- **Repeat workflow:** first prove interactively with focused skill; use `$solo-save-prompts` for reusable text or `$solo-automate` for programmatic integration.
