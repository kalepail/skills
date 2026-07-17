# Deep research provider guide

Use current tool discovery as authority; verify provider names and commands against live listings or current official documentation before use. These are the general-web surfaces; for Stellar-ecosystem questions read [stellar-raven.md](stellar-raven.md) first.

## Contents

- Provider roles and preferred flow
- Surface selection and CLI patterns
- Parallel Task MCP final pass
- Lane, citation, and recovery rules

## Provider roles

| Surface | Current tools or commands | Best role |
|---|---|---|
| Parallel CLI | `search`, `extract`, `research run/status/poll` | Reproducible shell-driven research with saved JSON or Markdown artifacts |
| Perplexity MCP | `perplexity_search`, `perplexity_ask`, `perplexity_research`, `perplexity_reason` | Independent discovery, cited deep research, conversational search, and evidence-based reasoning |
| Parallel Search MCP | `web_search`, `web_fetch` | Low-latency discovery, current facts, and focused URL retrieval inside an agent loop |
| Parallel Task MCP | `createDeepResearch`, `createTaskGroup`, `getStatus`, `getResultMarkdown` | Asynchronous cited deep reports; task groups for consistent research across rows or entities |

## Preferred provider flow

Orient the workflow toward:

1. `parallel-cli` for primary search, extraction, research, and saved artifacts.
2. Perplexity MCP for an independent second view, counterevidence, or reasoning.
3. Parallel Search MCP when CLI access is absent or an in-loop search/fetch is simpler.
4. Parallel Task MCP for an optional final deep-verification or report pass.

This is a preference, not a prerequisite chain. Skip or reorder providers when a lane is local-only, a tool is unavailable, cost or latency matters, or another surface clearly fits better. The lead synthesizes the final answer; no provider report is final authority.

## Choose the smallest useful surface

- Discover candidate sources: prefer `parallel-cli search`; use `perplexity_search` for an independent angle or Parallel `web_search` as fallback.
- Read known URLs: prefer `parallel-cli extract`; use Parallel `web_fetch` when CLI access is absent or an in-loop fetch is simpler.
- Produce the primary deep artifact: prefer `parallel-cli research run`.
- Challenge or independently analyze the primary artifact: use `perplexity_research` or `perplexity_reason`.
- Run a final deep verification when warranted: use Parallel Task MCP `createDeepResearch`.
- Analyze already-collected evidence: `perplexity_reason`; do not treat uncited reasoning as source evidence.
- Handle a quick conversational lookup: `perplexity_ask`; do not use it as the sole deep-research lane.
- Enrich a list or table consistently: Parallel Task MCP `createTaskGroup`; do not use a task group for one open-ended topic.

Do not call every provider by default. Assign distinct questions or evidence roles so fan-out adds coverage rather than duplicate cost.

## Parallel CLI patterns

Save authoritative output to disk:

```bash
parallel-cli search "research objective" -q "keyword" --json --max-results 10 -o /tmp/topic-search.json
parallel-cli extract https://example.com --objective "evidence needed" --full-content --json -o /tmp/topic-source.json
parallel-cli research run "research question" --processor pro-fast --text -o /tmp/topic-report
```

For asynchronous research:

```bash
parallel-cli research run "research question" --processor pro-fast --no-wait --json
parallel-cli research status trun_xxx --json
parallel-cli research poll trun_xxx --json
```

List current processor tiers before choosing one:

```bash
parallel-cli research processors --json
```

Use `--no-wait` when useful work can continue meanwhile. Record the returned run ID in your working state and check its status explicitly. Never infer completion from elapsed time.

## Parallel Task MCP final pass

Parallel Task MCP starts work but does not return the final report immediately:

1. Start with `createDeepResearch` or `createTaskGroup`.
2. Record the returned task identifier.
3. Use `getStatus` for lightweight checks when you return to the task.
4. Call `getResultMarkdown` once complete.

Tool names may be namespaced by the host. Discover them live rather than hard-coding the namespace.

## Lane patterns

Use the fewest lanes that cover the question:

- Local codebase: find existing behavior, callers, configuration, dependencies, tests, and reusable patterns before recommending change.
- Official docs: verify current library, framework, protocol, or product behavior from primary documentation.
- Primary evidence: official documents, filings, specifications, datasets, or direct statements.
- Landscape: broad discovery of actors, terminology, chronology, and current developments.
- Dependencies: compare installed versions and constraints against current compatibility or deprecation guidance.
- User impact: inspect flows, accessibility, error states, edge cases, and established interaction patterns when behavior is user-facing.
- Counterevidence: contradictory findings, failure cases, criticism, and missing data.
- Independent synthesis: a separate deep-research provider answers the same decision question without seeing the lead's conclusion.

For consequential conclusions, compare claims and underlying URLs—not provider summaries. Two engines repeating the same article provide one piece of evidence. Research the problem before the proposal: a lane may evaluate the proposed approach, but at least one lane should investigate whether a smaller or different solution addresses the root issue.

## Source and citation rules

- Prefer primary sources, then high-quality secondary reporting or research.
- Record title, URL, publisher, publication or update date, and access date when freshness matters.
- Keep provider-generated reports as research artifacts, not unquestioned authority.
- Cite the underlying sources when available; cite a provider report only when it is the actual artifact being discussed.
- Mark inference explicitly and preserve unresolved disagreement.

## Recovery

- Missing CLI: use Perplexity next, then Parallel Search MCP when useful; do not install without authority.
- Missing Perplexity: continue with CLI and add an MCP verification lane only when it improves coverage.
- Missing MCP tool: finish with CLI and Perplexity evidence when sufficient.
- Authentication or rate limit failure: record it and reroute.
- Parallel `402` or insufficient balance: stop paid work; never add credit without explicit approval.
- Long-running task: retain its ID and output path, continue other lanes, and check back explicitly.
- Weak or uncited result: narrow the question and run a targeted source-discovery lane instead of repeating the same broad prompt.

## Official references

- https://docs.parallel.ai/integrations/mcp/search-mcp
- https://docs.parallel.ai/integrations/mcp/task-mcp
- https://docs.parallel.ai/integrations/cli
- https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server
