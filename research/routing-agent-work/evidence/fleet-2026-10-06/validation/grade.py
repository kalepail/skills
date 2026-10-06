"""Grade routing answers against the updated policy key. Usage: python3 -I grade.py answers.json [...]"""
import json, re, sys

# id -> (allowed models, allowed efforts or None for any)
KEY = {
 2: ({"gpt-6.1 sol"}, {"medium", "high"}),
 3: ({"fable 5.1"}, {"xhigh"}),
 4: ({"opus 5.5"}, {"high", "xhigh"}),
 5: ({"glm-5.3 flash"}, {"high", "max"}),
 11: ({"gpt-6 luna"}, {"high"}),
 12: ({"grok 4.7"}, {"high", "xhigh"}),
 20: ({"unrouted"}, None),
 21: ({"kimi k3"}, {"high", "max"}),
 22: ({"muse spark 1.3"}, {"high", "xhigh", "max"}),
 24: ({"gpt-6.1 sol"}, {"high"}),
 25: ({"gpt-6.1 sol"}, {"medium"}),
 26: ({"gpt-6.1 sol"}, {"low"}),
 27: ({"gpt-6 astra"}, {"high"}),
 28: ({"gpt-6.1 sol"}, {"medium"}),
 29: ({"daybreak blue"}, {"high"}),
 31: ({"opus 5.5"}, None),
 41: ({"gpt-6.1 sol"}, {"medium"}),
 44: ({"unrouted"}, None),
 46: ({"unrouted"}, None),
 47: ({"gpt-6 luna"}, {"high"}),
 49: ({"gpt-6.1 sol"}, {"high"}),
 50: ({"gpt-6.1 sol"}, {"low", "medium"}),
 52: ({"sonnet 5.5"}, {"medium", "high"}),
 53: ({"opus 5.5"}, {"xhigh"}),
 54: ({"gpt-6.1 sol"}, {"xhigh"}),
 55: ({"glm-5.3", "muse spark 1.3", "kimi k3"}, None),
 56: ({"sonnet 5.5"}, {"xhigh"}),
 57: ({"daybreak blue"}, {"high"}),
 58: ({"unrouted"}, None),
 59: ({"daybreak blue", "gpt-6 astra", "gpt-6.1 sol", "glm-5.3"}, None),
 60: ({"gpt-6.1 sol"}, {"medium"}),
 61: ({"gpt-6.1 sol"}, {"high", "xhigh"}),
 62: ({"unrouted"}, None),
 63: ({"sonnet 5.5"}, {"high"}),
}

def norm(m):
    m = (m or "").lower().strip()
    m = m.replace("claude ", "").replace("-", " ").replace("_", " ")
    m = re.sub(r"\s+", " ", m)
    table = [
        ("gpt 6.1 sol", "gpt-6.1 sol"), ("gpt 6 astra", "gpt-6 astra"), ("gpt 6 luna", "gpt-6 luna"),
        ("daybreak", "daybreak blue"), ("glm 5.3 flash", "glm-5.3 flash"), ("glm 5.3", "glm-5.3"),
        ("kimi k3", "kimi k3"), ("muse spark 1.3", "muse spark 1.3"), ("grok 4.7", "grok 4.7"),
        ("sonnet 5.5", "sonnet 5.5"), ("sonnet 5 5", "sonnet 5.5"), ("opus 5.5", "opus 5.5"), ("opus 5 5", "opus 5.5"),
        ("fable 5.1", "fable 5.1"), ("fable 5 1", "fable 5.1"), ("unrouted", "unrouted"), ("gpt 6 sol", "gpt-6 sol"),
        ("terra", "gpt-5.6 terra"),
    ]
    for k, v in table:
        if k in m:
            return v
    return m

def grade(path):
    ans = {a["id"]: a for a in json.load(open(path))}
    rows, ok = [], 0
    for i, (models, efforts) in KEY.items():
        a = ans.get(i, {})
        m = norm(a.get("model"))
        e = (a.get("effort") or "none").lower().strip()
        good = m in models and (efforts is None or e in efforts)
        ok += good
        rows.append((i, good, m, e))
    return ok, rows

if __name__ == "__main__":
    for p in sys.argv[1:]:
        ok, rows = grade(p)
        print(f"{p}: {ok}/{len(KEY)}")
        for i, good, m, e in rows:
            if not good:
                print(f"  miss {i}: got {m} @ {e}; want {sorted(KEY[i][0])} @ {sorted(KEY[i][1]) if KEY[i][1] else 'any'}")
