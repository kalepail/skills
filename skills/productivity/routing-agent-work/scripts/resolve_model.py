#!/usr/bin/env python3
"""Resolve a model family to its newest model through a worker CLI's own listing.

The fleet reference gives each family an identifier pattern. This script runs the
CLI's listing, keeps the identifiers that match, and prints the newest one.

Usage:
  resolve_model.py --cli codex|grok|opencode --pattern '<regex>' [--pattern '<regex>' ...]
                   [--access-program <name>] [--dir <work-dir>] [--listing-file <path>]
  resolve_model.py --self-test

Listing sources: `codex debug models` (JSON), `grok models`, and `opencode models`
(run in --dir, because OpenCode catalogs are project-specific). The listing command
runs with stdin closed and a timeout. --listing-file reads saved output instead.

Matching rules:
- A pattern must match the whole identifier. Identifiers that carry an unlisted
  suffix, such as a speed variant or a sibling tier, do not match.
- A pattern has at most one named group, `v`. It captures the version, written as
  digits and dots. A match with no version ranks below every versioned match.
- Versions compare as integer tuples: 6 < 6.1 < 6.2 and 4.7 < 4.20. Trailing zero
  components are ignored. When the tuple winner and the plain-decimal winner differ
  (4.20 against 4.7, 6.10 against 6.9), the vendor's numbering is unclear and the
  result is `ambiguous`.
- --pattern repeats, one per provider row, in provider order. The script finds the
  highest version across every pattern and returns the first pattern that carries
  it. A pattern that carries only an older version is reported as `stale` and is
  never selected. Later patterns at the top version are reported as `alternates`.
- More than one identifier at the top version inside the selected pattern is
  `ambiguous`. The script never sorts snapshot suffixes.
- Codex entries with `visibility: hide` are ignored. --access-program (Codex only)
  keeps an entry only when `available_access_programs.cyber` lists that program.

Output: one JSON line on stdout with `status`, `cli`, `patterns`, `resolved`,
`version`, `pattern_index`, `alternates`, `stale`, and `candidates`.

Exit codes: 0 resolved; 1 no match; 3 ambiguous; 4 the listing failed, could not be
parsed, or the script hit an internal error; 64 usage error.
"""

import argparse
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from decimal import Decimal

LISTING_CMDS = {
    "codex": ["codex", "debug", "models"],
    "grok": ["grok", "models"],
    "opencode": ["opencode", "models"],
}
DEFAULT_TIMEOUT = 60
VERSION_RE = re.compile(r"[0-9]+(\.[0-9]+)*")
GROK_LINE = re.compile(r"^\s*[*-]\s+(\S+)")
ACCESS_KEY = "cyber"


class UsageError(Exception):
    """The caller passed bad arguments."""


class ListingError(Exception):
    """The listing could not be read or parsed."""


class QuietParser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def run_listing(cmd, work_dir, timeout):
    try:
        done = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=work_dir,
        )
    except subprocess.TimeoutExpired:
        raise ListingError("listing timed out after %ss: %s" % (timeout, " ".join(cmd)))
    except OSError as error:
        raise ListingError("cannot run %s: %s" % (cmd[0], error))
    if done.returncode != 0:
        raise ListingError("%s exited %d: %s" % (" ".join(cmd), done.returncode, done.stderr[-300:].strip()))
    return done.stdout


def codex_identifiers(text, access_program):
    try:
        data = json.loads(text)
        entries = data["models"]
        if not isinstance(entries, list):
            raise TypeError("models is not a list")
    except (ValueError, KeyError, TypeError) as error:
        raise ListingError("codex listing is not the expected JSON: %s" % error)
    found = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("slug"), str):
            raise ListingError("codex listing has an entry with no slug")
        if entry.get("visibility") == "hide":
            continue
        if access_program:
            programs = (entry.get("available_access_programs") or {}).get(ACCESS_KEY) or []
            if access_program not in programs:
                continue
        found.append(entry["slug"])
    return found


def grok_identifiers(text):
    return [m.group(1) for m in map(GROK_LINE.match, text.splitlines()) if m]


def opencode_identifiers(text):
    return [line.strip() for line in text.splitlines() if line.strip() and not re.search(r"\s", line.strip())]


def load_listing(cli, access_program, work_dir, listing_file, timeout):
    if listing_file:
        try:
            with open(listing_file, encoding="utf-8") as handle:
                text = handle.read()
        except OSError as error:
            raise ListingError("cannot read listing file: %s" % error)
    else:
        text = run_listing(LISTING_CMDS[cli], work_dir, timeout)
    if cli == "codex":
        return codex_identifiers(text, access_program)
    found = grok_identifiers(text) if cli == "grok" else opencode_identifiers(text)
    if not found:
        raise ListingError("no identifiers found in the %s listing" % cli)
    return found


def parse_version(text):
    """Return (comparison tuple, decimal or None). Empty text is unversioned."""
    if not text:
        return (), None
    if not VERSION_RE.fullmatch(text):
        raise ListingError("version is not digits and dots: %r" % text)
    parts = [int(p) for p in text.split(".")]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts), (Decimal(text) if text.count(".") <= 1 else None)


def compile_patterns(patterns):
    compiled = []
    for pattern in patterns:
        try:
            compiled.append(re.compile(pattern))
        except re.error as error:
            raise UsageError("bad pattern %r: %s" % (pattern, error))
    return compiled


def resolve(identifiers, patterns):
    """Return (status, result dict). Status is resolved, no-match, or ambiguous."""
    compiled = compile_patterns(patterns)
    seen = set()
    candidates = []
    for index, regex in enumerate(compiled):
        for ident in identifiers:
            match = regex.fullmatch(ident)
            if not match or ident in seen:
                continue
            seen.add(ident)
            text = match.groupdict().get("v") or ""
            key, dec = parse_version(text)
            candidates.append({"id": ident, "version": text, "pattern_index": index, "key": key, "dec": dec})
    result = {"patterns": list(patterns), "resolved": None, "version": None, "pattern_index": None,
              "alternates": [], "stale": [], "candidates": []}
    if not candidates:
        return "no-match", result
    top = max(c["key"] for c in candidates)
    tops = [c for c in candidates if c["key"] == top]
    versioned = [c for c in candidates if c["key"]]
    status = "resolved"
    if versioned and all(c["dec"] is not None for c in versioned):
        best = max(c["dec"] for c in versioned)
        decimal_tops = {c["id"] for c in versioned if c["dec"] == best}
        if decimal_tops != {c["id"] for c in tops}:
            status = "ambiguous"
    selected = min(c["pattern_index"] for c in tops)
    in_pattern = [c for c in tops if c["pattern_index"] == selected]
    if len(in_pattern) > 1:
        status = "ambiguous"
    public = lambda c: {"id": c["id"], "version": c["version"], "pattern_index": c["pattern_index"]}
    if status == "ambiguous":
        result["candidates"] = [public(c) for c in (tops if len(in_pattern) > 1 else candidates)]
        return status, result
    winner = in_pattern[0]
    result.update(resolved=winner["id"], version=winner["version"], pattern_index=selected,
                  alternates=[c["id"] for c in tops if c["pattern_index"] != selected],
                  candidates=[public(c) for c in candidates])
    top_patterns = {c["pattern_index"] for c in tops}
    for index in sorted({c["pattern_index"] for c in candidates} - top_patterns):
        newest = max((c for c in candidates if c["pattern_index"] == index), key=lambda c: c["key"])
        result["stale"].append({"pattern_index": index, "newest": newest["id"], "version": newest["version"]})
    return status, result


def build_parser():
    parser = QuietParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cli", choices=sorted(LISTING_CMDS), help="worker CLI whose listing to read")
    parser.add_argument("--pattern", action="append", default=[],
                        help="identifier regex with an optional (?P<v>...) version group; repeat once per provider row, in order")
    parser.add_argument("--access-program", help="Codex only: keep entries whose cyber access programs list this name")
    parser.add_argument("--dir", help="run the listing command in this directory")
    parser.add_argument("--listing-file", help="read saved listing output instead of running the CLI")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds before the listing command is stopped")
    parser.add_argument("--self-test", action="store_true", help="run offline checks")
    return parser


EXIT = {"resolved": 0, "no-match": 1, "ambiguous": 3}


def run(argv):
    args = build_parser().parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.cli or not args.pattern:
        raise UsageError("--cli and at least one --pattern are required")
    if args.access_program and args.cli != "codex":
        raise UsageError("--access-program applies to --cli codex only")
    if args.dir and not os.path.isdir(args.dir):
        raise UsageError("work directory does not exist: " + args.dir)
    if args.timeout < 1:
        raise UsageError("--timeout must be at least 1")
    compile_patterns(args.pattern)
    identifiers = load_listing(args.cli, args.access_program, args.dir, args.listing_file, args.timeout)
    status, result = resolve(identifiers, args.pattern)
    print(json.dumps({"status": status, "cli": args.cli, **result}))
    return EXIT[status]


def main(argv=None):
    try:
        return run(sys.argv[1:] if argv is None else argv)
    except UsageError as error:
        print(json.dumps({"status": "usage-error", "error": str(error)}))
        print("error: %s" % error, file=sys.stderr)
        return 64
    except ListingError as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        print("error: %s" % error, file=sys.stderr)
        return 4
    except Exception as error:  # a script bug must never read as "no match"
        print(json.dumps({"status": "error", "error": "internal error: %r" % error}))
        print("internal error: %r" % error, file=sys.stderr)
        return 4


def codex_fixture(entries):
    return json.dumps({"models": [
        {"slug": slug, "visibility": vis, "available_access_programs": {"cyber": programs}}
        for slug, vis, programs in entries]})


def self_test():
    std, dbl = ["standard"], ["standard", "daybreak_blue"]
    codex = codex_fixture([
        ("gpt-6.2-sol", "list", std), ("gpt-6.1-sol", "list", std), ("gpt-6-sol", "list", dbl),
        ("gpt-5.6-sol", "list", dbl), ("gpt-6.2-astra", "list", std), ("gpt-6-astra", "list", std),
        ("gpt-reserve", "hide", dbl), ("gpt-daybreak-blue-latest", "list", ["daybreak_blue"]),
    ])
    grok = ("You are logged in with grok.com.\n\nDefault model: grok-4.7\n\nAvailable models:\n"
            "  * grok-4.7 (default)\n  - grok-4.7-build-fast\n  - grok-4.6\n  - grok-4.5\n")
    oc = "\n".join([
        "cloudflare-workers-ai/@cf/zai-org/glm-4.7-flash",
        "cloudflare-workers-ai/@cf/zai-org/glm-5.3",
        "cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v4.1-flash-1017",
        "openrouter/z-ai/glm-4.7-flash", "openrouter/z-ai/glm-5.3", "openrouter/z-ai/glm-5.3-flash",
        "openrouter/z-ai/glm-5.3-flashx", "openrouter/z-ai/glm-5.3-prime", "openrouter/z-ai/glm-5v-turbo",
        "openrouter/deepseek/deepseek-v4-flash-0731", "openrouter/deepseek/deepseek-v4.1-flash",
        "openrouter/deepseek/deepseek-v4.1-flash-1017",
        "openrouter/moonshotai/kimi-k3", "openrouter/moonshotai/kimi-k3.1-pro",
        "openrouter/moonshotai/kimi-k2.7-code", "openrouter/moonshotai/kimi-k2-thinking",
        "moonshotai/kimi-k3.1-pro", "moonshotai/kimi-k3.1-pro-highspeed",
        "openrouter/meta/muse-ember", "openrouter/meta/muse-spark-1.3",
        "openrouter/x-ai/grok-4.7", "openrouter/x-ai/grok-4.20", "openrouter/x-ai/grok-4.3",
        "openrouter/xiaomi/mimo-v2.6-pro", "openrouter/xiaomi/mimo-v2.6-pro-ultraspeed",
    ]) + "\n"

    def listing(cli, text, patterns, extra=()):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "listing.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            argv = ["--cli", cli, "--listing-file", path]
            for pattern in patterns:
                argv += ["--pattern", pattern]
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(argv + list(extra))
            return code, json.loads(out.getvalue())

    def check(name, got, want_code, want_id=None, **extra):
        code, out = got
        assert code == want_code, (name, "exit", code, out)
        if want_id is not None or want_code == 0:
            assert out.get("resolved") == want_id, (name, "resolved", out)
        for key, value in extra.items():
            assert out.get(key) == value, (name, key, out)

    sol = r"gpt-(?P<v>[0-9.]+)-sol"
    check("codex sol picks 6.2", listing("codex", codex, [sol]), 0, "gpt-6.2-sol", version="6.2")
    check("codex astra", listing("codex", codex, [r"gpt-(?P<v>[0-9.]+)-astra"]), 0, "gpt-6.2-astra")
    check("daybreak program", listing("codex", codex, [sol], ["--access-program", "daybreak_blue"]), 0, "gpt-6-sol")
    check("hidden entry ignored", listing("codex", codex, [r"gpt-reserve"]), 1)
    check("latest alias not matched", listing("codex", codex, [r"gpt-(?P<v>[0-9.]+)-daybreak-blue"]), 1)
    check("codex bad json", listing("codex", "not json", [sol]), 4)
    check("codex wrong shape", listing("codex", '{"models": 3}', [sol]), 4)
    check("access program needs codex", listing("grok", grok, [r"grok-(?P<v>[0-9.]+)"], ["--access-program", "x"]), 64)

    check("grok skips speed variant", listing("grok", grok, [r"grok-(?P<v>[0-9.]+)"]), 0, "grok-4.7", version="4.7")
    check("grok unparseable listing", listing("grok", "Available models:\n", [r"grok-(?P<v>[0-9.]+)"]), 4)

    kimi = r"openrouter/moonshotai/kimi-k(?P<v>[0-9.]+)(-pro)?"
    check("kimi drops code, thinking, and highspeed", listing("opencode", oc, [kimi]), 0,
          "openrouter/moonshotai/kimi-k3.1-pro", version="3.1")
    check("kimi highspeed own call", listing("opencode", oc, [r"moonshotai/kimi-k(?P<v>[0-9.]+)-pro-highspeed"]), 0,
          "moonshotai/kimi-k3.1-pro-highspeed")
    check("kimi provider order", listing("opencode", oc, [kimi, r"moonshotai/kimi-k(?P<v>[0-9.]+)-pro"]), 0,
          "openrouter/moonshotai/kimi-k3.1-pro", alternates=["moonshotai/kimi-k3.1-pro"])

    glm = [r"cloudflare-workers-ai/@cf/zai-org/glm-(?P<v>[0-9.]+)", r"openrouter/z-ai/glm-(?P<v>[0-9.]+)"]
    check("glm drops flash, flashx, prime, and vision tiers", listing("opencode", oc, glm), 0,
          "cloudflare-workers-ai/@cf/zai-org/glm-5.3", alternates=["openrouter/z-ai/glm-5.3"], stale=[])
    flash = [r"cloudflare-workers-ai/@cf/zai-org/glm-(?P<v>[0-9.]+)-flash", r"openrouter/z-ai/glm-(?P<v>[0-9.]+)-flash"]
    got = listing("opencode", oc, flash)
    check("glm flash skips the stale first provider", got, 0, "openrouter/z-ai/glm-5.3-flash", version="5.3",
          pattern_index=1)
    assert got[1]["stale"] == [{"pattern_index": 0, "newest": "cloudflare-workers-ai/@cf/zai-org/glm-4.7-flash",
                                "version": "4.7"}], got

    snap = [r"cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v(?P<v>[0-9.]+)-flash-[0-9]{4}",
            r"openrouter/deepseek/deepseek-v(?P<v>[0-9.]+)-flash-[0-9]{4}"]
    check("deepseek requires the snapshot", listing("opencode", oc, snap), 0,
          "cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v4.1-flash-1017")
    check("deepseek second snapshot fails closed",
          listing("opencode", oc + "openrouter/deepseek/deepseek-v4.1-flash-1101\n", snap[1:]), 3, None)
    check("deepseek no-snapshot pattern ties", listing("opencode", oc, [r"openrouter/deepseek/deepseek-v(?P<v>[0-9.]+)-flash(-[0-9]{4})?"]), 3)

    grok_or = r"openrouter/x-ai/grok-(?P<v>[0-9.]+)"
    check("4.20 against 4.7 is ambiguous", listing("opencode", oc, [grok_or]), 3)
    check("6.10 against 6.9 is ambiguous", listing("opencode", "p/m-6.9\np/m-6.10\n", [r"p/m-(?P<v>[0-9.]+)"]), 3)
    check("6 < 6.1 < 6.2", listing("opencode", "p/m-6\np/m-6.2\np/m-6.1\n", [r"p/m-(?P<v>[0-9.]+)"]), 0, "p/m-6.2")
    check("trailing zero is the same version", listing("opencode", "p/m-6\np/m-6.0\n", [r"p/m-(?P<v>[0-9.]+)"]), 3)

    check("unversioned family", listing("opencode", oc, [r"openrouter/meta/muse-ember"]), 0, "openrouter/meta/muse-ember", version="")
    check("unversioned ranks below versioned",
          listing("opencode", "p/muse\np/muse-2\n", [r"p/muse(-(?P<v>[0-9.]+))?"]), 0, "p/muse-2")
    check("sibling tier excluded by full match", listing("opencode", oc, [r"openrouter/xiaomi/mimo-v(?P<v>[0-9.]+)-pro"]), 0,
          "openrouter/xiaomi/mimo-v2.6-pro")
    check("no match", listing("opencode", oc, [r"openrouter/google/gemini-(?P<v>[0-9.]+)-carbon"]), 1)
    check("no match keeps patterns empty of a pick", listing("opencode", oc, [r"openrouter/z-ai/glm-(?P<v>[0-9.]+)-pro"]), 1, resolved=None)
    check("empty opencode listing", listing("opencode", "\n", [r"p/m"]), 4)

    check("bad regex", listing("opencode", oc, ["(unclosed"]), 64)
    check("duplicate version group", listing("opencode", oc, [r"(?P<v>1)(?P<v>2)"]), 64)

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        assert main(["--cli", "bogus", "--pattern", "x"]) == 64, "argparse error"
        assert main(["--pattern", "x"]) == 64, "missing --cli"
        assert main(["--cli", "grok"]) == 64, "missing --pattern"
        assert main(["--cli", "grok", "--pattern", "x", "--dir", "/nonexistent-dir"]) == 64, "missing dir"
        assert main(["--cli", "grok", "--pattern", "x", "--listing-file", "/nonexistent/listing"]) == 4, "missing file"
        real = globals()["load_listing"]
        try:
            globals()["load_listing"] = lambda *a: 1 / 0
            assert main(["--cli", "grok", "--pattern", "x"]) == 4, "internal error"
        finally:
            globals()["load_listing"] = real
    try:
        run_listing([sys.executable, "-c", "import time; time.sleep(5)"], None, 1)
        raise AssertionError("timeout not raised")
    except ListingError:
        pass
    try:
        run_listing(["resolve-model-no-such-cli"], None, 5)
        raise AssertionError("missing CLI not raised")
    except ListingError:
        pass
    try:
        run_listing([sys.executable, "-c", "import sys; sys.exit(3)"], None, 5)
        raise AssertionError("failing listing not raised")
    except ListingError:
        pass
    assert run_listing([sys.executable, "-c", "import sys; print(len(sys.stdin.read()))"], None, 5).strip() == "0"
    print("resolve_model self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
