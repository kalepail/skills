#!/usr/bin/env python3
"""Run one headless OpenCode V2 worker and report whether it really finished.

`opencode run` can exit 0 without an answer. This launcher does these steps:
- It runs a private `--standalone` server, so the per-run config reaches it.
- It runs in the work directory and sets PWD to that directory.
- It clears multiplexer pane variables.
- It turns off configured MCP servers unless asked to keep them.
- It sends the prompt on stdin and then closes stdin.
- It stops the run after the time limit.
- It retries one start-up database lock.
- It classifies the JSON event stream.

Exit codes: 0 complete; 2 truncated, incomplete, empty, filtered, or
unconfirmed; 3 timeout; 4 CLI, provider, or launcher error; 64 usage error.
Stdout: one JSON summary line. The answer is the text of the final step;
--text-out writes it, and --events-out keeps the full stream.
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time

LOCK_TEXT = "database is locked"
# --standalone: only a private server sees OPENCODE_CONFIG_CONTENT.
PROBE_CMD = ["opencode", "debug", "config", "--standalone"]
# Pane plugins (Herdr, Moshi) report only when they see these variables.
PANE_VARS = ("TMUX", "TMUX_PANE", "ZELLIJ", "ZELLIJ_PANE_ID", "ZELLIJ_SESSION_NAME")
PANE_PREFIXES = ("HERDR_", "HC_")


def final_step(events):
    """Return the events from the last `step_start` to the end."""
    start = 0
    for index, event in enumerate(events):
        if event.get("type") == "step_start":
            start = index
    return events[start:]


def final_step_text(events):
    """Return the text of the last step. Earlier steps hold narration."""
    parts = {}
    for event in final_step(events):
        if event.get("type") == "text":
            part = event.get("part", {})
            parts[part.get("id") or len(parts)] = part.get("text", "")
    return "".join(parts.values())


def sum_tokens(finishes):
    total = {}
    for finish in finishes:
        for key, value in (finish.get("tokens") or {}).items():
            if isinstance(value, dict):
                bucket = total.setdefault(key, {})
                for inner, amount in value.items():
                    bucket[inner] = bucket.get(inner, 0) + (amount or 0)
            elif isinstance(value, (int, float)):
                total[key] = total.get(key, 0) + value
    return total or None


def classify(events, returncode, stderr, timed_out):
    """Return (status, exit_code, details) for one finished run."""
    text = final_step_text(events)
    finishes = [e.get("part", {}) for e in events if e.get("type") == "step_finish"]
    errors = [e.get("error") for e in events if e.get("type") == "error"]
    rejected = [
        e.get("part", {}).get("tool")
        for e in events
        if e.get("type") == "tool_use"
        and "rejected permission" in str(e.get("part", {}).get("state", {}).get("error", ""))
    ]
    # Judge only the final step: an earlier step's finish says nothing about it.
    step_finishes = [e.get("part", {}) for e in final_step(events) if e.get("type") == "step_finish"]
    reason = step_finishes[-1].get("reason") if step_finishes else None
    details = {
        "final_reason": reason,
        "text_chars": len(text),
        "steps": len(finishes),
        "tokens": sum_tokens(finishes),
        "rejected_tools": rejected,
        "errors": errors,
    }
    if timed_out:
        return "timeout", 3, details
    if errors or returncode != 0 or reason == "error":
        details["stderr_tail"] = stderr[-400:]
        return "error", 4, details
    if reason == "length":
        return "truncated", 2, details
    if reason == "content-filter":
        return "filtered", 2, details
    if reason in ("other", "unknown") and text.strip():
        return "unconfirmed", 2, details
    if reason != "stop":
        return "incomplete", 2, details
    if not text.strip():
        return "empty", 2, details
    return "complete", 0, details


def parse_events(stdout):
    events = []
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return events


def model_ref(model, variant):
    """V2 selects a variant with `provider/model#variant`."""
    return model + "#" + variant if variant else model


def worker_env(base, work_dir):
    """Copy the environment without multiplexer pane variables.

    OpenCode takes its project directory from PWD, not from the process
    working directory, so PWD must name the work directory.
    """
    env = {
        key: value
        for key, value in base.items()
        if key not in PANE_VARS and not key.startswith(PANE_PREFIXES)
    }
    env["PWD"] = os.path.abspath(work_dir)
    return env


def checked_content(content):
    """Check the container types this launcher merges into. Raise ValueError."""
    if not isinstance(content, dict):
        raise ValueError("OPENCODE_CONFIG_CONTENT must be a JSON object")
    if not isinstance(content.get("permissions", []), list):
        raise ValueError("OPENCODE_CONFIG_CONTENT permissions must be an array")
    mcp = content.get("mcp", {})
    if not isinstance(mcp, dict):
        raise ValueError("OPENCODE_CONFIG_CONTENT mcp must be an object")
    servers = mcp.get("servers", {})
    if not isinstance(servers, dict) or not all(isinstance(v, dict) for v in servers.values()):
        raise ValueError("OPENCODE_CONFIG_CONTENT mcp.servers must map names to objects")
    return content


def mcp_off_content(sources, base):
    """Turn off every MCP server in the `debug config` sources and in `base`.

    V2 replaces a whole server object on override. Each entry starts from the
    source fields, takes the base fields over them, and gains `disabled: true`.
    """
    servers = {}
    for source in sources:
        info = source.get("info") or {}
        for name, entry in ((info.get("mcp") or {}).get("servers") or {}).items():
            servers[name] = dict(entry)
    target = base.setdefault("mcp", {}).setdefault("servers", {})
    for name in set(servers) | set(target):
        merged = dict(servers.get(name, {}))
        merged.update(target.get(name, {}))
        merged["disabled"] = True
        target[name] = merged
    return base


def config_sources(env, work_dir):
    probe = subprocess.run(
        PROBE_CMD,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        cwd=work_dir,
    )
    if probe.returncode != 0:
        raise RuntimeError("opencode debug config failed: " + probe.stderr[-300:])
    sources = json.loads(probe.stdout)
    if not isinstance(sources, list):
        raise ValueError("opencode debug config did not return a source list")
    return sources


def run_once(cmd, prompt, env, timeout, cwd):
    started = time.monotonic()
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        cwd=cwd,
        start_new_session=True,
    )
    timed_out = False
    try:
        stdout, stderr = proc.communicate(input=prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode, timed_out, round(time.monotonic() - started, 1)


def fail(model, variant, message, code=4):
    print(json.dumps({"status": "error", "model": model, "variant": variant, "launcher_error": message}))
    return code


def self_test():
    def text(part_id, value):
        return {"type": "text", "part": {"id": part_id, "text": value}}

    def finish(reason):
        return {"type": "step_finish", "part": {"reason": reason, "tokens": {"input": 10, "output": 2, "cache": {"read": 5}}}}

    start = {"type": "step_start", "part": {}}
    tool_ok = {"type": "tool_use", "part": {"tool": "read", "state": {"status": "completed"}}}
    rejected = {"type": "tool_use", "part": {"tool": "read", "state": {"status": "error", "error": "The user rejected permission to use this specific tool call."}}}
    cases = [
        ([start, text("a", "ok"), finish("stop")], 0, "", False, "complete"),
        ([start, text("a", "Let me read it."), tool_ok, finish("tool-calls"), start, text("b", "answer"), finish("stop")], 0, "", False, "complete"),
        ([start, text("a", "Let me read it."), tool_ok, finish("tool-calls"), start, finish("stop")], 0, "", False, "empty"),
        ([start, finish("length")], 0, "", False, "truncated"),
        ([start, text("a", "partial"), finish("content-filter")], 0, "", False, "filtered"),
        ([start, text("a", "maybe done"), finish("unknown")], 0, "", False, "unconfirmed"),
        ([start], 0, "", False, "incomplete"),
        ([start, rejected, finish("tool-calls")], 0, "", False, "incomplete"),
        ([{"type": "error", "error": {"name": "UnknownError"}}], 1, "", False, "error"),
        ([], 1, "Error: " + LOCK_TEXT, False, "error"),
        ([start, text("a", "partial")], 0, "", True, "timeout"),
        ([start, finish("stop"), start, text("b", "partial")], 0, "", False, "incomplete"),
        ([start, text("a", "failed"), finish("error")], 0, "", False, "error"),
    ]
    for events, rc, err, timed_out, want in cases:
        got = classify(events, rc, err, timed_out)[0]
        assert got == want, (want, got, events)
    multi = [start, text("a", "narration"), finish("tool-calls"), start, text("b", "draft"), text("b", "final"), finish("stop")]
    assert final_step_text(multi) == "final"
    assert classify(multi, 0, "", False)[2]["tokens"] == {"input": 20, "output": 4, "cache": {"read": 10}}
    assert len(parse_events('noise\n{"type":"text","part":{"text":"a"}}\n{bad\n')) == 1
    assert model_ref("moonshotai/kimi-k3", "max") == "moonshotai/kimi-k3#max"
    assert model_ref("moonshotai/kimi-k3", None) == "moonshotai/kimi-k3"
    env = worker_env({"PATH": "/bin", "HERDR_PANE_ID": "p1", "HC_TERMINAL_ID": "t1", "TMUX": "x", "HOME": "/h", "PWD": "/caller"}, "/work")
    assert env == {"PATH": "/bin", "HOME": "/h", "PWD": "/work"}
    sources = [
        {"type": "document", "info": {"mcp": {"servers": {"a": {"type": "remote", "url": "https://a"}, "b": {"type": "local", "command": ["b"]}}}}},
        {"type": "directory", "info": {}},
        {"type": "document", "info": {"mcp": {"servers": {"a": {"type": "remote", "url": "https://a2"}}}}},
    ]
    off = mcp_off_content(sources, {"mcp": {"servers": {"b": {"type": "local", "command": ["mine"]}}}})["mcp"]["servers"]
    assert off["a"] == {"type": "remote", "url": "https://a2", "disabled": True}
    assert off["b"] == {"type": "local", "command": ["mine"], "disabled": True}
    assert mcp_off_content([], {}) == {"mcp": {"servers": {}}}
    partial = mcp_off_content(sources, {"mcp": {"servers": {"a": {"headers": {"X": "1"}}}}})["mcp"]["servers"]["a"]
    assert partial == {"type": "remote", "url": "https://a2", "headers": {"X": "1"}, "disabled": True}
    inline = mcp_off_content([], {"mcp": {"servers": {"i": {"type": "local", "command": ["i"]}}}})["mcp"]["servers"]["i"]
    assert inline == {"type": "local", "command": ["i"], "disabled": True}
    assert "--standalone" in PROBE_CMD
    clean = {}
    assert checked_content(clean) == {}
    for bad in ([], {"permissions": None}, {"permissions": {"shell": "allow"}}, {"mcp": None},
                {"mcp": {"servers": []}}, {"mcp": {"servers": {"a": 1}}}):
        try:
            checked_content(bad)
        except ValueError:
            continue
        raise AssertionError(("accepted bad config", bad))
    print("opencode_worker self-test passed")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", help="provider/model, for example openrouter/z-ai/glm-5.3")
    parser.add_argument("--variant", help="provider-supported effort variant, sent as provider/model#variant")
    parser.add_argument("--prompt", help="prompt text")
    parser.add_argument("--prompt-file", help="read the prompt from this file")
    parser.add_argument("--dir", help="work directory; the worker runs in it as its project")
    parser.add_argument("--timeout", type=int, default=900, help="seconds before the run is stopped")
    parser.add_argument("--keep-mcp", action="store_true", help="keep configured MCP servers on")
    parser.add_argument("--auto", action="store_true", help="pass --auto to approve tool permissions")
    parser.add_argument("--permission", help='JSON array of permission rules, for example [{"action":"shell","resource":"*","effect":"deny"}]')
    parser.add_argument("--text-out", help="write the final answer text to this file")
    parser.add_argument("--events-out", help="write the raw JSON event stream to this file")
    parser.add_argument("--self-test", action="store_true", help="run offline classifier checks")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.model or not args.variant or not args.dir or bool(args.prompt) == bool(args.prompt_file):
        parser.print_usage(sys.stderr)
        print("error: --model, --variant, --dir, and exactly one of --prompt or --prompt-file are required", file=sys.stderr)
        return 64
    if not os.path.isdir(args.dir):
        return fail(args.model, args.variant, "work directory does not exist: " + args.dir, 64)

    try:
        prompt = args.prompt if args.prompt else open(args.prompt_file, encoding="utf-8").read()
    except OSError as error:
        return fail(args.model, args.variant, "cannot read prompt file: " + str(error), 64)

    env = worker_env(os.environ, args.dir)
    env.setdefault("OPENCODE_DISABLE_AUTOUPDATE", "1")
    try:
        content = json.loads(env["OPENCODE_CONFIG_CONTENT"]) if env.get("OPENCODE_CONFIG_CONTENT") else {}
        checked_content(content)
        if args.permission:
            rules = json.loads(args.permission)
            if not isinstance(rules, list):
                raise ValueError("--permission must be a JSON array of rules")
            content.setdefault("permissions", []).extend(rules)
        if not args.keep_mcp:
            content = mcp_off_content(config_sources(env, args.dir), content)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        return fail(args.model, args.variant, "cannot build worker config: " + str(error))
    if content:
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps(content)

    cmd = ["opencode", "run", "--standalone", "--format", "json", "-m", model_ref(args.model, args.variant)]
    if args.auto:
        cmd.append("--auto")

    attempts = 0
    try:
        while True:
            attempts += 1
            stdout, stderr, rc, timed_out, secs = run_once(cmd, prompt, env, args.timeout, args.dir)
            events = parse_events(stdout)
            if LOCK_TEXT in stderr and not events and attempts == 1:
                time.sleep(3)
                continue
            break
    except OSError as error:
        return fail(args.model, args.variant, "cannot start opencode: " + str(error))

    status, code, details = classify(events, rc, stderr, timed_out)
    if args.text_out:
        with open(args.text_out, "w", encoding="utf-8") as handle:
            handle.write(final_step_text(events))
    if args.events_out:
        with open(args.events_out, "w", encoding="utf-8") as handle:
            handle.write(stdout)
    session = next((e.get("sessionID") for e in events if e.get("sessionID")), None)
    summary = {"status": status, "model": args.model, "variant": args.variant, "seconds": secs,
               "attempts": attempts, "session_id": session, **details}
    print(json.dumps(summary))
    return code


if __name__ == "__main__":
    sys.exit(main())
