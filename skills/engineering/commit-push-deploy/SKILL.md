---
name: commit-push-deploy
description: "Commit, push, deploy, and live-verify the current project's approved changes end to end. Use when the user asks to deploy, release, or ship changes live (\"git commit, git push, deploy\", \"push and deploy\", \"deploy and rebuild\", \"ship this live\"), even without the word \"commit\". Do not use for commit-only, push-only, or pull-request-only requests."
---

# Commit, push, deploy

Move the user's approved changes from the working tree to a verified live release. Use the project's own Git and deploy workflow.

## 1. Resolve scope and destination

- Read the project instructions (`AGENTS.md`, `CLAUDE.md`, `package.json`, deploy configs).
- Read Git status, branch, upstream, and ahead/behind state.
- List unpushed commits with `git log @{u}..HEAD`. A push publishes all of them, not only the working diff. If the branch has no upstream, compare against the remote target branch.
- Separate the approved changes from unrelated staged or unstaged work. Keep concurrent edits intact.
- Confirm the target repository, branch, and deploy account or profile from config and authenticated read-only checks. Keep secrets and tokens out of the output.
- Reuse release authorization that the user already gave in this conversation.
- Stop and ask when the destination or the owner of a change is ambiguous.

Done when you can name the approved files or hunks, every unpushed commit, the remote branch, and the deploy target.

## 2. Validate once

- Reuse passing build, lint, or test runs from this session when the relevant code, dependencies, and config are unchanged.
- Run the missing project checks that cover the diff.

Done when every check that covers the diff has passed on the current code.

## 3. Stage, scan, commit, and push

- Stage only the approved files or hunks, including new files. Keep unrelated staged and unstaged work intact. When unrelated changes are already staged, build and scan the approved snapshot in an isolated index (for example a temporary `GIT_INDEX_FILE` copied from `HEAD`) rather than using `git commit -- <path>`, which pulls in unstaged hunks of that file.
- Review the exact staged diff. Run `git diff --cached --check`; a non-zero exit means whitespace errors or conflict markers to fix.
- Scan staged changes (`gitleaks git --staged --redact`) and the full outgoing commit range (`gitleaks git --log-opts="<base>..HEAD" --redact`, where `<base>` is `@{u}` or the remote target branch) before pushing. If `gitleaks` is not installed, use the repository's configured scanner.
- On a scanner finding, stop. Report the file and rule, and keep the secret out of every commit and push.
- If the approved changes are already committed, reuse that commit after scanning the outgoing range. Create no empty commit.
- Push to the confirmed remote branch. Force-pushing and rewriting shared history are off limits.
- If the remote moved, inspect the incoming commits before you integrate them. Then re-validate the affected behavior.

Done when `git ls-remote <remote> refs/heads/<branch>` returns the intended commit SHA.

## 4. Deploy and live-verify

- Use the project's documented deploy or release script, profile, and environment. Do not rebuild raw provider flags by hand.
- Deploy the validated commit only. When unrelated dirty files exist and the deploy tool bundles the working tree (Wrangler, local builds, CLI installs), deploy from a clean worktree at the pushed commit.
- If the push already triggers a CI, Pages, or provider deploy, follow that run. Start no duplicate deploy.
- Record the live URL, the deployment or version ID, or the rebuilt artifact path.
- Verify the delivered change on the live target. A deploy exit code of `0` is not proof. Check the change directly:
  - Web app or API: fetch the response or rendered output.
  - Worker or service: check the live endpoint or health, then the changed behavior.
  - CLI or package: check the installed version and the changed behavior.
- If a network or permission error leaves the push or deploy state uncertain, inspect the remote state before you retry.
- If a push or deploy fails, stop the dependent steps. Report what completed and the exact blocker.

Done when you observe the specific change on the live target.

## 5. Report

Report the commit SHA, the deploy target and ID or link, the live verification result, and any material limitation.
