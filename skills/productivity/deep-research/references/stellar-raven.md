# Stellar Raven research guide

Stellar Raven MCP is the unified Stellar-ecosystem gateway: `search` discovers service operations and runnable skills; `execute` composes discovered operations in sandboxed JavaScript. For any Stellar-ecosystem question — protocol history, SEPs and CAPs, ecosystem projects and events, official docs wording, on-chain data — it is the first discovery surface, ahead of general web providers.

Raven is a discovery surface, not final authority. Verify consequential claims against the underlying primary source or an independent source family: official docs for protocol wording, RPC or Horizon for live chain state, primary records or general web for ecosystem claims.

## Workflow

1. Classify the claim scope and plan candidate source families.
2. Call `search` once per family with targeted vocabulary. Operation and skill ids are exact-match — never guess them; discover mid-script with `codemode.search(...)`.
3. Write one `execute` script: `Promise.all` for independent calls, then result-parameterized follow-ups. Payloads live under `.data` (`r.data.projects`, never `r.projects`).
4. Read runnable-skill sections with `codemode.skill.read(id, { sections })`; run whole pipelines with `codemode.skill.run("<exact id>", input)`.

## Source roles

Discover the live catalog each session; these roles orient, they do not enumerate:

| Question shape | Prefer |
|---|---|
| Cited history, standards, audits, incidents, "what does the SEP or spec say" | `scout.searchResearch` (source filters: `audit`, `incident`, `sep`, `cap`, `paper`, …) |
| Ecosystem content, events, spoken material, "what has been said about X" | `lumenloop.search_content_semantic` (dated, cite the returned URL) |
| Official technical wording and current docs truth | `stellarDocs.search_docs` and its facet variants |
| Live chain state or entity detail | operations discovered via `search` for the specific service |

## Result discipline

- Every call resolves to `{ ok: true, data }` or `{ ok: false, error: { kind, message, hint? } }`. `soft-empty` is inconclusive — never evidence of absence.
- For open-world identity, history, or topic questions, ok-but-empty, adjacent, or merely semantic candidates are also inconclusive. Make one bounded broad recovery pass (for example a semantic content search) before reporting a negative, then stop.
- Attribution requires exact identity or canonical slug plus source and date; otherwise report the claim as unverified.
- Cite the returned URL and date, not the Raven call that produced it.
- Keep calls targeted: smallest useful surface first, then cross-check only consequential unresolved claims against primary docs or general web lanes.
- Truncated results include a source-basis block; read any listed artifact via `codemode.artifact.read(id)` in a later `execute` and project a compact result.
