"""Grade the routing-judgment probe. Usage: python3 grade.py <workdir>. Prints JSON."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRAPS = {"q1": "effort_floor", "q2": "same_family_reviewer", "q3": "pinned_cli_unrouted"}


def norm_effort(e):
    return None if e in (None, "null", "", "None") else str(e).strip().lower()


def main(wd):
    gold = {g["id"]: g for g in json.load(open(os.path.join(HERE, "gold", "answers.json")))}
    res = {"pass": False, "score": 0.0}
    try:
        ans = json.load(open(os.path.join(wd, "answers.json")))
        if isinstance(ans, dict):
            ans = next((v for v in ans.values() if isinstance(v, list)), [])
        ans = {str(a.get("id")): a for a in ans if isinstance(a, dict)}
    except Exception as e:
        res["error"] = f"answers.json missing or invalid: {e}"
        print(json.dumps(res))
        return
    per = {}
    for qid, g in gold.items():
        a = ans.get(qid, {})
        ok = str(a.get("model", "")).strip() == g["model"] and norm_effort(a.get("effort")) == g["effort"]
        per[qid] = ok
        if not ok:
            res.setdefault("wrong", {})[qid] = {"got": [a.get("model"), a.get("effort")], "want": [g["model"], g["effort"]],
                                                "trap": TRAPS.get(qid)}
    res["correct"] = sum(per.values())
    res["traps_correct"] = sum(per[q] for q in TRAPS)
    res["score"] = res["correct"] / len(gold)
    res["pass"] = res["correct"] == len(gold)
    print(json.dumps(res))


if __name__ == "__main__":
    main(sys.argv[1])
