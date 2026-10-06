#!/usr/bin/env python3
"""Run one headless OpenCode worker and report whether it really finished.

`opencode run` can exit 0 without an answer. This launcher sends the prompt
on stdin and then closes stdin, turns off configured MCP servers unless asked
to keep them, raises the output token cap, enforces a time limit, retries one
start-up database lock, and classifies the JSON event stream.

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

DEFAULT_OUTPUT_MAX = "128000"
LOCK_TEXT = "database is locked"


def final_step_text(events):
    """Return the text of the last step. Earlier steps hold narration."""
    start = 0
    for index, event in enumerate(events):
        if event.get("type") == "step_start":
            start = index
    parts = {}
    for event in events[start:]:
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
    reason = finishes[-1].get("reason") if finishes else None
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
    if errors or returncode != 0:
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


def mcp_off_config(env, work_dir):
    """Build OPENCODE_CONFIG_CONTENT that turns off each MCP server the worker would load."""
    base = json.loads(env["OPENCODE_CONFIG_CONTENT"]) if env.get("OPENCODE_CONFIG_CONTENT") else {}
    probe = subprocess.run(
        ["opencode", "debug", "config"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        cwd=work_dir,
    )
    if probe.returncode != 0:
        raise RuntimeError("opencode debug config failed: " + probe.stderr[-300:])
    names = sorted(json.loads(probe.stdout).get("mcp", {}))
    mcp = base.setdefault("mcp", {})
    for name in names:
        mcp.setdefault(name, {})["enabled"] = False
    return json.dumps(base)


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
    ]
    for events, rc, err, timed_out, want in cases:
        got = classify(events, rc, err, timed_out)[0]
        assert got == want, (want, got, events)
    multi = [start, text("a", "narration"), finish("tool-calls"), start, text("b", "draft"), text("b", "final"), finish("stop")]
    assert final_step_text(multi) == "final"
    assert classify(multi, 0, "", False)[2]["tokens"] == {"input": 20, "output": 4, "cache": {"read": 10}}
    assert len(parse_events('noise\n{"type":"text","part":{"text":"a"}}\n{bad\n')) == 1
    print("opencode_worker self-test passed")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", help="provider/model, for example openrouter/z-ai/glm-5.3")
    parser.add_argument("--variant", help="provider-supported effort variant")
    parser.add_argument("--prompt", help="prompt text")
    parser.add_argument("--prompt-file", help="read the prompt from this file")
    parser.add_argument("--dir", help="working directory for the worker")
    parser.add_argument("--timeout", type=int, default=900, help="seconds before the run is stopped")
    parser.add_argument("--output-max", default=DEFAULT_OUTPUT_MAX, help="OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX value")
    parser.add_argument("--keep-mcp", action="store_true", help="keep configured MCP servers on")
    parser.add_argument("--auto", action="store_true", help="pass --auto to approve tool permissions")
    parser.add_argument("--permission", help="inline JSON for OPENCODE_PERMISSION")
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

    env = dict(os.environ)
    env.setdefault("OPENCODE_DISABLE_AUTOUPDATE", "1")
    env["OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX"] = str(args.output_max)
    if args.permission:
        env["OPENCODE_PERMISSION"] = args.permission
    try:
        if not args.keep_mcp:
            env["OPENCODE_CONFIG_CONTENT"] = mcp_off_config(env, args.dir)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        return fail(args.model, args.variant, "cannot build MCP-off config: " + str(error))

    cmd = ["opencode", "run", "--pure", "--format", "json", "--dir", args.dir, "-m", args.model, "--variant", args.variant]
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
