# Workspaces, windows, sidebar, and navigation

Use this reference for workspace organization, multi-window layout, sidebar density, favorites, activity signals, palettes, and keymaps. Verify labels and feature availability in live Solo before acting.

## Workspaces and windows

- Every install begins with one **Default Workspace**. Workspace rail appears only after second workspace exists.
- **Hide inactive workspaces** (rail menu or Settings → Workspaces) collapses other workspaces and their badges into a `+N` stack.
- Each project belongs to exactly one workspace. Switching workspaces changes visible sidebar but does not stop background processes.
- Rail top group contains workspaces open in current window; dimmed bottom group contains other workspaces. Unread badge caps at `99+`.
- Switch workspaces from the rail, the palette, a cycle shortcut for workspaces open in the current window, or numbered switch actions. Numbered actions follow configured workspace order. Read their current bindings in Settings before naming them.
- Move a project through its sidebar context menu or `move_project_to_workspace`. The menu can also create the destination workspace in the same step.
- Workspace identity supports initials, a color, or a small custom image. Read current limits and formats in the docs before choosing an image.
- Deleting only workspace is blocked. Deleting populated workspace requires destination; projects move and disk files remain.
- Moving project between workspaces does not stop its processes.
- A workspace can be open in only one Solo window. Moving last workspace out closes secondary window; main window hides instead.

Sources: [overview](https://soloterm.com/docs/workspaces/overview), [management](https://soloterm.com/docs/workspaces/managing-workspaces), [multiple windows](https://soloterm.com/docs/workspaces/multi-window).

## Sidebar structure and density

- Default section order: **Todos → Agents → Terminals → Commands → Scratchpads**.
- Section order persists locally per project; Sidebar settings can change preferred default across projects.
- Empty sections show by default unless per-section hide-empty controls say otherwise. Todos/Scratchpads can be disabled from **Settings → Notes & todos**.
- Clicking section label selects it; clicking chevron collapses it. No collapse-all/expand-all command exists.
- Sidebar filtering is case-insensitive across projects and matches commands, agents, terminals, active todos, and unarchived scratchpads.
- Filtering disables drag reordering. Hiding the filter input clears an active filter.
- Project and process quick actions can be toggled in Sidebar settings.

Sources: [sections](https://soloterm.com/docs/sidebar/understanding-sections), [reordering](https://soloterm.com/docs/sidebar/reordering-sections), [collapse](https://soloterm.com/docs/sidebar/collapsing-expanding), [filter](https://soloterm.com/docs/sidebar/filtering), [sidebar settings](https://soloterm.com/docs/settings/sidebar-settings).

## Favorites and resource signals

- Commands, terminals, and agents can be favorites; todos and scratchpads cannot.
- A favorites shortcut cycles favorites across the current workspace. If any favorite runs, cycling visits running favorites only.
- Focus jump ranks unread favorites, other unread processes, running favorites, remaining favorites.
- Resource badges appear above configurable CPU, memory, and subprocess thresholds. Read current values in Sidebar settings before tuning them.
- CPU is per core and can exceed 100%. Project aggregates include filtered-out running rows. Sampling can lag spikes.
- Port row shows first port plus `+N`; hover offers open in configured browser.
- Activity monitor default is running processes in tree view, highest CPU first. It can filter/sort and kill managed processes or tracked subprocesses.

Sources: [favorites](https://soloterm.com/docs/sidebar/favorites), [resource stats](https://soloterm.com/docs/sidebar/cpu-memory-stats), [Activity monitor](https://soloterm.com/docs/activity/activity-monitor).

## Palette modes

The palette has separate modes for destinations and actions together, actions only, current-context actions, go-to destinations, focus on unread or favorite processes, prompt templates, and creating new items. Each mode has its own shortcut. Read current mode names and bindings in Settings → Hotkeys or the command-palette docs.

- Scope a search with `project name > action`.
- With multiple workspaces, search defaults to the current workspace and can widen to all workspaces.
- Copy/paste `solo://` deep links from **Go to** results.
- **Refresh frontend** reloads the interface without stopping processes.
- Palette shortcuts retarget open palette but modal/pane overlays block them.

Sources: [command palette](https://soloterm.com/docs/command-palette/using), [actions](https://soloterm.com/docs/command-palette/actions), [context actions](https://soloterm.com/docs/command-palette/context-actions), [new item](https://soloterm.com/docs/command-palette/new-tab-picker).

## Keyboard map and customization

Solo ships numbered shortcuts for visible projects and for visible processes in the active project, plus section, focus, and running-item navigation. Some actions ship unbound. Fixed shortcuts, such as native copy and paste and quit, cannot be remapped.

Read the current default map and binding precedence in Settings → Hotkeys or the keyboard-shortcut docs before naming or remapping a shortcut. A custom binding can shadow another context's binding, so check collisions across contexts.

Sources: [default reference](https://soloterm.com/docs/keyboard-shortcuts/default-reference), [customizing](https://soloterm.com/docs/keyboard-shortcuts/customizing), [switching](https://soloterm.com/docs/keyboard-shortcuts/switching-projects-commands), [sidebar keyboard](https://soloterm.com/docs/keyboard-shortcuts/sidebar-navigation).

## Live verification

Check live Settings, MCP discovery, and the current [changelog](https://soloterm.com/changelog) before asserting Windows/WSL execution-profile badges, favorite controls, workspace MCP coverage, or shortcut availability.
