# Solo project/process configuration and runtime workflows

Research date: 2026-07-15. Solo docs snapshot: 2026-07-15T18:32:16Z (147 pages). Scope: project setup, `solo.yml`, command trust/lifecycle, execution environment, service readiness, and inspection. This describes current Solo behavior, then calls out version history where it changes interpretation.

## Executive model

Solo separates shared configuration from local runtime state:

- `solo.yml` is repo-controlled source of truth for command definitions. Solo parses it from project root and syncs file-backed commands into local database state.
- Runtime facts—PID, status, current output, port bindings, trust history, terminals, and agents—stay local. Terminals and agents cannot be declared in `solo.yml`.
- A “process” is umbrella term for three kinds: `command`, `terminal`, and `agent`. Only commands participate in YAML storage, auto-start, crash auto-restart, file-watch restart, and project-wide bulk command actions.
- File-defined commands are inert until trusted locally. Trust binds exact security-relevant command variant, not merely visible name.
- Readiness means Solo associated tracked process with listening localhost port. It is listener readiness, not HTTP/application health.

Sources: Solo MCP help topics `solo.yml`, `processes`, and `readiness`; [solo.yml overview][d-yml]; [Trust and Security][d-trust]; [Services MCP tools][d-services].

## `solo.yml`: complete supported shape

```yaml
# All root keys optional.
name: string
icon: path/relative/to/project.png
icon_initials: XY

# Missing or null means empty map.
processes:
  Process display name:
    command: string                 # required
    working_dir: string | null      # optional
    auto_start: boolean             # optional; default true
    auto_restart: boolean           # optional; default false
    restart_when_changed:           # optional; default []
      - glob/string
    env:                             # optional; default {}
      KEY: string
```

No additional supported process keys are documented. Unknown root/process keys are currently ignored during deserialization, not rejected; do not rely on them as extension points. Empty or comment-only files are valid empty config. `processes` missing or `null` is also empty config. `solo.yml` maximum size is 1 MB.[^help-yml] [solo.yml overview][d-yml]

### Root fields

| Field | Meaning | Constraints/behavior |
|---|---|---|
| `name` | Optional project display name | Used when project is first loaded from file. Local display-name changes can still exist. |
| `icon` | Optional project icon | Path relative to project root; must remain inside root, be at most 256 KB, and use `png`, `jpg`, `jpeg`, `gif`, `ico`, or `webp`.[^help-yml] |
| `icon_initials` | Optional swatch initials | Exactly 1–2 characters when synced; app edits write back when project has YAML. |
| `processes` | Map of display name to command config | Only command processes. Name collisions with existing terminal/agent rows are skipped instead of overwriting those rows. |

Source: [solo.yml overview][d-yml].

### Process fields and edge behavior

- `command` is shell command Solo launches through project’s resolved execution profile.
- `working_dir` defaults to project root when absent/null. Relative paths resolve from project root. Absolute paths are accepted only when resolved path stays inside project root. Parent traversal, external absolute paths, and symlink escapes are rejected.[^help-yml] [Changelog v0.6.5 and v0.9.3 fixes][changelog]
- `auto_start` defaults to `true` in YAML. This only marks command eligible; project-level Auto Start, trust, and license/project limits still gate automatic launch.
- `auto_restart` defaults to `false`; it reacts to unexpected exit, not file changes.
- `restart_when_changed` patterns match project-root-relative paths. Invalid patterns are ignored rather than failing whole config. Empty/all-invalid list creates no watcher.
- `env` values are strings. Environment overrides participate in trust fingerprint; never put secrets in committed YAML.

Sources: Solo MCP `help(topic="solo.yml")`; [solo.yml overview][d-yml]; [Auto-start][d-autostart]; [Auto-restart][d-autorestart]; [File-watch Auto-restart][d-filewatch].

### Shareable multi-service pattern

```yaml
name: storefront
icon_initials: SF

processes:
  Web:
    command: pnpm dev
    working_dir: apps/web
    auto_start: true
    auto_restart: false
    restart_when_changed: []
    env:
      NODE_ENV: development

  API:
    command: cargo run -p api
    working_dir: services/api
    auto_start: true
    auto_restart: true
    restart_when_changed:
      - services/api/config/**
      - services/api/migrations/**
    env:
      RUST_LOG: api=debug

  Queue:
    command: bundle exec sidekiq
    working_dir: null
    auto_start: true
    auto_restart: true
    restart_when_changed: []
    env: {}

  Tests:
    command: pnpm test
    working_dir: null
    auto_start: false
    auto_restart: false
    restart_when_changed: []
    env:
      CI: "false"
```

Pattern rationale:

- Keep long-running stack entries `auto_start: true`; mark one-shot tests/migrations/formatters false because YAML default is true.
- Prefer tool-native hot reload for dev server (`Web`) and leave `restart_when_changed` empty. Use Solo file watching only where process lacks reliable watch mode (`API`).
- Enable crash restart for persistent workers/services, not commands where clean exit is normal.
- Keep secrets in shell/keychain/local environment; committed `env` should contain non-secret deterministic flags only.
- Use narrow repo-root-relative globs. Solo’s `*` can cross path separators, so broad `*` patterns can restart on unrelated monorepo changes.

## Sync, storage, and trust

### File-backed versus local commands

UI-created commands are immediately trusted and can be saved to `solo.yml` or kept local. Existing commands can switch storage: **Save to YML** writes shared config; **Make local** removes YAML entry but preserves local command. Only command rows can move into YAML. Deleting running command is disabled; deleting YAML-backed command updates file and local synced state.[Adding and removing commands][d-add]

Solo watches open project root for `solo.yml` changes, debounces filesystem events, and compares hashes. Git pulls, branch switches, direct edits, rewrites, removal, unreadability, and oversize state can mark project out of sync. Returning file to last-synced content clears warning. Sync can add/update/remove commands and preserve an unambiguous rename when removed/added entries share command string. Running commands removed by sync are stopped. Sync changes configuration only; it does not auto-start or restart commands.[solo.yml change notifications][d-sync]

### Trust algorithm

Untrusted YAML commands cannot manually start, auto-start, restart, crash-restart, or file-watch-restart. User reviews exact command/config in UI, then trusts locally.[Trust and Security][d-trust]

Trust fingerprint includes:

- command string
- working directory
- environment
- `auto_start`
- `auto_restart`
- file-watch patterns (order normalized)

Rename alone can preserve trust when underlying variant stays identical. Previously trusted exact variant may regain trust after branch switches. Trust remains machine-local and project/variant-scoped; teammates and second machines review separately. New/changed variants require review unless exact variant was trusted, project **Automatically trust command changes** is enabled, or user-initiated create/save flow grants trust. Auto-trust suits private repos under direct control; unsafe working directories still require review.[Trust and Security][d-trust] [solo.yml change notifications][d-sync]

Practical review sequence:

1. Sync YAML.
2. Inspect command, `working_dir`, and `env`; treat them as one execution unit.
3. Trust individual commands (or project batch only after reviewing diff).
4. Start auto-start set manually after sync if desired; sync itself never launches it.

## Command lifecycle

### Start paths

Automatic launch needs all conditions:

1. process kind is command;
2. project Auto Start enabled for app/project-load startup;
3. command `auto_start` enabled;
4. command trusted;
5. license/project limits permit launch.

Project action **Start auto-start** respects per-command flag even when project startup toggle is off. **Start all** starts all trusted commands regardless of `auto_start`. Bulk stop/restart actions apply only to commands, not terminal/agent rows.[Auto-start][d-autostart] [Start, Stop, and Restart][d-lifecycle]

### Stop/restart semantics

- Stop terminates managed process, releases todo locks owned by it, and removes crash-recovery tracking.
- Restart stops current instance and launches latest saved configuration with current terminal size; untrusted commands remain blocked.
- Bulk actions: Start auto-start, Start all, Stop all, Restart running in UI; CLI exposes project `commands start-all`, `stop-all`, and `restart-all`.
- Restart uses existing stored entry. Spawn is for new terminal/agent; command creation remains config/UI flow.

Sources: [Start, Stop, and Restart][d-lifecycle]; [Process MCP tools][d-process-mcp]; [CLI projects/processes][d-cli-procs].

### Crash auto-restart

`auto_restart: true` launches fresh instance after crash/unexpected exit. Existing crash output remains and restart banner separates next run. Loop guard pauses after 10 restarts within 60 seconds and displays exhausted indicator. It applies only to commands, never terminals/agents, and is disabled during app shutdown.[Auto-restart][d-autorestart]

Recommended use:

- Good: queue workers, WebSocket servers, sidecars expected to stay alive.
- Usually bad: tests, migrations, build jobs, commands where exit 0 means completion.
- Crash loop: inspect retained output before manual restart; do not hide deterministic boot failure behind repeated starts.

### File-watch restart

Solo recursively watches project directory create/modify events. Matching events are debounced/coalesced during quiet window, then trigger full command restart plus file-restart event. Watch restart and crash restart are independent.[File-watch Auto-restart][d-filewatch]

```yaml
restart_when_changed:
  - services/api/config/**
  - services/api/migrations/**
  - shared/schema/**/*.json
```

Use explicit paths in large repos. Since Solo matcher lets `*` cross separators, `src/*.ts` is not equivalent to conventional single-directory glob assumption. Invalid patterns are ignored; empty/invalid list silently means no watcher, so verify behavior after edits.[File-watch Auto-restart][d-filewatch] [^help-yml]

## Execution profiles, shells, and environment

### Profile resolution

Every project resolves exactly one execution profile from global default, path auto-detection, or manual project override. It controls shell for commands, terminals, agents; on Windows it also selects Windows host versus WSL distribution. macOS/Linux UI calls it **Shell**; Windows calls it **Execution profile**.[Execution profiles][d-profiles]

Resolution patterns:

- macOS/Linux: System default plus installed Zsh, Bash, Fish, and `sh`; custom shell commands supported, including arguments such as `bash --login`.
- Windows: System default/`COMSPEC`, Command Prompt, PowerShell variants, Git Bash, WSL default, and per-distro `wsl:<distro>` profiles.
- Project setting can inherit default, be WSL path-auto-detected, or be manually selected. Unavailable selection is preserved and warned rather than silently replaced.
- Windows project on host drive assigned WSL profile needs distro-visible root mapping (suggested `/mnt/<drive>/...` or explicit native WSL clone path).
- One-off terminal launches may still choose explicit shell without changing project profile.

Solo v0.8.2 (2026-06-05) introduced project-level execution profiles and made commands inherit configured default terminal shell. v0.9.3 (2026-06-21) added per-environment WSL root mappings and fixed commands/agents incorrectly launching at project root instead of configured `working_dir`.[Changelog][changelog]

### Shell environment pipeline

On Unix-like systems Solo resolves login shell from `SHELL`, passwd entry, then `/bin/sh`; runs it as `-ilc env`; parses output; caches result 10 minutes. Capture failure falls back to app environment, with common Homebrew paths prepended on macOS. Refresh command exists in command palette. Already-running children never receive refreshed values; restart them.[Shell environment][d-shell-env]

On Windows there is no login-shell capture. Children inherit normalized app environment: missing `HOME` comes from `USERPROFILE`, missing `SHELL` comes from `COMSPEC`. WSL-launched processes use distro shell/config. Some Solo versions expose per-project Environment Pipeline; absent control means shell-capture path remains active.[Shell environment][d-shell-env]

Solo injects reserved variables into every managed command, terminal, and agent:

| Variable | Meaning |
|---|---|
| `SOLO_PROCESS_ID` | Solo process ID, not OS PID |
| `SOLO_PROJECT_ID` | owning Solo project ID |
| `SOLO_PROCESS_KIND` | `command`, `terminal`, or `agent` |

These are useful for conditional shell behavior, but must not be treated as authentication credentials.[Shell environment][d-shell-env]

### Version-manager pattern

`asdf`, `mise`, `pyenv`, Ruby managers, Homebrew language tools, and shell-initialized virtualenv tools work when their exports/shims are present in interactive login shell environment. Troubleshooting order: verify normal login shell, move/init exports into startup file that login shell loads, refresh Solo shell environment or wait 10 minutes, restart affected process.[Version managers][d-version-managers]

`nvm` caveat: if only available as interactive shell function and required paths are not exported for managed command launches, Solo cannot invoke it reliably. Prefer version-manager shims/exported `PATH`, or make command explicitly initialize runtime when project portability requires it.[Version managers][d-version-managers]

## Services, ports, and readiness

Solo derives services from listening localhost ports owned by tracked process or descendants. Three inspection levels:

| Need | MCP tool | Result |
|---|---|---|
| Discover whole project | `services_list` | detected services, readiness, URLs, ports |
| Wait for startup | `wait_for_bound_port` | blocks until target/project process binds; timeout returns `ready=false`, `timed_out=true` |
| Inspect known process | `get_process_ports` | current ports/URLs for process and children |

Sources: Solo MCP `help(topic="readiness")`; [Services MCP tools][d-services]; [Output MCP tools][d-output-mcp].

Practical readiness flow:

1. Start/restart command.
2. Call `wait_for_bound_port` rather than scrape “ready” log line.
3. Use returned detected URL/port; do not assume framework default or hard-code dynamic port.
4. If multiple services already run, call `services_list`; if target known, narrow with `get_process_ports`.
5. If application-level readiness matters (database migrations complete, HTTP dependency healthy), perform explicit protocol health request after port readiness. Solo port readiness proves listener only.

Activity monitor exposes bound ports for managed roots and descendants. Detected service URLs preserve HTTPS/custom local hostnames from process output when matching bound port as of v0.7.1.[Activity monitor][d-activity] [Changelog][changelog]

## Output, status, and inspection

### UI

- Sidebar states: starting, running/active, stopping, stopped, error/failed. Trust, unread output, and exhausted restart are separate indicators; terminal/sidebar can briefly update at different times.[Status Indicators][d-status]
- Selected command opens full terminal emulator with live output and up to 10,000 retained lines for current run. Scrolling up disables follow until jumping bottom. Clear removes retained buffer without stopping process.[Terminal basics][d-terminal]
- Terminal search is plain text, case-insensitive, current frame plus loaded main-buffer history; no regex. Alternate-screen search covers active frame only. Cleared/pruned output is unavailable.[Terminal search][d-terminal-search]
- Process definitions persist, but runtime terminal output is not archival across app restarts. Running pane can detach/reattach without restart.[Terminal persistence][d-terminal-persist]
- Activity monitor shows project, process/subprocess, CPU, memory, command, bound ports, PID, type, parent, and kill controls; supports tree/flat views and filters.[Activity monitor][d-activity]

### MCP inspection workflow

```text
list_projects -> select_project (if scope ambiguous)
get_project_status / list_processes
get_process_status(process_id|process_name)
get_process_output(...)          # rendered terminal rows; default 50, max 200
search_output(...)               # rendered search
get_process_raw_output(...)      # control sequences/raw bytes; default 50, max 200
search_raw_output(...)
get_process_ports(...)
clear_output(...)                # buffer only; PTY/process untouched
```

Rendered output is default for ordinary diagnosis; raw output is for escape-sequence/protocol investigation. `select_process` attaches/renders terminal in Solo UI. `send_input` can send text plus Enter or raw bytes (`3` Ctrl+C, `4` Ctrl+D, `27` Escape). Command start/restart remains trust-gated.[^help-processes] [Process MCP tools][d-process-mcp] [Output MCP tools][d-output-mcp]

### CLI workflow

CLI ships inside app; enable HTTP API and install app-provided symlink snippet. State-control commands require running Solo app and enabled HTTP API. `solo --version` is local CLI binary version; `solo version` contacts app. `solo status` reports readiness, versions, project count, process counts by state, data dir, and API port. `solo doctor` checks CLI version, discovery file, app reachability, and version compatibility.[CLI overview][d-cli]

```bash
solo projects list
solo projects get 2
solo processes list --project-id 2
solo processes list --project-id 2 --status failed
solo processes get 9
solo processes output 9 --lines 200
solo processes output 9 --raw --lines 500
solo processes start 9
solo processes stop 9
solo processes restart 9
solo commands start-all --project-id 2
solo commands stop-all --project-id 2
solo commands restart-all --project-id 2
```

All accept `--json`. Success prints single JSON envelope to stdout; error envelope goes stderr and exit nonzero. Process status filter values are `stopped`, `starting`, `running`, `stopping`, `exited`, `failed`. JSON list responses paginate and report `hasMore`/`nextOffset`. Bulk output distinguishes started, skipped, and failed commands; trust blocks start/restart but not stop.[CLI projects/processes][d-cli-procs] [JSON output and scripting][d-cli-json]

## Project setup workflow

### App onboarding

1. Add repo root by sidebar, `Cmd/Ctrl+O`, folder drag/drop, or macOS Finder/Open With.
2. Existing canonical path reuses project; no duplicate setup.
3. If root has `solo.yml`, Solo loads it instead of detection wizard and commands require trust review.
4. Without YAML, Solo scans recognized files, proposes commands, lets user enable/rename/add, then choose `solo.yml` (shareable) or local storage.
5. Confirm project Auto Start behavior separately. Commands do not run merely because setup completed.

Sources: [Creating and loading projects][d-project-create]; [Command auto-detection][d-detect].

Detection covers package scripts/managers, Procfiles, Make/Just/Task, PM2, Turbo/Nx, and common PHP/Rust/Java/Python/Ruby/Go/.NET/Phoenix/Docker ecosystems. For JS it chooses package manager from `packageManager`, then lockfiles, then npm. Detection runs once on initial add only when no `solo.yml`; later tooling changes require manual command/YAML edit.[Command auto-detection][d-detect]

Project root is preferred. Monorepo pattern: add monorepo root and use package filters or `working_dir` per command. Setup suggestions are convenience, not durable discovery; commit explicit `solo.yml` after review.[Creating and loading projects][d-project-create]

### CLI/MCP registration

```bash
solo projects create my-app /existing/path/to/repo
solo projects list
```

CLI create requires existing directory. MCP `create_project(path, name?, workspace_id?)` registers/imports without app onboarding UI; canonical duplicate returns existing project. Use MCP `list_projects`, then `select_project`, `get_project`, or `get_project_status` to establish scope. Project deletion removes Solo state, not repo files, and requires explicit confirmation—plus stop-running confirmation when active processes exist.[CLI projects/processes][d-cli-procs] [Project MCP tools][d-project-mcp]

## Changelog signals relevant to current practice

Official changelog is product history, not current API contract; current docs/help above win on behavior.[Changelog][changelog]

| Version/date | Relevant change | Current implication |
|---|---|---|
| v0.9.3 — 2026-06-21 | Per-environment WSL root mappings; fixed `working_dir` regression from v0.8.2; WSL path handling and shell probing fixes | Verify 0.9.3+ for WSL/profile-heavy workflows. Keep `working_dir` explicit where needed. |
| v0.8.2 — 2026-06-05 | Project execution profiles; commands inherit configured terminal shell; CLI/API gained recent output/status filters and broader process workflows | Treat project profile as shared launch context for terminals, commands, agents. |
| v0.7.1 — 2026-05-14 | Major local HTTP API/CLI; canonical external project flows; process lifecycle cleanup; bound URL preservation | CLI automation is first-class but still mediated by running app/local API. |
| v0.6.5 — 2026-04-28 | Absolute `working_dir` allowed inside root while rejecting traversal/symlink escape | In-root absolute paths valid, but relative paths remain more portable. |
| v0.6.4 — 2026-04-27 | Blank/comment-only YAML sync fixed | Empty starter file now valid. |
| v0.6.1 — 2026-04-22 | Activity monitor with process tree, stats, ports; MCP help gained YAML guidance | Prefer structured inspection over terminal guessing. |
| v0.6.0 — 2026-04-20 | Editable working dir with YAML writeback; per-project auto-trust setting; sync warning fixes | Review app edits as repo diffs; reserve auto-trust for controlled repos. |
| v0.5.8 — 2026-03-13 | Dedicated untrusted-command review, project trust-all, remembered variants, login/interactive shell improvements | Trust is variant history, not one blanket repository bit. |
| v0.2.0 — 2026-02-05 | Project start-auto/start-all/stop-all shortcuts; centralized output store; restart race fix | Bulk lifecycle and structured output have long-standing product roles. |

## Practical operating recipes

### Daily startup

1. Open/add project and sync changed `solo.yml`.
2. Review trust-sensitive diff; trust accepted variants.
3. Start `auto_start` subset, not all, unless every YAML command is persistent dev stack.
4. Wait for bound port(s); discover actual URLs.
5. Inspect `get_project_status`/Activity monitor for failed processes and port conflicts.

### Diagnose “command not running”

1. Separate trust state from run state.
2. Check profile availability and `working_dir` validity.
3. Inspect rendered output; use raw only for terminal-control issues.
4. Check crash-loop exhausted indicator if `auto_restart` enabled.
5. Run `solo doctor` if CLI/app connection failed; refresh shell environment and restart process if executable missing.

### Branch switch with YAML changes

1. Let Solo flag hash mismatch; inspect Git diff before Sync.
2. Sync; expect changed variants to become untrusted unless exact trusted history matches.
3. Remember sync does not restart currently retained commands or launch new auto-start commands.
4. Restart affected running commands explicitly after trust/config review.

### Portable team config checklist

- Commit commands, relative `working_dir`, safe defaults, and non-secret env only.
- Set every `auto_start` explicitly to defeat surprising default.
- Keep runtime-manager initialization in login-shell-visible exports/shims.
- Avoid machine-specific absolute paths and WSL distro names in command strings.
- Prefer native watcher; use narrow Solo restart globs only where needed.
- Document true application health endpoint separately from port binding.
- Treat output as operational scrollback, not durable logs.

## Sources

### Local Solo MCP help

[^help-yml]: Solo MCP `help(topic="solo.yml")`, queried 2026-07-15. Primary source for complete accepted YAML shape, defaults, path/glob validation, unknown-key behavior, YAML/icon size/type limits, and trust-sensitive fields.
[^help-processes]: Solo MCP `help(topic="processes")`, queried 2026-07-15. Primary source for process kinds, lifecycle/output/input tools, bulk command scope, and control-byte examples.

### Solo docs/API

[d-yml]: https://soloterm.com/api/v1/docs/projects/solo-yml
[d-sync]: https://soloterm.com/api/v1/docs/projects/yml-change-notifications
[d-project-create]: https://soloterm.com/api/v1/docs/projects/creating-loading-projects
[d-detect]: https://soloterm.com/api/v1/docs/projects/command-auto-detection
[d-add]: https://soloterm.com/api/v1/docs/commands/adding-removing
[d-trust]: https://soloterm.com/api/v1/docs/commands/trust-security
[d-autostart]: https://soloterm.com/api/v1/docs/commands/auto-start
[d-autorestart]: https://soloterm.com/api/v1/docs/commands/auto-restart
[d-filewatch]: https://soloterm.com/api/v1/docs/commands/file-watch-auto-restart
[d-lifecycle]: https://soloterm.com/api/v1/docs/commands/start-stop-restart
[d-status]: https://soloterm.com/api/v1/docs/commands/status-indicators
[d-profiles]: https://soloterm.com/api/v1/docs/environment/execution-profiles
[d-shell-env]: https://soloterm.com/api/v1/docs/environment/shell-environment
[d-version-managers]: https://soloterm.com/api/v1/docs/environment/version-managers
[d-services]: https://soloterm.com/api/v1/docs/mcp-tools/services
[d-process-mcp]: https://soloterm.com/api/v1/docs/mcp-tools/process
[d-output-mcp]: https://soloterm.com/api/v1/docs/mcp-tools/output
[d-project-mcp]: https://soloterm.com/api/v1/docs/mcp-tools/project
[d-terminal]: https://soloterm.com/api/v1/docs/terminal/basics
[d-terminal-search]: https://soloterm.com/api/v1/docs/terminal/search
[d-terminal-persist]: https://soloterm.com/api/v1/docs/terminal/persistent-sessions
[d-activity]: https://soloterm.com/api/v1/docs/activity/activity-monitor
[d-cli]: https://soloterm.com/api/v1/docs/cli/overview
[d-cli-procs]: https://soloterm.com/api/v1/docs/cli/projects-and-processes
[d-cli-json]: https://soloterm.com/api/v1/docs/cli/json-output-and-scripting
[changelog]: https://soloterm.com/changelog
