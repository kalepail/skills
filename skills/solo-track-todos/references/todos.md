# Todo tools and workflow reference

Read this reference before advanced todo filtering, blocker replacement, locking, completion, comments, tag replacement, or cross-project transfer.

## Live discovery

1. Call `whoami`; verify actor and project.
2. Call `help(topic="todos")` for current workflow and response semantics.
3. Call `help(topic="coordination")` when shared edit locks also matter.
4. Inspect live tool schemas for accepted values and enabled tools. Prefer discovered fields over this reference when they differ.

## Core surface

- `todo_create`: create project todo.
- `todo_list`: filter by status, completion, blocked state, priority, query, tags, sort, offset, and limit when current schema exposes them.
- `todo_tags_list`: discover project tag vocabulary.
- `todo_get`: read one todo; request comments when needed.
- `todo_update`: patch supplied fields; omitted optional fields remain unchanged. Passing full `tags` replaces set.
- `todo_add_tag` / `todo_remove_tag`: mutate one tag without replacing others.
- `todo_set_blockers`: replace full blocker list.
- `todo_add_blocker` / `todo_remove_blocker`: mutate one dependency.
- `todo_lock` / `todo_unlock`: acquire/release active todo edit claim.
- `todo_complete`: complete/incomplete; per live help, completion releases the actor's lock unless disabled.
- `todo_comment_create` / `update` / `delete` / `list`: maintain task activity trail.
- `todo_transfer`: move to target project; preserve comments/completion and clear blockers/locks.
- `todo_delete`: permanent removal; prefer completion or backlog unless deletion is intentional.

Todo/comment write tools default to slim receipts for normal orchestration; request rich response only when immediate hydrated state is necessary. Follow with explicit `todo_get` when authoritative read is clearer.

## Fields and conventions

Use statuses `open`, `in_progress`, `backlog`, and `completed` only when live schema confirms them. Use priorities `high`, `medium`, and `low` only when live schema confirms them.

Keep tags controlled and orthogonal:

```text
lane:api
component:billing
type:review
```

Do not encode status, priority, or blockers in tags. Prefer add/remove tag helpers under concurrency; full tag replacement can erase another actor's additions.

## Blocker graph

- Express actual prerequisite todo IDs, not vague prose.
- Block verification on implementation and integration on required worker handoffs.
- Use availability filters to find unblocked work.
- Comment exact missing evidence on blocked todo.
- Reconcile blockers when plan changes.
- Avoid cycles through lead review because cycle prevention is not documented.

## Locks and process ownership

Todo lock is advisory active-work signal, not authorization or file lock. Current MCP schema defaults todo lease to 300 seconds; verify live help before relying on duration. Process-owned locks are released when bound process closes.

- Lock only unclaimed/assigned work current actor is authorized to take; never steal active foreign lock.
- Inspect holder before editing locked todo.
- Do not assume idle/stopped/completed process transfers todo or process ownership.
- Use separate general lease for shared file/logical area.
- Never use todo state to justify process input, stop, restart, or close.

## Comments and completion

Use comments for author-attributed progress, decisions, blockers, and handoff. Final comment should include changed files/artifacts, exact checks/results, unresolved risk, and one next action.

Completion preserves the record and comments for downstream consumers; link the final handoff comment from consumer todos instead of copying it. Delete the record or strip its context only after every consumer acknowledges the handoff at its final state.

Complete only after evidence review. Worker self-report, idle, summary, or successful prompt delivery is insufficient. Root/operator keeps final integration and Git/publishing authority.

## Transfer

Before transfer:

1. Capture handoff and source context.
2. Stop source assignment and release owned lock.
3. Transfer explicitly to target project.
4. Rebuild blockers because source relationships clear.
5. Reassign owner and acquire new target claim.
6. Verify status and linked scratchpad context.

## Resources

Todo MCP resources are read-only Markdown including comments. URI shape is documented as `solo://proj/{project_id}/todo/{slug}--{todo_id}`. Use todo tools for mutation.

## Sources

- https://soloterm.com/api/v1/docs/mcp-tools/todos
- https://soloterm.com/api/v1/docs/todos/agent-tools
- https://soloterm.com/api/v1/docs/todos/using-todos
- https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos
- https://soloterm.com/api/v1/docs/mcp-tools/coordination
- https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources
- https://x.com/aarondfrancis/status/2041919379307184295
