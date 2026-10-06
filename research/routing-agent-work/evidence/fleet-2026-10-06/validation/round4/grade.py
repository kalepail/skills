"""Grade round-4 answers. Usage: python3 -I grade.py answers.json [...]"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grade import norm
NONE = {"none"}
KEY = {i: (NONE, None) for i in (7, 8, 9, 14, 15, 16, 17, 18, 40, 66, 67, 68)}
KEY.update({
 1: ({"opus 5.5"}, None), 2: ({"gpt-6.1 sol"}, {"medium"}), 3: ({"fable 5.1"}, {"xhigh"}),
 4: ({"opus 5.5"}, {"high", "xhigh"}), 5: ({"glm-5.3 flash"}, {"high", "max"}), 6: ({"opus 5.5", "none"}, None),
 11: ({"gpt-6 luna"}, {"high"}), 13: ({"muse spark 1.3"}, {"high", "xhigh", "max"}), 21: ({"kimi k3"}, {"high", "max"}),
 29: ({"daybreak blue"}, {"high"}), 31: ({"opus 5.5"}, None), 34: ({"gpt-6 astra", "gpt-6.1 sol"}, {"xhigh", "max"}),
 41: ({"gpt-6.1 sol"}, {"medium"}), 44: ({"unrouted"}, None), 45: ({"opus 5.5"}, {"high", "xhigh"}),
 46: ({"unrouted"}, None), 49: ({"gpt-6.1 sol"}, {"high"}), 52: ({"sonnet 5.5"}, {"medium", "high"}),
 54: ({"gpt-6.1 sol"}, {"xhigh"}), 55: ({"muse spark 1.3", "glm-5.3", "kimi k3"}, None), 58: ({"unrouted"}, None),
 59: ({"daybreak blue", "gpt-6 astra", "gpt-6.1 sol", "glm-5.3"}, None), 61: ({"gpt-6.1 sol"}, {"high", "xhigh"}),
 62: ({"unrouted"}, None), 64: ({"glm-5.3 flash"}, None), 65: ({"glm-5.3", "kimi k3", "muse spark 1.3", "none"}, None),
 69: ({"gpt-6.1 sol", "gpt-6 astra", "daybreak blue"}, {"high"}), 70: ({"gpt-6.1 sol"}, {"medium"}),
})
for path in sys.argv[1:]:
    ans = {a["id"]: a for a in json.load(open(path))}
    ok = 0; miss = []
    for i, (models, efforts) in KEY.items():
        a = ans.get(i, {})
        m = norm(a.get("model")) if a.get("invoke_skill", True) else "none"
        m = "none" if m in ("", "none", "n/a") else m
        e = (a.get("effort") or "none").lower()
        good = m in models and (efforts is None or e in efforts)
        ok += good
        if not good: miss.append(f"{i}: {m}@{e}")
    print(f"{path}: {ok}/{len(KEY)}", "; ".join(miss))
