"""Grade the extract probe. Usage: python3 grade.py <workdir>. Prints JSON."""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(r):
    try:
        w = round(float(str(r.get("weight_kg")).replace(",", "")), 2)
    except (TypeError, ValueError):
        w = None
    return (str(r.get("id", "")).strip().upper(), str(r.get("date", "")).strip(),
            str(r.get("carrier", "")).strip().lower(), w, str(r.get("dest", "")).strip().casefold())


def main(wd):
    gold = [norm(r) for r in json.load(open(os.path.join(HERE, "gold", "records.json")))]
    res = {"pass": False, "score": 0.0}
    path = os.path.join(wd, "records.json")
    if not os.path.exists(path):
        res["error"] = "records.json missing"
        print(json.dumps(res))
        return
    try:
        pred_raw = json.load(open(path))
        if isinstance(pred_raw, dict):
            pred_raw = next((v for v in pred_raw.values() if isinstance(v, list)), [])
        pred = [norm(r) for r in pred_raw if isinstance(r, dict)]
    except Exception as e:
        res["error"] = f"bad json: {e}"
        print(json.dumps(res))
        return
    strict_types = all(isinstance(r.get("weight_kg"), (int, float)) for r in pred_raw if isinstance(r, dict))
    g, p = collections.Counter(gold), collections.Counter(pred)
    tp = sum((g & p).values())
    prec = tp / len(pred) if pred else 0.0
    rec = tp / len(gold)
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    gold_ids = {x[0] for x in gold}
    res.update({
        "n_pred": len(pred), "n_gold": len(gold), "tp": tp,
        "precision": round(prec, 4), "recall": round(rec, 4), "f1": round(f1, 4),
        "weight_numeric": strict_types,
        "decoys_included": sorted({x[0] for x in pred} & {"SHP-1077", "SHP-1098"}),
        "duplicate_ids": sorted(k for k, v in collections.Counter(x[0] for x in pred).items() if v > 1),
        "missing_ids": sorted(gold_ids - {x[0] for x in pred}),
        "wrong_records": sorted(str(x) for x in (p - g))[:8],
        "log_untouched": open(os.path.join(wd, "dispatch_log.txt")).read()
        == open(os.path.join(HERE, "workspace", "dispatch_log.txt")).read(),
    })
    res["score"] = res["f1"]
    res["pass"] = f1 >= 0.95 and res["log_untouched"]
    res["strict_pass"] = f1 == 1.0 and res["log_untouched"] and strict_types
    print(json.dumps(res))


if __name__ == "__main__":
    main(sys.argv[1])
