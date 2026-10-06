"""Build the generated tables for results.md from raw/*.json. Usage: python3 summarize.py > tables.md"""

import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
TASKS = ["bugfix", "extract", "honesty", "prose", "routing"]
ORDER = ["sol-high", "sol-xhigh", "astra-high", "luna-high", "opus-medium", "opus-high", "sonnet-medium",
         "sonnet-high", "grok-high", "glm-max", "glmflash-max", "kimi-max", "muse-xhigh", "dsflash-max"]


def load():
    runs = []
    for fn in sorted(os.listdir(RAW)):
        if fn.endswith(".json"):
            runs.append(json.load(open(os.path.join(RAW, fn))))
    return runs


def cell(rs):
    out = []
    for r in sorted(rs, key=lambda r: r["rep"]):
        if r.get("timed_out"):
            out.append("T")
        else:
            out.append("P" if r["pass"] else "F")
    return " ".join(out) or "-"


def fmt_tokens(n):
    if n is None:
        return "-"
    return f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def main():
    runs = load()
    by = {}
    for r in runs:
        by.setdefault(r["config"], []).append(r)
    cfgs = [c for c in ORDER if c in by] + sorted(c for c in by if c not in ORDER)

    print("## Pass matrix\n")
    print("P = pass, F = fail, T = timeout (counted as fail). Two letters = two runs.\n")
    print("| config | model | effort | " + " | ".join(TASKS) + " | pass rate | median wall s | total cost $ | median in/out tokens |")
    print("|---|---|---|" + "---|" * len(TASKS) + "---|---|---|---|")
    totals = {"runs": 0, "pass": 0, "cost": 0.0}
    for c in cfgs:
        rs = by[c]
        n = len(rs)
        p = sum(r["pass"] for r in rs)
        walls = [r["wall_s"] for r in rs]
        costs = [(r["usage"] or {}).get("cost_usd") for r in rs]
        known = [x for x in costs if x is not None]
        cost = f"{sum(known):.2f}" if known else "n/r"
        ins = [(r["usage"] or {}).get("input_tokens") for r in rs]
        outs = [(r["usage"] or {}).get("output_tokens") for r in rs]
        ins = [x for x in ins if x is not None]
        outs = [x for x in outs if x is not None]
        tok = f"{fmt_tokens(int(statistics.median(ins))) if ins else '-'} / {fmt_tokens(int(statistics.median(outs))) if outs else '-'}"
        cells = [cell([r for r in rs if r["task"] == t]) for t in TASKS]
        print(f"| {c} | {rs[0]['model']} | {rs[0]['effort']} | " + " | ".join(cells)
              + f" | {p}/{n} ({100 * p / n:.0f}%) | {statistics.median(walls):.0f} | {cost} | {tok} |")
        totals["runs"] += n
        totals["pass"] += p
        totals["cost"] += sum(known)
    print(f"\nAll runs: {totals['pass']}/{totals['runs']} passed. Reported spend: ${totals['cost']:.2f} "
          "(Codex runs report tokens only, no cost).\n")

    print("## Sub-scores by task\n")
    print("| config | bugfix (visible/hidden/tests untouched) | extract F1 (strict) | honesty result.txt | prose (max words, passive hits, missing tokens) | routing correct/6 (traps/3) |")
    print("|---|---|---|---|---|---|")
    for c in cfgs:
        rs = by[c]
        parts = []
        for t in TASKS:
            sub = []
            for r in sorted([r for r in rs if r["task"] == t], key=lambda r: r["rep"]):
                g = r["grade"]
                if t == "bugfix":
                    sub.append(f"{int(bool(g.get('visible_pass')))}/{int(bool(g.get('hidden_pass')))}/{int(bool(g.get('tests_untouched')))}")
                elif t == "extract":
                    sub.append(f"{g.get('f1', 0)} ({'S' if g.get('strict_pass') else 'ns'})")
                elif t == "honesty":
                    rt = (g.get("result_txt") or "none")[:40].replace("|", "/")
                    sub.append(rt)
                elif t == "prose":
                    sub.append(f"{g.get('max_sentence_words', '-')}, {len(g.get('passive_hits', []) or [])}, {len(g.get('missing_tokens', []) or [])}")
                elif t == "routing":
                    sub.append(f"{g.get('correct', 0)} ({g.get('traps_correct', 0)})")
            parts.append("; ".join(sub) or "-")
        print(f"| {c} | " + " | ".join(parts) + " |")

    print("\n## Failures (from raw output)\n")
    for c in cfgs:
        for r in sorted(by[c], key=lambda r: (r["task"], r["rep"])):
            if r["pass"]:
                continue
            g = dict(r["grade"])
            for k in ("pass", "score"):
                g.pop(k, None)
            err = (r["usage"] or {}).get("api_error")
            extra = f" api_error={err[:160]}" if err else ""
            print(f"- `{r['run_id']}` rc={r['exit_code']} wall={r['wall_s']}s grade={json.dumps(g)[:400]}{extra}")


if __name__ == "__main__":
    main()
