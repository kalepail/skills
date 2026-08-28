# Workspaces, windows, sidebar, and navigation

Use this reference for workspace organization, multi-window layout, sidebar density, favorites, activity signals, palettes, and keymaps. Verify labels and feature availability in live Solo before acting.

## Workspaces and windows

- Every install begins with one **Default Workspace**. Workspace rail appears only after second workspace exists.
- Each project belongs to exactly one workspace. Switching workspaces changes visible sidebar but does not stop background processes.
- Rail top group contains workspaces open in current window; dimmed bottom group contains other workspaces. Unread badge caps at `99+`.
- Workspace launcher opens with `Cmd/Ctrl+Shift+L`; it searches workspace names, project names, and paths, opens/focuses owning window, and supports dragging projects between workspaces.
- **Switch to workspace 1–9** actions exist but ship unbound. Workspace order determines their targets.
- Workspace identity supports up to two initials, eight colors (slate, blue, green, red, purple, cyan, orange, pink) or neutral, and PNG/JPG/JPEG/GIF/ICO/WebP custom image copied into app data.
- Deleting only workspace is blocked. Deleting populated workspace requires destination; projects move and disk files remain.
- Moving project between workspaces does not stop its processes.
- A workspace can be open in only one Solo window. Moving last workspace out closes secondary window; main window hides instead.

Sources: [overview](https://soloterm.com/docs/workspaces/overview), [management](https://soloterm.com/docs/workspaces/managing-workspaces), [multiple windows](https://soloterm.com/docs/workspaces/multi-window).

## Sidebar structure and density

- Default section order: **Todos → Agents → Terminals → Commands → Scratchpads**.
- Section order persists locally per project; Sidebar settings can change preferred default across projects.
- Empty sections show by default unless per-section hide-empty controls say otherwise. Todos/Scratchpads can be disabled from **Settings → Notes & todos**.
- Clicking section label selects it; clicking chevron collapses it. No collapse-all/expand-all command exists.
- `\` focuses sidebar filter when sidebar is focused. Filtering is case-insensitive across projects and matches commands, agents, terminals, active todos, and unarchived scratchpads.
- Filtering disables drag reordering. Turning **Show filter input** off clears active filter and disables `\`.
- Project/process quick-action defaults: Open in editor off, Open in terminal off, Reveal in Finder on, Settings footer on.

Sources: [sections](https://soloterm.com/docs/sidebar/understanding-sections), [reordering](https://soloterm.com/docs/sidebar/reordering-sections), [collapse](https://soloterm.com/docs/sidebar/collapsing-expanding), [filter](https://soloterm.com/docs/sidebar/filtering), [sidebar settings](https://soloterm.com/docs/settings/sidebar-settings).

## Favorites and resource signals

- Commands, terminals, and agents can be favorites; todos and scratchpads cannot.
- `Cmd/Ctrl+Shift+[` and `]` cycle favorites across current workspace. If any favorite runs, cycling visits running favorites only.
- Focus jump ranks unread favorites, other unread processes, running favorites, remaining favorites.
- Resource-display defaults: project CPU 25%, project memory 1 GB, process CPU 30%, process memory 500 MB, subprocess badge 2+.
- CPU is per core and can exceed 100%. Project aggregates include filtered-out running rows. Sampling can lag spikes.
- Port row shows first port plus `+N`; hover offers open in configured browser.
- Activity monitor default is running processes in tree view, highest CPU first. It can filter/sort and kill managed processes or tracked subprocesses.

Sources: [favorites](https://soloterm.com/docs/sidebar/favorites), [resource stats](https://soloterm.com/docs/sidebar/cpu-memory-stats), [Activity monitor](https://soloterm.com/docs/activity/activity-monitor).

## Palette modes

| Shortcut | Mode | Purpose |
|---|---|---|
| `Cmd/Ctrl+K` | Command center | App and project actions |
| `Cmd/Ctrl+P` | Context actions | Current process/project actions |
| `Cmd/Ctrl+E` | Quick jump | Destinations across projects |
| `Cmd/Ctrl+Shift+E` | Focus jump | Unread or favorite processes |
| `Cmd/Ctrl+Shift+P` | Prompt templates | Insert/send/copy template |
| `Cmd/Ctrl+T` | New item | Create in active project |

- Scope a search with `project name > action`.
- With multiple workspaces, search defaults current workspace; press `Tab` for all.
- Copy/paste `solo://` deep links from Jump results.
- Palette shortcuts retarget open palette but modal/pane overlays block them.

Sources: [command palette](https://soloterm.com/docs/command-palette/using), [context actions](https://soloterm.com/docs/command-palette/context-actions), [new item](https://soloterm.com/docs/command-palette/new-tab-picker).

## Keyboard map and customization

- `Option/Alt+1–9`: visible projects by sidebar order.
- `Cmd/Ctrl+1–9`: visible command/agent/terminal in active project; excludes collapsed/filtered items, nested agents, todos, scratchpads, and headers.
- `Alt+A/C/T`: Agents/Commands/Terminals section.
- `Cmd/Ctrl+Left/Right`: sidebar/terminal focus.
- `Cmd/Ctrl+Up/Down`: previous/next running item.
- Sidebar arrows move/collapse/expand; Alt+Left reaches parent project; Alt+Up/Down reaches section headers.
- Fixed shortcuts include native copy/paste, hide/minimize, quit, and basic sidebar arrows.
- Custom routing precedence: always > global > sidebar-process > sidebar-project > sidebar > terminal.
- Clear terminal, Reset terminal font, workspace 1–9, and project-group navigation ship unbound.

Sources: [default reference](https://soloterm.com/docs/keyboard-shortcuts/default-reference), [customizing](https://soloterm.com/docs/keyboard-shortcuts/customizing), [switching](https://soloterm.com/docs/keyboard-shortcuts/switching-projects-commands), [sidebar keyboard](https://soloterm.com/docs/keyboard-shortcuts/sidebar-navigation).

## Live verification

Check live Settings, MCP discovery, and the current [changelog](https://soloterm.com/changelog) before asserting Windows/WSL execution-profile badges, favorite controls, workspace MCP coverage, or shortcut availability.
