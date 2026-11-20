---
name: commit-push-deploy
description: "Commit, push, deploy, and live-verify the current project's approved changes end to end. Use whenever the user asks to deploy, release, or ship changes live (e.g., \"git commit, git push, deploy\", \"push and deploy\", \"deploy and rebuild\", \"ship this live\"), even if they omit \"commit\". Not for commit-only or PR-only requests."
---

# Commit, push, deploy

Take the user's approved changes from working tree to a verified live release using the project's established Git and deployment workflow.

## 1. Resolve scope and destination

- Read project instructions (`AGENTS.md`, `CLAUDE.md`, `package.json`, deploy configs), Git status, branch, upstream, and ahead/behind state.
- Separate approved changes from unrelated staged or unstaged work so concurrent edits are preserved untouched.
- Inspect unpushed local commits (`git log @{u}..HEAD`) in addition to the working diff — a push publishes all ahead commits.
- Verify the target repository, branch, and deployment account/profile from config and authenticated read-only checks without printing secrets or tokens.
- Stop and clarify if the target destination or change ownership is ambiguous; reuse clear release authorization already given in the conversation.

## 2. Validate once

- Reuse passing build, lint, or test runs from this session when the relevant code, dependencies, and config have not changed.
- Run any missing project checks that cover the diff before publishing.

## 3. Stage, scan, commit, and push

- Stage only the approved files or hunks (including new files). If unrelated files were already staged, keep them out of this commit.
- Review the exact staged diff and run `git diff --cached --check`.
- Scan the staged payload for secrets before committing (`gitleaks git --staged --redact`, or the repo's configured scanner if `gitleaks` is unavailable).
- If the intended changes are already committed, reuse that commit instead of creating an empty commit.
- Push to the verified remote branch without rewriting shared history or force-pushing. If the remote moved, inspect incoming commits before integrating and re-validate affected behavior.
- Done with Git when the remote branch contains the intended commit SHA.

## 4. Deploy and live-verify

- Use the project's documented deploy/release script, profile, and environment rather than reconstructing raw provider flags.
- Deploy the validated commit, never unrelated working-tree edits. When unrelated dirty files exist and the deploy tool bundles the working tree (e.g., Wrangler, local builds, CLI installs), deploy from a clean worktree at the pushed commit.
- If pushing to the branch already triggers CI/Pages/provider deployment, follow that run instead of starting a duplicate deploy.
- Record the live URL, deployment/version ID, or rebuilt artifact path.
- Verify the specific delivered change on the live target — a `0` deploy exit code alone is not completion. Check live behavior directly (fetched response/rendered output for web apps or APIs, live endpoint/health + changed behavior for Workers/services, or version/behavior check for rebuilt CLIs/packages).
- If a network or permission error leaves push or deploy state uncertain, inspect remote state before retrying the mutation.
- On a failed push or deploy, stop dependent steps and report what completed plus the exact blocker.

## 5. Report

Return concisely: commit SHA, deployment target/ID or link, live verification result, and any material limitation.
