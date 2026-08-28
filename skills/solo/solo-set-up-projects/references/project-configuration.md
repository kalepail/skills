# Project configuration reference

Read for `solo.yml` shape, setup/storage decisions, sync/trust rules, or execution profile details.

## Supported `solo.yml` shape

```yaml
name: project-display-name
icon: assets/icon.png
icon_initials: XY
processes:
  Web:
    command: pnpm dev
    working_dir: apps/web
    auto_start: true
    auto_restart: false
    restart_when_changed:
      - apps/web/config/**
    env:
      NODE_ENV: development
```

Root fields:

- `name`: optional initial display name.
- `icon`: optional project-relative image path; keep inside root, at most 256 KB, with `png`, `jpg`, `jpeg`, `gif`, `ico`, or `webp` extension.
- `icon_initials`: optional 1–2 characters.
- `processes`: optional map; missing/null means empty.

Process fields:

- `command`: required string.
- `working_dir`: optional string/null; resolve relative to root. Absolute path is valid only inside root. Parent, outside-root, and symlink escapes are rejected.
- `auto_start`: optional boolean, default `true`.
- `auto_restart`: optional boolean, default `false`.
- `restart_when_changed`: optional string list, default empty. Match paths relative to project root. Invalid globs are ignored.
- `env`: optional string map, default empty.

Only commands are YAML-backed. Unknown extra keys are ignored, not extension points. Empty/comment-only YAML is valid. File limit is 1 MB.

## Setup and storage

- Add existing folder through app, CLI, or MCP. `create_project` requires existing path and returns existing project for canonical duplicate.
- Let app onboarding detect commands only for new folders without `solo.yml`; detection does not rerun automatically later.
- Prefer YAML for shared repeatable commands. Prefer local storage for personal or machine-specific commands.
- Model long-lived development infrastructure and external CLIs as named Solo commands instead of hiding them inside agent background work.
- Default shared command `auto_start` and `auto_restart` to false unless explicit user/runbook requirement says otherwise.
- Use **Save to YML** to move local command into file. Use **Make local** to remove YAML entry while preserving local command.
- Point Solo at repository root. For monorepos, use `working_dir` or package filters.
- Solo does not provide a command dependency DAG. Use explicit manual ordering or one transparent wrapper command when startup order matters; do not invent unsupported dependency keys.

Detection covers package scripts/managers, Procfiles, Make/Just/Task, PM2, Turbo/Nx, and common framework manifests. JavaScript package-manager order: `packageManager`, lockfile, then npm.

## Sync and trust

Solo watches root `solo.yml`, debounces events, and compares file hashes. Sync may add, update, rename, or remove commands. Removed running commands stop during sync. Sync never auto-starts or restarts commands.

Untrusted YAML commands cannot start or restart manually or automatically. Trust fingerprint includes command, working directory, environment, `auto_start`, `auto_restart`, and normalized file-watch patterns. Rename alone can preserve trust. Trust is local to machine and project/variant.

Use project auto-trust only for private controlled repositories. Unsafe working directories still require review.

Treat YAML-backed commands as shared runtime state. Configuration authority does not imply authority to start, stop, restart, rename, send input, select in UI, clear output, or otherwise control them. Require exact user/runbook authority for those actions.

## Execution profiles and environment

Each project resolves one profile through global inheritance, path auto-detection, or manual override. Profile controls shell for terminals, commands, and agents; on Windows it also selects host versus WSL distro.

- macOS/Linux: system default or installed Zsh, Bash, Fish, `sh`, or custom shell command.
- Windows: system/Command Prompt, PowerShell, Git Bash, WSL default, or `wsl:<distro>`.
- Preserve unavailable manual profile with warning; repair shell/distro or select another.
- Map Windows project root into distro when using WSL profile.

Unix shell environment capture runs login shell as `-ilc env` and caches 10 minutes. Windows normalizes app environment; WSL uses distro environment. Keep version-manager exports/shims in login-shell-loaded startup files.

## House boundaries

- Preserve unrelated working-tree changes.
- Leave Git staging, commits, pushes, publishing, deployment, and integration to root/operator.
- Do not treat project registration as requirement for committed YAML; empty processes or no YAML can be intentional.

## Sources

- https://soloterm.com/api/v1/docs/projects/solo-yml
- https://soloterm.com/api/v1/docs/projects/yml-change-notifications
- https://soloterm.com/api/v1/docs/projects/creating-loading-projects
- https://soloterm.com/api/v1/docs/projects/command-auto-detection
- https://soloterm.com/api/v1/docs/commands/adding-removing
- https://soloterm.com/api/v1/docs/commands/trust-security
- https://soloterm.com/api/v1/docs/environment/execution-profiles
- https://soloterm.com/api/v1/docs/environment/shell-environment
- https://soloterm.com/api/v1/docs/environment/version-managers
- https://soloterm.com/api/v1/docs/mcp-tools/project
- https://soloterm.com/changelog
