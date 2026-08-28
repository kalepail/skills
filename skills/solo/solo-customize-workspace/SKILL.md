---
name: solo-customize-workspace
description: Customize Solo workspaces, windows, sidebar, navigation, command palette, keymaps, appearance, external tools, notifications, account display, and updates. Use when organizing or personalizing Solo's app-level workspace experience. Do not use for repository or solo.yml changes, process lifecycle, or agent work.
---

# Customize Solo Workspace

Configure Solo's application shell around existing projects and processes. Preserve running work, local preferences, and neighboring skill boundaries.

## Read relevant references

- Read [references/workspaces-navigation.md](references/workspaces-navigation.md) for workspaces, windows, sidebar, favorites, resource indicators, navigation, palettes, and keymaps.
- Read [references/settings-appearance.md](references/settings-appearance.md) for Settings tabs, appearance, terminal display, and external editor/terminal/browser choices.
- Read [references/notifications-account-updates.md](references/notifications-account-updates.md) for notifications, licensing, updates, quitting, and destructive cautions.
- Read only references needed for request. Use cited official URLs when behavior or labels may have changed.

## Keep scope bounded

- Handle workspace grouping, app windows, app navigation, UI preferences, notification policy, and account/update surfaces.
- Route project creation, directory changes, onboarding, command detection, and `solo.yml` work to `$solo-set-up-projects`.
- Route command creation, trust, start/stop/restart, auto-start, auto-restart, output, ports, and process cleanup to `$solo-run-processes` or `$solo-observe-services` as appropriate.
- Route agent-tool setup, health, launch, resume, and session interaction to `$solo-work-with-agents`.
- Route multi-agent plans, todos, scratchpads, locks, timers, and worker coordination to `$solo-orchestrate-agents`.
- Change only app/workspace preferences when request mixes domains; state which remaining work belongs elsewhere.

## Follow customization workflow

1. Identify desired outcome: organization, navigation speed, visual density, appearance, notification signal, or account/update check.
2. Inspect current state before changing it. Use Solo MCP read/list/help tools when available; otherwise guide user to exact live Settings or UI surface.
3. Check live MCP catalog, current Solo version, Settings labels, and relevant official docs before relying on version-sensitive behavior. Treat changelog as newer than stale screenshots or marketing copy.
4. Choose smallest reversible change. Prefer local settings over project mutations.
5. Preview consequences before moving projects, deleting workspaces, changing notification levels, deactivating a license, installing an update, or relaunching.
6. Apply only authorized changes. Never infer permission for billing, license deactivation, update installation, quit/relaunch, workspace deletion, or process termination.
7. Verify resulting workspace/window assignment, visible sidebar order, active shortcut, effective theme/font, or notification level. Report any UI-only step user must complete.

## Customize workspaces and windows

- Create workspace only when grouping improves current project set; one workspace is valid and hides rail.
- Move projects between workspaces without changing repository config. Confirm destination and current window ownership.
- Reorder workspaces when numbered bindings or rail order matter.
- Move workspace to new window for multi-monitor layout; remember one workspace can be open in only one window.
- Before deleting populated workspace, require destination for contained projects. Never imply disk files are deleted.
- Use workspace launcher for cross-workspace search and drag moves when direct MCP support is absent.

## Tune sidebar and navigation

- Reorder Todos, Agents, Terminals, Commands, and Scratchpads per project or change default subgroup order when request is global.
- Use collapse state, per-section empty visibility, filter input, favorites, and resource thresholds to reduce noise before hiding useful signals.
- Preserve unread and running visibility. Running lesser-used commands remain visible by design.
- Remap configurable hotkeys only after checking collisions and fixed shortcuts.
- Distinguish command center, context actions, quick jump, focus jump, prompt templates, and new-item palettes; do not overload one shortcut with another mode's job.

## Tune settings and appearance

- Keep interface and terminal typography separate.
- Use Light, Dark, or System unless live Settings proves a named theme picker exists.
- Preserve readable focus indicators and terminal font coverage.
- Test custom editor/terminal entries before making them defaults. Do not promise system fallback when no tool is configured.
- Keep device-local preferences out of `solo.yml`.

## Tune notifications safely

- Separate native background alerts, in-app toasts, unread indicators, and bell sounds.
- Resolve project/process levels using most restrictive effective setting: All, Important, or None.
- Prefer Important for noisy processes when crashes matter but BEL/OSC events do not.
- Verify OS permission, Focus/Do Not Disturb, same-process suppression, and rate limiting before calling notification delivery broken.

## Handle account and updates cautiously

- Read license/account state before suggesting activation or upgrade.
- Never expose, copy into output, or persist license keys or bearer tokens.
- Do not deactivate or move a license without explicit request; deactivation can stop processes when usage exceeds free limits.
- Do not install an update or relaunch while processes run without explicit confirmation. Explain that commands, agents, and terminals stop on quit/relaunch.
- Prefer checking update availability and release notes over applying update when request is informational.

## Verify completion

- Re-read affected Solo state or revisit exact Settings control.
- Confirm no project config, command lifecycle, or agent session changed unless separately authorized through neighboring skill.
- Cite current docs/changelog for any version-sensitive caveat.
- Summarize changed preference, scope, and any deferred UI action in a few lines.
