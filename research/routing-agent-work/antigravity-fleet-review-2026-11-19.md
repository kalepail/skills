# Antigravity fleet review, 2026-11-19

## Decision

Add the official `agy` harness as a subscription worker. Use Neon High when Antigravity is selected for bounded implementation or an independent second opinion. Use Hydrogen High for routine work with cheap verification and Carbon High as a longer-horizon Gemini option. Keep Argon available to callers who select it. Use Neon XHigh for bounded problems that justify the extra effort. Keep the established defaults for general implementation, verification, architecture, and prose. Keep the pinned zero-retention OpenCode Carbon route eligible when its data terms or input mode are required.

The questions were where Antigravity earns a route, whether the Gemini tiers justify distinct roles, and what has to be verified on the Mac and agentpc. The review used direct benchmark publishers and Google documentation, actual Grok X search, and small existing fixtures. The claims are about these tested versions and harnesses.

## Published evidence

| Source and setup | Result | Routing implication |
|---|---|---|
| Artificial Analysis Coding Agent Index, November 18, provider harnesses | Antigravity Neon XHigh scored about 59 and Carbon High about 55. Claude Code Fable 5.2 XHigh and Opus 5.5 Max were about 58. Estimated cost per task was $6.86 for Neon and $12.61 for Opus. | There is a credible Antigravity coding route. The comparison includes different harnesses, effort settings, and API pricing. [Artificial Analysis](https://artificialanalysis.ai/articles/gemini-4-neon-intelligence-gain) |
| Artificial Analysis API Intelligence Index, November 18 | Neon High and Carbon High scored 60. Neon XHigh scored 61. Neon High cost about $3.74 per benchmark task, Neon XHigh $6.44, and Carbon High $7.76 at standard pricing. Hydrogen scored 51 on High and 41 on Medium. | High is the useful default. Higher effort and the smaller model fit specific tasks. API benchmark prices do not measure an Ultra account's remaining quota. [Neon analysis](https://artificialanalysis.ai/articles/gemini-4-neon-intelligence-gain) · [Hydrogen model results](https://artificialanalysis.ai/models/gemini-4-hydrogen) |
| Vals Terminal-Bench 4.0, November 18, Mini-SWE-agent | Opus and Fable 65.15%, Carbon 63.13%, Neon 61.62%, Sol 60.61%, Argon 57.58%, Hydrogen 54.04%. | The common harness reverses the Neon and Carbon order. Hydrogen looks like a bounded execution option. [Vals leaderboard](https://www.vals.ai/benchmarks/terminal-bench-4) |
| Arena Coding Index, November 18 | Fable Max ranked first, Opus Max second, Astra Max third, Neon High fifth, preliminary Carbon High seventh, Sol Max ninth, and preliminary Hydrogen High fifteenth. | The preference evidence supports an additional route. The existing quality-first and verification choices still have support. [Arena Coding Index](https://arena.ai/leaderboard/agent/code) |
| Google DeepMind's Neon model card and methodology | Vendor-reported SWE-sweep scores were 39.0% with Antigravity CLI and 12.8% with Mini-SWE-agent. The Antigravity configuration could use subagents. | Treat the CLI as part of the measured system. Google's Orchestrator pairs a planner with Hydrogen and belongs in an explicitly delegated workflow. [Model card](https://deepmind.google/models/model-cards/gemini-4-neon/) · [Methodology](https://deepmind.google/models/evals-methodology/gemini-4-neon/) · [Orchestrator](https://antigravity.google/docs/models#orchestrator) |

The live CLI lists Low through XHigh for Neon and Hydrogen, and Low through High for Carbon and Argon. The routing skill starts at Medium or High by role. Check the CLI's context limit and input support instead of inheriting the Gemini API's limits. Google documents up to 512K for Neon in Antigravity. Quota groups share five-hour and weekly limits across models in a group. [Antigravity model docs](https://antigravity.google/docs/models) · [Usage command](https://antigravity.google/docs/cli/commands/usage/)

## Grok X sample

Grok Build used its native X backend on November 19. The session trace records 14 keyword searches, three semantic searches, and ten thread fetches. The queries covered November 18–19 for Neon and November 10–19 for Carbon and Hydrogen. This convenience sample surfaced both positive and negative reports. X's public page fetch was blocked during direct cross-checks, so the linked accounts below are reports retrieved by Grok. Benchmark claims were checked against the publishers.

- SWE-sweep co-author Kilian Lieret flagged the gap between the Antigravity and Mini-SWE-agent settings. Google's methodology confirms the two setups. [Lieret on X](https://x.com/KLieret/status/2123172740043505968) · [DeepMind methodology](https://deepmind.google/models/evals-methodology/gemini-4-neon/)
- Anrry Petrin described a multi-file Expo redesign completed with the Neon planner and Hydrogen executor, with TypeScript, Jest, and physical-device checks. Elias reported a small Neon game that ran but missed the demo recording. These are concrete examples of the importance of a completion check. [Petrin on X](https://x.com/4nrry/status/2123424486112256049) · [Elias on X](https://x.com/eandualem/status/2123189826585243883)
- Jon Cooper reported latency and 429s from Carbon on a global GCP endpoint. The provider reply attributed the 429s to that project's quota. Jari Huomo reported high headless startup memory inside a large repository. These are reasons to inspect the endpoint and harness when a run is slow. [Cooper on X](https://x.com/jdc/status/2123083447371804872) · [Provider reply](https://x.com/tymofii/status/2123087819803373595) · [Huomo on X](https://x.com/jarimh1984/status/2123427564794376603)

## Local checks

Both Herdr hosts resolved the signed-in Antigravity catalog. The tests used `agy` 1.5.12 and fresh scratch copies of the existing [ledger bugfix](evidence/fleet-2026-10-06/probes/tasks/bugfix/) and [missing export](evidence/fleet-2026-10-06/probes/tasks/honesty/) fixtures. The Mac ledger run used `--mode auto --output-format json --print-timeout 115s`. The known output was the unchanged visible tests plus five independent hidden tests. The benchmark deliberately gave model workers only the workspaces and prompts, and scored their artifacts afterward.

| Mac ledger probe | Wall time | CLI result | Artifact |
|---|---:|---|---|
| Hydrogen High | 84.9 s | SUCCESS | Visible and 5/5 hidden tests passed |
| Neon High | 118.2 s | Timed out | Visible and 5/5 hidden tests passed |
| Carbon High | 38.8 s | SUCCESS | Visible and hidden tests failed |
| Argon High | 103.6 s | SUCCESS | Visible and 5/5 hidden tests passed |
| Neon XHigh | 116.8 s | Timed out | Visible and hidden tests failed |

On agentpc, the initial missing-export runs all returned exit 0 with `SUCCESS`, denied a shell action, and produced an empty response and no required result file. With session-only permission for exactly `ls -la`, `--mode accept-edits`, and a prompt using the workspace write tool, each High-effort tier produced a valid `BLOCKED` artifact and reported the blocker in its response. The rerun changed the permission and prompt together. It verifies an operating pattern, and cannot isolate an individual setting's effect.

I then ran the ledger task on agentpc with `--mode accept-edits --print-timeout 170s`, permission for exactly `python3 run_tests.py`, and explicit instructions to use workspace read and edit tools.

| agentpc ledger probe | Wall time | CLI result | Artifact |
|---|---:|---|---|
| Hydrogen High | 74.3 s | SUCCESS | Visible and 5/5 hidden tests passed |
| Neon High | 121.1 s | SUCCESS | Visible and 5/5 hidden tests passed |
| Carbon High | 55.5 s | SUCCESS | Visible and hidden tests failed |
| Neon XHigh | 172.3 s | Timed out | Visible and hidden tests failed |

Carbon's ledger runs recorded a denied `ReadFile` action and returned empty responses on both hosts. This limits what the fixture says about Carbon's coding ability and reproduces the harness problem. Neon XHigh hit the time limit on both hosts. These observations favor High for this bounded task. [Google's headless permission and status documentation](https://antigravity.google/docs/cli/headless/)

The routing change was compared with the previous skill in eight clean Codex Terra sessions. The new skill selected Neon High for the pinned Antigravity lane, while the previous skill marked it unrouted. Both chose Sol as a reviewer of Gemini work when Claude was unavailable and retained Sol Medium for an ordinary sweep. Both rejected a missing required artifact despite `SUCCESS`; the new answer cited `denied_actions` and gave a scoped recovery.

The local sample is too small to rank the families or compare throughput across machines. It supports specifying effort, keeping permission scopes explicit, and treating runtime status and task acceptance as separate checks.
