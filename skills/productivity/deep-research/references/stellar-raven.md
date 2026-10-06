# Stellar Raven research guide

Stellar Raven MCP is the unified Stellar-ecosystem gateway. Its `search` tool discovers service operations and runnable skills. Its `execute` tool composes the discovered operations in sandboxed JavaScript. Use Raven as the first discovery surface for each Stellar-ecosystem question: protocol history, SEPs and CAPs, ecosystem projects, funding, audits, events, and official docs wording. The Raven catalog covers content, research, directories, skills, and docs. It does not cover live chain state. For balances, ledgers, transactions, and contract state, use Stellar RPC or Horizon directly.

Raven is a discovery surface, not the final authority. Verify each consequential claim against the underlying primary source or an independent source family. Use official docs for protocol wording, RPC or Horizon for live chain state, and primary records or general web for ecosystem claims.

## Workflow

1. Classify the claim scope. Plan a primary source family and a corroborating family.
2. Call `search` once for each family, with targeted vocabulary. Use the `service` and `kind` filters when you know the family. Operation and skill ids are exact-match. Never guess an id. Discover ids mid-script with `codemode.search(...)`.
3. Write one `execute` script. Use `Promise.all` for independent calls, then make follow-up calls from the results. Payloads are under `.data` (`r.data.projects`, never `r.projects`).
4. When a signature shows a stubbed output type, get the full shape with `codemode.describe("<exact id>")` inside `execute`.
5. Read skill sections with `codemode.skill.read(id, { sections })`. Run a whole runnable skill with `codemode.skill.run("<exact id>", input)`. The constituent calls are in `data.calls`.

## Source roles

Discover the live catalog in each session. These roles give orientation. They are not a complete list:

| Question shape | Prefer |
|---|---|
| Cited history, standards, audits, incidents, release notes, "what does the SEP or spec say" | `scout.searchResearch` (with a `source` or `sources` filter such as `sep`, `cap`, `audit`, `incident`, `release`, `paper`) |
| Ecosystem content and events, "what has been said about X" | `lumenloop.search_content_semantic` (dated rows; cite the returned URL) |
| Spoken material in talks, videos, and podcasts | `lumenloop.find_av_passages` (cite the link and the passage summary) |
| Official technical wording and current docs truth | `stellarDocs.search_docs` and its topic variants |
| Projects, repos, people, funding, and audit registries | the `scout` or `lumenloop` directory operations that `search` returns |
| A tested multi-step pipeline, such as a dated ecosystem digest | a `skills.*` hit; run it with `codemode.skill.run` when its signature shows that line |

## Result discipline

- Each call resolves to `{ ok: true, data }` or `{ ok: false, error: { kind, message, hint? } }`. A `soft-empty` result is inconclusive. It is never evidence of absence.
- For an open-world identity, history, or topic question, an ok result that is empty, adjacent, or only a semantic candidate is also inconclusive. Make one bounded broad recovery pass, such as a semantic content search, before you report a negative. Then stop. Say "not found in these sources", not "does not exist".
- When a lookup stays empty or weak, call `search` again with `recoverFrom` (the exact ids that you tried) and a `reason`. Use only the recovery candidates that fit.
- Attribution requires exact identity or a canonical slug, plus a source and a date. If one is missing, report the claim as unverified.
- Cite the returned URL and date, not the Raven call that produced it. Give each volatile value its as-of date.
- Keep calls targeted. Use the smallest useful surface first. Then cross-check only the consequential unresolved claims against primary docs or general-web lanes.
- A truncated result lists its artifacts. Read each listed artifact with `codemode.artifact.info(id)` and `codemode.artifact.read(id)` in a later `execute`, and return a compact projection.
