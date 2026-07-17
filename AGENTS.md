# kalepail skills — agent guide

Personal, opinionated AI-agent skills for kalepail (Tyler van der Hoeven). Fleet model routing and tool preferences are baked into the skills on purpose. This file is the manifest for the fleet and for the third-party dependencies the skills expect.

## Model and agent fleet

Match model and effort to the lane; never route a pure-orchestrator or reviewer model as the coder.

| Lane | Model / effort |
|---|---|
| Plan, orchestrate, synthesize | Fable high (xhigh for the hardest); Sol high as alternate |
| Independent adversarial review | Fable high by default for Codex Sol work; otherwise use a model family different from the implementer |
| Implementation / coding | Codex Sol high (medium or xhigh as needed); Opus 4.8 high (xhigh as needed) |
| Prose, docs, comments | Opus 4.8, executing a Fable or Sol plan |
| Research, tool-calling, focused repo/docs sweeps | GPT-5.6 Terra, feeding an orchestrator/synthesizer |

Fable never codes. Grok is not a Solo built-in — add it as a custom Generic tool before spawning it. Discover launchable tools live with `list_agent_tools`; the table is intent, not proof a tool is installed and enabled.

Expanded fleet guidance — effort tiers, Solo built-in tool types, worker-prompt contracts — lives in `skills/fan-solo/references/house-style.md`; when routing changes, update its table too.

## Third-party dependencies

The skills orchestrate external tools; they do not bundle or authenticate them. Enable what a given skill needs:

- **Solo MCP** (`solo`) — required by `fan-solo` and every `solo-*` skill. Enable Solo's local MCP server: <https://soloterm.com/docs/integrations/mcp-server>
- **Parallel** — `solo-deep-research` prefers `parallel-cli` for reproducible saved artifacts, with Parallel Search / Task MCP as fallbacks.
- **Perplexity MCP** — `solo-deep-research` uses it as an independent reasoning and counter-evidence lane.
- **agent-browser** — `agent-browser-webauthn` drives passkey / Stellar smart-account browser tests via Chrome DevTools virtual WebAuthn authenticators.

Missing providers degrade to documented fallbacks, not hard failures.

## Conventions

- Skills follow the `SKILL.md` standard: `name` + `description` frontmatter, progressive disclosure (`SKILL.md` → `references/`, one hop deep), no re-teaching of base-model knowledge.
- Descriptions state what + when + trigger cues + an explicit "Do not use for…" exclusion, so sibling skills do not false-trigger on each other.
- Solo scratchpads and todos are **ephemeral but consumer-gated**: promote durable conclusions to repository docs, and retire a record — archive a scratchpad, delete a todo — only after its recorded consumers have consumed the current revision (scratchpads declare this in `## Retire after`). Mid-run cruft is acceptable; lost mid-cycle context is not.
- `agents/openai.yaml` in each skill is a skills.sh installer interface file (display name, prompt, tool deps), not an OpenAI format.
- This repo dogfoods itself: committed `.claude/skills` and `.agents/skills` symlinks point at `skills/`, so Claude Code and `.agents`-aware sessions here load the live skills. Route Solo work through the Fan Solo family while building it; a skill edit is picked up on its next invocation, while already-loaded instructions persist in the current conversation.
