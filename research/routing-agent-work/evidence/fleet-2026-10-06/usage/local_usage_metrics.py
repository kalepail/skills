#!/usr/bin/env python3
"""Aggregate local agent-CLI usage metadata per (CLI, model, effort).

Run:  python3 -I local_usage_metrics.py [--since 2026-09-01] [--out DIR]

Read-only against the logs. Emits aggregates only: no prompt text, message
content, file contents, secrets, or tokens are copied into the outputs.

Sources
  codex     ~/.codex/sessions/**/*.jsonl + ~/.codex/archived_sessions/**/*.jsonl
  claude    ~/.claude/projects/**/*.jsonl (incl. subagents/ sidechain files)
  opencode  ~/.local/share/opencode/opencode.db (SQLite, opened mode=ro)
  grok      ~/.grok/sessions/*/*/{events.jsonl,usage.json,summary.json}
"""
import argparse
import collections
import datetime as dt
import glob
import json
import os
import sqlite3
import urllib.parse

HOME = os.path.expanduser("~")
UTC = dt.timezone.utc


def parse_ts(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return dt.datetime.fromtimestamp(s / 1000 if s > 1e11 else s, UTC)
    s = s.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(s)
    except ValueError:
        return None


def jsonl(path):
    with open(path, errors="replace") as fh:
        for line in fh:
            try:
                yield json.loads(line)
            except ValueError:
                continue


def new_turn(cli, model, effort, thread, kind, ts):
    return {
        "cli": cli, "model": model or "unknown", "effort": effort or "unspecified",
        "thread": thread, "kind": kind, "ts": ts, "wall_ms": None,
        "outcome": "no_terminal_event", "tool_calls": 0, "tool_failures": 0,
    }


def new_tok():
    return collections.Counter()


# ---------------------------------------------------------------- Codex
TOOL_ITEMS = {"CommandExecution", "McpToolCall", "FileChange", "DynamicToolCall", "CollabAgentToolCall"}


def codex(since):
    files = [
        f for pat in ("~/.codex/sessions/**/*.jsonl", "~/.codex/archived_sessions/**/*.jsonl")
        for f in glob.glob(os.path.expanduser(pat), recursive=True)
        if os.path.getmtime(f) >= since.timestamp()
    ]
    # Pass 1: own thread per file; turn ownership. Forked/spawned threads replay
    # parent turns (same turn_id) into the child file, so a turn belongs to the
    # file whose own session_meta is earliest.
    meta = {}
    turn_files = collections.defaultdict(list)
    for f in files:
        own = None
        for o in jsonl(f):
            t, p = o.get("type"), o.get("payload") or {}
            if t == "session_meta" and own is None:
                src = p.get("source")
                if isinstance(src, dict) and "subagent" in src:
                    sa = src["subagent"]
                    kind = "guardian" if isinstance(sa, dict) and sa.get("other") == "guardian" else "subagent"
                else:
                    kind = "primary"
                own = {"thread": p.get("id"), "ts": o.get("timestamp"), "kind": kind,
                       "source": src if isinstance(src, str) else kind}
            if p.get("type") == "task_started" or t == "turn_context":
                if own:
                    turn_files[p.get("turn_id")].append((own["ts"], f))
        if own:
            meta[f] = own
    owner = {tid: min(v)[1] for tid, v in turn_files.items()}

    turns, toks = {}, collections.defaultdict(new_tok)
    turn_model = {}
    no_turn_tokens = new_tok()
    for f in files:
        own = meta.get(f)
        if not own:
            continue
        thread_model = thread_effort = None
        cur_turn = None
        has_tur = False
        last_total = None
        tc_events = []
        for o in jsonl(f):
            t, p = o.get("type"), o.get("payload") or {}
            pt = p.get("type")
            if pt == "thread_settings_applied":
                ts_ = p.get("thread_settings") or {}
                thread_model = ts_.get("model") or thread_model
                thread_effort = ts_.get("reasoning_effort") or thread_effort
            elif t == "turn_context":
                tid = p.get("turn_id")
                cur_turn = tid
                turn_model[tid] = (p.get("model") or thread_model, p.get("effort") or thread_effort)
                if owner.get(tid) == f:
                    tr = turns.get(tid)
                    if tr is None:
                        tr = turns[tid] = new_turn("codex", None, None, own["thread"], own["kind"], parse_ts(o.get("timestamp")))
                    tr["model"], tr["effort"] = p.get("model") or thread_model or "unknown", p.get("effort") or thread_effort or "unspecified"
            elif pt == "task_started":
                tid = p.get("turn_id")
                cur_turn = tid
                if owner.get(tid) == f:
                    tr = turns.get(tid)
                    started = parse_ts(p.get("started_at")) or parse_ts(o.get("timestamp"))
                    if tr is None:
                        m, e = turn_model.get(tid, (thread_model, thread_effort))
                        tr = turns[tid] = new_turn("codex", m, e, own["thread"], own["kind"], started)
                    else:
                        tr["ts"] = started
            elif pt in ("task_complete", "turn_aborted"):
                tid = p.get("turn_id")
                if owner.get(tid) == f and tid in turns:
                    tr = turns[tid]
                    tr["outcome"] = "completed" if pt == "task_complete" else "aborted:" + str(p.get("reason"))
                    tr["wall_ms"] = p.get("duration_ms")
            elif pt == "item_completed":
                it = p.get("item") or {}
                tid = p.get("turn_id")
                if it.get("type") in TOOL_ITEMS and owner.get(tid) == f and tid in turns:
                    turns[tid]["tool_calls"] += 1
                    if it.get("status") == "failed":
                        turns[tid]["tool_failures"] += 1
            elif t == "token_usage_record":
                has_tur = True
                u = p.get("usage") or {}
                tid = p.get("turn_id")
                c = toks[tid] if tid else no_turn_tokens
                c["calls"] += 1
                c["input"] += u.get("input_tokens", 0)
                c["cached"] += u.get("cached_input_tokens", 0)
                c["cache_write"] += u.get("cache_write_input_tokens", 0)
                c["output"] += u.get("output_tokens", 0)
                c["reasoning"] += u.get("reasoning_output_tokens", 0)
            elif pt == "token_count":
                info = p.get("info") or {}
                tot = json.dumps(info.get("total_token_usage"), sort_keys=True)
                if info.get("last_token_usage") and tot != last_total:
                    tc_events.append((cur_turn, info["last_token_usage"]))
                last_total = tot
        if not has_tur:
            # Older CLI builds (<= 0.152.x) have no token_usage_record; use
            # token_count last_token_usage, skipping re-emitted duplicates and
            # replayed parent turns.
            for tid, u in tc_events:
                if tid is None or owner.get(tid) != f:
                    continue
                c = toks[tid]
                c["calls"] += 1
                c["input"] += u.get("input_tokens", 0)
                c["cached"] += u.get("cached_input_tokens", 0)
                c["cache_write"] += u.get("cache_write_input_tokens", 0)
                c["output"] += u.get("output_tokens", 0)
                c["reasoning"] += u.get("reasoning_output_tokens", 0)
    for tid, c in toks.items():
        if tid in turns:
            turns[tid].setdefault("tok", new_tok()).update(c)
        else:
            no_turn_tokens.update(c)
    notes = {"files": len(files), "threads": len(meta),
             "token_records_without_owned_turn": dict(no_turn_tokens)}
    return list(turns.values()), notes


# ---------------------------------------------------------------- Claude Code
INTERRUPT = "[Request interrupted by user"


def claude(since):
    files = [f for f in glob.glob(os.path.expanduser("~/.claude/projects/**/*.jsonl"), recursive=True)
             if os.path.getmtime(f) >= since.timestamp()]
    seen_prompt, seen_call = set(), {}
    turns = []
    api_errors_unattributed = 0
    retry_events = collections.Counter()
    for f in files:
        is_sub = "/subagents/" in f
        cur = None
        for o in jsonl(f):
            t = o.get("type")
            if t == "user":
                m = o.get("message") or {}
                ct = m.get("content")
                if isinstance(ct, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in ct):
                    if cur is not None:
                        for b in ct:
                            if isinstance(b, dict) and b.get("type") == "tool_result":
                                cur["tool_calls"] += 1
                                cur["tool_failures"] += bool(b.get("is_error"))
                    continue
                if o.get("isMeta") or o.get("isCompactSummary"):
                    continue
                text = ct if isinstance(ct, str) else " ".join(
                    b.get("text", "") for b in ct if isinstance(b, dict) and b.get("type") == "text") if isinstance(ct, list) else ""
                if text.lstrip().startswith(INTERRUPT):
                    if cur is not None:
                        cur["outcome"] = "aborted:interrupted"
                    continue
                uid = o.get("uuid")
                if uid in seen_prompt:  # resumed/copied history
                    cur = None
                    continue
                seen_prompt.add(uid)
                origin = o.get("origin") or {}
                if is_sub:
                    okind = "subagent_task"
                elif isinstance(origin, dict) and origin.get("kind"):
                    okind = origin["kind"]
                else:
                    okind = o.get("promptSource") or "other"
                thread = f'{o.get("sessionId")}:{os.path.basename(f)}' if is_sub else o.get("sessionId")
                cur = new_turn("claude", None, None, thread,
                               "subagent" if is_sub else "primary", parse_ts(o.get("timestamp")))
                cur.update(calls=[], origin=okind, last=None)
                cur["outcome"] = "completed"
                turns.append(cur)
            elif t == "assistant":
                m = o.get("message") or {}
                key = m.get("id") or o.get("requestId") or o.get("uuid")
                err = bool(o.get("isApiErrorMessage") or o.get("error"))
                if cur is None:
                    if err:
                        api_errors_unattributed += 1
                    continue
                cur["last"] = parse_ts(o.get("timestamp"))
                if err:
                    cur["api_error"] = cur.get("api_error", 0) + 1
                    cur["outcome"] = "api_error"
                if m.get("model") in (None, "<synthetic>"):
                    continue
                if key in seen_call:
                    # streaming writes one line per content block; keep max usage
                    prev = seen_call[key]
                    u = m.get("usage") or {}
                    if u.get("output_tokens", 0) > prev["u"].get("output_tokens", 0) and prev["turn"] is cur:
                        prev["u"] = u
                    continue
                rec = {"model": m.get("model"), "effort": o.get("effort"), "u": m.get("usage") or {}, "turn": cur}
                seen_call[key] = rec
                cur["calls"].append(rec)
            elif t == "system" and o.get("subtype") == "api_error":
                retry_events["api_error_retry"] += 1
                if cur is not None:
                    cur["api_retry"] = cur.get("api_retry", 0) + 1
    out = []
    no_model = collections.Counter()
    for tr in turns:
        calls = tr.pop("calls")
        last = tr.pop("last")
        if not calls:
            no_model[tr["origin"]] += 1
            continue
        mc = collections.Counter((c["model"], c["effort"] or "unspecified") for c in calls)
        (tr["model"], tr["effort"]), _ = mc.most_common(1)[0]
        tr["models_in_turn"] = len({c["model"] for c in calls})
        tok = new_tok()
        for c in calls:
            u = c["u"]
            tok["calls"] += 1
            tok["input"] += u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            tok["cached"] += u.get("cache_read_input_tokens", 0)
            tok["cache_write"] += u.get("cache_creation_input_tokens", 0)
            tok["output"] += u.get("output_tokens", 0)
        tr["tok"] = tok
        if last and tr["ts"]:
            tr["wall_ms"] = (last - tr["ts"]).total_seconds() * 1000
        out.append(tr)
    notes = {"files": len(files), "turns_with_no_model_call_by_origin": dict(no_model),
             "api_error_messages_outside_turn": api_errors_unattributed, **retry_events}
    return out, notes


# ---------------------------------------------------------------- OpenCode
def opencode(since):
    path = os.path.join(HOME, ".local/share/opencode/opencode.db")
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    sess_parent = dict(con.execute("select id, parent_id from session"))
    cut = int(since.timestamp() * 1000)
    users, asst = {}, collections.defaultdict(list)
    for mid, sid, data in con.execute(
            "select id, session_id, data from message where time_created >= ? order by time_created", (cut,)):
        o = json.loads(data)
        if o.get("role") == "user":
            users[mid] = (sid, o)
        elif o.get("role") == "assistant":
            asst[o.get("parentID")].append(o)
    turns = []
    orphan_asst = sum(len(v) for k, v in asst.items() if k not in users)
    for mid, (sid, u) in users.items():
        calls = asst.get(mid, [])
        if not calls:
            continue
        mc = collections.Counter((a.get("modelID"), a.get("providerID"), a.get("variant") or "unspecified") for a in calls)
        (model, prov, effort), _ = mc.most_common(1)[0]
        tr = new_turn("opencode", model, effort, sid, "subagent" if sess_parent.get(sid) else "primary",
                      parse_ts((u.get("time") or {}).get("created")))
        tr["provider"] = prov
        tok = new_tok()
        errs = []
        done = []
        for a in calls:
            tk = a.get("tokens") or {}
            cache = tk.get("cache") or {}
            tok["calls"] += 1
            # OpenCode stores input net of cache read/write; add back for a prompt total.
            tok["input"] += tk.get("input", 0) + cache.get("read", 0) + cache.get("write", 0)
            tok["cached"] += cache.get("read", 0)
            tok["cache_write"] += cache.get("write", 0)
            tok["output"] += tk.get("output", 0)
            tok["reasoning"] += tk.get("reasoning", 0)
            tok["cost_usd_micro"] += round((a.get("cost") or 0) * 1e6)
            if a.get("error"):
                errs.append(a["error"].get("name") if isinstance(a["error"], dict) else "error")
            c = (a.get("time") or {}).get("completed")
            if c:
                done.append(c)
        tr["tok"] = tok
        if "MessageAbortedError" in errs:
            tr["outcome"] = "aborted:MessageAbortedError"
        elif errs:
            tr["outcome"] = "error:" + errs[-1]
        elif len(done) == len(calls):
            tr["outcome"] = "completed"
        if done and tr["ts"]:
            tr["wall_ms"] = max(done) - (u.get("time") or {}).get("created")
        tr["error_events"] = len(errs)
        turns.append(tr)
    return turns, {"user_messages": len(users), "assistant_messages_without_user_in_window": orphan_asst}


# ---------------------------------------------------------------- Grok
def grok(since):
    dirs = [d for d in glob.glob(os.path.join(HOME, ".grok/sessions/*/*/"))
            if os.path.exists(d + "events.jsonl") and os.path.getmtime(d + "events.jsonl") >= since.timestamp()]
    turns = []
    unmatched_usage = 0
    cwd_class = collections.Counter()
    for d in dirs:
        cwd = urllib.parse.unquote(d.split("/sessions/")[1].split("/")[0])
        cwd_class["tmp_or_scratchpad" if cwd.startswith(("/private/tmp", "/tmp")) else
                  "experiment_work_dir" if "/work/" in cwd or "/progressive-" in cwd else "other"] += 1
        effort = None
        try:
            effort = json.load(open(d + "summary.json")).get("reasoning_effort")
        except (OSError, ValueError):
            pass
        st = []
        cur = None
        for o in jsonl(d + "events.jsonl"):
            t = o.get("type")
            if t == "turn_started":
                cur = new_turn("grok", o.get("model_id"), effort, o.get("session_id") or d,
                               "primary" if o.get("session_relationship") == "primary" else str(o.get("session_relationship")),
                               parse_ts(o.get("ts")))
                st.append(cur)
            elif t == "tool_completed" and cur is not None:
                cur["tool_calls"] += 1
                cur["tool_failures"] += o.get("outcome") != "success"
            elif t == "turn_ended" and cur is not None:
                cur["outcome"] = {"completed": "completed", "cancelled": "aborted:cancelled"}.get(o.get("outcome"), "error:" + str(o.get("outcome")))
                end = parse_ts(o.get("ts"))
                if end and cur["ts"]:
                    cur["wall_ms"] = (end - cur["ts"]).total_seconds() * 1000
                cur = None
        try:
            ut = json.load(open(d + "usage.json")).get("turns") or []
        except (OSError, ValueError):
            ut = []
        ut = sorted(ut, key=lambda x: x.get("turnNumber", 0))
        if ut and len(ut) != len(st):
            unmatched_usage += 1
        for i, u in enumerate(ut):
            tr = st[min(i, len(st) - 1)] if st else None
            if tr is None:
                continue
            tok = tr.setdefault("tok", new_tok())
            tok["calls"] += u.get("modelCalls", 0)
            tok["input"] += u.get("inputTokens", 0)
            tok["cached"] += u.get("cachedReadTokens", 0)
            tok["cache_write"] += u.get("cacheCreationTokens", 0)
            tok["output"] += u.get("outputTokens", 0)
            tok["reasoning"] += u.get("reasoningTokens", 0)
            tok["cost_usd_ticks"] += u.get("costUsdTicks", 0)
            tr["billed_model"] = u.get("primaryModelId")
        turns.extend(st)
    return turns, {"session_dirs": len(dirs), "sessions_usage_turncount_mismatch": unmatched_usage,
                   "session_cwd_class": dict(cwd_class)}


# ---------------------------------------------------------------- aggregate
def pct(vals, q):
    if not vals:
        return None
    v = sorted(vals)
    k = max(0, min(len(v) - 1, int(round(q * len(v) + 0.5)) - 1))
    return round(v[k] / 1000, 1)


def week_of(ts):
    d = ts.date()
    return (d - dt.timedelta(days=d.weekday())).isoformat()


def aggregate(turns, keyf):
    groups = collections.defaultdict(list)
    for tr in turns:
        groups[keyf(tr)].append(tr)
    rows = []
    for key, trs in groups.items():
        tok = new_tok()
        for tr in trs:
            tok.update(tr.get("tok") or {})
        walls = [tr["wall_ms"] for tr in trs if tr["outcome"] == "completed" and tr["wall_ms"] is not None]
        oc = collections.Counter(tr["outcome"].split(":")[0] for tr in trs)
        n = len(trs)
        row = dict(zip(("cli", "model", "effort"), key)) if isinstance(key, tuple) else {"key": key}
        row.update({
            "threads": len({tr["thread"] for tr in trs}),
            "threads_by_kind": dict(collections.Counter(k for k, _ in {(tr["kind"], tr["thread"]) for tr in trs})),
            "turns": n,
            "turns_by_kind": dict(collections.Counter(tr["kind"] for tr in trs)),
            "api_calls": tok["calls"],
            "input_tokens_total": tok["input"],
            "cached_input_tokens": tok["cached"],
            "cache_write_tokens": tok["cache_write"],
            "output_tokens": tok["output"],
            "reasoning_output_tokens": tok["reasoning"] if trs[0]["cli"] != "claude" else None,
            "cache_hit_ratio": round(tok["cached"] / tok["input"], 4) if tok["input"] else None,
            "turn_wall_s_median": pct(walls, 0.5),
            "turn_wall_s_p90": pct(walls, 0.9),
            "wall_samples": len(walls),
            "outcomes": dict(oc),
            "tool_calls": sum(tr["tool_calls"] for tr in trs) if trs[0]["cli"] != "opencode" else None,
            "tool_failure_rate": (round(sum(tr["tool_failures"] for tr in trs) / max(1, sum(tr["tool_calls"] for tr in trs)), 4)
                                  if trs[0]["cli"] != "opencode" else None),
            "aborted_rate": round(oc["aborted"] / n, 4),
            "error_rate": round((oc["error"] + oc["api_error"]) / n, 4),
            "no_terminal_rate": round(oc["no_terminal_event"] / n, 4),
            "first_seen": min(tr["ts"] for tr in trs).date().isoformat(),
            "last_seen": max(tr["ts"] for tr in trs).date().isoformat(),
        })
        if tok["cost_usd_micro"]:
            row["cost_usd_logged"] = round(tok["cost_usd_micro"] / 1e6, 2)
        if tok["cost_usd_ticks"]:
            row["cost_usd_ticks_logged"] = tok["cost_usd_ticks"]
        if trs[0]["cli"] == "claude":
            row["api_error_messages"] = sum(tr.get("api_error", 0) for tr in trs)
            row["api_retry_events"] = sum(tr.get("api_retry", 0) for tr in trs)
            row["turns_by_origin"] = dict(collections.Counter(tr.get("origin") for tr in trs))
        if trs[0]["cli"] == "opencode":
            row["providers"] = dict(collections.Counter(tr.get("provider") for tr in trs))
            row["error_events"] = sum(tr.get("error_events", 0) for tr in trs)
        rows.append(row)
    rows.sort(key=lambda r: -r["turns"])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-09-01")
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()
    since = dt.datetime.fromisoformat(a.since).replace(tzinfo=UTC)
    all_turns, notes = [], {}
    for name, fn in (("codex", codex), ("claude", claude), ("opencode", opencode), ("grok", grok)):
        try:
            trs, n = fn(since)
        except Exception as e:  # keep other sources running
            trs, n = [], {"error": f"{type(e).__name__}: {e}"}
        trs = [t for t in trs if t["ts"] and t["ts"] >= since]
        notes[name] = n
        all_turns.extend(trs)
    by_model_effort = aggregate(all_turns, lambda t: (t["cli"], t["model"], t["effort"]))
    by_model = aggregate(all_turns, lambda t: (t["cli"], t["model"], "*"))
    weeks = sorted({week_of(t["ts"]) for t in all_turns})
    series = collections.defaultdict(lambda: collections.Counter())
    for t in all_turns:
        series[f'{t["cli"]}/{t["model"]}'][week_of(t["ts"])] += 1
    weekly = {k: {w: v.get(w, 0) for w in weeks} for k, v in sorted(series.items(), key=lambda kv: -sum(kv[1].values()))}
    daily = collections.defaultdict(collections.Counter)
    for t in all_turns:
        daily[f'{t["cli"]}/{t["model"]}'][t["ts"].date().isoformat()] += 1
    daily = {k: dict(sorted(v.items())) for k, v in sorted(daily.items())}
    out = {
        "generated_at": dt.datetime.now(UTC).isoformat(timespec="seconds"),
        "since_utc": since.isoformat(),
        "definitions": {
            "turn": "codex: task_started/turn_context turn_id (deduped across forked files); claude: non-tool-result, non-meta user entry with >=1 model API call before the next such entry; opencode: user message with >=1 assistant reply; grok: events.jsonl turn_started",
            "input_tokens_total": "all prompt tokens incl. cache reads and cache writes (codex input_tokens; claude input+cache_read+cache_creation; opencode input+cache.read+cache.write; grok inputTokens)",
            "cache_hit_ratio": "cached_input_tokens / input_tokens_total",
            "turn_wall_s": "completed turns only; codex task_complete.duration_ms; claude prompt ts -> last assistant entry ts; opencode user created -> last assistant completed; grok turn_started -> turn_ended",
            "aborted": "codex turn_aborted; claude '[Request interrupted by user' marker; opencode MessageAbortedError; grok turn_ended outcome=cancelled",
            "error": "claude assistant isApiErrorMessage/error; opencode assistant error other than abort; grok turn_ended outcome=error; codex has no error event type in these logs",
            "tool_failure_rate": "codex item_completed status=failed over CommandExecution/McpToolCall/FileChange/DynamicToolCall/CollabAgentToolCall items; claude tool_result is_error; grok tool_completed outcome!=success; not computed for opencode",
            "no_terminal_event": "turn start seen but no completion/abort record (crash, kill, still running, or log truncation)",
            "week": "ISO week starting Monday, UTC",
        },
        "source_notes": notes,
        "by_cli_model": by_model,
        "by_cli_model_effort": by_model_effort,
        "weekly_turns": weekly,
        "daily_turns": daily,
    }
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "usage-summary.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"turns={len(all_turns)} rows={len(by_model_effort)} -> {a.out}/usage-summary.json")


if __name__ == "__main__":
    main()
