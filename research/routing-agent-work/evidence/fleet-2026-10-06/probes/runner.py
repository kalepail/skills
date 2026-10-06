"""Probe runner: run each (config, task, rep) in a fresh temp copy, grade it, save raw JSON.

Usage:
  python3 runner.py run [--configs a,b] [--tasks t1,t2] [--reps N] [--extra-reps-tasks bugfix,routing] [--jobs 6]
  python3 runner.py reparse        # recompute usage/cost from saved logs and re-grade nothing
Python 3.9, stdlib only.
"""

import argparse
import concurrent.futures as cf
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LOGS = os.path.join(RAW, "logs")
SCRATCH = os.environ.get("PROBE_SCRATCH", "/private/tmp/claude-501/-Users-kalepail-Desktop-kalepail-skills/"
                         "fd5aae97-76bc-4bb3-8597-af0fa91bb3f0/scratchpad/probe-runs")
TIMEOUT_S = 12 * 60
TASKS = ["bugfix", "extract", "honesty", "prose", "routing"]
RUN_COST_CAP = 3.0
TOTAL_COST_CAP = 55.0

CONFIGS = {
    "sol-high": {"cli": "codex", "model": "gpt-6.1-sol", "effort": "high"},
    "sol-xhigh": {"cli": "codex", "model": "gpt-6.1-sol", "effort": "xhigh"},
    "astra-high": {"cli": "codex", "model": "gpt-6-astra", "effort": "high"},
    "luna-high": {"cli": "codex", "model": "gpt-6-luna", "effort": "high"},
    "opus-medium": {"cli": "claude", "model": "claude-opus-5-5", "effort": "medium"},
    "opus-high": {"cli": "claude", "model": "claude-opus-5-5", "effort": "high"},
    "sonnet-medium": {"cli": "claude", "model": "claude-sonnet-5-5", "effort": "medium"},
    "sonnet-high": {"cli": "claude", "model": "claude-sonnet-5-5", "effort": "high"},
    "grok-high": {"cli": "grok", "model": "grok-4.7", "effort": "high"},
    "glm-max": {"cli": "opencode", "model": "openrouter/z-ai/glm-5.3", "effort": "max"},
    "glmflash-max": {"cli": "opencode", "model": "openrouter/z-ai/glm-5.3-flash", "effort": "max"},
    "kimi-max": {"cli": "opencode", "model": "moonshotai/kimi-k3", "effort": "max"},
    "muse-xhigh": {"cli": "opencode", "model": "openrouter/meta/muse-spark-1.3", "effort": "xhigh",
                   "note": "meta/ direct route returned HTTP 402 billing verification failed"},
    "dsflash-max": {"cli": "opencode", "model": "openrouter/deepseek/deepseek-v4.1-flash", "effort": "max"},
}

CLAUDE_BASH_ALLOW = ["Bash(python3 *)", "Bash(ls *)", "Bash(ls)", "Bash(cat *)", "Bash(head *)", "Bash(tail *)",
                     "Bash(wc *)", "Bash(grep *)", "Bash(diff *)", "Bash(./upload_report.sh *)", "Bash(sh *)",
                     "Bash(test *)", "Bash(pwd)", "Bash(find *)"]

lock = threading.Lock()
spend = {"total": 0.0, "by_config": {}, "capped": set()}


def build_cmd(cfg, wd, prompt, last_path):
    cli, model, effort = cfg["cli"], cfg["model"], cfg["effort"]
    if cli == "codex":
        return ["codex", "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
                "-s", "workspace-write", "-C", wd, "-m", model, "-c", f'model_reasoning_effort="{effort}"',
                "--json", "-o", last_path, prompt]
    if cli == "claude":
        return ["claude", "-p", "--model", model, "--effort", effort, "--output-format", "json",
                "--restricted", "--strict-mcp-config", "--no-session-persistence",
                "--tools", "Bash,Read,Edit,Write,Glob,Grep", "--permission-mode", "acceptEdits",
                "--allowedTools", *CLAUDE_BASH_ALLOW, "--", prompt]
    if cli == "grok":
        return ["grok", "-p", prompt, "--cwd", wd, "-m", model, "--reasoning-effort", effort,
                "--output-format", "json", "--always-approve", "--disable-web-search", "--no-subagents"]
    if cli == "opencode":
        return ["opencode", "run", "--pure", "-m", model, "--variant", effort, "--format", "json",
                "--dir", wd, "--auto", prompt]
    raise ValueError(cli)


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def parse_output(cli, stdout, last_path):
    """Return dict(final, input_tokens, output_tokens, cached_tokens, reasoning_tokens, cost_usd, api_error)."""
    out = {"final": None, "input_tokens": None, "output_tokens": None, "cached_tokens": None,
           "reasoning_tokens": None, "cost_usd": None, "api_error": None}
    lines = [l for l in stdout.splitlines() if l.strip()]
    if cli == "codex":
        inp = outp = cached = reas = 0
        seen = False
        for l in lines:
            try:
                ev = json.loads(l)
            except ValueError:
                continue
            t = ev.get("type")
            if t == "turn.completed" and isinstance(ev.get("usage"), dict):
                u = ev["usage"]
                seen = True
                inp += u.get("input_tokens", 0) or 0
                outp += u.get("output_tokens", 0) or 0
                cached += u.get("cached_input_tokens", 0) or 0
                reas += u.get("reasoning_output_tokens", 0) or 0
            elif t in ("error", "turn.failed"):
                out["api_error"] = json.dumps(ev)[:500]
            elif t == "item.completed" and (ev.get("item") or {}).get("type") == "agent_message":
                out["final"] = ev["item"].get("text")
        if seen:
            out.update(input_tokens=inp, output_tokens=outp, cached_tokens=cached, reasoning_tokens=reas or None)
        if os.path.exists(last_path):
            txt = open(last_path).read()
            if txt.strip():
                out["final"] = txt
    elif cli == "claude":
        try:
            j = json.loads(stdout.strip().splitlines()[-1]) if lines else {}
        except ValueError:
            j = {}
        if isinstance(j, list):
            j = next((x for x in reversed(j) if isinstance(x, dict) and x.get("type") == "result"), {})
        u = j.get("usage") or {}
        out.update(final=j.get("result"), cost_usd=_num(j.get("total_cost_usd")),
                   input_tokens=(u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
                   + (u.get("cache_read_input_tokens") or 0) if u else None,
                   output_tokens=u.get("output_tokens"), cached_tokens=u.get("cache_read_input_tokens"))
        if j.get("is_error"):
            out["api_error"] = str(j.get("result") or j.get("subtype"))[:500]
    elif cli == "grok":
        j = None
        try:
            j = json.loads(stdout)
        except ValueError:
            for l in reversed(lines):
                try:
                    j = json.loads(l)
                    break
                except ValueError:
                    continue
        if isinstance(j, dict):
            out["final"] = j.get("text") or j.get("result") or j.get("response") or j.get("output")
            u = j.get("usage") or {}
            out.update(input_tokens=(u.get("input_tokens") or u.get("prompt_tokens") or 0)
                       + (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0),
                       output_tokens=u.get("output_tokens") or u.get("completion_tokens"),
                       cached_tokens=u.get("cache_read_input_tokens") or u.get("cached_tokens"),
                       reasoning_tokens=u.get("reasoning_tokens"),
                       cost_usd=_num(j.get("total_cost_usd") or j.get("cost_usd") or j.get("cost")))
            if j.get("is_error") or j.get("error"):
                out["api_error"] = str(j.get("error") or j.get("result"))[:500]
    elif cli == "opencode":
        inp = outp = cached = reas = 0
        cost = 0.0
        texts = []
        seen = False
        for l in lines:
            try:
                ev = json.loads(l)
            except ValueError:
                continue
            part = ev.get("part") or {}
            if ev.get("type") == "step_finish" or part.get("type") == "step-finish":
                tk = part.get("tokens") or {}
                seen = True
                inp += (tk.get("input") or 0)
                outp += (tk.get("output") or 0)
                reas += (tk.get("reasoning") or 0)
                cached += ((tk.get("cache") or {}).get("read") or 0)
                cost += _num(part.get("cost")) or 0.0
            elif ev.get("type") == "text" or part.get("type") == "text":
                if part.get("text"):
                    texts.append(part["text"])
            elif ev.get("type") == "error":
                out["api_error"] = json.dumps(ev.get("error") or ev)[:500]
        if seen:
            out.update(input_tokens=inp + cached, output_tokens=outp, cached_tokens=cached,
                       reasoning_tokens=reas or None, cost_usd=round(cost, 6))
        if texts:
            out["final"] = texts[-1]
    return out


def grade(task, wd, final_path):
    cmd = [sys.executable, "-I", "-B", os.path.join(HERE, "tasks", task, "grade.py"), wd]
    if task == "honesty":
        cmd.append(final_path)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return {"pass": False, "score": 0.0, "error": "grader crashed: " + (p.stderr or p.stdout)[-800:]}


def run_one(cfg_name, task, rep):
    cfg = CONFIGS[cfg_name]
    run_id = f"{cfg_name}__{task}__r{rep}"
    raw_path = os.path.join(RAW, run_id + ".json")
    if os.path.exists(raw_path):
        return json.load(open(raw_path))
    with lock:
        if spend["total"] >= TOTAL_COST_CAP:
            return {"run_id": run_id, "skipped": "total budget cap"}
        if rep > 1 and cfg_name in spend["capped"]:
            return {"run_id": run_id, "skipped": "config run cost > $3"}
    base = os.path.join(SCRATCH, run_id + "__" + str(int(time.time())))
    wd = os.path.join(base, "work")
    shutil.copytree(os.path.join(HERE, "tasks", task, "workspace"), wd)
    last_path = os.path.join(base, "last_message.txt")
    prompt = open(os.path.join(HERE, "tasks", task, "prompt.txt")).read()
    cmd = build_cmd(cfg, wd, prompt, last_path)
    env = os.environ.copy()
    for k in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT"):
        env.pop(k, None)
    os.makedirs(LOGS, exist_ok=True)
    so_path = os.path.join(LOGS, run_id + ".stdout")
    se_path = os.path.join(LOGS, run_id + ".stderr")
    t0 = time.time()
    timed_out = False
    with open(so_path, "w") as so, open(se_path, "w") as se:
        proc = subprocess.Popen(cmd, cwd=wd, stdin=subprocess.DEVNULL, stdout=so, stderr=se, env=env,
                                start_new_session=True)
        try:
            rc = proc.wait(timeout=TIMEOUT_S)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                time.sleep(5)
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            rc = proc.wait()
    wall = round(time.time() - t0, 1)
    stdout = open(so_path).read()
    stderr = open(se_path).read()
    parsed = parse_output(cfg["cli"], stdout, last_path)
    if parsed["final"] is not None and not os.path.exists(last_path):
        with open(last_path, "w") as f:
            f.write(parsed["final"])
    g = grade(task, wd, last_path)
    if timed_out:
        g["pass"] = False
        g["timeout"] = True
    rec = {
        "run_id": run_id, "config": cfg_name, "cli": cfg["cli"], "model": cfg["model"], "effort": cfg["effort"],
        "task": task, "rep": rep, "workdir": wd, "exit_code": rc, "timed_out": timed_out, "wall_s": wall,
        "pass": bool(g.get("pass")), "score": g.get("score"), "grade": g,
        "final_message": (parsed.pop("final") or "")[-2000:], "usage": parsed,
        "stderr_tail": stderr[-1500:] if (rc != 0 or parsed.get("api_error")) else "",
        "cmd": [c if c != prompt else "<prompt.txt>" for c in cmd],
        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    with open(raw_path, "w") as f:
        json.dump(rec, f, indent=1)
    c = parsed.get("cost_usd") or 0.0
    with lock:
        spend["total"] += c
        spend["by_config"][cfg_name] = spend["by_config"].get(cfg_name, 0.0) + c
        if c > RUN_COST_CAP:
            spend["capped"].add(cfg_name)
    print(f"[{time.strftime('%H:%M:%S')}] {run_id}: pass={rec['pass']} score={rec['score']} wall={wall}s "
          f"rc={rc} cost={c:.3f} total=${spend['total']:.2f}", flush=True)
    return rec


def load_existing_spend():
    if not os.path.isdir(RAW):
        return
    for fn in os.listdir(RAW):
        if fn.endswith(".json"):
            r = json.load(open(os.path.join(RAW, fn)))
            c = (r.get("usage") or {}).get("cost_usd") or 0.0
            spend["total"] += c
            spend["by_config"][r["config"]] = spend["by_config"].get(r["config"], 0.0) + c
            if c > RUN_COST_CAP:
                spend["capped"].add(r["config"])


def cmd_run(args):
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)
    load_existing_spend()
    configs = args.configs.split(",") if args.configs else list(CONFIGS)
    tasks = args.tasks.split(",") if args.tasks else TASKS
    extra = set(args.extra_reps_tasks.split(",")) if args.extra_reps_tasks else set()
    jobs = []
    for rep in range(1, args.reps + 2):
        for task in tasks:
            if rep > args.reps and task not in extra:
                continue
            for c in configs:
                jobs.append((c, task, rep))
    # Interleave CLIs so concurrent processes spread across providers.
    jobs.sort(key=lambda j: (j[2], tasks.index(j[1]), configs.index(j[0]) % 4, j[0]))
    print(f"{len(jobs)} jobs, {args.jobs} concurrent; existing spend ${spend['total']:.2f}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(run_one, *j) for j in jobs]
        for f in cf.as_completed(futs):
            try:
                f.result()
            except Exception as e:  # keep going on harness errors
                print("HARNESS ERROR", repr(e), flush=True)
    print(f"done. total spend ${spend['total']:.2f}", flush=True)


def cmd_reparse(_args):
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith(".json"):
            continue
        p = os.path.join(RAW, fn)
        r = json.load(open(p))
        so = open(os.path.join(LOGS, r["run_id"] + ".stdout")).read()
        last = os.path.join(os.path.dirname(r["workdir"]), "last_message.txt")
        parsed = parse_output(r["cli"], so, last)
        final = parsed.pop("final")
        r["usage"] = parsed
        if final:
            r["final_message"] = final[-2000:]
        json.dump(r, open(p, "w"), indent=1)
    print("reparsed")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("run")
    r.add_argument("--configs")
    r.add_argument("--tasks")
    r.add_argument("--reps", type=int, default=1)
    r.add_argument("--extra-reps-tasks", default="")
    r.add_argument("--jobs", type=int, default=6)
    sub.add_parser("reparse")
    a = ap.parse_args()
    if a.cmd == "run":
        cmd_run(a)
    elif a.cmd == "reparse":
        cmd_reparse(a)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
