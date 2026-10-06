# Deep research provider guide

Live tool discovery is the authority. Before use, verify provider names and commands against live listings, `parallel-cli <command> --help`, or current official documentation. This guide covers the general-web surfaces. For a Stellar-ecosystem question, read [stellar-raven.md](stellar-raven.md) first.

## Contents

- Provider roles
- Preferred provider flow
- Choose the smallest useful surface
- Parallel CLI patterns
- Parallel Task MCP final pass
- Lane patterns
- Source and citation rules
- Recovery

## Provider roles

| Surface | Tools or commands | Best role |
|---|---|---|
| Parallel CLI | `search`, `extract` (alias `fetch`), `research run/status/poll/processors`, `findall`, `enrich`, `memory retrieve` | Reproducible shell-driven research with saved JSON or Markdown artifacts |
| Perplexity MCP | `perplexity_search`, `perplexity_ask`, `perplexity_research`, `perplexity_reason` | Independent discovery, cited deep research, conversational search, and evidence-based reasoning |
| Parallel Search MCP | `web_search`, `web_fetch` | Low-latency discovery, current facts, and focused URL retrieval inside an agent loop |
| Parallel Task MCP | `createDeepResearch`, `createTaskGroup`, `getStatus`, `getResultMarkdown` | Asynchronous cited deep reports, and task groups for consistent research across rows or entities |

## Preferred provider flow

Use the providers in this order:

1. `parallel-cli` for primary search, extraction, research, entity discovery, and saved artifacts.
2. Perplexity MCP for an independent second view, counterevidence, or reasoning.
3. Parallel Search MCP when CLI access is not available, or when an in-loop search or fetch is simpler.
4. Parallel Task MCP for an optional final deep-verification or report pass.

This order is a preference, not a chain of prerequisites. Skip or reorder providers when a lane is local-only, a tool is not available, cost or latency matters, or another surface fits better. The lead synthesizes the final answer. No provider report is the final authority.

## Choose the smallest useful surface

- Find candidate sources: use `parallel-cli search`. Use `perplexity_search` for an independent angle. Use Parallel `web_search` as the fallback.
- Read known URLs: use `parallel-cli extract`. Use Parallel `web_fetch` when CLI access is not available or an in-loop fetch is simpler.
- Make the primary deep artifact: use `parallel-cli research run`.
- Continue a completed run with a follow-up question: use `parallel-cli research run --previous-interaction-id <run_id>`.
- Find the set of entities for a landscape lane (companies or people): use `parallel-cli findall entity-search` for a fast ranked list, or `parallel-cli findall run` for matched and verified candidates.
- Add the same fields to each row of a list: use `parallel-cli enrich run`, or Parallel Task MCP `createTaskGroup` when CLI access is not available. Do not use a task group for one open-ended topic.
- Challenge or analyze the primary artifact independently: use `perplexity_research` or `perplexity_reason`.
- Run a final deep verification when it is necessary: use Parallel Task MCP `createDeepResearch`.
- Analyze evidence that you already have: use `perplexity_reason`. Uncited reasoning is not source evidence.
- Do a quick conversational lookup: use `perplexity_ask`. Do not use it as the only deep-research lane.

Do not call every provider by default. Give each provider a distinct question or evidence role, so that fan-out adds coverage and not duplicate cost.

## Parallel CLI patterns

Save each authoritative output to disk. Set `RESEARCH_DIR` to the working-state directory of the session. Use the same `--session-id` value for all `search` and `extract` calls in one lane.

```bash
parallel-cli search "research objective" -q "keyword" --mode advanced --after-date YYYY-MM-DD \
  --session-id lane-docs --json --max-results 10 -o "$RESEARCH_DIR/topic-search.json"
parallel-cli search "primary filings" --include-domains sec.gov --json -o "$RESEARCH_DIR/topic-primary.json"
parallel-cli extract https://example.com --objective "evidence needed" --full-content \
  --session-id lane-docs --json -o "$RESEARCH_DIR/topic-source.json"
parallel-cli research run "research question" --processor pro-fast --text -o "$RESEARCH_DIR/topic-report"
```

- `--mode` sets the search quality. Use `advanced` for primary discovery lanes and `fast` for quick in-loop checks. Run `parallel-cli search --help` for the current modes.
- `--after-date` (`YYYY-MM-DD`) enforces the freshness date of the brief. `--include-domains` keeps a primary-source lane on official domains.
- `research run -o NAME` writes `NAME.json`, and also `NAME.md` with `--text`. Without `-o`, the CLI saves under the current directory, outside the working state.

Run research asynchronously when useful work can continue:

```bash
parallel-cli research run "research question" --processor pro-fast --text --no-wait --json
parallel-cli research status trun_xxx --json
parallel-cli research poll trun_xxx -o "$RESEARCH_DIR/topic-report" --json
```

`--no-wait` returns the run ID and saves nothing. Record the run ID in the working state immediately. `research poll` waits for completion and saves the result. Always give `poll` an `-o` path. Check the status explicitly. Do not infer completion from elapsed time.

Before you choose a processor tier, list the current tiers. Use `--dry-run` to preview a paid command without an API call:

```bash
parallel-cli research processors --json
parallel-cli research run "research question" --processor ultra --dry-run
```

## Parallel Task MCP final pass

Parallel Task MCP starts work but does not return the final report immediately:

1. Start the work with `createDeepResearch` or `createTaskGroup`.
2. Record the task identifier that it returns (`trun_*` or `tgrp_*`).
3. Use `getStatus` for a lightweight check when you return to the task.
4. Call `getResultMarkdown` when the task is complete.

The host can add a namespace to the tool names. Discover the names live. Do not hard-code the namespace.

## Lane patterns

Use the fewest lanes that cover the question:

- Local codebase: find current behavior, callers, configuration, dependencies, tests, and reusable patterns before you recommend a change.
- Official docs: verify the current behavior of the library, framework, protocol, or product from primary documentation.
- Primary evidence: official documents, filings, specifications, datasets, or direct statements.
- Landscape: broad discovery of actors, terminology, chronology, and current developments.
- Dependencies: compare installed versions and constraints with current compatibility or deprecation guidance.
- User impact: examine flows, accessibility, error states, edge cases, and established interaction patterns when the behavior is user-facing.
- Counterevidence: contradictory findings, failure cases, criticism, and missing data.
- Independent synthesis: a separate deep-research provider answers the same decision question. It does not see the conclusion of the lead.

For consequential conclusions, compare claims and the underlying URLs, not provider summaries. Research the problem before the proposal. A lane can evaluate the proposed approach. At least one lane must examine whether a smaller or different solution solves the root issue.

## Source and citation rules

- Prefer primary sources. Then use high-quality secondary reporting or research.
- Record the title, URL, publisher, publication or update date, and access date when freshness matters.
- Keep provider-generated reports as research artifacts, not as authority.
- Cite the underlying sources when they are available. Cite a provider report only when the report itself is the subject.
- Mark each inference explicitly. Keep each unresolved disagreement visible.

## Recovery

- Missing CLI: use Perplexity next, then Parallel Search MCP when it helps. Do not install without authority.
- Missing Perplexity: continue with the CLI. Add an MCP verification lane only when it improves coverage.
- Missing MCP tool: finish with CLI and Perplexity evidence when that evidence is sufficient.
- Authentication failure: check `parallel-cli auth --json`, record the result, and reroute. Do not run `parallel-cli login` without authority.
- Rate limit: record it and reroute the lane to a different provider.
- Parallel `402` or insufficient balance: stop paid work. `parallel-cli balance get` shows the balance. Never run `parallel-cli balance add` without explicit approval.
- Lost run ID: use `parallel-cli memory retrieve "topic" --kind task --json` to find saved runs, then `poll` the run. If the run used a memory scope key, pass the same `--scope-key`. If Memory is not available, report the lost run. Do not start a new paid run for the same question without budget authority.
- Long-running task: keep its ID and output path, continue other lanes, and check back explicitly.
- Weak or uncited result: make the question narrower and run a targeted source-discovery lane. Do not repeat the same broad prompt.

## Official references

- https://docs.parallel.ai/integrations/cli
- https://docs.parallel.ai/integrations/mcp/search-mcp
- https://docs.parallel.ai/integrations/mcp/task-mcp
- https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server
