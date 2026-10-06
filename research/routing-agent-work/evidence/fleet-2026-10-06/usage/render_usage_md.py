#!/usr/bin/env python3
"""Render usage-summary.md from usage-summary.json.

Run after local_usage_metrics.py:  python3 -I render_usage_md.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def m(n):
    return "-" if n is None else f"{n / 1e6:,.1f}"


def pc(x):
    return "-" if x is None else f"{x * 100:.1f}%"


def s(x):
    return "-" if x is None else f"{x:,.0f}"


def cost(r):
    if r.get("cost_usd_logged") is not None:
        return f"${r['cost_usd_logged']:,.2f}"
    if r.get("cost_usd_ticks_logged"):
        return f"{r['cost_usd_ticks_logged'] / 1e10:,.2f} (ticks/1e10)"
    return "-"


def threads(r):
    k = r["threads_by_kind"]
    parts = [f"{v} {n}" for n, v in sorted(k.items())] if len(k) > 1 or "primary" not in k else []
    return f"{r['threads']}" + (f" ({', '.join(parts)})" if parts else "")


def table(rows, with_effort):
    head = ["CLI", "Model"] + (["Effort"] if with_effort else []) + [
        "Threads", "Turns", "API calls", "Input M", "Cache hit", "Output M", "Reasoning M",
        "Wall p50 s", "Wall p90 s", "Aborted", "Error", "No end", "Tool fail", "First", "Last", "Logged cost"]
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        cells = [r["cli"], f"`{r['model']}`"] + ([r["effort"]] if with_effort else []) + [
            threads(r), s(r["turns"]), s(r["api_calls"]), m(r["input_tokens_total"]), pc(r["cache_hit_ratio"]),
            m(r["output_tokens"]), m(r["reasoning_output_tokens"]), s(r["turn_wall_s_median"]), s(r["turn_wall_s_p90"]),
            pc(r["aborted_rate"]), pc(r["error_rate"]), pc(r["no_terminal_rate"]), pc(r["tool_failure_rate"]),
            r["first_seen"], r["last_seen"], cost(r)]
        out.append("| " + " | ".join(str(c) for c in cells) + " |")
    return "\n".join(out)


CAVEATS = """\
- **Window.** Turns start on or after 2026-09-01 00:00 UTC. The snapshot time is in `usage-summary.json` (`generated_at`). Live sessions, including this audit, still write logs, so a rerun gives slightly different numbers.
- **Claude Code retention.** `~/.claude/settings.json` sets `cleanupPeriodDays: 7`. Claude Code deletes older transcripts, so Claude rows cover about 2026-09-29 onward. Only a few long-lived files reach back to 2026-09-06. The `claude-opus-5` to `claude-opus-5-5` change on 2026-09-22 is not derivable from these logs: no `claude-opus-5` call survives.
- **Turn definitions differ by CLI.** Codex: one `turn_id` (deduplicated across forked thread files). Claude: one non-tool-result user entry that gets one or more model calls; it includes harness-injected task notifications (see `turns_by_origin`). OpenCode: one user message with one or more assistant replies. Grok: one `turn_started` event. Compare turn counts across CLIs with care.
- **Threads.** Codex `subagent` = `thread_spawn` children; `guardian` = `codex-auto-review` approval reviewers (a harness feature, not a routed lane). Claude `subagent` = files under `subagents/` (Agent tool and workflow agents). OpenCode `subagent` = sessions with a `parent_id`. Grok logs mark every session `primary`, but most Grok sessions run in agent scratchpads or experiment work directories (see `source_notes.grok.session_cwd_class`), so they are delegated or batch runs.
- **Batch runs inflate counts.** Grok `grok-4.7` (3,481 turns in the week of 2026-09-21) and Claude `claude-sonnet-5` (407 one-turn `sdk` sessions on 2026-10-01 and 2026-10-02) are mostly scripted runs. Turn counts measure volume, not interactive preference.
- **Tokens.** Input M includes cache reads and cache writes for every CLI. Totals include orchestration overhead: system prompts, tool schemas, subagent context, and compaction. Codex reasoning tokens are a subset of output tokens. Claude logs do not report reasoning tokens. OpenCode input is stored net of cache, and the script adds the cache back. Codex files from CLI 0.152.x and older have no `token_usage_record`; the script uses deduplicated `token_count` events for them.
- **Wall time.** Medians and p90 use completed turns only. Codex uses `task_complete.duration_ms`. Claude uses prompt time to the last assistant entry, so it excludes trailing tool time. OpenCode uses user message creation to the last assistant completion. Grok uses `turn_started` to `turn_ended`. Long values often include user approval waits and subagent waits.
- **Error and abort rates are harness events, not task success.** Aborted = user interrupt or cancel (Codex `turn_aborted`, Claude interrupt marker, OpenCode `MessageAbortedError`, Grok `cancelled`). Error = an API error surfaced in the log (Claude `isApiErrorMessage`, OpenCode `APIError`, Grok outcome `error`). Codex logs have no API-error event type, so the Codex error rate is 0 by construction. No end = a turn start without a completion record (crash, kill, still running). A completed turn can still be a wrong answer.
- **Tool failure rate** counts failed tool items: Codex `item_completed` status `failed`, Claude `tool_result` `is_error`, Grok `tool_completed` outcome other than `success`. A failed shell command (for example a failing test) counts as a failure, so this is a noisy signal. It is not computed for OpenCode.
- **Cost.** OpenCode cost is the `cost` field that OpenCode logged per message (provider-reported or OpenCode-priced). Grok cost is the logged `costUsdTicks`; the USD column assumes 10^10 ticks per USD, which this audit did not verify. Codex and Claude logs carry no cost, so cost is not derivable for them. No prices were invented.
- **Effort.** Codex: `turn_context.effort`. Claude: the per-entry `effort` field. OpenCode: the message `variant` (`unspecified` when absent). Grok: the session-level `summary.json` `reasoning_effort`, which is the last value set in the session.
- **Not covered.** Cloud or web sessions, other machines, and API calls that do not write these local logs. The Codex `archived_sessions` folder is included. OpenCode legacy `storage/` JSON has no files newer than 2026-09-01.
"""


def main():
    d = json.load(open(os.path.join(HERE, "usage-summary.json")))
    rows = d["by_cli_model"]
    eff = d["by_cli_model_effort"]
    weeks = list(next(iter(d["weekly_turns"].values())).keys())
    wk = ["| CLI/model | " + " | ".join(weeks) + " | Total |", "|" + "---|" * (len(weeks) + 2)]
    for k, v in d["weekly_turns"].items():
        tot = sum(v.values())
        if tot < 5:
            continue
        wk.append(f"| `{k}` | " + " | ".join(str(v[w]) for w in weeks) + f" | {tot} |")
    daily_keys = ["codex/gpt-6-astra", "codex/gpt-6-sol", "codex/gpt-6.1-sol", "codex/gpt-6-luna",
                  "claude/claude-opus-5-5", "claude/claude-fable-5-1", "claude/claude-sonnet-5", "claude/claude-sonnet-5-5"]
    days = sorted({day for k in daily_keys for day in d["daily_turns"].get(k, {}) if day >= "2026-09-20"})
    dl = ["| CLI/model | " + " | ".join(x[5:] for x in days) + " |", "|" + "---|" * (len(days) + 1)]
    for k in daily_keys:
        v = d["daily_turns"].get(k, {})
        dl.append(f"| `{k}` | " + " | ".join(str(v.get(x, 0)) for x in days) + " |")
    total_turns = sum(r["turns"] for r in rows)
    md = f"""# Local agent usage since 2026-09-01

Generated {d['generated_at']} by `local_usage_metrics.py` and `render_usage_md.py` (run with `python3 -I`). Total turns: {total_turns:,}. The data is aggregate metadata only. No prompt or message content is included.

Column key: Input M and Output M are millions of tokens. Cache hit = cached input / total input. Wall p50 and p90 are seconds per completed turn. Aborted, Error, and No end are shares of turns. Tool fail is the share of tool calls that failed. The Caveats section defines each metric.

## Per CLI and model

{table(rows, False)}

## Per CLI, model, and effort (top 25 by turns)

{table(eff[:25], True)}

## Weekly turns (week starts Monday, UTC; rows with 5 or more turns)

{chr(10).join(wk)}

## Daily turns around the model changes (from 2026-09-20)

{chr(10).join(dl)}

## Source notes

```json
{json.dumps(d['source_notes'], indent=1)}
```

## Caveats

{CAVEATS}"""
    with open(os.path.join(HERE, "usage-summary.md"), "w") as fh:
        fh.write(md)
    print("wrote usage-summary.md")


if __name__ == "__main__":
    main()
