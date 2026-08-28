---
name: solo-set-up-projects
description: Configure and import Solo projects and shared solo.yml command stacks. Use when adding repositories, defining commands, working directories, environment values, execution profiles, auto-start or restart policy, YAML sync, command storage, or trust review. Do not use for personal workspace UI, runtime process control, or failure diagnosis.
---

# Set Up Solo Projects

Configure minimum project state needed for repeatable local work. Keep shared command definitions in `solo.yml`; keep machine-specific runtime state local.

## Workflow

1. Confirm target repository root and whether project already exists.
   - Call `list_projects` before creating anything.
   - Call `select_project` when scope is ambiguous.
   - Call `get_project` or `get_project_status` to inspect existing registration.
   - Call `create_project` only for an existing directory not already registered.
2. Inspect repository entry points before proposing commands.
   - Prefer existing `solo.yml` over command auto-detection.
   - Otherwise inspect package scripts, lockfiles, Procfiles, task runners, framework manifests, and monorepo layout.
   - Reuse existing project commands instead of inventing wrappers.
3. Choose storage deliberately.
   - Save team-relevant repeatable commands to root `solo.yml`.
   - Keep personal, experimental, or machine-specific commands local.
   - Never place terminals or agents in `solo.yml`; only command processes are supported.
4. Write smallest explicit configuration.
   - Set `auto_start` on every command because omitted YAML defaults to `true`; default it to `false` unless user requests automatic launch.
   - Use relative `working_dir` paths inside project root.
   - Commit only non-secret environment values.
   - Prefer native tool watch mode; add narrow `restart_when_changed` globs only when needed.
5. Configure execution environment when requested.
   - Choose global inheritance unless project needs specific shell or Windows/WSL environment.
   - Configure per-distro WSL root mapping when host path cannot run directly inside distribution.
   - Leave unavailable profile selected only when reinstall/repair is intentional.
6. Review sync and trust.
   - Treat file-backed command changes as executable code review.
   - Sync changed YAML in Solo.
   - Require user to review and trust new or changed variants in Solo UI; never bypass trust.
   - Do not assume sync starts or restarts commands.
7. Verify setup without broad runtime mutation.
   - Re-read project status and command definitions.
   - Report local-only versus YAML-backed choices, trust blockers, and any required manual UI action.

## Decisions

- Prefer repository root as Solo project root. For monorepos, use per-command `working_dir` or package filters.
- Prefer relative paths over valid in-root absolute paths for portability.
- Default shared commands to `auto_start: false` and `auto_restart: false`; enable either only for named always-on service requested by user/runbook.
- Enable crash auto-restart only for processes expected to remain alive.
- Enable project auto-trust only for private repositories fully controlled by user.
- Preserve existing `solo.yml` formatting and unrelated entries when editing.

## Boundary

- Stop after configuration and trust handoff unless user also asks to run processes.
- Do not start, stop, restart, clear output, or delete project as setup side effects.
- Treat YAML-backed commands as shared processes; do not mutate their runtime state without explicit user/runbook authority.
- Do not delete project files; Solo project deletion removes Solo state only and requires explicit confirmation.
- Do not add scripts or wrapper commands when repository-native command already works.
- Preserve unrelated dirty-tree work. Leave Git index, commits, pushes, publishing, deployment, and integration to root/operator.

## Reference

Read [project configuration reference](references/project-configuration.md) before editing `solo.yml`, choosing local versus shared storage, handling sync/trust, or configuring execution profiles.
