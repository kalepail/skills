![kalepail Skills](public/header.png)

# kalepail Skills

Personal, opinionated AI-agent skills by [Tyler van der Hoeven](https://github.com/kalepail), portable across Claude Code, Codex, OpenCode, and Grok, in three families: **Fan Solo**, a router plus focused `solo-*` skills for driving [Solo](https://soloterm.com) (SoloTerm); **Kalepail house skills**, `kalepail-*` workflows tuned to Tyler's own tool stack; and **Agent Browser WebAuthn**, standalone passkey and Stellar smart-account browser testing through `agent-browser`.

## Skills

### Fan Solo

[Fan Solo](skills/fan-solo/) routes broad Solo and SoloTerm requests to the focused skills below. Install the router together with all of them.

**Setup and workspace**

- [Set up projects](skills/solo-set-up-projects/) — configure projects, `solo.yml`, and shared commands.
- [Customize workspace](skills/solo-customize-workspace/) — tune workspaces, navigation, appearance, settings, and notifications.

**Processes and services**

- [Run processes](skills/solo-run-processes/) — start, stop, restart, rename, and manage process lifecycle.
- [Observe services](skills/solo-observe-services/) — inspect status, output, ports, URLs, and readiness.
- [Troubleshoot](skills/solo-troubleshoot/) — diagnose project, discovery, trust, shell, CLI, API, and runtime failures.

**Agents and coordination**

- [Work with agents](skills/solo-work-with-agents/) — manage one bounded, owned Solo agent.
- [Orchestrate agents](skills/solo-orchestrate-agents/) — coordinate independent worker lanes—implementation, review, or evidence-gathering—and integrate verified results.

**Durable work**

- [Track todos](skills/solo-track-todos/) — keep actionable work, blockers, locks, comments, and handoffs.
- [Keep scratchpads](skills/solo-keep-scratchpads/) — preserve plans, research, decisions, evidence, and project context.
- [Close out work](skills/solo-close-out-work/) — reconcile a finished run: promote durable conclusions to repo docs, then retire completed ephemeral copies without losing incomplete work.
- [Save prompts](skills/solo-save-prompts/) — maintain reusable cross-agent prompt templates.

**Integration**

- [Automate](skills/solo-automate/) — use Solo MCP, CLI, local HTTP API, hosted API, and deep links.

### Kalepail house skills

Personal `kalepail-*` workflows tuned to Tyler's own stack. They compose with Fan Solo when it is installed but do not require it.

- [Deep research](skills/kalepail-deep-research/) — cited multi-lane research synthesis across Parallel CLI/MCP, Perplexity MCP, and Stellar Raven (the first discovery surface for Stellar-ecosystem questions), with optional Solo fan-out.

### Agent Browser WebAuthn

Standalone; tied to neither family.

- [Agent Browser WebAuthn](skills/agent-browser-webauthn/) — drive passkey and Stellar smart account browser tests with `agent-browser` and Chrome DevTools virtual WebAuthn authenticators.

## Requirements

Skills orchestrate external tools; they do not bundle or authenticate them.

- **Solo MCP** — required by `fan-solo` and every `solo-*` skill; optional for `kalepail-deep-research`, which runs sequentially without it. Enable [Solo's local MCP server](https://soloterm.com/docs/integrations/mcp-server) and connect your agent host to it.
- **Optional research providers** — `kalepail-deep-research` prefers Parallel CLI, falls back to Parallel Search/Task MCP, uses Perplexity MCP as an independent lane, and uses Stellar Raven MCP as the first discovery surface for Stellar-ecosystem questions; missing providers degrade to documented fallbacks.
- **agent-browser and Node.js 22+** — Agent Browser WebAuthn requires the `agent-browser` CLI and Node.js 22 or newer; the `$agent-browser` skill is recommended but not bundled here.

## Install

### skills.sh CLI

```bash
# list available skills
npx skills add kalepail/skills --list

# install everything globally for Claude Code, Codex, and OpenCode
npx skills add kalepail/skills -g --skill '*' -a claude-code -a codex -a opencode -y

# install one skill
npx skills add kalepail/skills -g --skill agent-browser-webauthn -a claude-code -a codex -a opencode -y

# install Fan Solo without the other families
npx skills add kalepail/skills -g -a claude-code -a codex -a opencode -y --skill fan-solo solo-set-up-projects solo-customize-workspace solo-run-processes solo-observe-services solo-troubleshoot solo-work-with-agents solo-orchestrate-agents solo-track-todos solo-keep-scratchpads solo-close-out-work solo-save-prompts solo-automate
```

### Claude Code

```bash
claude plugin marketplace add kalepail/skills

# complete collection
claude plugin install kalepail-skills@kalepail-skills

# or Agent Browser WebAuthn alone
claude plugin install agent-browser-webauthn@kalepail-skills
```

### Codex

```bash
codex plugin marketplace add kalepail/skills
codex plugin add kalepail-skills@kalepail-skills
```

Use the skills.sh CLI when only selected Codex skills are wanted.

### OpenCode

Use the skills.sh CLI above. OpenCode natively discovers `.agents/skills` project installs and `~/.agents/skills` global installs; no mirror or plugin is needed.

### Grok

Grok reads Claude-compatible plugins directly:

```bash
# complete collection
grok plugin install kalepail/skills

# Agent Browser WebAuthn only
grok plugin install kalepail/skills#skills/agent-browser-webauthn
```

Review Grok's trust prompt before enabling.

### Manual

```bash
git clone https://github.com/kalepail/skills.git
```

Copy chosen `skills/<name>` directories intact into your agent's skill directory.

## Use

For broad or mixed Solo work:

```text
Use $fan-solo to choose and run the right Solo workflow for this task.
```

For one clearly scoped task, invoke the matching `$solo-*` skill directly. For passkey testing, use `$agent-browser-webauthn` with `$agent-browser` to drive a flow against a virtual WebAuthn authenticator.

These skills are personal and opinionated: model routing and tool preferences are baked in. [AGENTS.md](AGENTS.md) is the guide for working in this repo.

## Research

Architecture derives from [OpenAI and Anthropic skill best practices](research/skill-best-practices.md) plus Solo research on [product docs](research/fan-solo/solo-product-docs.md), [MCP and APIs](research/fan-solo/solo-mcp-api.md), [coordination](research/fan-solo/solo-coordination.md), and [first-party X posts](research/fan-solo/solo-x-research.md).

## Status and license

Unofficial community work, licensed [Apache-2.0](LICENSE). Not affiliated with, endorsed by, or maintained by Solo, SoloTerm, OpenAI, or Anthropic. Product names belong to their respective owners.
