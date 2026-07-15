# Solo product: end-to-end product and documentation research

Research date: 2026-07-15 (America/New_York)
Documentation snapshot: Solo docs MCP corpus generated 2026-07-15T18:32:16.369Z; 147 pages
Current public build observed: v0.9.3, released 2026-06-21

## Scope, evidence, and source hierarchy

This report covers Solo's user-visible information architecture, setup, projects, workspaces, process management, terminals, agents, agent orchestration, navigation, Activity monitor, todos, scratchpads, prompt templates, notifications, keyboard behavior, appearance, settings, environment handling, integrations, CLI, account/licensing, updates, and recovery workflows.

Evidence used:

1. Solo docs MCP `search` supplied the complete 147-page corpus, titles, descriptions, canonical API URLs, and snapshot timestamp.
2. Solo docs MCP `execute` fetched the live docs index from `https://soloterm.com/api/v1/docs` and confirmed all top-level sections.
3. Public docs pages under [soloterm.com/docs](https://soloterm.com/docs) supplied human-facing canonical URLs.
4. [Product site](https://soloterm.com/), [agent product page](https://soloterm.com/agents), [download page](https://soloterm.com/download), and [changelog](https://soloterm.com/changelog) supplied positioning, pricing, current build, and release-history evidence.
5. `parallel-cli search` and `parallel-cli extract` were used to discover and capture current public pages and full changelog/product content.

When marketing and operational docs conflict, this report treats docs as authority for shipped UI and current limitations; product site remains authority for public positioning and pricing. Important conflicts are called out explicitly.

## Product model and boundaries

Solo is a lightweight native terminal workspace around existing tools, not an IDE and not its own coding agent. It runs CLI agents, managed project commands, and interactive shells together; supplies lifecycle controls, status, notifications, logs, ports, resource monitoring, and team-shareable `solo.yml`; and exposes workspace context to external agents through MCP. It uses the user's locally installed agent CLIs, accounts, subscriptions, API keys, config, and authentication rather than proxying provider credentials. [Product](https://soloterm.com/) · [Agents](https://soloterm.com/agents) · [Agent concepts](https://soloterm.com/docs/agents/what-are-agents)

Core hierarchy:

```text
Solo app
└── Workspace (one or more; one visible per window)
    └── Project (filesystem folder)
        ├── Todos
        ├── Agents
        ├── Terminals
        ├── Commands
        └── Scratchpads
```

"Process" is Solo's umbrella term for a command, agent, or terminal. Commands are reusable managed shell commands; agents are interactive AI CLI sessions; terminals are ad hoc shells. Todos and scratchpads are project-scoped records, not processes. [Concepts](https://soloterm.com/docs/getting-started/concepts)

Product boundaries and caveats:

- Solo manages processes, not containers. Docker workflows run as commands such as `docker compose up`; Solo does not replace Docker. [Product FAQ](https://soloterm.com/)
- Solo is not a git-worktree isolation/review orchestrator. Linked checkouts can share todos, scratchpads, and project templates, but agents otherwise work in the selected project environment. [Product FAQ](https://soloterm.com/) · [Changelog](https://soloterm.com/changelog)
- Runtime terminal output is not permanent archival history. Main-buffer history is limited to 10,000 lines for the current run. [Terminal persistence](https://soloterm.com/docs/terminal/persistent-sessions)
- Closing or quitting Solo stops managed commands, agents, and terminals after confirmation. A crash/force-quit can leave recoverable orphan records. [Safe restart](https://soloterm.com/docs/updates/restarting-safely) · [Orphaned processes](https://soloterm.com/docs/commands/orphaned-processes)

## Platform, installation, and first-run onboarding

### Platforms and build

Current docs and download page show packaged macOS and Windows builds:

- macOS 11 Big Sur minimum; Apple Silicon and Intel.
- Windows 10 version 1809 minimum; 64-bit.
- Linux/Ubuntu 20.04-equivalent is displayed as coming soon, not currently downloadable.
- Public download page labels v0.9.3 as beta and offers signed installers. [Installation](https://soloterm.com/docs/getting-started/installation) · [Download](https://soloterm.com/download)

macOS install uses a `.dmg` dragged into Applications. Windows uses an `.exe` installer. Packaged builds have a signed built-in updater. macOS may require the normal downloaded-app Open confirmation; a stricter verification warning can be cleared with Finder's right-click **Open** flow. [Installation](https://soloterm.com/docs/getting-started/installation)

### True first launch

Solo initializes local app data, license state, settings, and project list, then creates a **Welcome to Solo** demo project only on a true fresh install with no existing projects. Removing it is immediate; it never reappears automatically. Upgrades with existing projects never receive it. [First launch](https://soloterm.com/docs/getting-started/first-launch) · [Demo project](https://soloterm.com/docs/getting-started/demo-project)

Demo project content:

- **Click here first** guided tour and command-palette shortcut.
- Simulated **Dev server (example)**.
- Crash **Auto-restart** demonstration.
- Interactive **Notifications** walkthrough.
- **Colors** terminal test.
- **Agents and terminals** introduction.
- **Cleanup** instructions.
- Starter todo plus two scratchpads, including workflow-orchestration guidance.

Demo files live inside Solo's app-data directory, not user repositories. Commands run bundled shell scripts on macOS/Linux and PowerShell scripts on Windows. Updates may refresh bundled scripts but retain customized commands. [Demo project](https://soloterm.com/docs/getting-started/demo-project)

### First real project flow

1. Add/open project folder.
2. Review auto-detected command suggestions when no `solo.yml` exists.
3. Enable, disable, rename, or add commands.
4. Save suggestions to recommended repo-root `solo.yml` or keep them local.
5. Review trust-sensitive repo-defined commands before launch.
6. Configure optional Appearance, Notifications, Hotkeys, Tools, MCP, HTTP API, and Account settings.

If `solo.yml` already exists, Solo syncs and watches it instead of showing detection suggestions. Auto-start still obeys project enablement, per-command `auto_start`, trust, and license limits. [First launch](https://soloterm.com/docs/getting-started/first-launch) · [Creating projects](https://soloterm.com/docs/projects/creating-loading-projects)

## Main UI and navigation

### Window anatomy

- **Sidebar:** workspaces/projects and Todos, Agents, Terminals, Commands, Scratchpads sections.
- **Main area:** selected terminal/process, todo list/detail, scratchpad list/editor, section overview, Activity monitor, settings, or project list.
- **Title bar:** current selection, free/license state, unread attention count, and update/relaunch state.
- **Settings:** in-app panel, not separate window. [Interface overview](https://soloterm.com/docs/getting-started/interface-overview) · [Settings](https://soloterm.com/docs/settings/overview)

When nothing is selected, Solo shows either the first-run **Welcome** pane or a **Projects** pane listing current-workspace projects plus Add project. Selecting a project header lands on Projects, not a dedicated per-project detail page. Selecting Agents, Terminals, or Commands section labels opens section overview/splash panes; Todos and Scratchpads labels open their list views. Chevron clicks collapse instead of selecting. [Section panes](https://soloterm.com/docs/sidebar/section-splash-screens)

### Sidebar sections and defaults

Canonical new-project order: **Todos → Agents → Terminals → Commands → Scratchpads**. Sections are draggable and order persists locally per project; a preferred global default exists in Sidebar settings. Todos and Scratchpads can be disabled entirely from **Settings → Notes & todos**. Empty built-in sections are shown by default unless per-section hide-empty controls say otherwise. No collapse-all/expand-all action exists. [Sections](https://soloterm.com/docs/sidebar/understanding-sections) · [Reordering](https://soloterm.com/docs/sidebar/reordering-sections) · [Collapse](https://soloterm.com/docs/sidebar/collapsing-expanding)

Section headers can show icon, name, and running/total or visible-item count. Decorations/counts can be hidden. Empty visible sections provide inline add rows where supported. [Sections](https://soloterm.com/docs/sidebar/understanding-sections)

### Sidebar filter

With sidebar focused, `\` focuses filter input. Filter is case-insensitive substring matching across all sidebar projects and includes commands, agents, terminals, active todos, and unarchived scratchpads. A matching project name keeps its items visible. `Escape` clears and blurs. **Show filter input** defaults on; turning it off hides and clears filter and disables `\`. Drag reorder is unavailable while filtering. [Sidebar filter](https://soloterm.com/docs/sidebar/filtering) · [Sidebar settings](https://soloterm.com/docs/settings/sidebar-settings)

### Command palette family

| Shortcut | Mode | Scope/purpose |
|---|---|---|
| `Cmd/Ctrl+K` | Command center | App-wide plus project actions; active project preferred |
| `Cmd/Ctrl+P` | Context actions | Current process or active project actions; no app-global actions |
| `Cmd/Ctrl+E` | Quick jump | Projects, processes, sections, todos, scratchpads, templates |
| `Cmd/Ctrl+Shift+E` | Focus jump | Unread or favorite processes |
| `Cmd/Ctrl+Shift+P` | Prompt template picker | Insert/send/copy reusable prompt |
| `Cmd/Ctrl+T` | New item | Command, terminal, agent, scratchpad/import, todo in active project |

Palette shortcuts retarget an already-open palette but are blocked by modal/pane overlays. Project-scoped search syntax is `project name > action`. With two or more workspaces, palette defaults to current workspace; `Tab` toggles all-workspace search. Jump results can copy `solo://` links, and pasting a deep link produces a **Go** result. [Command palette](https://soloterm.com/docs/command-palette/using) · [Context actions](https://soloterm.com/docs/command-palette/context-actions) · [New item](https://soloterm.com/docs/command-palette/new-tab-picker)

### Favorites and attention navigation

Commands, terminals, and agents can be favorited from hover star, context menu, or palette; todos/scratchpads cannot. `Cmd/Ctrl+Shift+[` and `]` cycle favorites across current workspace, wrapping. If any favorites run, cycling visits only running favorites; otherwise all. Focus jump ranks unread favorites, other unread processes, running favorites, then remaining favorites. [Favorites](https://soloterm.com/docs/sidebar/favorites)

## Workspaces and multiple windows

Every install begins with one **Default Workspace**. Rail stays hidden until second workspace exists. Each project belongs to exactly one workspace; switching swaps sidebar contents but does not stop background processes. [Workspace overview](https://soloterm.com/docs/workspaces/overview)

Workspace rail:

- Top group: workspaces open in current window; active has highlight.
- Bottom group: other workspaces, dimmed.
- Unread-process badge caps at `99+`.
- Keyboard within rail: arrows, Home/End, Enter/Space.
- `+` and context menus open/create/manage workspaces.

Workspace launcher `Cmd/Ctrl+Shift+L` searches workspace names plus project names/paths, opens/focuses workspace owners, expands project lists, and supports drag-moving/reordering projects. Numbered workspace actions 1–9 exist but ship unbound. [Workspace overview](https://soloterm.com/docs/workspaces/overview) · [Multiple windows](https://soloterm.com/docs/workspaces/multi-window)

Workspace management supports name, derived/override 1–2 initials, eight swatch colors or neutral, and custom PNG/JPG/JPEG/GIF/ICO/WebP copied into app data. Workspace names autosave after brief pause. Only workspace cannot be deleted; deleting a populated workspace requires a destination and moves projects without deleting disk files. Project moves never stop processes. [Managing workspaces](https://soloterm.com/docs/workspaces/managing-workspaces)

Workspaces can be moved to new windows or dragged between Solo windows. A workspace can exist in only one window; clicking it elsewhere focuses owner window. Empty secondary windows close; empty main window hides. Placement is remembered. [Multiple windows](https://soloterm.com/docs/workspaces/multi-window)

## Projects and `solo.yml`

### Adding, restoring, moving, and removing

Add project via sidebar, `Cmd/Ctrl+O`, drag one/more folders from Finder/Explorer, macOS Finder **Open in Solo** service/Open With, or `open -a Solo /path`. Files in a drag are ignored. Canonical duplicate folders select existing project and skip setup. External open works when app is closed and focuses after launch. [Creating projects](https://soloterm.com/docs/projects/creating-loading-projects)

Solo restores projects/settings at launch. Missing project paths are removed as stale with notification; to retain project state after a move, use **Edit directory** before relaunch. New path must exist, be directory, and not belong to another project. Running processes keep old cwd until restart. Removing project stops/removes managed rows but never deletes repo or `solo.yml`. [Creating projects](https://soloterm.com/docs/projects/creating-loading-projects)

### Auto-detection

Detection runs automatically only when first adding a folder without `solo.yml`; it does not rerun after repo/tooling changes. Suggestions can be toggled, renamed, or augmented before confirmation. [Auto-detection](https://soloterm.com/docs/projects/command-auto-detection)

Detected sources include:

- `package.json` priority scripts (`dev`, `start`, `serve`, `build`, `test`) and major JS frameworks/tools; package-manager choice order: `packageManager`, then bun/pnpm/yarn/npm lockfiles, then npm.
- `Procfile.dev` before `Procfile`.
- Task runner priority when multiple exist: Taskfile, Justfile, Makefile; private `_` just recipes skipped.
- PM2 JSON/YAML app arrays; JS/TS PM2 config becomes one start-config command rather than being parsed.
- Turborepo, Nx, Laravel/PHP/Composer, Rust/Cargo, Spring Boot, FastAPI, Flask, Django, Rails, Go, .NET, Phoenix, Docker Compose, plus framework workers/tooling.
- Laravel Herd detection offers `php artisan serve` unchecked to avoid conflict.

Primary dev servers are often preselected with auto-start/restart; build/test/lint/format/migration/console/GUI tools may be offered unchecked. These remain suggestions, not mandatory config. [Auto-detection](https://soloterm.com/docs/projects/command-auto-detection)

### Project customization

Display name defaults to folder name; rename affects Solo only. Project icons can be built-in swatch with 1–2 initials or project-local image. Image formats: PNG/JPG/JPEG/GIF/ICO/WebP, not SVG; maximum 256 KB; resolved path/symlink must remain inside project. Automatic favicon fallback searches root, `public`, `static`, `app`, `src/app`; explicit icon wins. Swatch colors: slate, blue, green, red, purple, cyan, orange, pink. [Project customization](https://soloterm.com/docs/projects/project-customization)

Name/color are local. Image path is shared through `solo.yml`. Initials are local and also written as `icon_initials` when YAML exists. Removing/re-adding loses local customization but committed top-level name/icon can return. [Project customization](https://soloterm.com/docs/projects/project-customization)

### `solo.yml` facts and defaults

Top-level fields: optional `name`, project-relative `icon`, 1–2-character `icon_initials`, and `processes`. Per-process fields:

- `command` required.
- `working_dir` optional; relative to project root, absolute allowed only if it resolves inside project.
- `auto_start` defaults **true when omitted in YAML**.
- `auto_restart` defaults **false**.
- `restart_when_changed` optional glob list.
- `env` optional map.

File limit is 1 MB. Empty/comment-only files are empty config. Name collisions with agents/terminals are skipped. File-backed unambiguous rename can preserve row and trust when command and security-sensitive config remain unchanged. [solo.yml](https://soloterm.com/docs/projects/solo-yml)

Watcher debounces events and compares hashes. Sync can add/update/remove commands and preserve unambiguous renames; removed running commands stop. Trust is rechecked for command/cwd/auto-start/auto-restart/watch/env changes unless exact variant was previously trusted or project auto-trust changes is enabled. Sync itself does not start/restart commands. [YAML changes](https://soloterm.com/docs/projects/yml-change-notifications)

## Commands and process lifecycle

### Create, storage, duplicate, rename, reorder, delete

UI-created commands are immediately trusted and can be local or written to `solo.yml`. Storage can later switch with **Save to YML** / **Make local**. A minimal YAML file can be created from project Config. Only commands—not agents/terminals—can be file-backed. [Adding commands](https://soloterm.com/docs/commands/adding-removing)

Duplicate one or all commands to another project; full configuration, notifications, storage type, and trust copy. Name conflicts become `Name copy`, `Name copy 2`, etc. File-backed copies write/create destination YAML. Running commands cannot be deleted; YAML deletion prompts and rewrites file. [Adding commands](https://soloterm.com/docs/commands/adding-removing)

Rename changes display/process name, not shell command/files. YAML key is rewritten for file-backed commands. Name must be non-empty and project-unique. OSC runtime title can rename transiently, but manual display override wins. Agent automatic renaming is globally on by default and can override per-agent behavior when disabled. [Renaming](https://soloterm.com/docs/commands/renaming)

Commands reorder only within same project/section. **Lesser used** hides stopped marked commands behind affordance; running marked commands stay visible. It affects no lifecycle/trust/watch behavior and stays local. [Reordering](https://soloterm.com/docs/commands/reordering) · [Lesser used](https://soloterm.com/docs/commands/lesser-used)

### Start, stop, restart, bulk actions

Start/restart requires trusted command and limits. Stop releases todo locks held by process and removes crash-recovery tracking. Restart uses latest saved config and terminal size. Bulk actions apply to commands only: start auto-start, start all, stop all, restart running. Universal GUI agents lack PTY restart. Hotkey/palette stop/restart can ask confirmation and store per-command **Don't ask again**. [Lifecycle](https://soloterm.com/docs/commands/start-stop-restart)

Project context menu includes Start all, Stop all, Restart all, Restart running, Trust all, Show lesser-used; Add command/terminal/agent/agent with flags/conditional Universal GUI agent; Copy link; move workspace; edit/remove project. Bulk lifecycle excludes agents and terminals. Removal has no undo but never deletes disk files. [Project menu](https://soloterm.com/docs/projects/project-context-menu)

### Auto-start, crash restart, file-watch restart

Auto-start requires command kind, project Auto Start for app/project-load startup, command flag, trust, and license allowance. Manual **Start auto-start** works even when project startup switch is off; Start all ignores per-command flag. [Auto-start](https://soloterm.com/docs/commands/auto-start)

Crash auto-restart keeps crash output and inserts restart banner. Limit: 10 restarts in 60-second sliding window, then pause/exhaust indicator and alert. Command-only, trusted-only, disabled during shutdown. [Auto-restart](https://soloterm.com/docs/commands/auto-restart)

File-watch restarts recursively watch create/modify events, debounce and coalesce, and fully restart on relative-root glob match. `*` can match path separators; use explicit globs such as `src/**/*.ts`. Empty/invalid list creates no watcher. It is independent of crash-loop restart. [File-watch restart](https://soloterm.com/docs/commands/file-watch-auto-restart)

### Status and crash recovery

Lifecycle states include starting, running, stopping, stopped, exited/error/failed; trust, unread, and exhausted-auto-restart are separate indicators. Brief UI/output timing differences can occur. [Status](https://soloterm.com/docs/commands/status-indicators)

After crash/force-quit, Solo adopts orphan only when project path, process name, and command still match. Remaining records offer Kill/Kill All or Leave running; leaving dismisses management, requiring OS tools later. Output while disconnected may not be fully recoverable. [Orphans](https://soloterm.com/docs/commands/orphaned-processes)

### Trust model

Untrusted `solo.yml` command cannot manually start, auto-start, restart, crash-restart, or file-watch restart. Trust is local, project-scoped, exact-variant history including command, cwd, env, auto-start/restart, and normalized watch patterns. Teammates and other devices must review separately. UI-created command and terminals/agents are trusted by design. [Trust](https://soloterm.com/docs/commands/trust-security)

## Terminal experience

### Surface and data model

Terminal pane is full terminal emulator, not log-only view. It supports default/indexed/true color, HiDPI rendering, cursor/alternate screen, bracketed paste, mouse, OSC links/titles, and history. Commands may accept stdin; interactive terminals provide full shell; agent sessions combine process output with interactive conversation. [Terminal basics](https://soloterm.com/docs/terminal/basics)

Main-buffer scrollback retains up to 10,000 lines for current run. Scrolling upward disables follow mode and shows **Jump to bottom**; returning to bottom resumes. Alternate-screen TUI forces follow for active screen. Follow changes display only, not process speed. [Terminal basics](https://soloterm.com/docs/terminal/basics) · [Follow output](https://soloterm.com/docs/terminal/pause-resume)

View reattach automatically reconnects/refreshes stale terminal snapshots without process restart; history can page when scrolling upward. PTY resize is debounced. Clear output is destructive and separate from refresh. [Reattach](https://soloterm.com/docs/terminal/reattach)

### Selection, copy, paste, files, links, mouse

- Copy: `Cmd+C` macOS / `Ctrl+Shift+C` Windows; double-click word, triple-click visible terminal row, drag extends by unit.
- Paste: `Cmd+V` / `Ctrl+Shift+V`; bracketed-paste markers honored.
- File URLs and dropped files become shell-escaped paths; pasted images become temp files and path is inserted.
- Drag over a running sidebar process pauses/selects it, then drop into its terminal.
- OSC 8 and detected plain URLs support `http`, `https`, `mailto`, local-only `file://`, and valid `solo:` links.
- Mouse-reporting TUIs receive events; modified click can force links. Normal context menu is suppressed while mouse reporting is active.

[Terminal basics](https://soloterm.com/docs/terminal/basics) · [OSC and links](https://soloterm.com/docs/terminal/osc-kitty-protocol)

### Terminal context menu

Copy, Paste, Select all, Clear selection, Clear output, Search, process lifecycle, automatic rename toggle, and link open/copy. Selected output can create scratchpad: first line becomes title (trimmed to 120 characters), full selection body. Clear output cannot be undone. [Terminal menu](https://soloterm.com/docs/terminal/context-menu)

### Search

`Cmd/Ctrl+F` is context-aware; terminal view opens terminal search. Plain-text, case-insensitive only; no regex/case toggle. Enter next, Shift+Enter previous, Escape close. Search covers current frame plus loaded main history, groups wrapped rows, and is limited to active frame on alternate screen. Pruned/cleared/unloaded output is unavailable. [Terminal search](https://soloterm.com/docs/terminal/search)

### Focus and control bar

`Cmd/Ctrl+Right` focuses terminal; `Cmd/Ctrl+Left` sidebar. Printable keys go to process only with terminal focus. Global app bindings and native copy/paste win; unbound keys pass through. Old single-click-focus setting is gone. Top/bottom focus borders are independently configurable and both default on. [Focus](https://soloterm.com/docs/terminal/focus-behavior)

Footer shows focus toggle, previous/next running (`Cmd/Ctrl+Up/Down`), context Start/Stop/Restart/Clear when unfocused, process/agent state, timer, spawned-by link, CPU/MEM across full tree, and `+N subprocesses`. Tracked-process modal shows command, PID, uptime, CPU, memory; supports per-child Kill, Activity monitor, Copy all PIDs. [Control bar](https://soloterm.com/docs/terminal/control-bar)

### Keyboard protocol and macOS input

Supports classic xterm and common Kitty CSI-u mode behaviors, though not every optional flag combination. Advertises `TERM=xterm-ghostty` locally with Solo-owned terminfo; ssh/sudo compatibility wrapper can avoid leaking identity remotely. OSC 0/1/2 titles, OSC 8 hyperlinks, color queries, focus reports, synchronized output, device/cursor/window queries supported. [OSC/Kitty](https://soloterm.com/docs/terminal/osc-kitty-protocol)

Both macOS Option keys default to Meta; configure independently. Meta sends Esc-prefixed key; disabling lets Option type layout/dead-key characters. TUI scroll multiplier range 1x–6x affects captured scroll only. macOS editing translations include Option arrows/backspace, Cmd+Backspace/Delete → Ctrl+U, Cmd arrows → Ctrl+A/E unless Solo focus shortcuts remain bound. [Terminal input](https://soloterm.com/docs/terminal/keyboard-input)

### Terminal appearance defaults

- Bundled fonts: JetBrains Mono, Geist Mono, MonoLisa, Input Mono.
- Default: Geist Mono, regular 300, bold 700.
- Size range 10–18 px on 13 px base.
- Letter spacing labels 0.5–1.3, default 1.0.
- Line height labels 1.0–1.8, default display 1.2.
- Copy on select default off.
- Top and bottom focus borders default on.

[Terminal fonts](https://soloterm.com/docs/appearance/font-settings)

## Agents

### Tool setup and supported CLIs

Built-in tool types: Claude, Codex, Amp, Gemini, OpenCode, Copilot, Kimi. Any terminal-based agent can be added as a custom Generic tool. Solo does not install CLIs. Tool fields: name, command, default arguments, auto/manual classification, generic prompt mode, optional headless summarizer command. Generic prompt delivery can use stdin or appended argument. Disabled tools disappear from creation UIs. [Agent setup](https://soloterm.com/docs/agents/setting-up-tools)

### Installation health and Runtime Doctor

Per-environment statuses:

| Status | Launchable | Meaning |
|---|---:|---|
| Ready | Yes | CLI found, `--version` succeeded |
| Not checked | Yes | Not checked or timed out/inconclusive |
| Missing | No | Not on PATH |
| Broken | No | Version check or environment failed |

Health runs only on **Refresh health**, concurrently. Missing/Broken hidden from launch menus; Not checked remains launchable. Disabled is separate. macOS/Linux check via effective shell; Windows tracks host and each non-service WSL distro; custom tools check host only. Runtime Doctor counts launchable tool/environment targets and explains tool disabled, install disabled, missing/broken/not checked, environment mismatch, invalid WSL root. MCP connection health is separate from launchability. [Installation health](https://soloterm.com/docs/agents/installation-health)

### Launch, interaction, nesting, resume, close

Launch through `Cmd/Ctrl+T`, project/process Add Agent menu, or **Agent with flags** one-off command editor. Agent uses currently selected project/effective environment and opens project directory. Multiple copies/tools/projects can run independently. Child agent spawned through MCP can nest under same-project parent; parent can collapse with `(+N subagents)`. [Launching](https://soloterm.com/docs/agents/launching-agents)

Stopped supported agents can **Resume last session** by exact saved ID or **Choose session to resume** through tool picker. Resume is agent-conversation resume, separate from terminal frame reattach. Options depend on tool capability and saved session. [Terminal persistence](https://soloterm.com/docs/terminal/persistent-sessions)

`Cmd/Ctrl+W` or **Remove agent** stops and removes row after state-sensitive confirmation; unlike commands, no restartable slot remains. Closing active task preserves filesystem edits already made and can leave partial changes. Parent close asks whether to include descendants. [Closing](https://soloterm.com/docs/agents/closing-agents)

### State and summaries

Idle state combines tool-specific heuristics and optional summarizer classification: idle, permission wait, thinking, working, error. It remains heuristic; quiet is not proof of completion. [Idle detection](https://soloterm.com/docs/agents/idle-detection)

Auto-summarization is disabled until summarizer selected. It uses compact rendered terminal snapshot, not raw/full transcript, after human input and quiet/activity cadence. Cadences: 15 sec, 30 sec, 1 min. Too little output skips. Spawned subagents skip automatic summaries. Claude's own recap may be used directly even without summarizer. [Auto-summarization](https://soloterm.com/docs/agents/auto-summarization)

Native summarizer defaults:

- Claude `sonnet`
- Codex `gpt-5-codex`
- Gemini `flash-lite`
- Copilot `auto`

Claude/Codex/Gemini/Copilot summarize natively. Amp/OpenCode/Kimi require custom tool plus headless command. Claude summaries disable session persistence; Codex summaries are ephemeral. Test passes only on exact `solo okay`. Summaries aid triage, not evidence. [Auto-summarization](https://soloterm.com/docs/agents/auto-summarization)

## Agent orchestration workflows

Solo's recommended lead-agent workflow:

1. Start with one lead agent and interview for goal, constraints, files, risks, verification, non-goals.
2. Write durable scratchpad plan: project/branch/worktree, context, lanes, dependencies, verification.
3. Convert plan into todos with ownership, acceptance checks, priority/tags, and blocker graph.
4. Spawn only independent, unblocked, bounded worker lanes through Solo MCP.
5. Give each worker explicit ownership, exclusions, context, and handoff requirements.
6. Monitor real process state/output; update todos/comments/scratchpad.
7. Set delay or idle timers for any/all worker completion.
8. Integrate one lane at a time; inspect actual diff/output and run focused checks.
9. Capture changed files/tests/blockers/risk in durable records before closing worker.
10. Close finished workers; closing never undoes filesystem changes.

Guiding principle: maximize useful independent work, not agent count. Keep dependent/small/same-file work with lead to avoid coordination overhead. [Orchestration workflow](https://soloterm.com/docs/workflows/agent-orchestration)

Cross-lab spawn is supported: Claude can spawn Codex, Codex can spawn Gemini/Amp/OpenCode/Claude/custom, provided target tool is enabled and launchable in effective environment and caller has MCP. Child does not inherit parent judgment; each needs self-contained prompt. [Agents spawning agents](https://soloterm.com/docs/workflows/agents-spawning-agents)

Daily operating pattern: order/collapse sections for workflow, scan project aggregate signals then section counts then process rows, use quick/focus jump instead of scrolling, treat unread as inbox, inspect anomalies in Activity monitor, use timers for intentional checkpoints, and end day by stopping unnecessary commands/checking subprocesses/clearing stale unread/collapsing inactive projects. [Daily patterns](https://soloterm.com/docs/workflows/daily-operating-patterns)

## Activity monitor and resource visibility

Activity monitor opens from command palette or terminal subprocess modal. It is app-level and returns to prior selection when closed. Fields: project, managed process/subprocess, CPU, memory, command, bound ports, PID, type, kill, and parent in flat view. Managed names navigate to terminal; subprocess rows do not. [Activity monitor](https://soloterm.com/docs/activity/activity-monitor)

Tree and flat views; filters by project/type/status/has-port; sorts by project/name/CPU/memory/command/ports/PID/type/parent. Default: running activity, tree mode, highest CPU first. Managed Kill follows normal stop; subprocess Kill targets OS PID. CPU is per-core and may exceed 100%. [Activity monitor](https://soloterm.com/docs/activity/activity-monitor)

Sidebar stats defaults:

- Project CPU threshold: 25%.
- Project memory: 1 GB.
- Process CPU: 30%.
- Process memory: 500 MB.
- Subprocess badge: 2+.

Always shows dash when missing; Never hides. Project aggregate includes all running processes even if filtered out. Port badge shows first plus `+N`; hover URL/quick action opens default browser. Sampling may lag spikes. [Sidebar resources](https://soloterm.com/docs/sidebar/cpu-memory-stats)

## Scratchpads

Project-scoped Markdown notes with editable title/content/tags and active/archive state. Open from sidebar/palette; create blank, import Markdown, or create from terminal selection. Editor autosaves and uses revision number for conflict detection. Headings build outline rail. [Scratchpads](https://soloterm.com/docs/scratchpads/using-scratchpads)

List supports search, active/archive filter, tag filter, and updated/name sorting. `Cmd/Ctrl+F` in note performs live wraparound match navigation; on list it focuses list search. Actions: deep link, copy Markdown, save file, duplicate, move project, archive. Archive hides without deleting. Import uses leading H1 as title else filename; export writes leading H1. [Scratchpads](https://soloterm.com/docs/scratchpads/using-scratchpads)

Images render inline. Remote images are fetched by Solo, verified by content type/bytes, limited 10 MB, timeout 15 sec, cached once per URL per app session. Supported detected formats PNG/JPEG/GIF/WebP/AVIF/BMP. Fail/loading shows alt/URL placeholder. [Scratchpads](https://soloterm.com/docs/scratchpads/using-scratchpads)

MCP scratchpad toggle augments main server. Agents can list/read/write/rename/tag/append/clear/delete/archive/transfer/load/save. Revision guards prevent stale replacement. Reads can target full/content/headings/section; project-relative file paths cannot escape project. [Scratchpad tools](https://soloterm.com/docs/scratchpads/agent-tools)

## Todos

Project-scoped fields:

- Title and Markdown notes.
- Status: Open, In progress, Backlog, Completed.
- Priority: High, Medium, Low.
- Tags.
- Same-project blockers/blocking relationships.
- Comments/activity.

List filters search/blocker/status/priority/tag; groups priority/status/availability/tag/flat; sorts priority/title/created/updated/completed. Multi-select bulk status/tags. **Blocked by** marks prerequisites; availability separates ready/blocked. [Todos](https://soloterm.com/docs/todos/using-todos)

Agent todo locks show up to three clickable pills atop process terminal plus `+N more`; updates live and release automatically when process closes. Moving todo preserves comments/completion but clears project-scoped blockers and locks. Comments submit Enter; Shift+Enter newline. [Todos](https://soloterm.com/docs/todos/using-todos)

MCP todo toggle augments main server. Agents create/list/read/update/tag/complete/transfer/lock/unlock/delete/comment and manage blockers/tags. UI and MCP share records. Locks are advisory coordination, not permanent ownership. [Todo tools](https://soloterm.com/docs/todos/agent-tools)

Recommended memory split: scratchpads hold durable background/decisions/source notes; todos hold actionable work/status/owner/acceptance/blockers; comments hold compact progress/handoff. Reconcile all before dispatch and completion. [Agent memory workflow](https://soloterm.com/docs/workflows/scratchpads-and-todos)

## Prompt templates

Reusable prompt body plus name, optional description, and `{{placeholder}}`; either Global (all projects) or Project scope. Project templates are deleted when project is removed unless automation API chooses conversion policy. Library groups Projects/Global, supports all-word search across name/description/body/scope, filters scopes, and sorts Last used (default), Recently updated, Name, Recently created. [Templates overview](https://soloterm.com/docs/prompt-templates/overview)

Create makes **Untitled template**, numbered on collision. Editor does **not** autosave. Names required, no `/` or control chars, case-insensitive unique within scope. Duplicate uses `name copy`, `copy 2`; delete is permanent after confirmation. Scope changes on save and fail on destination-name collision. [Create/edit](https://soloterm.com/docs/prompt-templates/creating-and-editing)

Placeholder rules:

- Letters/digits/underscores; first letter or underscore.
- Inner spaces accepted.
- Case-insensitive and normalized lowercase.
- Invalid syntax stays literal.
- Repeated placeholder filled once and substituted everywhere.
- Empty values become empty string.

[Placeholders](https://soloterm.com/docs/prompt-templates/placeholders)

Picker `Cmd/Ctrl+Shift+P` shows current project + global, sorted last-used. Enter inserts; Shift+Enter inserts/submits; Cmd+C macOS / Ctrl+Shift+C Windows copies; Escape closes. Text targets most recently focused running agent/terminal. If no target, copies with notice. Fill wizard supports Enter/Shift+Enter, Tab/Shift+Tab, copy partial with unfilled placeholders intact, Backspace-on-empty/Escape back. [Using templates](https://soloterm.com/docs/prompt-templates/using-templates)

MCP tools optionally list/read/create/update/delete/export. Markdown export includes YAML frontmatter and raw body; slugified filename never overwrites, adding numeric suffix. Unix line endings. [Create/edit](https://soloterm.com/docs/prompt-templates/creating-and-editing)

## Notifications and attention

Routing is focus-aware:

- Solo background: native desktop notification if permitted.
- Solo foreground: in-app toast.
- Same process already viewed: terminal BEL/OSC alert suppressed entirely.
- Server announcements remain persistent in-app.

[Toasts](https://soloterm.com/docs/notifications/in-app-toasts) · [Permissions](https://soloterm.com/docs/notifications/macos-permissions)

Toasts auto-dismiss for lightweight feedback or persist for crashes, YAML changes, restart exhaustion, announcements. Hover pauses then restarts full countdown; click linked alert navigates process. Newest stacks first. [Toasts](https://soloterm.com/docs/notifications/in-app-toasts)

Levels combine project/process by more restrictive:

- **All:** terminal BEL/OSC plus important crashes/restart exhaustion.
- **Important:** important only; terminal events suppressed.
- **None:** suppress all those categories.

Ordinary output alone does not create unread. Unread clears by selecting process, dismissing linked toast, row dismiss, or title-bar Clear all. Project dot remains until each child unread handled. App/workspace badge caps `99+`; app badge clears when Solo regains focus. [Indicators](https://soloterm.com/docs/notifications/indicators)

Bell default **Ping**. macOS lists system plus `~/Library/Sounds`; **None** mutes. Windows uses standard notification sound. Bell follows effective level and suppression. [Bell](https://soloterm.com/docs/notifications/bell-sounds)

Script signals: OSC 9 message, OSC 777 title/body, Kitty OSC 99 one-shot/multipart/base64, or BEL. Terminal notification rate limit: 5 per 10 seconds per process reader. Auto-restart only alerts on exhaustion, not each retry. [Script notifications](https://soloterm.com/docs/notifications/triggering-from-scripts) · [Troubleshooting notifications](https://soloterm.com/docs/troubleshooting/notifications)

## Keyboard reference

Important configurable defaults:

| Shortcut | Action |
|---|---|
| `Cmd/Ctrl+K`, `P`, `E`, `Shift+E` | Command center, context, jump, attention/favorites |
| `Cmd/Ctrl+Shift+P` | Prompt templates |
| `Cmd/Ctrl+T` | New item |
| `Cmd/Ctrl+W` | Close selected agent/terminal |
| `Cmd/Ctrl+Shift+W` | Complete todo/archive scratchpad then navigate back |
| `Cmd/Ctrl+O`, `,`, `Shift+U`, `Shift+L` | Add project, Settings, update check, workspace launcher |
| `Cmd/Ctrl+F` | Context search |
| `Cmd/Ctrl+Left/Right` | Sidebar/terminal focus |
| `Cmd/Ctrl+[/]` | Back/forward history |
| `Option/Alt+1–9` | Visible project 1–9 |
| `Cmd/Ctrl+1–9` | Visible command/agent/terminal 1–9 in active project |
| `Alt+A/C/T` | Agents/Commands/Terminals section |
| `Cmd/Ctrl+Up/Down` | Previous/next running item |
| `Cmd/Ctrl+Shift+Up/Down` | Previous/next visible item from anywhere |
| `Cmd/Ctrl+=/-` | Terminal font size |
| `Cmd/Ctrl+Shift+=/-` | App font size |

Sidebar-focused fixed navigation: arrows; Left collapse/up; Right expand/in; Alt+Left parent project; Alt+Up/Down section headers; Enter primary action. Project row single keys: `S` start auto-start, `A` start all, `P` stop all, `R` restart running. Process row: `S` start/stop, `R` restart, `C` clear. [Default shortcuts](https://soloterm.com/docs/keyboard-shortcuts/default-reference) · [Sidebar keyboard](https://soloterm.com/docs/keyboard-shortcuts/sidebar-navigation)

Fixed/unremappable: native copy/paste, hide/minimize, quit, basic sidebar arrows. Hotkey recording saves first valid non-modifier combination, warns conflicts, supports disable and per-row/all reset. Dispatch precedence: always > global > sidebar-process > sidebar-project > sidebar > terminal. Customizations are device-local. [Customizing](https://soloterm.com/docs/keyboard-shortcuts/customizing)

Numbered process selection excludes collapsed/filtered items, nested children, todos, scratchpads, section/add rows. Filters/reorder change numbering. Workspace 1–9, Clear terminal, Reset terminal font, next/previous project group ship unbound. [Switching](https://soloterm.com/docs/keyboard-shortcuts/switching-projects-commands) · [Default shortcuts](https://soloterm.com/docs/keyboard-shortcuts/default-reference)

## Appearance and settings

### App theme and interface scale

Shipped user-facing theme modes are **Light**, **Dark**, **System**; System follows OS. No named VS Code theme picker or importer exists, despite internal compatibility palettes and marketing copy. No supported file-drop/CLI importer. [Themes](https://soloterm.com/docs/appearance/themes) · [Bundled palettes](https://soloterm.com/docs/appearance/bundled-vscode-themes) · [Theme import caveat](https://soloterm.com/docs/appearance/importing-vscode-themes)

Interface font default is System default. Scale steps 77%, 85%, 92%, 100%, 108%, 115%, 123%, 131%, 138%, based on 14 px root. Personal/local, separate from terminal. [Interface font](https://soloterm.com/docs/appearance/font-scale)

### Settings tabs and save behavior

Tabs: Appearance, Terminal, Notifications, Sidebar, Workspaces, Notes & todos, Hotkeys, Agents, Tools, MCP, Account. Most save immediately; explicit Save used for some model/port fields. HTTP API port can change only while disabled and applies next start. Escape closes. All settings are local device state, not `solo.yml`. [Settings](https://soloterm.com/docs/settings/overview)

Sidebar defaults/caveats:

- Filter shown on.
- Open editor quick action off.
- Open terminal quick action off.
- Reveal in Finder on.
- Settings footer on.
- Empty sections shown unless legacy/per-section saved value differs.

[Sidebar settings](https://soloterm.com/docs/settings/sidebar-settings)

### External tools

Editor entries support Application, Command, Terminal modes; `$PROJECT_DIR` substituted or appended. Per-project override available. Terminal-mode editor requires configured terminal. Terminal entries support Application/Command and append project path. Browser defaults System default plus detected browsers. Test runs editor against home directory. No editor/terminal means quick-open errors—no system fallback. Built-in terminal entries cannot be deleted. [Tools](https://soloterm.com/docs/settings/tools-editors-terminals)

## Environment and shells

Execution profile controls shell and, on Windows, host vs WSL. macOS/Linux detect System default, Zsh, Bash, Fish, sh. Windows detects System/Command Prompt, PowerShell 7, Windows PowerShell, Git Bash, WSL default and each distro. Global default in Terminal settings; per-project Inherited/Auto/Manual override. WSL path projects auto-select distro. Unavailable profile is retained and badged rather than silently replaced. [Execution profiles](https://soloterm.com/docs/environment/execution-profiles)

Windows project assigned WSL profile needs Linux root mapping, default suggested `/mnt/<drive>/...`, with custom native-WSL clone path allowed. v0.9.3 added per-project/distro mappings. Custom shells accept name + command/args but cannot target WSL. Built-ins hide, not delete. [Execution profiles](https://soloterm.com/docs/environment/execution-profiles) · [Changelog](https://soloterm.com/changelog)

Unix shell environment resolution: `SHELL`, passwd entry, `/bin/sh`; runs `-ilc env`, caches 10 minutes. Capture failure falls back to app environment and macOS Homebrew prefix paths. Windows normalizes `HOME` from `USERPROFILE`, `SHELL` from `COMSPEC`; WSL uses distro config. Injected variables: `SOLO_PROCESS_ID` (not OS PID), `SOLO_PROJECT_ID`, `SOLO_PROCESS_KIND`. Refresh through command palette, then restart affected process. [Shell environment](https://soloterm.com/docs/environment/shell-environment)

Version managers work when interactive login shell exports paths. `asdf`, `mise`, `pyenv`, Ruby managers, Homebrew, and virtualenvs generally work; `nvm` as shell-only function may not. [Version managers](https://soloterm.com/docs/environment/version-managers)

## Integrations and automation

### MCP server

Settings → MCP enables bundled local stdio helper; no public host/port. Setup snippets for detected Claude Code, Codex, Gemini, Amp, OpenCode, Copilot, Kimi and Cursor, Windsurf, Cline, Claude Desktop. Supported CLI clients can use Run. Enabling server alone does not configure every agent client; v0.9.3 added connection counts, one-click Connect Solo, per-environment setup/repair. [MCP integration](https://soloterm.com/docs/integrations/mcp-server) · [Changelog](https://soloterm.com/changelog)

Core MCP groups: project/workspace/status/stats, services/ports, process lifecycle/input, bulk commands, rendered/raw output/search/clear, agent/terminal spawn and session identity, coordination locks, help/catalog/smoke-test/feedback/setup. Optional groups:

- Scratchpads, todos, timers inherit server enablement until explicitly saved.
- Key-value and prompt-template tools default off.
- Optional groups augment same server.

Helper reconnects across app restart with backoff, bounded request buffering, and per-process identity/session persistence for Solo-launched agents. Other clients remain stable for helper lifetime but not helper restart. [MCP integration](https://soloterm.com/docs/integrations/mcp-server)

### HTTP API

Local only `127.0.0.1`, bearer token fresh each start, default port 24678. Busy port falls back random; consumers must read `http-api.json`. Default path macOS/Linux `~/.config/soloterm/http-api.json`, Windows `%USERPROFILE%\.config\soloterm\http-api.json`; custom `SOLOTERM_APP_DATA_DIR` overrides. File mode 0600 on Unix, removed on API off/quit. All endpoints including version require token. [HTTP API](https://soloterm.com/docs/integrations/http-api)

API covers version/status/discovery, projects, workspaces, processes/output/spawn/lifecycle/bulk, todos, scratchpads, comments/blockers/locks, and related cataloged capabilities. Stable envelope has `ok`, `requestId`, `data` or structured `error.code/details`; bodies max 2 MB; default page 50/max 500; workspace list unpaged. Human labels cap 200, scratchpad names 120, todo body/comments 64 KB, tags max 32 × 48 chars. Browser origins loopback only. [HTTP API](https://soloterm.com/docs/integrations/http-api)

### CLI

Bundled `solo` CLI symlinked into `~/.local/bin`; symlink follows app updates. Requires running app + HTTP API except help, `--version`, local routine bundling. Discovery/token automatic; custom data dir flag/env supported. Diagnostics: `solo version` (running app), `solo status`, `solo doctor`; `solo --version` is local binary. [CLI overview](https://soloterm.com/docs/cli/overview)

Groups: `projects`, `processes`, `commands`, `agents`, `todos`, `scratchpads`, `routine`. Process output defaults last 50 rendered lines, supports `--raw` and lines. Spawning supports terminal or agent with tool ID and repeated args. Bulk command aliases report started/skipped/errors. Todos support status/block/priority/query/tag/sort; create priority defaults medium. Scratchpad update/append/rename/delete require expected revision. [Projects/process CLI](https://soloterm.com/docs/cli/projects-and-processes) · [Todo/scratchpad CLI](https://soloterm.com/docs/cli/todos-and-scratchpads)

Every command accepts stable one-line `--json`; success stdout, error stderr. Exit codes: 0 success, 64 usage, 65 app rejection, 66 input file, 69 app unavailable, 70 protocol/internal, 74 stdin I/O, 77 permission/token/discovery, 78 config/version mismatch. [CLI JSON](https://soloterm.com/docs/cli/json-output-and-scripting)

### Deep links

Formats:

- `solo://proj/{projectId}`
- `solo://proj/{projectId}/process/{slug}--{id}`
- `solo://proj/{projectId}/scratchpad/{slug}--{id}`
- `solo://proj/{projectId}/todo/{slug}--{id}`

Slug is readable only, lowercased/dashed/truncated 20; numeric ID resolves, so rename-safe. Links launch/focus app, switch workspace, and navigate. Stale/malformed links are silently ignored. Copy from context/views/palette; terminal and scratchpad rendered links open in-app. [Deep links](https://soloterm.com/docs/integrations/deep-links)

## Account, licensing, pricing, and privacy

### Free and Pro

Free never expires and includes all features/updates, 4 projects, 20 total managed processes. At limit, add opens license prompt; unlicensed over-limit blocks starts. Deactivation while over-limit returns to Free and stops managed processes. [Free tier](https://soloterm.com/docs/account/free-tier)

Public pricing observed:

- Free: $0 forever, 4 projects, 20 processes.
- Pro: $99/year, unlimited projects/processes, priority email support, 3 devices, future updates; 30-day money-back guarantee.
- Team bracket pricing: seats 1–3 $99/seat/year; 4–10 $89; 11–50 $79; 51+ $69, bracketed per seat. [Product](https://soloterm.com/)

Activation sends key, Solo version, device ID/name, platform, OS version; stores signed token. Offline grace 14 days after check-in. Background validation occurs on connected launches. Expired license can continue within Free limits. [Activation](https://soloterm.com/docs/account/activating-license) · [License errors](https://soloterm.com/docs/account/license-errors)

License moves: deactivate old, activate new. Local deactivation still happens if server request fails; projects/settings do not move. Public product says up to three machines per Pro license. [Moving license](https://soloterm.com/docs/account/moving-license) · [Product](https://soloterm.com/)

### Team licensing

Central billing plus first-come claim link, not full seat management. Raw link shown once because only hash stored; regeneration invalidates previous. Claimed normal Pro license stays through paid term. Auto-grow is optional/off default, bills prorated immediately up to limit; anyone with link can cause billed growth. Revoke invalidates immediately and frees seat; member can reclaim. v1 lacks domain gating, SSO, assigned-seat UI, directory sync. [Team licenses](https://soloterm.com/docs/account/team-licenses)

### Privacy

Product states Aptabase privacy-first basic usage analytics; never sends project/process names or code. License validation communicates with Solo server. Agent provider keys/accounts remain local to their CLI tools. [Product](https://soloterm.com/)

## Updates, quitting, recovery, and support

Built-in updater checks background and via app menu, Account, title badge. Signed update downloads/stages; no immediate restart required; title becomes **Relaunch** and update applies next launch. Requests include current version, platform, device ID, active license key. [Installing updates](https://soloterm.com/docs/updates/installing-updates)

Restart/quit with running processes lists up to six names and confirms; all commands/agents/terminals stop. No running process means immediate quit. Relaunch reloads projects and eligible trusted auto-start commands. [Safe restart](https://soloterm.com/docs/updates/restarting-safely)

Troubleshooting order:

- PATH: command palette **Refresh shell environment**, then restart process; compare `which`/`PATH`; full binary path last resort. [PATH](https://soloterm.com/docs/troubleshooting/path-issues)
- Notifications: permission, OS settings, Focus/DND, test button, focus routing, levels, rate limits. [Notifications](https://soloterm.com/docs/troubleshooting/notifications)
- Feedback: command palette **Send feedback** with version, OS, command/tool, reproduction, screenshots and relevant YAML. [Reporting](https://soloterm.com/docs/troubleshooting/reporting-issues)
- Hotkey reset is in Settings. Core DB is `~/.config/soloterm/solo.db` unless custom app-data dir. Window placement uses `.window-state.json`/`.display-snapshot.json`. Visual preferences also live in browser storage `solo-ui-storage`, so deleting DB alone is not full visual reset. No built-in full/window reset command exists. [Resetting](https://soloterm.com/docs/troubleshooting/resetting-settings)

## Changelog synthesis

Current [changelog](https://soloterm.com/changelog) spans v0.1.4 (2026-02-03) through v0.9.3 (2026-06-21). Major user-facing milestones:

- **v0.9.3, 2026-06-21:** Connect Solo per agent/environment, Runtime Doctor, MCP connection counts/repair, WSL root mapping, process favorites/navigation, MCP reconnect/buffering, terminal/WSL/process-tree safety fixes.
- **v0.8.2, 2026-06-05:** full prompt templates, execution profiles and Windows/WSL environment-specific agents, agent session resume, linked-checkout sharing, expanded scratchpad/todo search/edit, broader HTTP/CLI/MCP, terminal reliability.
- **v0.7.1, 2026-05-14:** Copilot/Kimi first-class, major local API/CLI, expanded MCP project/scratchpad/spawn tools, editable/drag-added projects, favicon icons, terminal-selection-to-scratchpad, input/performance improvements.
- **v0.6.x, 2026-04-20 through 2026-05-01:** rapid feature/fix line leading into richer agents, MCP, project, terminal, and workspace workflows.
- **v0.5.x and earlier, 2026-02 through 2026-03:** foundational app lifecycle, terminal/process/project behavior.

Release notes are unusually detailed and should be checked when behavior differs from static docs, especially Windows/WSL, terminal rendering, MCP continuity, and agent connection health.

## Documentation/product conflicts and caveats

1. **Named themes:** product site claims twelve bundled VS Code themes; current docs explicitly say packaged UI exposes only Light/Dark/System and no named picker/importer. Treat named palettes as internal compatibility data, not selectable feature. [Product](https://soloterm.com/) · [Bundled palettes](https://soloterm.com/docs/appearance/bundled-vscode-themes) · [Importer](https://soloterm.com/docs/appearance/importing-vscode-themes)
2. **Agent list:** product page markets Aider/Goose among agents; built-in Settings tool types documented are Claude/Codex/Amp/Gemini/OpenCode/Copilot/Kimi. Aider/Goose should work through custom terminal agent tooling, not necessarily built-in rows. [Agents product](https://soloterm.com/agents) · [Agent setup](https://soloterm.com/docs/agents/setting-up-tools)
3. **Platforms:** older/general snippets may say Mac only; current download/docs show macOS and Windows available, Linux coming soon. [Download](https://soloterm.com/download) · [Installation](https://soloterm.com/docs/getting-started/installation)
4. **Universal agent GUI:** docs repeatedly qualify it with “if your version includes” / “when available.” Do not assume universal GUI agent exists in every build/license/platform. [Agent concepts](https://soloterm.com/docs/agents/what-are-agents) · [Launching](https://soloterm.com/docs/agents/launching-agents)
5. **Auto-start default nuance:** YAML `auto_start` omitted defaults true, but commands do not necessarily run immediately after setup; project Auto Start, trust, lifecycle entry point, and limits still gate launch. [solo.yml](https://soloterm.com/docs/projects/solo-yml) · [Auto-start](https://soloterm.com/docs/commands/auto-start)
6. **Agent counts:** product says launch as many as wanted; free tier's 20-process total remains a hard unlicensed constraint. [Launching](https://soloterm.com/docs/agents/launching-agents) · [Free tier](https://soloterm.com/docs/account/free-tier)
7. **Output persistence:** project/process definitions persist, agent conversation resume may persist, but terminal runtime output is not archival across restarts. [Terminal persistence](https://soloterm.com/docs/terminal/persistent-sessions)
8. **MCP enabled vs connected:** server toggle does not configure installed agent CLIs automatically. v0.9.3 UI makes connection count explicit. [MCP](https://soloterm.com/docs/integrations/mcp-server) · [Changelog](https://soloterm.com/changelog)
9. **Health unknown:** Not checked is launchable; Missing/Broken are not. A timeout deliberately remains inconclusive instead of blocking launch. [Installation health](https://soloterm.com/docs/agents/installation-health)
10. **Closing semantics:** normal app quit cleanly stops all; crash can create orphans that Solo may adopt or offer to kill. Marketing “no orphans” describes normal shutdown, not every failure path. [Product](https://soloterm.com/) · [Orphans](https://soloterm.com/docs/commands/orphaned-processes)

## Exact default/cap matrix

| Area | Default / exact limit | Source |
|---|---|---|
| Free tier | 4 projects, 20 processes | [Free tier](https://soloterm.com/docs/account/free-tier) |
| Offline license | 14 days | [License errors](https://soloterm.com/docs/account/license-errors) |
| HTTP API | 127.0.0.1, port 24678, random fallback | [HTTP API](https://soloterm.com/docs/integrations/http-api) |
| HTTP bodies/pages | 2 MB; page 50 default/500 max | [HTTP API](https://soloterm.com/docs/integrations/http-api) |
| YAML | 1 MB max; auto_start true; auto_restart false | [solo.yml](https://soloterm.com/docs/projects/solo-yml) |
| Crash restart | pause after 10/60 sec | [Auto-restart](https://soloterm.com/docs/commands/auto-restart) |
| Terminal notification | 5/10 sec/process reader | [Notification troubleshooting](https://soloterm.com/docs/troubleshooting/notifications) |
| Scrollback | 10,000 main-buffer lines/current run | [Terminal basics](https://soloterm.com/docs/terminal/basics) |
| Bell | Ping | [Bell sounds](https://soloterm.com/docs/notifications/bell-sounds) |
| Terminal font | Geist Mono 300/700, 13 px base | [Terminal fonts](https://soloterm.com/docs/appearance/font-settings) |
| Copy on select | Off | [Terminal fonts](https://soloterm.com/docs/appearance/font-settings) |
| Focus borders | Top and bottom on | [Terminal fonts](https://soloterm.com/docs/appearance/font-settings) |
| macOS Option Meta | Both keys on | [Keyboard input](https://soloterm.com/docs/terminal/keyboard-input) |
| Interface font/scale | System default / 100% | [Interface font](https://soloterm.com/docs/appearance/font-scale) |
| Theme | Light/Dark/System; no named picker documented | [Themes](https://soloterm.com/docs/appearance/themes) |
| Sidebar filter/footer | On / on | [Sidebar settings](https://soloterm.com/docs/settings/sidebar-settings) |
| Project quick actions | Editor off, terminal off, Finder on | [Sidebar settings](https://soloterm.com/docs/settings/sidebar-settings) |
| Section order | Todos, Agents, Terminals, Commands, Scratchpads | [Sections](https://soloterm.com/docs/sidebar/understanding-sections) |
| Resource thresholds | Project 25%/1GB; process 30%/500MB; subprocess 2+ | [Sidebar resources](https://soloterm.com/docs/sidebar/cpu-memory-stats) |
| Activity monitor | Running tree, CPU descending | [Activity monitor](https://soloterm.com/docs/activity/activity-monitor) |
| Auto-summary cadence | 15 sec / 30 sec / 1 min choices; disabled until tool selected | [Auto-summarization](https://soloterm.com/docs/agents/auto-summarization) |
| Team auto-grow | Off | [Team licenses](https://soloterm.com/docs/account/team-licenses) |
| CLI process output | 50 rendered lines | [CLI projects/processes](https://soloterm.com/docs/cli/projects-and-processes) |
| Todo CLI priority | Medium | [CLI todos/scratchpads](https://soloterm.com/docs/cli/todos-and-scratchpads) |

## Primary sources

- [Solo product site](https://soloterm.com/)
- [Solo agent workspace](https://soloterm.com/agents)
- [Solo download](https://soloterm.com/download)
- [Solo changelog](https://soloterm.com/changelog)
- [Solo docs index](https://soloterm.com/docs)
- [Getting started](https://soloterm.com/docs/getting-started)
- [Projects](https://soloterm.com/docs/projects)
- [Workspaces](https://soloterm.com/docs/workspaces)
- [Commands](https://soloterm.com/docs/commands)
- [Terminal](https://soloterm.com/docs/terminal)
- [Agents](https://soloterm.com/docs/agents)
- [Workflows](https://soloterm.com/docs/workflows)
- [Todos](https://soloterm.com/docs/todos)
- [Scratchpads](https://soloterm.com/docs/scratchpads)
- [Prompt templates](https://soloterm.com/docs/prompt-templates)
- [Sidebar](https://soloterm.com/docs/sidebar)
- [Activity](https://soloterm.com/docs/activity)
- [Keyboard shortcuts](https://soloterm.com/docs/keyboard-shortcuts)
- [Command palette](https://soloterm.com/docs/command-palette)
- [Notifications](https://soloterm.com/docs/notifications)
- [Appearance](https://soloterm.com/docs/appearance)
- [Settings](https://soloterm.com/docs/settings)
- [Environment](https://soloterm.com/docs/environment)
- [Integrations](https://soloterm.com/docs/integrations)
- [CLI](https://soloterm.com/docs/cli)
- [Account](https://soloterm.com/docs/account)
- [Updates](https://soloterm.com/docs/updates)
- [Troubleshooting](https://soloterm.com/docs/troubleshooting)
