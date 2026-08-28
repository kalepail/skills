---
name: solo-track-todos
description: Create and maintain project-scoped Solo todos with status, priority, tags, blockers, comments, locks, completion, and cross-project transfer. Use when turning plans into tasks, finding ready work, claiming todos, recording progress or handoffs, updating dependencies, or completing work. Do not use for narrative context, which belongs in scratchpads, or for controlling processes.
---

# Track Solo Todos

Maintain honest actionable work graph. Keep durable context in scratchpad and task trail in todos.

## Discover Current Todo Surface

1. Call `whoami`; confirm effective project.
2. Call `help(topic="todos")` before todo mutations.
3. Call `help(topic="coordination")` before combining todo locks with general locks.
4. Use live tool discovery when names, fields, or response shapes matter. Do not assume stale schemas.

Read [todos.md](references/todos.md) before setting blockers, taking locks, transferring todos, changing tags under concurrency, or relying on write response fields.

## Create Actionable Todos

Create one todo per meaningful outcome. Include:

```text
Objective
Authoritative inputs and scratchpad link/section
Owned scope
Forbidden work
Acceptance checks
Expected handoff
```

Set honest status, priority, and small controlled tag set. Do not duplicate full scratchpad plan.

Keep todos ephemeral. Complete them as work lands after evidence review; completion unblocks dependents and preserves the record and comments, so it is a status change, not erasure. Move only real future work to `backlog`. Except for accidental duplicates, delete a record only after every downstream consumer—lead harvest, reviewer, dependent lane—acknowledges the handoff; never reap it mid-cycle to shorten a list. Durable conclusions belong in repository docs, not a stale todo list.

## Model Dependencies

- Add explicit blockers before dispatch.
- Use `todo_add_blocker` or `todo_remove_blocker` for local graph changes.
- Use `todo_set_blockers` only when full replacement set is known.
- Dispatch only unblocked todos.
- Avoid cycles; docs do not promise cycle prevention.
- Comment exact missing evidence or decision on blocked todo.

## Claim and Update Work

1. Inspect todo and current lock owner.
2. Lock an unclaimed or assigned todo only when current actor is authorized to take it; never steal active foreign lock.
3. Set `in_progress` when work starts.
4. Add comments for meaningful progress, decisions, blockers, and handoff.
5. Keep broad reasoning in scratchpad; keep task-specific trail in comments.
6. Complete only after output, diff/artifact, and checks are reviewed.

Todo lock signals task claim only. Acquire separate general lease for shared file or logical edit area.

## Record Durable Handoff

Use final comment:

```text
Changed files/artifacts:
Checks run and results:
Blockers/unresolved risk:
Next unblocked action:
```

Release lock after handoff. Keep root/operator responsible for Git, publishing, deployment, and final integration unless explicitly delegated.

## Transfer Carefully

- Treat project transfer as lifecycle transition.
- Capture handoff before transfer.
- Expect comments and completion to persist.
- Expect blockers and locks to clear.
- Rebuild target-project blockers, ownership, and claim explicitly.

## Fail Closed

Do not modify locked todo without inspecting owner. Do not infer ownership from idle/completed process. Do not control any process through todo tools. Ask before cross-project transfer when target intent is not explicit.
