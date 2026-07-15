# Solo coordination and multi-agent workflows

Research date: 2026-07-15. Solo docs snapshot: 2026-07-15T18:32:16.369Z. Sources: live Solo MCP `help` topics (`processes`, `spawning`, `timers`, `coordination`, `locks`, `scratchpads`, `todos`, `docs`), Solo MCP tool schemas, and current official SoloTerm docs.

## Executive findings

Solo works best as coordination substrate around autonomous agents, not as shared-brain abstraction. Lead agent owns decomposition and integration; worker agents own bounded, independent lanes. Durable state belongs in project-scoped scratchpads and todos, exclusion belongs in leases, small machine-readable signals belong in KV, and resumption belongs in timers. Chat and agent summaries are observation surfaces, not source of truth. [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration) [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)

Strongest safety invariant: identity, project scope, work ownership, and completion evidence stay separate. `whoami` establishes caller/process/project; todo identifies work; lock signals active ownership; output/diff/tests prove completion. None substitutes for another. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal) [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination) [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

Solo's coordination primitives are deliberately narrow. Locks are advisory leases, KV lacks compare-and-swap, idle is heuristic, MCP resources are read-only, scratchpad concurrency is optimistic, and todo transfer intentionally destroys source-project blockers and locks. Robust orchestration must account for those limits instead of assuming transactional workflow engine semantics. [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination) [Key-value MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/key-value) [Agent idle detection](https://soloterm.com/api/v1/docs/agents/idle-detection) [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources) [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads) [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos)

## Primitive map

| Need | Solo primitive | Correct payload | Key limit |
|---|---|---|---|
| Caller attribution | `whoami`, `identify_session` | Actor, Solo process, effective project | Identity does not select another process or timer target |
| Worker creation | `list_agent_tools`, `spawn_agent`, `send_input` | One bounded prompt plus returned bootstrap instructions | Spawn does not change caller identity |
| Wake-up/resumption | timers | Self-contained next action and durable IDs | Idle is heuristic; timer body becomes fresh user turn |
| Mutual exclusion | general lease lock | Stable project-scoped file/logical-area key | Advisory, expiring, non-blocking |
| Active task claim | todo lock | One owned todo | Coordination signal, not permanent ownership |
| Small shared state | KV | Small JSON status/heartbeat/result pointer | No CAS; poor fit for logs or prose |
| Durable context | scratchpad | Markdown plan, findings, decisions, handoff | Revision conflicts require reread/merge |
| Work graph | todo | Objective, acceptance, status, priority, tags, blockers | Transfer clears blockers and locks |
| Task-local history | todo comments | Progress, changed files, tests, risk, blocker detail | Not broad project narrative |
| Reusable dispatch shape | prompt template | Stable prompt with placeholders | Template tools off by default; no orchestration state |
| Read-only context distribution | MCP resources | Scratchpad/todo Markdown URI | Writes require feature tools |

This separation follows Solo's own guidance: KV for small project JSON, scratchpads for durable text, todos for actionable work, and locks for short-lived collision avoidance. [Key-value MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/key-value) [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads) [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools) [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination)

## Spawning agents and identity

### Spawn contract

1. Resolve current project and caller with `whoami`; use explicit `project_id` for cross-project work. Most tools otherwise use selected project, then identified process project. Solo process IDs are Solo-managed IDs, not host PIDs or IDs from another agent runtime. [MCP tools overview](https://soloterm.com/api/v1/docs/mcp-tools/overview) [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
2. Call `list_agent_tools`; choose returned tool or environment-specific installation ID. Do not hardcode IDs across machines or project environments. Target runtime must be configured, enabled, and launchable; ready and unknown-health installations may launch, while missing or broken installations cannot. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal) [Agents spawning agents](https://soloterm.com/api/v1/docs/workflows/agents-spawning-agents)
3. Prefer `spawn_agent`; generic `spawn_process(kind="agent")` is equivalent when generic process creation is needed. Returned `process_id` addresses later input, inspection, timers, and cleanup. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
4. Prepend returned `agent_instructions` to first worker prompt. Those instructions carry worker process/project identity and Solo MCP bootstrap hints. Then deliver prompt with `send_input(process_id=..., input=...)`. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
5. Record process ID and worker/tool choice beside todo or in lead scratchpad. Spawn response is transient; durable mapping prevents orphaned work after lead restart. This is derived from Solo's durable-memory and handoff guidance. [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos) [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

Spawn does not change caller identity or default scope. `project_id` controls destination project; it is not identity switching. Cross-lab workers are valid: parent and child may use different tools, models, providers, or custom commands. Child inherits neither judgment nor unstated context, so each spawn needs explicit objective, ownership, constraints, acceptance, and handoff. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal) [Agents spawning agents](https://soloterm.com/api/v1/docs/workflows/agents-spawning-agents)

### Identity modes and safety

- Auto-detection is normal for Solo-managed agents. Start with `whoami`; call `identify_session` without arguments only to detect/report identity. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
- If auto-detection fails, self-assert only caller's own `SOLO_PROCESS_ID`. This value is Solo process ID, not OS PID. Never pass another process ID to impersonate or target it. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
- External callers may register external actor name plus optional agent ID/metadata. This grants attribution needed by locks, todos, and scratchpads; it does not turn external actor into another Solo process. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
- Use `delivery_process_id` for timer destination and `project_id` for scope. Re-identification is never routing mechanism. [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)
- Identity associates timers, locks, todo/scratchpad actions, and cleanup with correct process. Re-check `whoami` after reconnection, project switch, or ambiguous lock ownership. Solo's bundled helper preserves Solo-launched process identity and selected project across Solo/helper restart, but other clients only keep stable session for helper lifetime. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal) [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server)

### Worker prompt contract

Minimum useful worker prompt:

```text
Objective: {{objective}}
Todo: {{todo_id}}
Shared context: scratchpad {{scratchpad_id}}, section {{section}}
Ownership: {{owned_paths_or_surface}}
Do not change: {{non_goals_or_neighbor_paths}}
Other agents: may edit nearby files; preserve unrelated changes
Acceptance: {{checks}}
Handoff: comment on todo with changed files, checks run, blockers, remaining risk
Lock: acquire todo lock and any named shared-area lock before edits; release after handoff
```

This structure captures exact objective, durable context, file boundary, concurrent-edit warning, prohibited changes, verification, and concrete handoff requested by Solo's orchestration workflow. [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

## Timers: delay, idle-any, idle-all

Timers are Solo agent wake-up mechanism; use them instead of sleep loops or repeated status polling. A timer belongs to actor, watches zero or more Solo processes, and delivers to exactly one Solo agent. `processes` on idle timers is watch set; `delivery_process_id` is recipient. [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)

### Semantics

| Timer | Schedule behavior | Correct use |
|---|---|---|
| `timer_set(delay_ms, body)` | One-shot after delay; `loop: true` repeats same interval; `repeat_every_ms` sets explicit interval | Time-based follow-up, bounded periodic check |
| `timer_fire_when_idle_any(processes, max_wait_ms, body)` | Ignores members already idle at scheduling; fires on next transition by any watched non-idle member or deadline | Harvest first newly quiet worker, then reschedule for remainder |
| `timer_fire_when_idle_all(processes, max_wait_ms, body)` | Already-idle members count satisfied; if all already idle, returns `already_satisfied` and creates no pending timer | Batch integration after current worker cohort quiets |

Scheduling results may contain `already_idle`, `waiting_on`, status, and no pending timer for already-satisfied idle-all. `max_wait_ms` is hard guard, not poll cadence. Timer bodies are injected verbatim into recipient conversation as fresh user turns, so they must be self-contained and should include process IDs, scratchpad/todo IDs, expected evidence, and next action. [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)

Idle means Solo runtime appears quiet, not completed work. Detection mixes output, terminal-title, and summarization signals by agent runtime; agents may pause before continuing. On wake, inspect current process status and real output before completing todo or closing worker. [Agent idle detection](https://soloterm.com/api/v1/docs/agents/idle-detection) [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

Use `wait_for_bound_port` for service readiness. Idle timers answer worker-quiet questions, not whether HTTP/database listener is ready. [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)

### Robust event loop

```text
spawn cohort -> record process/todo mapping
schedule idle-any(watched cohort, bounded max wait, lead recipient)
on wake:
  re-check identity/scope
  inspect status + output of candidate workers
  if handoff complete: persist todo comment, review diff/checks, release/complete todo
  if waiting/blocked: update todo + scratchpad, send bounded follow-up
  remove finished workers from watch set
  if workers remain: schedule new idle-any
  else: reconcile plan, then integrate or dispatch next unblocked cohort
cancel stale periodic timers when phase ends
```

Use idle-all only when downstream action truly needs whole cohort. Using it for incremental harvesting creates head-of-line blocking; using idle-any for barrier integration risks acting on incomplete lanes. This distinction follows documented any/all satisfaction rules. [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)

Timer safety: do not embed raw untrusted issue text, web content, or XML-like control text in `body`; place source material in scratchpad and reference ID/section. Verbatim fresh-turn delivery gives timer text instruction authority, so concise lead-authored next actions reduce ambiguity and prompt-injection surface. This is derived from documented verbatim-delivery contract and recommendation for plain prose. [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)

## Locks

General locks are project-scoped, non-blocking advisory leases. `lock_acquire(lock_key, lease_ttl_seconds)` succeeds or reports contention; `lock_status` identifies current holder; only owner may `lock_release`. Use them around shared files, plans, migrations, generated artifacts, or logical areas where overlap is costly. [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination)

Recommended keys are stable and specific:

```text
file:src/auth/session.ts
area:billing-schema
artifact:research/solo-coordination
integration:release-2026-07
```

Prefer one smallest lock covering actual collision domain. Acquire immediately before protected read/edit/write, set TTL slightly above expected critical section, renew/reacquire only while work is active, and release immediately after durable handoff. Locks signal coordination, not authorization, correctness, or permanent ownership. [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination) [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools)

Todo locks are separate task-edit leases. MCP default lease is 300 seconds; process-owned todo locks are released when bound process closes. `todo_complete` releases completing actor's todo lock by default unless `release_lock=false`. Use todo lock for task claim/status/comment editing; use general lock for shared file/logical resource. One does not imply other. [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos) [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools)

No atomic multi-lock primitive is documented. If lane needs several locks, acquire keys in deterministic lexical order and release all on failure, or collapse tightly coupled resources under one area lock. Never wait indefinitely while holding earlier lock; leases plus retry timer avoid deadlock. This is a derived pattern from non-blocking single-key lease API. [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination)

## KV shared state

KV stores project-scoped JSON; `kv_set` optionally sets TTL. Use it for discoverable, small structured values such as cohort ID, phase, process-to-todo map, last heartbeat, or pointer to scratchpad revision. Use scratchpads for long text and todos/comments for workflow history. [Key-value MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/key-value)

Example:

```json
{
  "phase": "worker-review",
  "cohort": "billing-2",
  "workers": { "2177": 41, "2286": 42 },
  "scratchpad_id": 9,
  "scratchpad_revision": 12,
  "updated_by": "lead"
}
```

KV tool surface has set/get/list/delete but no compare-and-swap or expected revision. Protect read-modify-write with general lease lock when competing writers exist; otherwise last write wins. Use TTL for heartbeats, temporary routing, and phase claims; omit TTL for durable pointers only when another artifact remains authoritative. Never use KV as lock, append-only log, report store, or completion proof. [Key-value MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/key-value) [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination)

## Scratchpads

Scratchpads are project-scoped Markdown memory for plans, research, decisions, commands, and handoffs. Shape long notes with stable headings because readers can request full content, heading outline, a section, line slice, tail, or bounded literal search. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads) [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)

Recommended orchestration note:

```markdown
# <run name>

## Goal
## Scope and non-goals
## Project, branch, and worktree
## Constraints and risky files
## Work lanes and ownership
## Dependency graph
## Decisions
## Findings
## Verification
## Open questions
## Current summary
## Handoffs
```

### Reads and targeted mutation

- Start with `scratchpad_list`/`scratchpad_read`. For large notes, read headings then required section; use `scratchpad_find` for bounded literal search and `scratchpad_tail` for newest append-only notes. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- Use `scratchpad_edit` for section or zero-based line-range replacement. Section matching normalizes whitespace and case. Replacement starting with heading replaces whole section; body-only replacement preserves matched heading. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- Use `scratchpad_append_section` to add under existing heading and `scratchpad_append` for chronological end notes. Prefer targeted mutations over full rewrite. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- `scratchpad_write` creates or fully replaces content/tags. Leading H1 overrides supplied name. Reserve overwrite for create or intentional whole-document rewrite. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- `scratchpad_rename`, `scratchpad_add_tags`, and `scratchpad_remove_tags` avoid needless content rewrite. Tags are project-scoped discovery metadata, not task status. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)

### Revision discipline

Read returns revision. Whole replace, edit, rename, clear, delete, tag mutation, and transfer use expected-revision protection; append and append-section may also accept revision guards. On conflict: reread latest, recompute smallest targeted mutation, retry. Never suppress conflict by overwriting latest version. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads) [Scratchpad agent tools](https://soloterm.com/api/v1/docs/scratchpads/agent-tools)

For concurrent lanes, assign one writer per section and use `append_section` or section `edit`; this narrows conflict surface but does not make writes transactional. Lead owns summary/decision sections; workers append findings or update named lane sections. [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)

### Archive, transfer, files, resources

- Archive hides note from active lists without deletion; archived notes remain viewable through status filters but are skipped by MCP resource listing. Use archive after integration, not as completion signal. [Using scratchpads](https://soloterm.com/api/v1/docs/scratchpads/using-scratchpads) [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)
- Transfer moves note to another project at expected revision. Since scratchpad context is project-scoped, update linked todo/resource references after transfer. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- Save/load tools exchange UTF-8 Markdown and treat leading H1 as title. Relative paths resolve inside project and reject `..` or symlink escape; absolute paths are honored directly when accessible. Default to project-relative trusted paths. Require explicit user intent before absolute path crosses project boundary. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads) [Scratchpad agent tools](https://soloterm.com/api/v1/docs/scratchpads/agent-tools)
- Scratchpad MCP resources are read-only and use `solo://proj/{project_id}/scratchpad/{slug}--{scratchpad_id}`. Use tools for writes. [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)

Do not stage ordinary scratchpad edits through files. Direct read/edit preserves revision semantics and avoids split-brain between file and Solo record. File import/export is explicit interchange or backup path. [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)

## Todos

Todos are project-scoped executable work records: title/body, `open|in_progress|backlog|completed`, `high|medium|low`, tags, blockers, comments, and locks. They should point to scratchpad context instead of duplicating it. [Using todos](https://soloterm.com/api/v1/docs/todos/using-todos) [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)

### Good todo contract

```text
Title: bounded outcome
Body: objective; owned files/surface; scratchpad link/section; acceptance checks; non-goals; handoff format
Status: honest current phase
Priority: scheduling importance
Tags: lane/component/type
Blockers: actual prerequisite todo IDs
```

Todo body carries contract; comments carry activity trail. Worker should lock todo when active, set `in_progress`, comment material progress/blocker/handoff, and complete only after evidence is reviewed. [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools) [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

### Blockers

Use `todo_add_blocker`/`remove_blocker` for local graph edits; use `todo_set_blockers` only when replacing full known set. Verification can depend on implementation lanes; integration can depend on all handoffs. Dispatch only unblocked independent work. [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos) [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

Treat blockers as dependency graph, not status prose. A blocked todo should also receive comment naming exact missing evidence or decision. Reconcile graph when plan changes, and avoid cycles through lead review because docs do not promise cycle prevention. [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)

### Comments and tags

Comments preserve author-attributed handoffs and decisions in task timeline. Standard final comment: changed files/artifacts, checks run and results, blockers, remaining risk, and recommended next action. Use scratchpad for cross-task narrative. [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools) [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)

Tags support filtering and bulk organization. Keep small controlled vocabulary (`lane:api`, `type:review`, `component:billing`) instead of encoding state already represented by status, priority, blockers, or lock. `todo_add_tag`/`remove_tag` preserve other tags; `todo_update(tags=...)` replaces set and is riskier under concurrency. [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos)

### Locks and completion

Todo locks signal active editing and appear in UI. Bind MCP session to process so locks release when process closes. Before touching locked todo, inspect owner/process rather than overriding. Completing normally releases completing actor's lock; still capture handoff before completion. [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools) [Using todos](https://soloterm.com/api/v1/docs/todos/using-todos)

Use slim write receipts during normal orchestration; request rich response only when immediate hydrated todo/comment is needed. Then `todo_get` remains explicit read boundary. This reduces payload and stale-state assumptions. Live Solo MCP `help(topic="coordination")` and `help(topic="todos")` document slim default and rich opt-in.

### Transfer

`todo_transfer` preserves comments and completion state but clears blockers and locks because both are source-project scoped. Treat transfer as state transition: capture handoff, unlock/stop source worker, transfer, rebuild target-project dependencies, assign target owner, then verify status. Never assume moved todo remains runnable or claimed. [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos) [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools)

Todo MCP resources are read-only Markdown including comments and use `solo://proj/{project_id}/todo/{slug}--{todo_id}`. Resource URIs double as Solo deep links; mutation still requires todo tools. [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)

## Prompt templates and built-in prompts

Prompt templates are reusable global or project-scoped prompts. MCP tools can list, get, create, patch, delete, and export; feature is off by default for MCP even though templates remain available in Solo UI. Same-scope names are case-insensitively unique. [Prompt template MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/prompt-templates) [Prompt templates](https://soloterm.com/api/v1/docs/prompt-templates/overview)

Use project template for repository-specific worker contract and global template for provider-neutral orchestration grammar. Placeholders use `{{name}}`; names start with letter/underscore, contain letters/digits/underscores, normalize case, and repeat occurrences share one value. Empty values disappear, so do not make safety-critical constraint optional. [Placeholders](https://soloterm.com/api/v1/docs/prompt-templates/placeholders)

Recommended templates:

- `worker-lane`: objective, todo, scratchpad section, owned area, non-goals, acceptance, handoff.
- `worker-review`: diff scope, correctness risks, expected one-line findings, no edits unless authorized.
- `timer-followup`: watched process IDs, todo IDs, evidence to inspect, reschedule/cancel rule.
- `handoff`: artifacts, changed files, checks, blockers, risk, next action.
- `integration-pass`: cohort, prerequisite todos, diff/check sequence, completion policy.

Templates standardize prompt shape, not current truth. Fill IDs, revision, ownership, and acceptance at dispatch time; keep dynamic coordination state in scratchpad/todo/KV. Prefer insert-and-review over immediate submit for prompts that can mutate files, spawn agents, or close processes. Picker supports both insertion and insert+submit, so human/lead review remains available. [Using templates](https://soloterm.com/api/v1/docs/prompt-templates/using-templates)

Exports are Markdown plus YAML frontmatter. Export creates destination directory, slugifies filenames, numbers collisions, and does not overwrite existing file. Use exports for versioned backup/repository sharing, not live synchronization. [Creating and editing templates](https://soloterm.com/api/v1/docs/prompt-templates/creating-and-editing) [Prompt template MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/prompt-templates)

Solo also exposes built-in MCP prompts: `worker_bootstrap`, `wait_for_bound_port`, and `timer_followup`. `worker_bootstrap` covers identity, locks, KV, scratchpads, todos, and non-polling readiness; `timer_followup` covers wake processing and stale timer cancellation. Prefer these maintained playbooks when client supports MCP prompts, then add project-specific template/context. [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)

## Robust orchestration blueprint

### 1. Bootstrap

Call `whoami`; verify actor, Solo process ID, effective project. Confirm feature tools are enabled. Load built-in `worker_bootstrap` prompt when available. Create lead scratchpad only after project is correct. [MCP tools overview](https://soloterm.com/api/v1/docs/mcp-tools/overview) [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)

### 2. Interview and plan

Clarify goal, constraints, non-goals, files, risks, deadline, and verification before spawning. Write plan scratchpad with independent lanes and dependency graph. Parallelism is optimization after decomposition, not starting condition. [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

### 3. Materialize work graph

Create one todo per meaningful lane, plus explicit integration/verification todos. Add blockers, priorities, tags, ownership boundaries, scratchpad section, acceptance, and handoff format. Keep tightly coupled or tiny edits with lead. [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

### 4. Dispatch one cohort

Select unblocked lanes with disjoint write surfaces. Resolve available agent tools, spawn one worker per lane, prepend returned instructions, send self-contained prompt, record process-to-todo map, and have workers take todo/general locks. [Agents spawning agents](https://soloterm.com/api/v1/docs/workflows/agents-spawning-agents) [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)

### 5. Wait eventfully

Schedule bounded idle-any timer to lead. On wake, inspect process status/output; do not trust idle or summary alone. Persist worker state in comment/scratchpad. Reschedule for remaining processes. Use idle-all only for true barrier. [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers) [Agent idle detection](https://soloterm.com/api/v1/docs/agents/idle-detection)

### 6. Harvest and integrate

Require handoff comment. Review actual diff/artifact and checks. Integrate one lane at time, run focused verification after meaningful step, then unblock dependents. Notify still-running workers of relevant overlapping changes. [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)

### 7. Reconcile

Update scratchpad current summary and decisions; update todo status/blockers/comments honestly; refresh KV phase pointer if used. New findings may delete a lane or change dependency graph before next dispatch. [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)

### 8. Complete and clean up

Complete todo only after evidence passes. Capture all useful context before closing worker. Cancel stale timers, release general locks, verify todo locks released, archive scratchpad only when run no longer active, then close finished agents. Closing removes session and stops process but does not undo filesystem edits. [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration) [Closing agents](https://soloterm.com/api/v1/docs/agents/closing-agents)

## Failure recovery

| Failure | Recovery |
|---|---|
| Spawn unavailable | Refresh `list_agent_tools`; keep lane with lead or choose launchable runtime; do not repeatedly spawn broken installation. |
| Wrong/ambiguous identity | Stop state mutation; `whoami`; self-assert only own `SOLO_PROCESS_ID` or register external actor. |
| Worker silent/idle | Inspect status/output and todo comment; idle is heuristic. Send bounded follow-up or max-wait timer. |
| Worker waiting for human/permission | Record blocker; route exact question to lead/user; do not mark complete. |
| Lease contention | Inspect owner, avoid overlapping edit, schedule retry after bounded delay. Do not treat lock as stale solely because worker is quiet. |
| Lease expires mid-work | Reacquire before next protected mutation; review concurrent changes first. |
| Scratchpad revision conflict | Reread, merge latest, retry smallest section/line/tag mutation. |
| KV race | Acquire general lock around get/modify/set or redesign as single-writer. |
| Timer max-wait fires | Treat as checkpoint, not success; inspect watched processes and reschedule/cancel explicitly. |
| Todo transferred | Rebuild target blockers/ownership because transfer cleared locks and source dependencies. |
| Solo restarts | Bundled helper reconnects/buffers bounded requests; re-check identity/scope and reconcile durable state before writes. |
| Worker closed mid-task | Inspect filesystem diff first; handoff may be absent and closing does not roll back edits. |

These recoveries follow documented identity, lease, optimistic revision, idle, transfer, reconnect, and close behavior. [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal) [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination) [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads) [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers) [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos) [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server) [Closing agents](https://soloterm.com/api/v1/docs/agents/closing-agents)

## Anti-patterns

| Anti-pattern | Why it fails | Replacement |
|---|---|---|
| Spawn swarm before plan | Shared context, boundaries, and dependencies absent | Interview, scratchpad, todos, then independent cohort |
| Give every worker whole goal | Duplicate work and contradictory judgment | One lane, ownership boundary, non-goals, acceptance, handoff |
| Parallel workers on same files | Locks become contention, integration cost exceeds wait saved | Keep coupled edit with lead or split by non-overlapping surface |
| Treat child as inheriting parent context | Spawned agent is separate collaborator | Prepend Solo instructions plus self-contained prompt |
| Hardcode agent tool/process IDs | IDs vary by environment/session | Discover tools; persist returned process mapping |
| Re-identify as target process | Identity spoofing and wrong cleanup/attribution | `project_id` for scope, `delivery_process_id` for timer routing |
| Sleep/poll loops | Wastes turns and can miss meaningful transition | Timer or `wait_for_bound_port` |
| Use idle-all for first result | Slow worker blocks every harvest | Idle-any, inspect, reschedule |
| Use idle-any for barrier | Integrates before cohort complete | Idle-all plus real completion checks |
| Treat idle/summary as done | Idle and summaries are heuristic/triage | Inspect output, diff/artifact, checks, handoff |
| Vague timer body | Fresh turn lacks prior context | Include process/todo/scratchpad IDs and next action |
| Put untrusted content in timer body | Verbatim body becomes instruction turn | Store content in scratchpad; reference section |
| Lock as security or permanent ownership | Advisory lease expires and cannot prove authority | Use lock only for collision avoidance; validate permission separately |
| Hold broad lock across whole task | Starves independent work and lease may expire | Small collision-domain lock around mutation |
| Use todo lock as file lock | Task record and shared file are different resources | Todo lock plus general file/area lock when needed |
| Use KV for prose/logs | Loses search/history and invites last-write-wins races | Scratchpad or todo comments |
| Use KV as lock | No atomic compare-and-swap | General lease lock |
| Full scratchpad overwrite for one update | Maximizes conflicts and can erase newer work | Revision-guarded section edit/append |
| File round-trip for normal scratchpad edit | Splits source of truth and bypasses direct revision flow | Direct scratchpad read/edit |
| Ignore scratchpad conflict | Silently destroys concurrent update | Reread/merge/retry |
| Duplicate full plan into todos | Context drifts in two places | Todo points to scratchpad and states next action |
| Encode dependencies only in prose | Lead dispatches blocked lane | Explicit todo blockers |
| Move todo and assume dependencies survive | Transfer clears blockers and locks | Rebuild target-project graph/claim |
| Complete on worker self-report | Summary may omit failure/risk | Lead reviews evidence first |
| Close worker before handoff | Session-only context disappears | Comment/scratchpad handoff, then close |
| Template stores live IDs/state | Reuse injects stale process/revision | Placeholders plus durable current records |
| Immediate-submit destructive template | Skips review of rendered prompt | Insert/review; submit after scope check |

Anti-patterns derive from Solo's explicit emphasis on bounded workers, durable source of truth, blockers, event-driven wakeups, evidence-based integration, and handoff-before-close. [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration) [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos) [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)

## Coordination safety checklist

- [ ] `whoami` matches intended actor, Solo process, and project before mutation.
- [ ] No identity assertion targets another process.
- [ ] Worker lane is independent, bounded, and worth spawn overhead.
- [ ] Prompt contains ownership, non-goals, concurrency warning, acceptance, and handoff.
- [ ] Todo blockers model real prerequisites; no obvious cycles.
- [ ] Todo lock covers task claim; general lock covers shared edit surface.
- [ ] Lease TTL bounded; release/expiry path exists.
- [ ] KV values small; concurrent read-modify-write protected.
- [ ] Scratchpad edits use current revision and smallest target.
- [ ] File import/export stays project-relative unless explicit trusted absolute path required.
- [ ] Timer recipient distinct from watch set; body self-contained and trusted.
- [ ] Idle/summary treated as inspection trigger, never proof.
- [ ] Completion follows actual diff/artifact/check review.
- [ ] Todo transfer followed by dependency/lock reconstruction.
- [ ] Worker handoff persisted before close.
- [ ] Stale timers and locks cleaned after phase.
- [ ] Untrusted `solo.yml` commands reviewed in UI; Solo blocks their start/restart until trusted. [Trust and Security](https://soloterm.com/api/v1/docs/commands/trust-security)

## Source notes

Official docs consulted:

- [MCP tools overview](https://soloterm.com/api/v1/docs/mcp-tools/overview)
- [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server)
- [Agent and terminal MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/agent-terminal)
- [Agents spawning agents](https://soloterm.com/api/v1/docs/workflows/agents-spawning-agents)
- [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)
- [Agent idle detection](https://soloterm.com/api/v1/docs/agents/idle-detection)
- [Timer MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/timers)
- [Coordination MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/coordination)
- [Key-value MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/key-value)
- [Scratchpad MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/scratchpads)
- [Scratchpad agent tools](https://soloterm.com/api/v1/docs/scratchpads/agent-tools)
- [Using scratchpads](https://soloterm.com/api/v1/docs/scratchpads/using-scratchpads)
- [Todo MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/todos)
- [Todo agent tools](https://soloterm.com/api/v1/docs/todos/agent-tools)
- [Using todos](https://soloterm.com/api/v1/docs/todos/using-todos)
- [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)
- [Prompt template MCP tools](https://soloterm.com/api/v1/docs/mcp-tools/prompt-templates)
- [Prompt templates](https://soloterm.com/api/v1/docs/prompt-templates/overview)
- [Placeholders](https://soloterm.com/api/v1/docs/prompt-templates/placeholders)
- [Creating and editing templates](https://soloterm.com/api/v1/docs/prompt-templates/creating-and-editing)
- [Using templates](https://soloterm.com/api/v1/docs/prompt-templates/using-templates)
- [MCP prompts and resources](https://soloterm.com/api/v1/docs/mcp-tools/prompts-and-resources)
- [Closing agents](https://soloterm.com/api/v1/docs/agents/closing-agents)
- [Trust and Security](https://soloterm.com/api/v1/docs/commands/trust-security)

Live-tool-only details cross-checked from Solo MCP schemas/help on research date: general lock acquisition is non-blocking; KV supports optional TTL but no CAS field; todo lock defaults to 300-second lease; `todo_complete` releases caller lock unless disabled; todo/comment writes default to slim receipts; scratchpad transfer requires expected revision; and archive hides without deleting. These details should be rechecked with `help`/tool schemas if Solo version changes.
