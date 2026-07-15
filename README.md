# Kalepail Skills

Reusable AI-agent skills maintained by Kalepail.

## Skills

### Agent Browser WebAuthn Testing

- [Agent Browser WebAuthn](skills/agent-browser-webauthn/) — drive passkey and Stellar smart account browser tests with `agent-browser` and Chrome DevTools virtual WebAuthn authenticators.

### Fan Solo

[Fan Solo](skills/fan-solo/) routes broad Solo and SoloTerm requests to focused skills. Install router plus all 11 skills below.

**Setup and workspace**

- [Set up projects](skills/solo-set-up-projects/) — configure projects, `solo.yml`, and shared commands.
- [Customize workspace](skills/solo-customize-workspace/) — tune workspaces, navigation, appearance, settings, and notifications.

**Processes and services**

- [Run processes](skills/solo-run-processes/) — start, stop, restart, rename, and manage process lifecycle.
- [Observe services](skills/solo-observe-services/) — inspect status, output, ports, URLs, and readiness.
- [Troubleshoot](skills/solo-troubleshoot/) — diagnose project, discovery, trust, shell, CLI, API, and runtime failures.

**Agents and coordination**

- [Work with agents](skills/solo-work-with-agents/) — manage one bounded, owned Solo agent.
- [Orchestrate agents](skills/solo-orchestrate-agents/) — coordinate independent worker lanes and integrate verified results.

**Durable work**

- [Track todos](skills/solo-track-todos/) — keep actionable work, blockers, locks, comments, and handoffs.
- [Keep scratchpads](skills/solo-keep-scratchpads/) — preserve plans, research, decisions, evidence, and project context.
- [Save prompts](skills/solo-save-prompts/) — maintain reusable cross-agent prompt templates.

**Integration**

- [Automate](skills/solo-automate/) — use Solo MCP, CLI, local HTTP API, hosted API, and deep links.

## Install

### skills.sh CLI

List available skills, then install one selected skill explicitly:

```bash
npx skills add kalepail/skills --list
npx skills add kalepail/skills -g --skill agent-browser-webauthn -a claude-code -a codex -a opencode -y
```

Install every skill globally for Claude Code, Codex, and OpenCode:

```bash
npx skills add kalepail/skills -g --skill '*' -a claude-code -a codex -a opencode -y
```

Replace `agent-browser-webauthn` with any listed skill name. Use it alone for WebAuthn and passkey testing through `agent-browser`. Install `fan-solo` plus every `solo-*` skill for the complete Fan Solo collection.

Install Fan Solo without the unrelated WebAuthn skill:

```bash
npx skills add kalepail/skills -g -a claude-code -a codex -a opencode -y --skill fan-solo solo-set-up-projects solo-customize-workspace solo-run-processes solo-observe-services solo-troubleshoot solo-work-with-agents solo-orchestrate-agents solo-track-todos solo-keep-scratchpads solo-save-prompts solo-automate
```

### Claude Code

The Claude marketplace offers two alternatives. Install the complete collection:

```bash
claude plugin marketplace add kalepail/skills
claude plugin install kalepail-skills@kalepail-skills
```

Or install Agent Browser WebAuthn alone:

```bash
claude plugin marketplace add kalepail/skills
claude plugin install agent-browser-webauthn@kalepail-skills
```

### Codex

The Codex marketplace installs the complete general collection:

```bash
codex plugin marketplace add kalepail/skills
codex plugin add kalepail-skills@kalepail-skills
```

Use the skills.sh CLI above when only selected Codex skills are wanted.

### OpenCode

Use the skills.sh CLI above. OpenCode natively discovers shared `.agents/skills` project installs and `~/.agents/skills` global installs. No `.opencode/` mirror or plugin is needed.

### Grok

Grok reads Claude-compatible plugins directly. Install one of these alternatives:

```bash
# Complete collection
grok plugin install kalepail/skills

# Agent Browser WebAuthn only
grok plugin install kalepail/skills#skills/agent-browser-webauthn
```

Review Grok's trust prompt before enabling either plugin. No `.grok/` mirror is needed.

### Manual fallback

Clone repository and copy chosen `skills/<name>` directories into the agent's supported skill directory:

```bash
git clone https://github.com/kalepail/skills.git
```

Keep each skill directory intact so its scripts, references, evals, and metadata remain available.

## Use

For broad or mixed Solo work, ask:

```text
Use $fan-solo to choose and run the right Solo workflow for this task.
```

For one clearly scoped task, invoke matching `$solo-*` skill directly. Fan Solo expects local Solo MCP dependency named `solo`; it checks live identity, help, and documentation before static guidance.

Before using Fan Solo in any host, enable Solo's local MCP server and configure that host to connect to it. Follow [Solo's MCP setup](https://soloterm.com/docs/integrations/mcp-server); the skill plugins do not bundle or authenticate Solo itself.

## Research and status

Architecture derives from [OpenAI and Anthropic skill best practices](research/fan-solo/skill-best-practices.md) plus Solo research on [product docs](research/fan-solo/solo-product-docs.md), [MCP and APIs](research/fan-solo/solo-mcp-api.md), [coordination](research/fan-solo/solo-coordination.md), and [first-party X posts](research/fan-solo/solo-x-research.md). Anonymized project and session research informed house style but is intentionally excluded from publishable files. Research snapshot: 2026-07-15.

Fan Solo is unofficial community work. Not affiliated with, endorsed by, or maintained by Solo, SoloTerm, OpenAI, or Anthropic. Product names belong to respective owners.
