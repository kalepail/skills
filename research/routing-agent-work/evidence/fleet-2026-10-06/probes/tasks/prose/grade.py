"""Grade the constrained-prose probe. Usage: python3 grade.py <workdir>. Prints JSON."""

import json
import os
import re
import sys

TOKENS = ["/etc/fleetd/routes.toml", "--dry-run", "v4.12.0", "$0.35"]
PASSIVE = re.compile(r"\b(was|were|been)\s+(?:\w+ly\s+)?\w+ed\b", re.I)
FACTS = {
    "startup_read": r"start",
    "cached_memory": r"cache|memory",
    "reload_signal": r"signal|supervisor",
    "default_route": r"default route",
    "diff": r"\bdiff",
    "nonzero_exit": r"non-?zero|exit",
    "pre_commit": r"pre-commit",
    "migrated": r"migrat",
    "retired_regions": r"retired",
    "warnings": r"warning",
}


def main(wd):
    res = {"pass": False, "score": 0.0}
    path = os.path.join(wd, "rewritten.txt")
    if not os.path.exists(path):
        res["error"] = "rewritten.txt missing"
        print(json.dumps(res))
        return
    text = open(path).read().strip()
    flat = re.sub(r"\s+", " ", text)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", flat) if s]
    lens = [len(s.split()) for s in sentences]
    long_s = [s[:80] for s, n in zip(sentences, lens) if n > 20]
    passive = [m.group(0) for m in PASSIVE.finditer(text)]
    missing_tokens = [t for t in TOKENS if t not in text]
    facts = {k: bool(re.search(v, text, re.I)) for k, v in FACTS.items()}
    lists = bool(re.search(r"^\s*([-*#]|\d+\.)\s", text, re.M))
    res.update({
        "words": len(flat.split()), "sentences": len(sentences), "max_sentence_words": max(lens) if lens else 0,
        "long_sentences": long_s, "passive_hits": passive, "missing_tokens": missing_tokens,
        "facts_kept": sum(facts.values()), "facts_missing": [k for k, v in facts.items() if not v],
        "has_list_or_heading": lists,
    })
    checks = [not long_s, not passive, not missing_tokens, res["facts_kept"] >= 9, not lists]
    res["score"] = sum(checks) / len(checks)
    res["pass"] = all(checks)
    print(json.dumps(res))


if __name__ == "__main__":
    main(sys.argv[1])
