# Fan Solo sources

Use the live Solo runtime and current official docs as authority for behavior, schemas, and availability.

## Authority order

1. Current user authorization and project instructions.
2. Live Solo `whoami`, `help`, topic help, and enabled-tool discovery.
3. Current official docs, through `help(query="...")`, the hosted docs index, or `GET /api/v1/docs/search`.
4. Current product site/changelog for positioning and released-version claims.
5. First-party X posts for intent, examples, and product philosophy.

When sources conflict, runtime controls availability; official docs control supported behavior; product site controls public positioning; and X supplies author commentary.

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

## Live authority limits

- Discover available MCP tools at runtime; do not hard-code tool counts, ports, tokens, agent-tool IDs, or optional groups.
- Use first-party posts for intent and examples only, never as a changelog or schema source.
