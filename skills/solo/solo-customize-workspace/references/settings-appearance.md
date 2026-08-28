# Settings, appearance, and external tools

Use this reference for app-level preferences. Keep these local settings separate from project configuration and `solo.yml`.

## Settings map

Open Settings with `Cmd/Ctrl+,`, app menu, or command palette. Settings is an in-app panel; Escape closes it.

| Tab | Main controls |
|---|---|
| Appearance | Theme, interface font, interface scale |
| Terminal | Shell/profile, terminal font/weight/size, spacing, focus borders, copy-on-select, TUI scroll, macOS Option-as-Meta |
| Notifications | Permission, test, bell |
| Sidebar | Filter, order, decorations, empty visibility, focus, stats, header actions, footer |
| Workspaces | Names, icons, order, deletion |
| Notes & todos | Visibility, previews, MCP exposure |
| Hotkeys | Search, remap, disable, reset |
| Agents | Naming, tool settings, summary settings |
| Tools | Default editor, terminal, browser |
| MCP | Server, client setup, feature toggles, HTTP API |
| Account | License, feedback, updates, version, acknowledgements |

Most controls save immediately; some model/port fields require Save. HTTP API port changes only while API is off and applies on next start. Settings are per-device and not stored in `solo.yml`.

Source: [Settings overview](https://soloterm.com/docs/settings/overview).

## App appearance

- User-facing themes documented for packaged app: **Light**, **Dark**, **System**. System follows OS.
- Current docs explicitly say no named VS Code theme picker and no in-app/file-drop/CLI theme importer.
- Internal compatibility palettes include twelve named VS Code-style palettes, but docs do not expose them as selectable UI.
- Interface font default: **System default**.
- Interface scale steps: 77%, 85%, 92%, 100%, 108%, 115%, 123%, 131%, 138%; 14 px base.
- `Cmd/Ctrl+Shift+=/-` changes interface scale.

Sources: [themes](https://soloterm.com/docs/appearance/themes), [bundled palettes caveat](https://soloterm.com/docs/appearance/bundled-vscode-themes), [import caveat](https://soloterm.com/docs/appearance/importing-vscode-themes), [interface font/scale](https://soloterm.com/docs/appearance/font-scale).

## Terminal display

- Bundled fonts: JetBrains Mono, Geist Mono, MonoLisa, Input Mono.
- Default: Geist Mono, regular weight 300, bold 700.
- Terminal size 10–18 px on 13 px base; `Cmd/Ctrl+=/-` adjusts.
- Letter spacing labels 0.5–1.3, default 1.0.
- Line-height labels 1.0–1.8, default display 1.2.
- Top and bottom focus borders default on.
- Copy on select defaults off.
- Both macOS Option keys default to Meta and can be changed independently.
- TUI scroll multiplier ranges 1x–6x and does not affect normal scrollback.

Preserve terminal punctuation coverage warnings and renderer warnings. Keep terminal typography separate from app UI scale.

Sources: [terminal fonts](https://soloterm.com/docs/appearance/font-settings), [keyboard input](https://soloterm.com/docs/terminal/keyboard-input), [focus](https://soloterm.com/docs/terminal/focus-behavior).

## External editor, terminal, and browser

- Editor supports Application, Command, or Terminal mode plus per-project override.
- Command editor entries substitute `$PROJECT_DIR`; if missing, Solo appends project path.
- Terminal-mode editor requires configured default terminal.
- Terminal entries support Application or Command; command path is appended.
- Browser offers System default plus detected browsers and opens service URLs.
- Test custom editor/terminal entries before relying on them.
- If no editor or terminal is configured, quick-open fails; Solo does not silently fall back.
- Built-in terminal entries cannot be removed.

Source: [Tools](https://soloterm.com/docs/settings/tools-editors-terminals).

## Shell and execution-profile boundary

Changing default shell/execution profile is app customization, but changing project directory, command `working_dir`, or agent installation belongs to neighboring skills.

- macOS/Linux profiles are shell choices; Windows profiles also select host vs WSL.
- Per-project Manual override beats Auto or Inherited default.
- Unavailable profile is retained and warned rather than silently replaced.
- WSL profiles may require a project/distro root mapping.
- Refresh shell environment after PATH changes, then restart affected processes through process skill.

Sources: [execution profiles](https://soloterm.com/docs/environment/execution-profiles), [shell environment](https://soloterm.com/docs/environment/shell-environment), [version managers](https://soloterm.com/docs/environment/version-managers).

## Live verification

Check live Settings and the current [changelog](https://soloterm.com/changelog) before promising named themes, Universal Agent GUI, Windows/WSL controls, or exact defaults; offer only the themes and controls those surfaces expose.
