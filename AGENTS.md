<!-- headroom:rtk-instructions -->
# RTK (Rust Token Killer) - Token-Optimized Commands

When running shell commands, **always prefix with `rtk`**. This reduces context
usage by 60-90% with zero behavior change. If rtk has no filter for a command,
it passes through unchanged — so it is always safe to use.

## Key Commands
```bash
# Git (59-80% savings)
rtk git status          rtk git diff            rtk git log

# Files & Search (60-75% savings)
rtk ls <path>           rtk read <file>         rtk grep <pattern>
rtk find <pattern>      rtk diff <file>

# Test (90-99% savings) — shows failures only
rtk pytest tests/       rtk cargo test          rtk test <cmd>

# Build & Lint (80-90% savings) — shows errors only
rtk tsc                 rtk lint                rtk cargo build
rtk prettier --check    rtk mypy                rtk ruff check

# Analysis (70-90% savings)
rtk err <cmd>           rtk log <file>          rtk json <file>
rtk summary <cmd>       rtk deps                rtk env

# GitHub (26-87% savings)
rtk gh pr view <n>      rtk gh run list         rtk gh issue list

# Infrastructure (85% savings)
rtk docker ps           rtk kubectl get         rtk docker logs <c>

# Package managers (70-90% savings)
rtk pip list            rtk pnpm install        rtk npm run <script>
```

## Rules
- In command chains, prefix each segment: `rtk git add . && rtk git commit -m "msg"`
- For debugging, use raw command without rtk prefix
- `rtk proxy <cmd>` runs command without filtering but tracks usage
<!-- /headroom:rtk-instructions -->

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

- **Fable** orchestrates, reviews, and synthesizes — and is a strong independent adversarial reviewer. It does not code.
- **Codex Sol** is the default coder (high; drop to medium or step to xhigh as needed). **Opus 4.8** also codes and writes prose against a Sol or Fable plan.
- Consequential independent review must use a different model family from the implementation; when Codex Sol writes the change, prefer Fable for review.
- **GPT-5.6 Terra** runs focused sub / sub-sub tool-calling lanes (for example, driving `parallel-cli` in a subagent) and hands structured evidence up to a root Sol or Fable agent.
- **Grok** (xAI) is available but is **not** a Solo built-in — add it as a custom Generic tool in Solo before spawning it.
- Solo built-in agent tool types: Claude, Codex, Amp, Gemini, OpenCode, Copilot, Kimi. Discover launchable tools live with `list_agent_tools`; this table is intent, not proof a tool is installed and enabled.

The canonical copy of this routing lives in `skills/fan-solo/references/house-style.md`; keep the two in sync.

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
- Keep Solo scratchpads and todos **ephemeral**: they guide live and legitimately backlogged work only. Complete or backlog todos as lanes finish, archive scratchpads when a run goes cold, and promote durable conclusions to repository docs.
- `agents/openai.yaml` in each skill is a skills.sh installer interface file (display name, prompt, tool deps), not an OpenAI format.
