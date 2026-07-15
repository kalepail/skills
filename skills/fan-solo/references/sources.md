# Fan Solo sources

Research snapshot: 2026-07-15. Use live Solo runtime and current official docs before these static notes when behavior may have changed.

## Maintainer research basis

These provenance records live in the repository, not the standalone skill package, and are not required at runtime.

- [Skill best practices](https://github.com/kalepail/skills/blob/main/research/fan-solo/skill-best-practices.md) — OpenAI/Anthropic skill architecture, triggering, disclosure, evals, and portability.
- [Solo product docs synthesis](https://github.com/kalepail/skills/blob/main/research/fan-solo/solo-product-docs.md) — product hierarchy, UI, projects, processes, settings, and official documentation map.
- [Solo MCP/API synthesis](https://github.com/kalepail/skills/blob/main/research/fan-solo/solo-mcp-api.md) — MCP, CLI, local HTTP, deep links, hosted API, schemas, discovery, and safety.
- [Solo coordination synthesis](https://github.com/kalepail/skills/blob/main/research/fan-solo/solo-coordination.md) — agent ownership, spawning, timers, locks, KV, scratchpads, todos, handoffs, and completion.
- [Solo X research](https://github.com/kalepail/skills/blob/main/research/fan-solo/solo-x-research.md) — first-party product philosophy and workflow examples from Aaron Francis; narrative evidence, not API authority.

House style also reflects anonymized local project and session research. Raw local evidence and machine-specific reports are intentionally not shipped.

## Authority order

1. Current user authorization and project instructions.
2. Live Solo `whoami`, `help`, topic help, and enabled-tool discovery.
3. Live Solo Docs MCP/current official docs.
4. Current product site/changelog for positioning and released-version claims.
5. First-party X posts for intent, examples, and product philosophy.
6. Local research syntheses above.

When sources conflict, runtime controls availability; official docs control supported behavior; product site controls public positioning; X supplies author commentary; local audit supplies user-specific convention.

## Official entry points

- [Solo product](https://soloterm.com/)
- [Solo docs](https://soloterm.com/docs)
- [Raw docs index](https://soloterm.com/api/v1/docs)
- [MCP overview](https://soloterm.com/api/v1/docs/mcp-tools/overview)
- [Agent orchestration workflow](https://soloterm.com/api/v1/docs/workflows/agent-orchestration)
- [Scratchpads and todos as agent memory](https://soloterm.com/api/v1/docs/workflows/scratchpads-and-todos)
- [MCP server integration](https://soloterm.com/api/v1/docs/integrations/mcp-server)
- [CLI overview](https://soloterm.com/api/v1/docs/cli/overview)
- [Local HTTP API](https://soloterm.com/api/v1/docs/integrations/http-api)
- [Deep links](https://soloterm.com/api/v1/docs/integrations/deep-links)
- [Changelog](https://soloterm.com/changelog)

## Known snapshot limits

- Queried runtime exposed 95 MCP tools while hosted docs described additional version-dependent workspace tools. Discover live availability.
- Solo product and integrations continue changing; do not hard-code counts, ports, tokens, agent tool IDs, or optional groups.
- X corpus is sampled and incomplete. Do not use it as complete changelog or schema source.
