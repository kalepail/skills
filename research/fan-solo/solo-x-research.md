# Solo / SoloTerm — Official X Research (@aarondfrancis)

**Research date:** 2026-07-15
**Primary source:** [@aarondfrancis](https://x.com/aarondfrancis) (Aaron Francis)
**Product site:** https://soloterm.com/
**Official changelog (supplementary, not X):** https://soloterm.com/changelog
**Discord (mentioned on X):** https://discord.com/invite/dwU3HQgXMd

**Scope:** Posts, threads, replies, screenshots, videos/demos, and launch/changelog commentary about Solo / SoloTerm — workflows, philosophy, shortcuts, agents, commands, terminals, todos, scratchpads, MCP, APIs, implementation tips.
**Method:** X keyword/semantic search (`from:aarondfrancis`), thread fetches, web search, media download to `research/fan-solo/x-evidence/`.
**Not in scope of this file:** Editing any skill files.

---

## Executive summary

Solo evolved from a **Laravel multi-process TUI package** (2024) into a **desktop “agentic meta-harness”** (2026) at [soloterm.com](https://soloterm.com/). Aaron’s X presence is the richest public narrative of:

1. **Dev-stack process manager** → detect processes, `solo.yml`, start/stop/restart, free tier
2. **Agent workspace** → run Claude / Codex / Amp / Gemini / etc. as real CLI terminals inside Solo
3. **Solo MCP** → agents spawn agents, read/write terminals (PTY I/O), durable todos & scratchpads, wakeup timers, locks, optional k/v
4. **Orchestration workflows** → plan → multi-agent review on shared scratchpad → timers → build → review vs plan
5. **Multi-project / multi-repo** → projects as lightweight scopes, not hard boundaries
6. **Implementation stack** → Tauri + React/TS UI + Rust PTY/vt100 + custom frontend renderer; stdio MCP; progressive tool discovery

**Catchphrase pattern on X (2026-07):** “https://soloterm.com/ it's very good” — repeated endorsement replies.

---

## Account & product identity

| Item | Detail | Source |
|------|--------|--------|
| Handle | `@aarondfrancis` | Profile |
| Bio links | faster.dev, soloterm.com, DatabaseSchool.com, @MostlyTechPod | Profile |
| Followers (snapshot) | ~61k | X user search 2026-07-15 |
| Product names | “Solo”, “SoloTerm”, soloterm.com | Launch + site |
| Brand umbrella | faster.dev | Launch thread |
| Related open-source lineage | `soloterm/solo` (Laravel), dumps, notify, screen, grapheme | Packagist / GitHub / early X |

---

## Timeline of major public milestones (from X)

| Date (UTC) | Event | Post ID / URL |
|------------|--------|----------------|
| 2024-11-07 | **Solo for Laravel** open-source release (`php artisan solo`) | [1854585789726048509](https://x.com/aarondfrancis/status/1854585789726048509) |
| 2025-01-31 | Terminal GUI tour (PHP TUI) YouTube | [1885376322152624148](https://x.com/aarondfrancis/status/1885376322152624148) |
| 2025-03-20 | `soloterm/dumps` package extracted from Solo | [1902774090206749089](https://x.com/aarondfrancis/status/1902774090206749089) |
| 2026-02-06 | **Desktop Solo public launch** (Mac, free ≤3 projects) | [2019832589482356878](https://x.com/aarondfrancis/status/2019832589482356878) |
| 2026-02-09 | Users run Claudes/Codex **inside** Solo; “bigger than imagined” | [2020904631862174148](https://x.com/aarondfrancis/status/2020904631862174148) |
| 2026-02-19 | Early feedback on “Solo vNext” | [2024560175625953672](https://x.com/aarondfrancis/status/2024560175625953672) |
| 2026-03-08 | Beta → 25% rollout of new desktop app | [2030725472443683225](https://x.com/aarondfrancis/status/2030725472443683225) |
| 2026-03-13 | **New Solo app GA-style release** (agents + terminals + devstack; free tier increased) | [2032570894040613354](https://x.com/aarondfrancis/status/2032570894040613354) |
| 2026-04-08 | Todos + markdown scratchpads + agent MCP R/W/comment | [2041919379307184295](https://x.com/aarondfrancis/status/2041919379307184295) |
| 2026-04-20–22 | Terminal rewrite payoff; **“Your terminal now has an MCP”** | [2046707759324782640](https://x.com/aarondfrancis/status/2046707759324782640), [2047079877489164714](https://x.com/aarondfrancis/status/2047079877489164714) |
| 2026-04-27 | Live broadcast: “Testing a New Solo Version” | [2048851167787237403](https://x.com/aarondfrancis/status/2048851167787237403) |
| 2026-04-29–30 | Auto-summaries; MCP philosophy; “spoken more to Solo than Ghostty” | Multiple (see below) |
| 2026-05-15 | **v0.7.0 changelog** teaser + link to soloterm.com/changelog | [2055388298722328906](https://x.com/aarondfrancis/status/2055388298722328906) |
| 2026-05-24 | Agent spawns terminal for sudo password flow | [2058610122197274684](https://x.com/aarondfrancis/status/2058610122197274684) |
| 2026-05-25 | **JS sandbox / routines** (worktrees) preview | [2058990625081446527](https://x.com/aarondfrancis/status/2058990625081446527) |
| 2026-06-09 | **Prompt templates** shipped | [2064420770667762155](https://x.com/aarondfrancis/status/2064420770667762155) |
| 2026-06-11 | Dev env as first-class (Stripe CLI as Solo command) | [2065086701446275115](https://x.com/aarondfrancis/status/2065086701446275115) |
| 2026-06-12 | Team licensing | [2065530410612768889](https://x.com/aarondfrancis/status/2065530410612768889) |
| 2026-07-09 | **Canonical multi-agent orchestration workflow** (most detailed) | [2075213903332581379](https://x.com/aarondfrancis/status/2075213903332581379) |
| 2026-07-10 | **MCP progressive disclosure** design essay | [2075571055041675691](https://x.com/aarondfrancis/status/2075571055041675691) |
| 2026-07-12–14 | Stack notes (Tauri/vt100); multi-repo; stored prompts vs skills; Ghostty/MCP control | Multiple |

---

## 1. Philosophy & product framing

### 1.1 What Solo is (Aaron’s words)

| Theme | Exact / near-exact quotes | URL | Date |
|-------|---------------------------|-----|------|
| Dev stack manager (launch) | “It's a desktop app that manages your entire dev stack.” | [2019832589482356878](https://x.com/aarondfrancis/status/2019832589482356878) | 2026-02-06 |
| Always-on stack + agents | “I view solo as your always running dev stack handler, meant to be used alongside your terminal where you're working with your agents.” | [2020831314543563002](https://x.com/aarondfrancis/status/2020831314543563002) | 2026-02-09 |
| All-in-one agentic env | “Solo - your ALL IN ONE agentic dev environment” | [2041604026748342502](https://x.com/aarondfrancis/status/2041604026748342502) | 2026-04-07 |
| Meta-harness | “Solo is a meta-harness, doesn't compete with OpenCode, Codex, Pi, Amp, etc” | [2050981218754105486](https://x.com/aarondfrancis/status/2050981218754105486) | 2026-05-03 |
| Harness of harnesses | “A harness for your favorite harness” | [2056880989536727211](https://x.com/aarondfrancis/status/2056880989536727211) | 2026-05-19 |
| Meta harness capabilities | “Solo excels as a meta harness in that processes can talk to each other, control each other, coordinate, write durable markdown + todos, etc.” | [2065546707497099666](https://x.com/aarondfrancis/status/2065546707497099666) | 2026-06-12 |
| More than chats | “it treats your dev env as more than just a dumb series of chats.” | [2065086701446275115](https://x.com/aarondfrancis/status/2065086701446275115) | 2026-06-11 |
| Real CLIs, not wrappers | “Solo uses the real claude cli, it's "just" a terminal at the end of the day” | [2055310004937236985](https://x.com/aarondfrancis/status/2055310004937236985) | 2026-05-15 |
| Claude -p safety | “Fortunately, Solo … uses the real Claude CLI, so we're safe.” | [2054619137817678286](https://x.com/aarondfrancis/status/2054619137817678286) | 2026-05-13 |
| Not an editor product | “Solo doesn't speak to the editor. The underlying tools might! I don't think editors are the future though” | [2033288908142702763](https://x.com/aarondfrancis/status/2033288908142702763) | 2026-03-15 |
| Diff from tmux | “I remember when I first released Solo and people made fun of me because "lol tmux exists." Glad I didn't listen to them” | [2049843097891111420](https://x.com/aarondfrancis/status/2049843097891111420) | 2026-04-30 |
| Human-built products | “Products are built by humans, and I'm leaning into that. Added a new section to the Solo homepage.” | [2035067821718208513](https://x.com/aarondfrancis/status/2035067821718208513) | 2026-03-20 |
| Dogfooding | “it's super hard to develop Solo without using Solo.” | [2041919379307184295](https://x.com/aarondfrancis/status/2041919379307184295) | 2026-04-08 |
| AI-built product | “I built https://soloterm.com/ solo, and there's no way I would've even gotten close without AI.” | [2036157484079984948](https://x.com/aarondfrancis/status/2036157484079984948) | 2026-03-23 |
| Editor usage | “I've never opened the editor for https://soloterm.com/ but I am intimately familiar with the structure of the code. I primarily work with one agent at a time, have very strict guardrails…” | [2074853190709690594](https://x.com/aarondfrancis/status/2074853190709690594) | 2026-07-08 |

### 1.2 Design principles (MCP / surface)

From [2075571055041675691](https://x.com/aarondfrancis/status/2075571055041675691) (2026-07-10):

- Progressive disclosure for agents: slim initial context, detailed docs on demand
- Prefer **boring, typed MCP** inspectable by every client over runtime-specific “Code Mode” SDKs
- “I want Solo’s public surface to remain boring, typed MCP that every client can inspect and call. Smarter clients can always layer Code Mode on top!” — [2075575821549670853](https://x.com/aarondfrancis/status/2075575821549670853)
- Solo MCP is **stdio-only**; “never uses that HTTP session header” — [2075675276772512047](https://x.com/aarondfrancis/status/2075675276772512047)
- Feature flags: disabled tools disappear from discovery — “if someone turns off the e.g. todo tools, the Solo MCP doesn't expose them any more” — [2075717542396477766](https://x.com/aarondfrancis/status/2075717542396477766)
- Deterministic enablement via DB for k/v, scratchpads, etc. — [2075681938250072483](https://x.com/aarondfrancis/status/2075681938250072483)

### 1.3 Skills vs stored prompts

> “I encode best practices into stored prompts (a solo primitive) and they usually abide by them pretty strictly. I'm somewhat down on skills atm, preferring just c&p prompts (which solo has a nice affordance for)”
> — [2077143606469538241](https://x.com/aarondfrancis/status/2077143606469538241) (2026-07-14)

Prompt templates marketed as:

> “Think of them like skills, but they work across all agents (they're just text) and don't clutter up your context at all.”
> — [2064420770667762155](https://x.com/aarondfrancis/status/2064420770667762155) (2026-06-09)

### 1.4 GitHub vs Solo todos

> “Just in Solo. The idea is that GitHub is for collabing with humans, todos in Solo are for agents. So you could tell your agent to grab a github issue, explore, make a scratchpad/todo to implement, and then work off of those”
> — [2049876238085329185](https://x.com/aarondfrancis/status/2049876238085329185) (2026-04-30)

---

## 2. Launch narrative & product primitives

### 2.1 Desktop launch thread (2026-02-06)

**Root:** [2019832589482356878](https://x.com/aarondfrancis/status/2019832589482356878)
**Engagement (snapshot):** ~1.7k likes, ~119 RTs, ~441k views
**Media:** Launch demo video (~76s)

Thread claims (exact paraphrases from thread posts):

1. Out today; free; add project → auto-detect processes → one-click start
2. Problem: README → 6 commands → 6 tabs; Solo starts them together / shuts down one click
3. Auto-restart crashed processes; file-watching globs restart on code changes
4. Commit `solo.yml` so team shares stack (or keep some processes secret)
5. Free for up to **3 projects**, every feature; **Mac now**, Windows/Linux coming
6. First product under **faster.dev** brand

**Follow-up videos in thread** (IDs 2019832591696683304, 2019832593613521168, 2019832595438240052) — short product demos.

### 2.2 March 2026 “new Solo app” release

**Root:** [2032570894040613354](https://x.com/aarondfrancis/status/2032570894040613354)
**Quote:** “Run your agents, terminals, and devstack all in one app.”
**Changelog-ish bullets on X:** increased free tier, cleaned terminal, less annoying command trust, zsh fixes, shift+enter fixes.
**Media:** Long demo video (~10 minutes).
**Link reply:** “Fresh off the press https://soloterm.com/”

### 2.3 Early product evolution signal (agents inside Solo)

Ian Landsman quote-tweet context + Aaron:

> “Something I didn't expect was people running their Claudes, Vim, Codex, etc *inside* of Solo. I need to add better affordances for that. Also that makes me think Solo could be bigger than I originally imagined?”
> — [2020904631862174148](https://x.com/aarondfrancis/status/2020904631862174148) (2026-02-09)

### 2.4 Commands / solo.yml

- Commands defined in **`solo.yml`** (file-first configuration)
- “If the command is in solo.yml you can do that via the file, but i need to surface it in the UI.” — [2036555829524992234](https://x.com/aarondfrancis/status/2036555829524992234) (2026-03-24) + screenshot
- Auto-restart: “Solo will auto restart it” (with noted bug history) — [2020164159673933826](https://x.com/aarondfrancis/status/2020164159673933826)
- No command DAG yet: “Currently there is not DAG for "this command relies on that one running"” — [2074524680044552296](https://x.com/aarondfrancis/status/2074524680044552296)
- Stripe CLI example as Solo **command** (shared visibility to human + agents, not buried in agent background) — [2065086701446275115](https://x.com/aarondfrancis/status/2065086701446275115)

### 2.5 Free tier / licensing

- Launch: free ≤3 projects
- “Solo has a generous free tier!” — [2032904836111282366](https://x.com/aarondfrancis/status/2032904836111282366)
- “delete that welcome to solo project! free up a slot!” — [2058661602874859986](https://x.com/aarondfrancis/status/2058661602874859986)
- Team licensing: fixed seats or auto-expanding pool via claim link — [2065530410612768889](https://x.com/aarondfrancis/status/2065530410612768889)

---

## 3. Agents

### 3.1 Supported agent ecosystem (from X)

Mentioned as first-class or runnable inside Solo:

- Claude / Claude CLI / Claude Code
- Codex / OpenAI Codex
- Amp (@AmpCode)
- Gemini
- Generic “any agent in a terminal”
- Cross-agent spawning: “Codex → Claude → Amp → Gemini” — [2047079877489164714](https://x.com/aarondfrancis/status/2047079877489164714)

### 3.2 Agent configuration & spawn

| Tip | Quote | URL | Date |
|-----|-------|-----|------|
| Settings path | “go to settings > agents and configure an e.g. Codex High with your desired flags baked in” | [2077126031736033551](https://x.com/aarondfrancis/status/2077126031736033551) | 2026-07-14 |
| MCP spawn flags | “telling your lead agent to append those flags when using the MCP spawn tool” | same | 2026-07-14 |
| Inspect spawn | “spin up a new agent and ask it to inspect the spawning tools, and then have it spawn one with a certain reasoning level. then hover over it to see the full command” | [2077127269848412593](https://x.com/aarondfrancis/status/2077127269848412593) | 2026-07-14 |
| Nested agents | Sidebar nesting of review agents under orchestrator (UI evidence) | media below | 2026-07-09 |

### 3.3 Auto-summarization

> “Solo has an option for "auto summarizing" your agent chats, so you can remember what the heck each one is working on. If you turn them off, we still make best efforts to do it without a model! Here, we're taking the Claude recaps and putting them in the sidebar.”
> — [2049542287605092536](https://x.com/aarondfrancis/status/2049542287605092536) (2026-04-29)

### 3.4 Trust / sudo flow

> “Codex was trying to install something that needed sudo and since it's running in Solo it just spawned a new terminal, sent it the install commands, and waited for me to type my password. Pretty cool flow!”
> — [2058610122197274684](https://x.com/aarondfrancis/status/2058610122197274684) (2026-05-24)

### 3.5 Workstyle (Aaron personal)

- “usually one thing at a time per repo so I can keep my eye on it” — [2077143606469538241](https://x.com/aarondfrancis/status/2077143606469538241)
- “I barely touch the mouse in Solo these days!” — [2077108337716416834](https://x.com/aarondfrancis/status/2077108337716416834)
- Strict plan-up-front; stored prompts as guardrails
- “I don't need worktrees, and I don't care how many agents get spawned. That's up to the lead agent” — [2075213903332581379](https://x.com/aarondfrancis/status/2075213903332581379)
- Earlier (May): “No worktrees yet” — [2054726475383738498](https://x.com/aarondfrancis/status/2054726475383738498); later JS sandbox worktree **routine** preview (May 25)

---

## 4. Canonical orchestration workflow (highest-value post)

Earlier proof-of-primitives post: [2048124783208886565](https://x.com/aarondfrancis/status/2048124783208886565) (2026-04-25). Aaron shows one orchestrator Codex handling four child Codexes through shared Markdown, timers, input, and child spawning. Evidence: `research/fan-solo/x-evidence/orchestrator-four-codexes.png`.

**Post:** [2075213903332581379](https://x.com/aarondfrancis/status/2075213903332581379)
**Date:** 2026-07-09
**Engagement:** ~364 likes, ~404 bookmarks, ~39k views
**Media:** 2 screenshots — multi-agent review tree + plan build mode follow-up

### 4.1 Step sequence (Aaron’s exact structure)

1. Long conversation with an agent → plan
2. Agent writes plan to a **Solo scratchpad** (“durable markdown doc, via MCP”)
3. Lead agent **spawns** reviewer agents; they write gaps back to **same shared scratchpad** via MCP
4. Lead sets a **wakeup timer** so it doesn’t busy-loop / bother subagents; “Solo will wake it up”
5. When done, lead synthesizes; human chats more
6. Confident plan → lead switches to **“orchestration” role**
7. Via MCP: interact with terminals; instruct subagents from plan; **read/write terminal panes**
8. Final review: built work vs planning doc

**Follow-up in thread:** “Plan is finalized, now we switch to build mode” — [2075245976927785416](https://x.com/aarondfrancis/status/2075245976927785416) with screenshots.

### 4.2 Media description — orchestration sidebar

File: `research/fan-solo/x-evidence/2026-07-09-orchestration-workflow-1.jpg`

- macOS Solo window chrome
- Projects: Solo Parent, soloterm.com, **Desktop 1** (expanded)
- **AGENTS 4/5**: Codex (committed terminal file link detection); **Attach pane** orchestrating multi-agent review; nested `attach-plan-review-claude|codex|amp`
- **COMMANDS 0/10** collapsed
- Landscape wallpaper background

### 4.3 Earlier “no worktrees yet” orchestration framing

[2054726475383738498](https://x.com/aarondfrancis/status/2054726475383738498) (2026-05-14):

> “Solo is mostly focused on the terminal workflow. We also have a built in MCP that lets you run orchestration flows (agents spawning agents, sending input to each other, reading output, writing durable todos and markdown, etc) No worktrees yet”

---

## 5. Multi-repo / multi-project model

**Post:** [2077090002496872671](https://x.com/aarondfrancis/status/2077090002496872671) (2026-07-14)

> “I've gotten a few questions about working across multiple repos in Solo. The good news is: do whatever you want!
> Here, I have web, desktop, and mobile as individual projects, and then one "Solo Parent" that's the folder above it.
> The mobile orchestrator just spawn agents in each one of those projects! It's controlling those agents, even though it's in a different Solo project.
> **Projects are not hard boundaries, just lightweight scopes.**”

### 5.1 Media description — multi-repo

File: `research/fan-solo/x-evidence/2026-07-14-multi-repo-projects.jpg`

- Left: Solo Parent → soloterm.com → Desktop 1–4 → classifier → **MB mobile** (boxed) with multiple review agents
- Red arrows: cross-project orchestration from mobile up into parent/desktop/web
- Right: OpenAI Codex session with **[SOLO ORCHESTRATION CONTEXT]** block:
  - Sets `SOLO_PROCESS_ID` / `SOLO_PROJECT_ID`
  - Instructs `whoami()`, `identify_session()`, locks, scratchpads, todos, timers
  - Live `solo.whoami` JSON (process_id, actor_id, project Desktop 1, `server_enabled_tool_count`: 102)
- Note: some MCP clients solo2/solo3 fail to start (env noise in screenshot)

### 5.2 Related workflow discipline

> “I'm pretty strict about defining the plan up front and then also working on usually one thing at a time per repo…”
> — [2077143606469538241](https://x.com/aarondfrancis/status/2077143606469538241)

### 5.3 Emergent agent behavior (PTY cross-talk)

> “today my agents, by no prompting of my own, start writing to each other's PTYs instead of communicating via scratchpads. What hath I wrought?”
> — [2077100480258359564](https://x.com/aarondfrancis/status/2077100480258359564) (2026-07-14)

Implies preferred intentional coordination is **scratchpads** (and locks/todos/timers), while direct PTY write is possible and sometimes emergent.

---

## 6. MCP deep dive

### 6.1 “Your terminal now has an MCP” launch

**Post:** [2047079877489164714](https://x.com/aarondfrancis/status/2047079877489164714) (2026-04-22)
**Media:** ~82s demo video
**Claims:**

- Agents can spawn agents across brands
- “They can chat back and forth, dispatch tasks, monitor, do research, read output, and set durable wakeup timers.”
- Follow-up: https://soloterm.com/

### 6.2 MCP value prop (differentiation)

> “I think the main things that set it apart right now are the agent coordination tools via the Solo MCP. Agents can talk to each other, create todos, write markdown, set timers for themselves to wakeup, etc”
> — [2049976814169145540](https://x.com/aarondfrancis/status/2049976814169145540) (2026-04-30)

> “gives you control over Solo itself. So reading from / writing to other running processes, writing shared markdown, managing shared todos, setting durable timers (wake me up in 1 hour, wake me up when that process goes idle, etc)”
> — [2049878491965927498](https://x.com/aarondfrancis/status/2049878491965927498)

> “Via the Solo MCP, any agent can control (send input, read output, start / stop) any agent, command, or blank terminal. The other day I ssh'ed into prod and then told an agent to just control that terminal to poke around. Kinda awesome”
> — [2049584901549076636](https://x.com/aarondfrancis/status/2049584901549076636)
> **Also:** “docs are severely lagging.” (as of 2026-04-29)

### 6.3 Progressive discovery design essay (2026-07-10)

**Post:** [2075571055041675691](https://x.com/aarondfrancis/status/2075571055041675691)

Key implementation tips (public):

| Mechanism | Detail |
|-----------|--------|
| Ordered `tools/list` | When caller runs **inside Solo**, reorder so `whoami` + `help` first + small starter pack |
| Init instructions | 1) `whoami` 2) `help` 3) topic help when needed |
| `whoami` | Process identity, actor, effective project |
| `help` | Internal docs library; aliases: ports, services, status, "how do I", yaml |
| `mcp_tools_summary` | Compact categorized list **without full schemas** |
| Disable tools | Removed from discovery entirely |
| Contextual next-tool suggestions | e.g. after spawn → timer; **suggestions decay** to save tokens |
| Tool count example | Screenshot shows `server_enabled_tool_count`: **102** |

**Media:** `2026-07-10-mcp-progressive-disclosure.jpg` — agent log showing:

- `solo.whoami` → JSON identity for Codex agent on “Desktop 1”
- `solo.help({topic:"scratchpads"})` → “SCRATCHPADS – Shared text buffers”
- Direct update workflow: `scratchpad_read` → `scratchpad_edit` / `append_section` / `append` / `write`
- Guidance: “Do not stage through the filesystem unless the user explicitly wants file import/export.”

### 6.4 Onboarding tip for new users

> “I would suggest just start by using it as a terminal. then add the solo mcp to your favorite agent. then ask the agent "what can you do with the solo mcp" and go from there!”
> — [2055311627784785924](https://x.com/aarondfrancis/status/2055311627784785924) (2026-05-15)

### 6.5 Control Solo from outside Solo

> “yup! you could control solo from an agent running in ghostty, or from any desktop app that supports MCP”
> — [2077108568822587490](https://x.com/aarondfrancis/status/2077108568822587490) (2026-07-14)

> “No mobile app yet but with the Claude or codex apps and a session inside of solo you could control it all via MCP. Working on mobile”
> — [2076072363389538685](https://x.com/aarondfrancis/status/2076072363389538685) (2026-07-11)

> “yesssss it's working! I've spent a HUGE amount of time on the MCP and its instructions!”
> — [2077404705152552986](https://x.com/aarondfrancis/status/2077404705152552986) (2026-07-15)

### 6.6 MCP feature surface named on X

From multiple posts (union):

| Capability | Notes |
|------------|-------|
| Process list / start / stop / restart | Any agent, command, blank terminal |
| `send_input` / read output | PTY control |
| Spawn process / spawn agent | Cross-agent orchestration |
| Scratchpads | Durable shared markdown; comment; edit/append/find |
| Todos | Agent work tracking; comments; locks |
| Timers | Durable wakeup; idle triggers; max wait |
| Locks | Coordination |
| k/v | Optional; can be disabled |
| Prompt templates | Optional MCP tools (changelog + X) |
| Project tools | Scope / import (changelog; MCP essay) |
| `help` / `whoami` / `identify_session` | Bootstrap |
| `mcp_tools_summary` | Catalog without schema dump |
| Inbox (changelog) | `fetch_project_inbox` unified project inbox |

### 6.7 Context-rot defense

> “It can be for solo Solo agents! Just tell it to use the MCP. I usually do that after a big round of back-and-forth and we finally land on a plan. I tell it to make a scratchpad or discrete todos so we don't lose anything to context rot”
> — [2049850352090927521](https://x.com/aarondfrancis/status/2049850352090927521)

---

## 7. Todos & scratchpads

### 7.1 Introduction post

**Post:** [2041919379307184295](https://x.com/aarondfrancis/status/2041919379307184295) (2026-04-08)
**Quote:** “It holds all my todos and markdown scratchpads. Agents can read / write / comment on all of them via MCP.”

**Media:** `2026-04-08-todos-scratchpads-mcp.jpg` — Solo desktop todos UI:

- Sidebar: projects (persona, desktop, desktop-2…), todos, agents, commands, scratchpads
- Todo detail: markdown body, dependencies/blockers, activity comments
- Todo titles reference MCP work (“Include canonical todo URL in todo_get response”, deep links like `solo://todo/<projectId>/<slug>---<todoId>`)
- Dogfooding Solo **to build Solo**

### 7.2 Scratchpad semantics (from MCP help screenshot)

- Shared text buffers
- Prefer MCP edits over filesystem staging
- Tools: write, edit (section/line), append_section, append, read with revision

### 7.3 Visual scratchpads

> “This is *visual* scratchpads in Solo!” — [2064373096191041632](https://x.com/aarondfrancis/status/2064373096191041632) (2026-06-09)

### 7.4 File explorer / cmd+click

> “I'll fix cmd+click. I'm adding a file explorer / editor, but you can also have your agent write them to solo scratchpads and view them there. Then all the agents can read / write to them from there!”
> — [2055037456110457306](https://x.com/aarondfrancis/status/2055037456110457306) (2026-05-14)

### 7.5 Automation idea (routines)

> “Pull nightwatch issues every morning and sync them to my local solo todos. Ok, done”
> — [2058995241256919050](https://x.com/aarondfrancis/status/2058995241256919050) (2026-05-25)

---

## 8. Prompt templates (stored prompts)

**Ship post:** [2064420770667762155](https://x.com/aarondfrancis/status/2064420770667762155) (2026-06-09)

> “Prompt templates have shipped in the latest version of Solo! You can save your favorite prompts and even add placeholders.”

**Media:** `2026-06-09-prompt-templates-1.jpg` — modal “Value for agent” with `{{agent}}` placeholders; actions **insert / send / ⌘C copy prompt**

Template content (excerpt, verbatim from image): instructs lead agent to spawn `{{agent}}` via Solo MCP, set idle timer, avoid interrupting long TUI review, optionally dump findings or write Solo scratchpad + link.

Also: Aaron prefers c&p / stored prompts over agent “skills” (July 14).

---

## 9. Keyboard shortcuts & navigation (X-explicit)

Aaron listed navigation shortcuts explicitly:

> “Cmd+k, cmd+e, cmd+shift+e, cmd up, cmd down, cmd [, cmd ] all navigate. Dealers choice”
> — [2050645820622426256](https://x.com/aarondfrancis/status/2050645820622426256) (2026-05-02)

Interpretation (with changelog corroboration, not pure X):

| Shortcut | Likely role (X + product docs) |
|----------|--------------------------------|
| `Cmd+K` | Command palette |
| `Cmd+E` | Jump / search destinations |
| `Cmd+Shift+E` | Extended jump/search variant |
| `Cmd+↑/↓` | Sidebar process navigation |
| `Cmd+[/]` | History back/forward |

Other X mentions:

- Keyboard bugs get real tests: “what operating system, what version of solo, and what keyboard?” + screenshot — [2075555085824786621](https://x.com/aarondfrancis/status/2075555085824786621)
- Shift+enter fixed in March release notes on X
- Mouse-light usage: “I barely touch the mouse in Solo these days!”

**Gap:** Full default keymap not published as a single X post; official docs at soloterm.com cover default reference (see changelog links to `/docs/keyboard-shortcuts/default-reference`).

---

## 10. Terminals & implementation tips

### 10.1 Stack

> “I went with Tauri, largely because of the Rust crate ecosystem around PTYs and process management. The UI is React/TypeScript, and the terminal itself uses Rust's vt100 crate with a custom frontend renderer so I can keep the heavy stuff in Rust”
> — [2076422654408491106](https://x.com/aarondfrancis/status/2076422654408491106) (2026-07-12)

### 10.2 Fifth terminal rewrite

> “Ok maybe rewriting the terminal 5 times was actually worth it.” — [2046707759324782640](https://x.com/aarondfrancis/status/2046707759324782640) (2026-04-21) + video
> “Big time. And the fifth terminal rewrite was partly to lay that base” — [2076870240420364365](https://x.com/aarondfrancis/status/2076870240420364365) (2026-07-14) (context: less exposed surface / mobile & headless)

### 10.3 “Make a multiplexer” war story

> “Make a multiplexer! It'll be fun! What could go wrong! Well, here's my @AmpCode thread map from today 🫠 running down a rendering bug in Solo.”
> — [2034073618619973863](https://x.com/aarondfrancis/status/2034073618619973863) (2026-03-18) + video

### 10.4 Headless / remote roadmap

| Quote | URL | Date |
|-------|-----|------|
| “yeah I'm thinking solo as host and solo as remote… exact same gui… no need for complicated SSH setups” | [2036813468058132699](https://x.com/aarondfrancis/status/2036813468058132699) | 2026-03-25 |
| “headless solo soon that you can put on your remote machine and talk to from local” | [2058933342402195968](https://x.com/aarondfrancis/status/2058933342402195968) | 2026-05-25 |
| “headless solo deployed on your vps not yet, but soon” | [2058631263842435370](https://x.com/aarondfrancis/status/2058631263842435370) | 2026-05-24 |
| Regular terminal + SSH works now | same | 2026-05-24 |
| Fifth rewrite base for mobile/headless/cloud agents/VPS | [2076871074902384750](https://x.com/aarondfrancis/status/2076871074902384750) | 2026-07-14 |

### 10.5 Solo CLI / API centralization

> “that's where we're headed! trying to get all operations centralized, so then mcp, cli, http share a catalog. then I can have agents use their hooks to call solo. then we're home free”
> — [2052819281168011383](https://x.com/aarondfrancis/status/2052819281168011383) (2026-05-08)

> “Yes! needed Solo CLI first, and now that it's there, we're good.” — [2065097113319379204](https://x.com/aarondfrancis/status/2065097113319379204) (2026-06-11)

### 10.6 JS sandbox / routines (coming / preview)

**Post:** [2058990625081446527](https://x.com/aarondfrancis/status/2058990625081446527) (2026-05-25)

> “What if every surface, workflow, and routine of your agentic meta-harness was controllable?
> Coming soon to Solo: a built in JS sandbox that allows you to deeply control how Solo works.
> We will ship some first-party routines like worktrees, pictured here.”

**Media:** `2026-05-25-js-sandbox-worktrees.jpg` — `worktrees/routine.ts` showing:

- `solo.entrypoint`
- `linkedCheckouts.createPlan` / hooks
- `solo.git.worktrees.add`
- `solo.projects.linkedCheckouts.create` / `select`
- `solo.hookRunner.run`
- Preview/validate path

**Tech note reply:** Tauri + [Boa](https://github.com/boa-dev/boa) JS engine — [2058991977111122254](https://x.com/aarondfrancis/status/2058991977111122254)

---

## 11. Changelog commentary on X

| Date | X claim | Link |
|------|---------|------|
| 2026-05-15 | “The Solo v0.7.0 changelog is... extensive.” | [2055388298722328906](https://x.com/aarondfrancis/status/2055388298722328906) |
| 2026-05-15 | Full text at https://soloterm.com/changelog | [2055389475832754283](https://x.com/aarondfrancis/status/2055389475832754283) |
| 2026-03-13 | Free tier, terminal cleanup, trust, zsh, shift+enter | [2032570894040613354](https://x.com/aarondfrancis/status/2032570894040613354) |
| 2026-06-09 | Prompt templates in latest version | [2064420770667762155](https://x.com/aarondfrancis/status/2064420770667762155) |
| 2026-06-12 | Team licensing | [2065530410612768889](https://x.com/aarondfrancis/status/2065530410612768889) |

**Official changelog highlights (not X-primary, but linked from X and useful for completeness):**

Versions through **v0.9.3** (2026-06-21) document: Connect Solo one-click MCP, favorites shortcuts, Windows/WSL execution profiles, prompt templates, HTTP API + CLI parity, scratchpad/todo MCP/CLI, terminal GPU renderer (v0.6.0), nested agents, timers, activity monitor, etc.
Full text: https://soloterm.com/changelog

---

## 12. Implementation tips distilled for builders / skill authors

These are **operational patterns Aaron publicly recommends**:

1. **Bootstrap MCP:** `whoami` → `help` → topic help → only then broad tools
2. **Prefer shared scratchpads/todos over chat context** after planning lands
3. **Use timers** for multi-agent wait (idle / duration) instead of busy-looping
4. **Orchestrator reads/writes PTYs** of workers; workers can also write shared docs
5. **Projects = scopes**, not sandboxes — orchestrators can span projects
6. **Run long-lived infra as Solo commands** (Stripe CLI, docker, queues) so all agents see the same process
7. **Bake agent flags** in Settings → Agents *or* pass via MCP spawn
8. **Stored prompt templates** for cross-agent reusable workflows (placeholders)
9. **Start simple:** use as terminal first, then attach MCP
10. **stdio MCP** surface; optional feature toggles remove tools from catalog
11. **External control:** any MCP client (Ghostty agent, Claude app, desktop) can drive Solo
12. **Avoid relying solely on agent “skills”** if Solo prompts suffice (Aaron’s personal stance July 2026)

---

## 13. Early lineage (Laravel Solo)

| Date | Post | URL |
|------|------|-----|
| 2024-11-07 | Solo for Laravel beta release, `php artisan solo` | [1854585789726048509](https://x.com/aarondfrancis/status/1854585789726048509) |
| 2025-01-31 | PHP terminal GUI tour video | [1885376322152624148](https://x.com/aarondfrancis/status/1885376322152624148) |
| 2025-03-20 | dumps package extracted from Solo | [1902774090206749089](https://x.com/aarondfrancis/status/1902774090206749089) |

Evidence image: `2024-11-07-laravel-solo-release.jpg` — TUI tabs (About, Logs, Vite, HTTP, Queue, Reverb, Pail, Dumps).

Packagist: https://packagist.org/packages/soloterm/solo
GitHub org pattern: `soloterm/*`

---

## 14. Notable third-party X signal (quoted by Aaron)

**@aienginerd** (quoted in [2049843097891111420](https://x.com/aarondfrancis/status/2049843097891111420)):

- soloterm MCP tools used to build wrapper orchestration CLI
- Multi-day multi-project stability vs tmux heat/fan issues
- Evidence file: `2026-04-30-user-endorsement-orchestration.png`

**@IanLandsman** (2026-02-09): organizes Claudes across projects inside Solo rather than 10 terminal tabs.

---

## 15. Media index (`research/fan-solo/x-evidence/`)

| File | Source post / date | Description |
|------|-------------------|-------------|
| `2024-11-07-laravel-solo-release.jpg` | 1854585789726048509 | Laravel Solo TUI screenshot |
| `2026-02-19-early-feedback-vnext.jpg` | 2024560175625953672 | Early vNext UI feedback shot |
| `2026-03-20-products-built-by-humans.jpg` | 2035067821718208513 | Homepage “built by humans” section |
| `2026-03-24-solo-yml-commands.jpg` | 2036555829524992234 | solo.yml / command config UI |
| `2026-04-08-todos-scratchpads-mcp.jpg` | 2041919379307184295 | Todos UI dogfooding Solo-on-Solo |
| `2026-04-29-auto-summarizing-chats.jpg` | 2049542287605092536 | Sidebar agent summaries / Claude recaps |
| `2026-04-30-spoken-more-to-solo.jpg` | 2049949812481536316 | Social/UI moment “spoken more to Solo than Ghostty” |
| `2026-04-30-user-endorsement-orchestration.png` | quoted 2049841685719331298 | User orchestration endorsement |
| `2026-05-14-orchestration-no-worktrees.jpg` | 2054726475383738498 | Terminal/MCP orchestration UI |
| `2026-05-15-v0.7.0-changelog.jpg` | 2055388298722328906 | Changelog teaser graphic (tall) |
| `2026-05-24-sudo-spawn-terminal-1.jpg` | 2058610122197274684 | Sudo password agent flow (1) |
| `2026-05-24-sudo-spawn-terminal-2.jpg` | 2058610122197274684 | Sudo password agent flow (2) |
| `2026-05-25-js-sandbox-worktrees.jpg` | 2058990625081446527 | worktrees routine TypeScript source |
| `2026-06-09-prompt-templates-1.jpg` | 2064420770667762155 | Prompt template placeholder fill modal |
| `2026-06-09-prompt-templates-2.jpg` | 2064420770667762155 | Prompt templates second UI shot |
| `2026-06-11-stripe-cli-command-1.jpg` | 2065086701446275115 | Stripe CLI as Solo command (1) |
| `2026-06-11-stripe-cli-command-2.jpg` | 2065086701446275115 | Stripe CLI as Solo command (2) |
| `2026-06-12-team-licensing.jpg` | 2065530410612768889 | Team licensing UI |
| `2026-07-09-orchestration-workflow-1.jpg` | 2075213903332581379 | Nested multi-agent review tree |
| `2026-07-09-orchestration-workflow-2.jpg` | 2075213903332581379 | Orchestration second frame |
| `2026-07-09-plan-build-mode-1.png` | 2075245976927785416 | Build mode transition (1) |
| `2026-07-09-plan-build-mode-2.jpg` | 2075245976927785416 | Build mode transition (2) |
| `2026-07-10-mcp-progressive-disclosure.jpg` | 2075571055041675691 | whoami + help(scratchpads) agent log |
| `2026-07-10-keyboard-test-case.jpg` | 2075555085824786621 | Keyboard bug investigation screenshot |
| `2026-07-14-multi-repo-projects.jpg` | 2077090002496872671 | Cross-project mobile orchestrator |
| `2026-07-14-spawn-reasoning-level.png` | 2077127269848412593 | Spawn tool / reasoning level hover |
| `orchestrator-four-codexes.png` | 2048124783208886565 | One orchestrator coordinating four child Codexes |
| `aarondfrancis-profile.png` | [@aarondfrancis](https://x.com/aarondfrancis) profile capture | Official account/context capture |

### Videos referenced (not re-downloaded as full files)

| Post | Duration / notes | URL |
|------|------------------|-----|
| Desktop launch | ~76s + shorter follow-ups | [2019832589482356878](https://x.com/aarondfrancis/status/2019832589482356878) |
| Beta rollout | ~10s | [2030725472443683225](https://x.com/aarondfrancis/status/2030725472443683225) |
| Multiplexer bug war | ~22s | [2034073618619973863](https://x.com/aarondfrancis/status/2034073618619973863) |
| New Solo app | ~10 min | [2032570894040613354](https://x.com/aarondfrancis/status/2032570894040613354) |
| Terminal rewrite 5× | ~12s | [2046707759324782640](https://x.com/aarondfrancis/status/2046707759324782640) |
| Terminal has MCP | ~82s | [2047079877489164714](https://x.com/aarondfrancis/status/2047079877489164714) |
| X Spaces / broadcast | “Testing a New Solo Version” | [2048851167787237403](https://x.com/aarondfrancis/status/2048851167787237403) |

---

## 16. High-value post URL index (canonical list)

```
https://x.com/aarondfrancis/status/1854585789726048509  # Laravel Solo release
https://x.com/aarondfrancis/status/1885376322152624148  # PHP TUI tour
https://x.com/aarondfrancis/status/1902774090206749089  # dumps package
https://x.com/aarondfrancis/status/2019832589482356878  # Desktop launch
https://x.com/aarondfrancis/status/2020904631862174148  # Agents inside Solo surprise
https://x.com/aarondfrancis/status/2024560175625953672  # vNext early feedback
https://x.com/aarondfrancis/status/2030725472443683225  # 25% rollout
https://x.com/aarondfrancis/status/2032570894040613354  # New Solo app out
https://x.com/aarondfrancis/status/2034073618619973863  # Multiplexer bug
https://x.com/aarondfrancis/status/2035067821718208513  # Products by humans
https://x.com/aarondfrancis/status/2041919379307184295  # Todos + scratchpads
https://x.com/aarondfrancis/status/2046707759324782640  # Terminal rewrite 5×
https://x.com/aarondfrancis/status/2047079877489164714  # Terminal MCP launch
https://x.com/aarondfrancis/status/2048124783208886565  # One orchestrator, four child Codexes
https://x.com/aarondfrancis/status/2049542287605092536  # Auto-summaries
https://x.com/aarondfrancis/status/2049843097891111420  # vs tmux vindication
https://x.com/aarondfrancis/status/2049949812481536316  # More Solo than Ghostty
https://x.com/aarondfrancis/status/2054619137817678286  # Real Claude CLI
https://x.com/aarondfrancis/status/2054726475383738498  # Terminal workflow + MCP
https://x.com/aarondfrancis/status/2055388298722328906  # v0.7.0 changelog
https://x.com/aarondfrancis/status/2058610122197274684  # sudo spawn terminal
https://x.com/aarondfrancis/status/2058990625081446527  # JS sandbox / worktrees
https://x.com/aarondfrancis/status/2064420770667762155  # Prompt templates
https://x.com/aarondfrancis/status/2065086701446275115  # Stripe CLI command
https://x.com/aarondfrancis/status/2065530410612768889  # Team licensing
https://x.com/aarondfrancis/status/2075213903332581379  # Canonical orchestration
https://x.com/aarondfrancis/status/2075571055041675691  # MCP progressive disclosure
https://x.com/aarondfrancis/status/2076422654408491106  # Tauri / vt100 stack
https://x.com/aarondfrancis/status/2077090002496872671  # Multi-repo projects
https://x.com/aarondfrancis/status/2077143606469538241  # Stored prompts vs skills
https://x.com/aarondfrancis/status/2077404705152552986  # MCP instructions investment
```

---

## 17. Gaps & limitations of this research

| Gap | Detail |
|-----|--------|
| **Incomplete X corpus** | X search returns capped sets (~10 per query). Many low-engagement support replies likely missing. Not a full archive of every @aarondfrancis Solo mention. |
| **Videos not transcribed** | Launch, MCP, rewrite, and 10-min GA demos not speech-to-text’d here; content inferred from captions + stills. |
| **No full keymap on X** | Only partial shortcut list on X; complete defaults live in product docs. |
| **No full MCP tool schema dump on X** | Progressive disclosure is explained; complete tool list is ~100+ tools (screenshot: 102 enabled) — see live MCP / docs, not a single X post. |
| **Changelog detail mostly off-X** | Aaron points to soloterm.com/changelog rather than pasting full release notes. |
| **API/HTTP surface** | Mentioned as roadmap/central catalog + CLI; detailed routes primarily in docs/changelog, not deep X essays. |
| **JS sandbox ship status** | Announced “coming soon” 2026-05-25; this research does not verify final GA status on X after that date beyond related CLI/headless notes. |
| **Mobile** | “Working on mobile” / “about a month out” (May) — not verified shipped by 2026-07-15 X results. |
| **Windows/Linux launch promises** | Launch said “coming soon”; later changelog shows Windows/WSL work — platform GA marketing on X not exhaustively tracked. |
| **Live page screenshots of x.com** | Media saved via CDN (`pbs.twimg.com`), not browser viewport screenshots of x.com threads. |
| **Replies from Aaron deep in other users’ threads** | Partially covered via keyword search; semantic search may miss keyword-light replies. |
| **@soloterm account** | Aaron noted “I have @soloterm but it's dormant / not yet used!” (2026-05-25) — primary voice remains @aarondfrancis. |
| **Pricing beyond free tier / team seats** | Not fully detailed on sampled X posts. |
| **Security model** | Trusting commands, MCP safety hints, auto-trust per-project settings appear more in changelog than X essays. |

---

## 18. Suggested follow-ups (if deepening research)

1. Transcribe top demo videos (launch, MCP, 10-min GA).
2. Archive full `from:aarondfrancis Solo` via paid X API / export for completeness.
3. Cross-link every changelog version bullet to X announce posts.
4. Capture product docs pages (`/docs/mcp-tools/*`, `/docs/keyboard-shortcuts/*`) as second research file.
5. Monitor mobile/headless GA posts after 2026-07-15.
6. Pull Discord announcements if official and public.

---

## 19. Research metadata

| Field | Value |
|-------|-------|
| Researcher role | Web research specialist (agent) |
| Workspace | `kalepail-skills` |
| Outputs | `research/fan-solo/solo-x-research.md`, `research/fan-solo/x-evidence/*` |
| Skills edited | **None** (per request) |
| Tools used | X keyword/semantic search, thread fetch, user search, parallel-cli search, web_fetch (changelog), curl media download, image inspection |
| Confidence | **High** on major product narrative and quoted posts; **Medium** on completeness of long-tail replies |

---

*End of report.*
