# Products for intelligent fleet routing

Research date: 2026-09-22.
Sources: Parallel CLI, Perplexity MCP, official documentation, repository source, and read-only Herdr checks.

## Answer

Several products can improve parts of this workflow.
The verified shortlist contains no complete replacement for the fleet skill and Herdr together.
The important choice is the unit of selection: a whole agent task or an individual model request.

**Not Diamond's custom routing API offers the most useful commercial building block for this fleet.**
It returns a model choice without running the selected completion.
Its training system accepts custom candidates, including agents, using their evaluated outputs.
An adapter could represent each approved CLI, model, and effort combination as a candidate.
That adapter is a proposal; this research did not verify a ready-made Herdr integration.
[Selection API](https://docs.notdiamond.ai/reference/token_model_select_v2_modelrouter_modelselect_post), [custom candidates](https://docs.notdiamond.ai/docs/routing-between-custom-models)

**Not Diamond Code is a separate, more packaged product.**
It selects model and reasoning effort during a coding session.
Current documentation supports Claude Code and describes broader support as ongoing work.
It does not document selection among Claude Code, Codex, Grok CLI, and OpenCode as separate workers.
[Current support and benchmarks](https://www.notdiamond.ai/blog/interactive-benchmarks-a-new-methodology-for-evaluating-model-routing)

**Nexus Agents is the closest open-source project in task-selection scope.**
Its internal router selects a CLI, but its public MCP recommendation omits CLI and effort.
Its default execution feedback does not establish successful engineering.
[Recommendation schema](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/mcp/tools/delegate-to-model-types.ts#L54-L104), [execution feedback](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/composite-router.ts#L574-L636)

**OmO with `omo-herdr-dag` has a direct Herdr integration for workflow display.**
It does not dispatch arbitrary CLI workers through Herdr.
[Herdr extension](https://github.com/jc01rho/omo-herdr-dag)

## What the current skill already controls

The [fleet skill](../../skills/productivity/routing-agent-work/SKILL.md) chooses the worker CLI, model, effort, fallback, and reviewer.
It also controls task limits, supported settings, reviewer independence, and the report contract.
Herdr supplies terminal ownership, agent startup, prompting, lifecycle observation, and persistent sessions.

The local Herdr client and server both report version `0.9.1`, with compatible protocol `22`.
Its installed command surface includes Claude, Codex, Grok, and OpenCode.
It passes native arguments to those CLIs.
These checks establish an integration surface, not successful operation of a proposed router.
[Herdr automation](https://herdr.dev/docs/agent-automation/)

An API router normally chooses a model inside an already selected agent.
That differs from choosing which agent should own a repository task.
Changing the model inside Claude Code does not turn that worker into Codex.
The candidate comparisons below preserve that distinction.

## Product comparison

| Candidate | Useful capability | Fit with this fleet | Main limit |
|---|---|---|---|
| **Not Diamond custom routing API** | Learns selection from evaluated candidate outputs; returns a decision | An adapter could map custom agent candidates to Herdr launches | Requires training data and integration; full CLI/model/effort output is not built in |
| **Not Diamond Code** | Chooses model and reasoning effort per step using session and cache information | Promising for reducing cost inside Claude Code sessions | Early access; documented current harness support is narrower than its general marketing |
| **Nexus Agents** | Recommends agent/model routes and records execution outcomes | Closest open-source task-routing candidate | No native Grok adapter; incomplete public route contract; weak default success signal |
| **OmO + omo-herdr-dag** | Coordinates work and displays workflow dependencies in Herdr | Relevant if an OpenCode-centered system is acceptable | The Herdr extension supplies a viewer, not heterogeneous worker dispatch |
| **Claude Code Router** | Supports profiles for all four named CLIs; routes their model requests | Useful common gateway under existing Herdr sessions | Rules and agent-written tags do not establish outcome-trained routing |
| **LiteLLM Auto Routing** | Classifiers, configured tiers, adaptive model selection, and effort variants | Flexible model-request layer; a Claude Code preview exists | Beta; does not control heterogeneous CLI lifecycles |
| **vLLM Semantic Router** | Trainable model selection with a route-preview interface | A self-hosted selector could feed a Herdr adapter | Greater infrastructure and training burden |
| **OpenRouter Auto** | Selects catalog models by task category and aggregate spending patterns | Easy API-level routing inside a compatible client | Market usage does not measure success on this user's tasks |
| **Cloudflare AI Gateway** | Conditions, budgets, retries, versioned routes, and provider access | Useful execution and observation layer for Cloudflare and external models | Its documented dynamic routing is configured logic, not a learned task selector |

The detailed findings below provide the sources and qualifications for these rows.

## Commercial selection: Not Diamond

The public `modelSelect` API accepts messages and candidate models, then returns a recommendation and decision identifier.
Custom training accepts input examples, candidate responses, and evaluation scores.
Custom candidates can represent an agent or arbitrary inference endpoint.
They require unique names and declared context, price, and latency properties.
[API](https://docs.notdiamond.ai/reference/token_model_select_v2_modelrouter_modelselect_post), [training](https://docs.notdiamond.ai/docs/router-training-quickstart), [custom candidates](https://docs.notdiamond.ai/docs/routing-between-custom-models)

My proposed mapping is a candidate such as `custom/codex-sol-high` to one approved Herdr launch configuration.
The candidate name alone supplies no quality evidence.
Training must score the complete task outcome from that configuration.
The same method could include an OpenCode worker using a Cloudflare model.
These mappings are integration inferences, not tested product features.

Not Diamond Code instead uses a local proxy and a hosted optimizer.
The proxy sends derived session metadata and receives model and effort recommendations.
The user's provider or gateway executes the model request.
Code documents metadata-only routing; the general API separately accepts messages and training examples.
Do not assume the general API has Code's metadata-only boundary.
[Code documentation](https://code.notdiamond.ai/docs/), [general API](https://docs.notdiamond.ai/reference/token_model_select_v2_modelrouter_modelselect_post)

The vendor reports lower cost at comparable coding quality.
Its published trials use Claude Code and named Anthropic models.
They do not establish improvements across this fleet or these repositories.
Current Code pricing lists **$0.05 per million routed tokens**, with access by application.
Older API pricing documentation describes a different request-based offer.
Confirm custom-router pricing separately; do not apply Code pricing to that API.
[Benchmarks](https://www.notdiamond.ai/blog/interactive-benchmarks-a-new-methodology-for-evaluating-model-routing), [current pricing](https://www.notdiamond.ai/pricing), [older API pricing](https://docs.notdiamond.ai/docs/pricing)

## Agent selection: Nexus Agents

Nexus combines task classification, ranked capability scores, adaptive selection, and maintained specialization preferences.
Its internal `route()` returns a CLI decision without executing the task.
Its `executeTask()` uses that decision to call a CLI adapter.
This makes it closer to the fleet skill than a model-request proxy.
[Router source](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/composite-router.ts)

Its public `delegate_to_model` MCP tool returns a model recommendation, explanation, and alternatives.
It does not return the complete CLI, effort, and reviewer contract.
The inspected factory supports Claude, Codex, Gemini, and OpenCode, but lacks a native Grok CLI adapter.
A Herdr connection therefore needs an adapter and strict checks on eligible choices.
[MCP schema](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/mcp/tools/delegate-to-model-types.ts#L54-L104), [adapter factory](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/factory.ts)

Nexus enables outcome persistence by default and replays recent outcomes after restart.
However, `executeTask()` derives success from the adapter's `Result.ok` value.
Its execution feedback also uses routing confidence as a quality value.
Neither value proves that tests passed or the requested task finished.
Useful learning requires feedback from independent task checks.
[Persistence setting](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/config/learning-persistence.ts#L103-L115), [outcome replay](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/composite-router.ts#L431-L476), [execution feedback](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/composite-router.ts#L574-L636)

A separate confidence-based recommendation-feedback helper remains conditional in the source.
The inspected changeset removes its initialization and injection from the MCP server.
Do not describe that helper as current default MCP behavior.
[Removal changeset](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/.changeset/drop-unused-server-feedback-integration.md)

The OpenCode adapter can omit an unavailable model override.
That behavior needs correction or external rejection when the fleet requires an exact model.
This research verified implementation details, but found no independent benchmark proving better routing for this fleet.
[OpenCode adapter](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/adapters/opencode-adapter.ts)

## Existing Herdr connection: OmO

Oh My OpenAgent, or OmO, maps task categories to configured models and fallbacks.
The inspected documentation does not establish learning from verified task outcomes.
Its editions target different hosts; these do not establish one shared controller for every CLI.
[OmO repository](https://github.com/code-yeongyu/oh-my-openagent), [configuration](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/configuration.md)

The community `omo-herdr-dag` extension consumes workflow events and opens a Herdr display pane.
It uses `herdr pane` commands, not `herdr agent start` for worker dispatch.
Its verification record also identifies incomplete testing on a clean Herdr installation.
It is useful visibility tooling, but it does not replace the fleet selector.
[Extension](https://github.com/jc01rho/omo-herdr-dag), [verification record](https://github.com/jc01rho/omo-herdr-dag/blob/main/VERIFICATION.md)

OmO uses the Sustainable Use License; the Herdr extension separately uses MIT.
[OmO license](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/LICENSE.md), [extension license](https://github.com/jc01rho/omo-herdr-dag/blob/main/LICENSE)

## Common gateway: Claude Code Router

CCR explicitly lists Claude Code, Codex, Grok CLI, and OpenCode profiles.
It supports custom compatible providers, request rewrites, retries, ordered fallbacks, and request logs.
It can run without the desktop application.
This makes it a practical gateway candidate beneath existing Herdr sessions.
That Herdr arrangement remains an integration inference.
[Repository](https://github.com/musistudio/claude-code-router), [CLI](https://ccrdesk.top/en/guides/cli/)

CCR has task-aware Claude subagent selection.
It inserts model descriptions into agent tools; the agent then writes a tag selecting the desired model.
This resembles the current skill's description-based selection more than a trained outcome model.
Custom JavaScript rules can call an external policy service.
Script errors continue to later rules, so hard fleet limits need separate enforcement.
[Routing behavior](https://ccrdesk.top/en/configuration/routing/)

## Configurable model selectors

LiteLLM's current Auto Routing extends beyond ordinary load balancing.
It documents heuristic, semantic, LLM, and custom classifiers, plus adaptive selection within model tiers.
Separate deployments can represent different reasoning efforts.
Its test endpoint previews selection without executing the selected completion.
Classifier or embedding calls can still cost money.
The preview endpoint is not a verified production contract for an external task scheduler.
[Auto Routing](https://docs.litellm.ai/docs/proxy/auto_routing)

Its `lite autoroute` preview connects Claude Code through a LiteLLM proxy.
Session affinity can reduce incompatible history transfers between models.
These controls do not choose which independent CLI owns the task.
[Claude Code preview](https://docs.litellm.ai/docs/learn/autorouter_cli)

vLLM Semantic Router trains model selection from evaluation data and exposes `vllm-sr route preview --json`.
It offers more self-hosted policy control, with greater operational cost.
RouteLLM is a smaller research baseline with a Python decision interface.
However, its completion routing reads the last message, and its source notes first-turn training.
That limits its suitability for long agent sessions without additional work.
[vLLM training](https://vllm-sr.ai/docs/training/ml-model-selection), [vLLM CLI](https://github.com/vllm-project/semantic-router/blob/main/src/vllm-sr/README.md), [RouteLLM source](https://github.com/lm-sys/RouteLLM/blob/main/routellm/controller.py)

OpenRouter Auto now ranks models using task categories and recent aggregate spending patterns.
Allowed-model lists and session stickiness provide useful controls.
It does not document learning from this user's verified task outcomes.
Older descriptions that associate its current algorithm with Not Diamond can mislead.
[Current Auto Router](https://openrouter.ai/docs/guides/routing/routers/auto-router), [change announcement](https://openrouter.ai/blog/announcements/introducing-the-new-auto-router)

## Broader orchestration alternatives

Agent Orchestrator and CodeMachine manage worker execution and workspaces themselves.
Their documented controls emphasize configured agent choices and workflows, rather than learned fleet selection.
They are candidates for a broader workflow change, not small additions beside Herdr.
Agent Orchestrator now documents a Go daemon; older TypeScript plugin descriptions are stale.
[Current AO architecture](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/docs/architecture.md), [AO CLI](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/docs/cli/README.md), [CodeMachine](https://github.com/moazbuilds/CodeMachine-CLI)

Oh My ClaudeCode explicitly supports Grok CLI and other CLI workers.
Its team mode requires tmux, which overlaps Herdr's session role.
Docker Agent also supports external coding CLI workers, but those workers bypass its model-routing configuration.
Neither establishes a ready-made learned selector for this Herdr fleet.
[OMC](https://github.com/Yeachan-Heo/oh-my-claudecode), [Docker harness restrictions](https://docs.docker.com/ai/docker-agent/features/harnesses/)

## Cloudflare integration

OpenCode explicitly documents both Cloudflare Workers AI and Cloudflare AI Gateway providers.
This is stronger integration evidence than assuming every OpenAI-compatible endpoint works in every CLI.
[OpenCode providers](https://opencode.ai/docs/providers/)

Cloudflare AI Gateway supports conditional routes, quotas, percentage splits, retries, and fallback models.
It can observe and control Workers AI and supported external-provider requests.
Its current dynamic routes use the compatibility endpoint, not the newer unified REST endpoint.
[Dynamic routing](https://developers.cloudflare.com/ai-gateway/features/dynamic-routing/), [Workers AI](https://developers.cloudflare.com/ai-gateway/usage/providers/workersai/), [xAI](https://developers.cloudflare.com/ai-gateway/usage/providers/grok/)

Protocol compatibility still matters.
Cloudflare's Workers AI documentation restricts Responses requests to its GPT-OSS models and non-streaming requests.
The unified Anthropic Messages endpoint does not support Workers AI model identifiers.
The router must therefore validate the selected model's protocol and tools before choosing an execution path.
[Workers AI compatibility](https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/), [Gateway REST API](https://developers.cloudflare.com/ai-gateway/usage/rest-api/)

## Recommended direction

Keep Herdr as the owner of terminal sessions.
Keep the fleet skill as the policy that restricts eligible choices.
Add learned selection only among choices that satisfy the task's hard requirements.
Prefer whole-task selection before attempting model changes inside an active session.

For a commercial path, evaluate Not Diamond's custom decision API against representative task outcomes.
For an open-source path, inspect Nexus's recommendation interface and connect execution through Herdr.
Use OpenCode's documented Cloudflare providers where those models fit the task.
Use CCR or LiteLLM only if a shared model gateway solves an additional operational need.

The useful target is:

```text
Task and hard requirements
  -> approved CLI/model/effort candidates
  -> learned selection recommendation
  -> Herdr starts or directs the chosen CLI
  -> verified result, cost, and correction data
  -> routing evaluation and feedback
```

Measure passing checks, accepted changes, reviewer corrections, total cost, and elapsed time.
A process exit or a confident answer does not prove task completion.
First compare recommendations against the existing skill without granting the router execution control.
This is a suggested evaluation boundary, not an implemented trial.

## Research boundaries and artifacts

Parallel CLI supplied discovery and targeted extraction across independent product and orchestration research lanes.
Perplexity MCP supplied independent discovery and a challenge report.
The lead checked primary evidence and resolved disagreements between provider summaries.
These checks corrected Nexus feedback claims, OmO integration scope, and older OpenRouter algorithm descriptions.

No software was installed, no router was configured, and no product executed a coding task.
No fleet rule changed during this research.
Some products remain early access or beta; documentation does not establish performance on this user's workload.
The search covered a useful shortlist, not every routing product.

Raw outputs and detailed research notes: `/tmp/fleet-routing-products-2026-09-22/`.
Those temporary files are not durable repository evidence.
Primary source URLs in this report remain the citation record.

## Sources

- [Selection API](https://docs.notdiamond.ai/reference/token_model_select_v2_modelrouter_modelselect_post)
- [custom candidates](https://docs.notdiamond.ai/docs/routing-between-custom-models)
- [Current support and benchmarks](https://www.notdiamond.ai/blog/interactive-benchmarks-a-new-methodology-for-evaluating-model-routing)
- [Recommendation schema](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/mcp/tools/delegate-to-model-types.ts#L54-L104)
- [execution feedback](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/composite-router.ts#L574-L636)
- [Herdr extension](https://github.com/jc01rho/omo-herdr-dag)
- [Herdr automation](https://herdr.dev/docs/agent-automation/)
- [training](https://docs.notdiamond.ai/docs/router-training-quickstart)
- [Code documentation](https://code.notdiamond.ai/docs/)
- [current pricing](https://www.notdiamond.ai/pricing)
- [older API pricing](https://docs.notdiamond.ai/docs/pricing)
- [Router source](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/composite-router.ts)
- [adapter factory](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/factory.ts)
- [Persistence setting](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/config/learning-persistence.ts#L103-L115)
- [outcome replay](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/composite-router.ts#L431-L476)
- [Removal changeset](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/.changeset/drop-unused-server-feedback-integration.md)
- [OpenCode adapter](https://github.com/williamzujkowski/nexus-agents/blob/bc8f0925d33a2ac59010613afb22e00a682dde76/packages/nexus-agents/src/cli-adapters/adapters/opencode-adapter.ts)
- [OmO repository](https://github.com/code-yeongyu/oh-my-openagent)
- [configuration](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/configuration.md)
- [verification record](https://github.com/jc01rho/omo-herdr-dag/blob/main/VERIFICATION.md)
- [OmO license](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/LICENSE.md)
- [extension license](https://github.com/jc01rho/omo-herdr-dag/blob/main/LICENSE)
- [Repository](https://github.com/musistudio/claude-code-router)
- [CLI](https://ccrdesk.top/en/guides/cli/)
- [Routing behavior](https://ccrdesk.top/en/configuration/routing/)
- [Auto Routing](https://docs.litellm.ai/docs/proxy/auto_routing)
- [Claude Code preview](https://docs.litellm.ai/docs/learn/autorouter_cli)
- [vLLM training](https://vllm-sr.ai/docs/training/ml-model-selection)
- [vLLM CLI](https://github.com/vllm-project/semantic-router/blob/main/src/vllm-sr/README.md)
- [RouteLLM source](https://github.com/lm-sys/RouteLLM/blob/main/routellm/controller.py)
- [Current Auto Router](https://openrouter.ai/docs/guides/routing/routers/auto-router)
- [change announcement](https://openrouter.ai/blog/announcements/introducing-the-new-auto-router)
- [Current AO architecture](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/docs/architecture.md)
- [AO CLI](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/docs/cli/README.md)
- [CodeMachine](https://github.com/moazbuilds/CodeMachine-CLI)
- [OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Docker harness restrictions](https://docs.docker.com/ai/docker-agent/features/harnesses/)
- [OpenCode providers](https://opencode.ai/docs/providers/)
- [Dynamic routing](https://developers.cloudflare.com/ai-gateway/features/dynamic-routing/)
- [Workers AI](https://developers.cloudflare.com/ai-gateway/usage/providers/workersai/)
- [xAI](https://developers.cloudflare.com/ai-gateway/usage/providers/grok/)
- [Workers AI compatibility](https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/)
- [Gateway REST API](https://developers.cloudflare.com/ai-gateway/usage/rest-api/)

Parallel and Perplexity output directory: `/tmp/fleet-routing-products-2026-09-22/`.
