![kalepail Skills](public/header.png)

# kalepail Skills

Personal, opinionated AI-agent skills by [Tyler van der Hoeven](https://github.com/kalepail). The collection works across Claude Code, Codex, OpenCode, and Grok.

Skills use plain task names and live in three categories: engineering, productivity, and Solo.

## Skills

### Engineering

Technical testing skills. See the [engineering catalog](skills/engineering/README.md).

- [Agent Browser WebAuthn](skills/engineering/agent-browser-webauthn/) — test passkey, WebAuthn, wallet, and Stellar smart-account browser flows.

### Productivity

General workflows that are not tied to one product. See the [productivity catalog](skills/productivity/README.md).

- [Deep research](skills/productivity/deep-research/) — produce cited syntheses from independent evidence lanes.
- [Routing agent work](skills/productivity/routing-agent-work/) — choose an agent CLI, model, effort, fallback, reviewer, and report contract.

### Solo

[Fan Solo](skills/solo/fan-solo/) routes broad Solo and SoloTerm requests. See the [Solo catalog](skills/solo/README.md).

**Setup and workspace**

- [Set up projects](skills/solo/solo-set-up-projects/) — configure projects, `solo.yml`, and shared commands.
- [Customize workspace](skills/solo/solo-customize-workspace/) — configure workspaces, navigation, appearance, settings, and notifications.

**Processes and services**

- [Run processes](skills/solo/solo-run-processes/) — control process lifecycle and restart behavior.
- [Observe services](skills/solo/solo-observe-services/) — inspect status, output, ports, URLs, and readiness.
- [Troubleshoot](skills/solo/solo-troubleshoot/) — diagnose project, trust, shell, CLI, API, and runtime failures.

**Agents and coordination**

- [Work with agents](skills/solo/solo-work-with-agents/) — manage one bounded, owned Solo agent.
- [Orchestrate agents](skills/solo/solo-orchestrate-agents/) — coordinate independent Solo worker lanes and verified integration.

**Durable work**

- [Track todos](skills/solo/solo-track-todos/) — maintain actionable work, blockers, locks, comments, and handoffs.
- [Keep scratchpads](skills/solo/solo-keep-scratchpads/) — preserve plans, research, decisions, evidence, and project context.
- [Close out work](skills/solo/solo-close-out-work/) — promote durable conclusions and retire completed temporary state.
- [Save prompts](skills/solo/solo-save-prompts/) — maintain reusable Solo prompt templates.

**Integration**

- [Automate](skills/solo/solo-automate/) — use Solo MCP, CLI, local HTTP API, hosted API, and deep links.

## Requirements

Skills orchestrate external tools; they do not bundle or authenticate them.

- **Solo MCP** — required by `fan-solo` and every `solo-*` skill. Enable [Solo's local MCP server](https://soloterm.com/docs/integrations/mcp-server) and connect your agent host to it.
- **A fan-out vehicle** — optional for `deep-research`. It runs lanes sequentially when no orchestration vehicle exists.
- **Optional research providers** — `deep-research` prefers Parallel CLI and uses Perplexity as an independent lane. It uses Stellar Raven first for Stellar questions.
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

# install the Solo category without the other categories
npx skills add kalepail/skills -g -a claude-code -a codex -a opencode -y --skill fan-solo solo-set-up-projects solo-customize-workspace solo-run-processes solo-observe-services solo-troubleshoot solo-work-with-agents solo-orchestrate-agents solo-track-todos solo-keep-scratchpads solo-close-out-work solo-save-prompts solo-automate
```

### Claude Code

```bash
claude plugin marketplace add kalepail/skills

# complete collection
claude plugin install kalepail-skills@kalepail-skills

# install Agent Browser WebAuthn alone
claude plugin install agent-browser-webauthn@kalepail-skills
```

### Codex

```bash
npx skills add kalepail/skills -g -a codex -y --skill '*'
```

Use `--skill <name>` when only selected Codex skills are wanted. The repository does not ship a native Codex plugin.

### OpenCode

Use the skills.sh CLI above. OpenCode natively discovers `.agents/skills` project installs and `~/.agents/skills` global installs; no mirror or plugin is needed.

### Grok

Grok reads Claude-compatible plugins directly:

```bash
# complete collection
grok plugin install kalepail/skills

# Agent Browser WebAuthn only
grok plugin install kalepail/skills#skills/engineering/agent-browser-webauthn
```

Review Grok's trust prompt before enabling.

### Manual

```bash
git clone https://github.com/kalepail/skills.git
```

Copy chosen `skills/<category>/<name>` directories intact into your agent's skill directory.

## Use

For broad or mixed Solo work:

```text
Use $fan-solo to choose and run the right Solo workflow for this task.
```

For one clearly scoped Solo task, invoke the matching `$solo-*` skill directly.

Use `$routing-agent-work` when delegated lanes need model and effort selection. Use `$deep-research` for deep, cross-checked research.

Use `$agent-browser-webauthn` with `$agent-browser` for virtual WebAuthn browser tests.

These skills are personal and opinionated: model routing and tool preferences are baked in. [AGENTS.md](AGENTS.md) is the guide for working in this repo.

## Research

Architecture derives from [skill authoring research](research/skill-best-practices.md) and [agent-routing research](research/agent-routing.md). Solo evidence lives under [research/fan-solo](research/fan-solo/).

## Status and license

Unofficial community work, licensed [Apache-2.0](LICENSE). Not affiliated with, endorsed by, or maintained by Solo, SoloTerm, OpenAI, or Anthropic. Product names belong to their respective owners.
