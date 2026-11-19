#!/usr/bin/env python3
"""Resolve a model family to its newest model through a worker CLI's own listing.

The fleet reference gives each family an identifier pattern. This script runs the
CLI's listing, keeps the identifiers that match, and prints the newest one.

Usage:
  resolve_model.py --cli agy|codex|grok|opencode --pattern '<regex>' [--pattern '<regex>' ...]
                   [--access-program <name>] [--dir <work-dir>] [--listing-file <path>]
  resolve_model.py --self-test

Listing sources: `agy models`, `codex debug models` (JSON), `grok models`, and `opencode models`
(run in --dir, because OpenCode catalogs are project-specific). The listing command
runs with stdin closed and a timeout. --listing-file reads saved output instead.

Matching rules:
- A pattern must match the whole identifier. Identifiers that carry an unlisted
  suffix, such as a speed variant or a sibling tier, do not match.
- A pattern may use two named groups and no others (any other name is a usage
  error). `v` captures the version, written as digits and dots. `s` captures a
  snapshot identity, which is compared for equality only and never sorted. A match
  with no `v` ranks below every versioned match.
- Versions compare as integer tuples: 6 < 6.1 < 6.2 and 4.7 < 4.20. Trailing zero
  components are ignored. The result is `ambiguous` when that order and the plain
  decimal order of the major.minor prefix disagree about the newest version
  (4.20 against 4.7, 6.10 against 6.9, or 4.20 beside 4.7 and 4.6.1). A patch
  release of one prefix (4.7.1 beside 4.7) is not a disagreement.
- --pattern repeats, one per provider row, in provider order. The script finds the
  highest version across every pattern and returns the first pattern that carries
  it. A pattern that carries only an older version is reported as `stale` and is
  never selected. Later patterns at the top version are reported as `alternates`.
- Each of these is `ambiguous`: more than one distinct identifier at the top
  version inside any one row, selected or not; more than one distinct `s` value
  (or an `s` value beside a match with none) among the top-version matches of all
  rows. Mirrors of one snapshot across rows resolve in provider order.
- Codex entries with `visibility: hide` are ignored. --access-program (Codex only)
  keeps an entry only when `available_access_programs.cyber` lists that program.
  Missing or null metadata means no programs. Any other shape than a mapping with a
  list of strings under `cyber` is a listing error.
- Grok rows must sit under an `Available models:` line. OpenCode rows must be
  provider-qualified identifiers. A malformed row is a listing error, not a no
  match. --dir sets both the working directory and `PWD` of the listing command.
- Antigravity rows carry the identifier and display name separated by a tab.
  Gemini effort suffixes collapse to the base identifier before version selection.
  Check the selected model's effort with Antigravity's /effort command.

Output, one JSON line on stdout. Exit 0, 1, and 3 print the full shape: `status`
(resolved, no-match, or ambiguous), `cli`, `patterns`, `resolved`, `version`,
`pattern_index`, `alternates`, `stale`, and `candidates`. Ambiguous results list
every contender in `candidates`. Exit 4 and 64 print only `{status, error}`, with
status `error` or `usage-error`.

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
    "agy": ["agy", "models"],
    "codex": ["codex", "debug", "models"],
    "grok": ["grok", "models"],
    "opencode": ["opencode", "models"],
}
DEFAULT_TIMEOUT = 60
VERSION_RE = re.compile(r"[0-9]+(\.[0-9]+)*")
GROK_SECTION = re.compile(r"^\s*Available models:\s*$")
GROK_ROW = re.compile(r"^\s+[*-]\s+([A-Za-z0-9][A-Za-z0-9._-]*)(\s+\(default\))?\s*$")
QUALIFIED_ID = re.compile(r"[^\s/]+(/[^\s/]+)+")
AGY_ID = re.compile(r"[a-z0-9][a-z0-9._-]*")
AGY_EFFORT_ID = re.compile(r"(gemini-[0-9.]+-[a-z0-9-]+)-(low|medium|high|xhigh|max)")
ALLOWED_GROUPS = {"v", "s"}
ACCESS_KEY = "cyber"


class UsageError(Exception):
    """The caller passed bad arguments."""


class ListingError(Exception):
    """The listing could not be read or parsed."""


class QuietParser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def run_listing(cmd, work_dir, timeout):
    cwd = os.path.abspath(work_dir) if work_dir else None
    env = dict(os.environ, PWD=cwd) if cwd else None
    try:
        done = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise ListingError("listing timed out after %ss: %s" % (timeout, " ".join(cmd)))
    except OSError as error:
        raise ListingError("cannot run %s: %s" % (cmd[0], error))
    if done.returncode != 0:
        raise ListingError("%s exited %d: %s" % (" ".join(cmd), done.returncode, done.stderr[-300:].strip()))
    return done.stdout


def entry_programs(entry):
    programs = entry.get("available_access_programs")
    if programs is None:
        return []
    if not isinstance(programs, dict):
        raise ListingError("%s: available_access_programs is not a mapping" % entry["slug"])
    cyber = programs.get(ACCESS_KEY)
    if cyber is None:
        return []
    if not isinstance(cyber, list) or not all(isinstance(item, str) for item in cyber):
        raise ListingError("%s: available_access_programs.%s is not a list of strings" % (entry["slug"], ACCESS_KEY))
    return cyber


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
        if access_program and access_program not in entry_programs(entry):
            continue
        found.append(entry["slug"])
    return found


def grok_identifiers(text):
    lines = text.splitlines()
    start = next((n + 1 for n, line in enumerate(lines) if GROK_SECTION.match(line)), None)
    if start is None:
        raise ListingError("grok listing has no 'Available models:' section")
    found = []
    for line in lines[start:]:
        if not line.strip():
            continue
        match = GROK_ROW.match(line)
        if not match:
            raise ListingError("grok listing has a malformed model row: %r" % line.strip()[:80])
        found.append(match.group(1))
    return found


def opencode_identifiers(text):
    found = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if not QUALIFIED_ID.fullmatch(line):
            raise ListingError("opencode listing has a malformed row: %r" % line[:80])
        found.append(line)
    return found


def agy_identifiers(text):
    found = []
    for line in text.splitlines():
        if not line.strip():
            continue
        identifier, _, label = line.partition("\t")
        if not AGY_ID.fullmatch(identifier) or not label.strip():
            raise ListingError("agy listing has a malformed model row")
        effort_variant = AGY_EFFORT_ID.fullmatch(identifier)
        found.append(effort_variant.group(1) if effort_variant else identifier)
    return list(dict.fromkeys(found))


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
    parse = {"agy": agy_identifiers, "grok": grok_identifiers, "opencode": opencode_identifiers}[cli]
    found = parse(text)
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
            regex = re.compile(pattern)
        except re.error as error:
            raise UsageError("bad pattern %r: %s" % (pattern, error))
        extra = sorted(set(regex.groupindex) - ALLOWED_GROUPS)
        if extra:
            raise UsageError("pattern %r has unsupported named groups %s; only v and s are allowed" % (pattern, extra))
        compiled.append(regex)
    return compiled


def prefix_decimal(text):
    parts = text.split(".")
    return Decimal(parts[0] + ("." + parts[1] if len(parts) > 1 else ""))


def prefix_tuple(key):
    return (key[0], key[1] if len(key) > 1 else 0)


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
            groups = match.groupdict()
            text = groups.get("v") or ""
            key, _ = parse_version(text)
            candidates.append({"id": ident, "version": text, "pattern_index": index, "key": key,
                               "snap": groups.get("s"), "dec": prefix_decimal(text) if text else None})
    result = {"patterns": list(patterns), "resolved": None, "version": None, "pattern_index": None,
              "alternates": [], "stale": [], "candidates": []}
    if not candidates:
        return "no-match", result
    top = max(c["key"] for c in candidates)
    tops = [c for c in candidates if c["key"] == top]
    contenders = []  # every identifier that makes the result unclear

    def contend(items):
        for item in items:
            if item not in contenders:
                contenders.append(item)

    if len({c["snap"] for c in tops}) > 1:
        contend(tops)
    for index in sorted({c["pattern_index"] for c in tops}):
        row = [c for c in tops if c["pattern_index"] == index]
        if len(row) > 1:
            contend(row)
    versioned = [c for c in candidates if c["key"]]
    if versioned and top:
        best = max(c["dec"] for c in versioned)
        if any(c["dec"] > t["dec"] or (c["dec"] == t["dec"] and prefix_tuple(c["key"]) != prefix_tuple(t["key"]))
               for t in tops for c in versioned):
            contend(tops)
            contend([c for c in versioned if c["dec"] == best])
    public = lambda c: {"id": c["id"], "version": c["version"], "pattern_index": c["pattern_index"]}
    if contenders:
        result["candidates"] = [public(c) for c in sorted(contenders, key=lambda c: (c["pattern_index"], c["id"]))]
        return "ambiguous", result
    selected = min(c["pattern_index"] for c in tops)
    winner = next(c for c in tops if c["pattern_index"] == selected)
    result.update(resolved=winner["id"], version=winner["version"], pattern_index=selected,
                  alternates=[c["id"] for c in tops if c["pattern_index"] != selected],
                  candidates=[public(c) for c in candidates])
    top_patterns = {c["pattern_index"] for c in tops}
    for index in sorted({c["pattern_index"] for c in candidates} - top_patterns):
        newest = max((c for c in candidates if c["pattern_index"] == index), key=lambda c: c["key"])
        result["stale"].append({"pattern_index": index, "newest": newest["id"], "version": newest["version"]})
    return "resolved", result


def build_parser():
    parser = QuietParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cli", choices=sorted(LISTING_CMDS), help="worker CLI whose listing to read")
    parser.add_argument("--pattern", action="append", default=[],
                        help="identifier regex with optional (?P<v>...) version and (?P<s>...) snapshot groups; repeat once per provider row, in order")
    parser.add_argument("--access-program", help="Codex only: keep entries whose cyber access programs list this name")
    parser.add_argument("--dir", help="run the listing command in this directory, with PWD set to it")
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

    def check(name, got, want_code, want_id=None, candidate_ids=None, **extra):
        code, out = got
        assert code == want_code, (name, "exit", code, out)
        if want_id is not None or want_code == 0:
            assert out.get("resolved") == want_id, (name, "resolved", out)
        if candidate_ids is not None:
            assert {c["id"] for c in out["candidates"]} == set(candidate_ids), (name, "candidates", out["candidates"])
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

    neon = r"gemini-(?P<v>[0-9.]+)-neon"
    agy = ("gemini-4-neon-high\tGemini 4 Neon (High)\n"
           "gemini-4-neon-xhigh\tGemini 4 Neon (XHigh)\n"
           "gemini-5-neon-high\tGemini 5 Neon (High)\n"
           "gemini-5-neon-medium\tGemini 5 Neon (Medium)\n"
           "gemini-5-neon-fast\tGemini 5 Neon Fast\n"
           "gemini-5-carbon-high\tGemini 5 Carbon (High)\n"
           "gemini-pro-orchestrator-neon\tOrchestrator (Neon)\n")
    check("agy resolves newest family before selecting effort", listing("agy", agy, [neon]), 0,
          "gemini-5-neon", candidate_ids=["gemini-4-neon", "gemini-5-neon"])
    check("agy orchestrator stays outside single-model lane",
          listing("agy", "gemini-pro-orchestrator-neon\tOrchestrator (Neon)\n", [neon]), 1)
    check("agy invalid catalog", listing("agy", "Error: Please sign in\n", [neon]), 4)

    kimi = r"openrouter/moonshotai/kimi-k(?P<v>[0-9.]+)(-pro)?"
    check("kimi drops code, thinking, and highspeed", listing("opencode", oc, [kimi]), 0,
          "openrouter/moonshotai/kimi-k3.1-pro", version="3.1",
          candidate_ids=["openrouter/moonshotai/kimi-k3", "openrouter/moonshotai/kimi-k3.1-pro"])
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

    snap = [r"cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v(?P<v>[0-9.]+)-flash-(?P<s>[0-9]{4})",
            r"openrouter/deepseek/deepseek-v(?P<v>[0-9.]+)-flash-(?P<s>[0-9]{4})"]
    cf, orr = "cloudflare-workers-ai/@cf/deepseek-ai/deepseek-v", "openrouter/deepseek/deepseek-v"
    check("deepseek requires the snapshot", listing("opencode", oc, snap), 0,
          cf + "4.1-flash-1017", alternates=[orr + "4.1-flash-1017"], stale=[])
    check("deepseek second snapshot fails closed",
          listing("opencode", oc + orr + "4.1-flash-1101\n", snap[1:]), 3)
    check("deepseek split snapshots across rows", listing("opencode", cf + "5-flash-0301\n" + orr + "5-flash-0415\n", snap), 3,
          candidate_ids=[cf + "5-flash-0301", orr + "5-flash-0415"])
    check("deepseek tied alternate row",
          listing("opencode", cf + "5-flash-0301\n" + orr + "5-flash-0301\n" + orr + "5-flash-0415\n", snap), 3,
          candidate_ids=[cf + "5-flash-0301", orr + "5-flash-0301", orr + "5-flash-0415"])
    check("deepseek same-snapshot mirrors keep provider order",
          listing("opencode", cf + "5-flash-0301\n" + orr + "5-flash-0301\n", snap), 0, cf + "5-flash-0301",
          alternates=[orr + "5-flash-0301"])
    check("deepseek older snapshot row is stale",
          listing("opencode", cf + "4.1-flash-1017\n" + orr + "5-flash-0301\n", snap), 0, orr + "5-flash-0301",
          stale=[{"pattern_index": 0, "newest": cf + "4.1-flash-1017", "version": "4.1"}])
    check("deepseek no-snapshot pattern ties", listing("opencode", oc, [r"openrouter/deepseek/deepseek-v(?P<v>[0-9.]+)-flash(-[0-9]{4})?"]), 3)
    check("snapshot beside a match with none is ambiguous",
          listing("opencode", "p/m-1-0301\np/m-1\n", [r"p/m-(?P<v>[0-9.]+)-(?P<s>[0-9]{4})", r"p/m-(?P<v>[0-9.]+)"]), 3)

    grok_or = r"openrouter/x-ai/grok-(?P<v>[0-9.]+)"
    check("4.20 against 4.7 is ambiguous", listing("opencode", oc, [grok_or]), 3)
    check("6.10 against 6.9 is ambiguous", listing("opencode", "p/m-6.9\np/m-6.10\n", [r"p/m-(?P<v>[0-9.]+)"]), 3)
    check("6 < 6.1 < 6.2", listing("opencode", "p/m-6\np/m-6.2\np/m-6.1\n", [r"p/m-(?P<v>[0-9.]+)"]), 0, "p/m-6.2")
    gv = r"p/g-(?P<v>[0-9.]+)"
    check("4.20 beside 4.7 and an older patch release", listing("opencode", "p/g-4.20\np/g-4.7\np/g-4.6.1\n", [gv]), 3,
          candidate_ids=["p/g-4.20", "p/g-4.7"])
    check("patch release of the same prefix", listing("opencode", "p/g-4.7.1\np/g-4.7\n", [gv]), 0, "p/g-4.7.1")
    check("4.70 beside 4.7 is unclear", listing("opencode", "p/g-4.70\np/g-4.7\n", [gv]), 3)
    check("row tie and decimal disagreement list both sets",
          listing("opencode", "p/g-4.20\np/g-4.20.0\np/g-4.7\n", [gv]), 3,
          candidate_ids=["p/g-4.20", "p/g-4.20.0", "p/g-4.7"])
    check("trailing zero is the same version", listing("opencode", "p/m-6\np/m-6.0\n", [r"p/m-(?P<v>[0-9.]+)"]), 3)

    check("unversioned family", listing("opencode", oc, [r"openrouter/meta/muse-ember"]), 0, "openrouter/meta/muse-ember", version="")
    check("unversioned ranks below versioned",
          listing("opencode", "p/muse\np/muse-2\n", [r"p/muse(-(?P<v>[0-9.]+))?"]), 0, "p/muse-2")
    check("sibling tier excluded by full match", listing("opencode", oc, [r"openrouter/xiaomi/mimo-v(?P<v>[0-9.]+)-pro"]), 0,
          "openrouter/xiaomi/mimo-v2.6-pro")
    check("no match", listing("opencode", oc, [r"openrouter/google/gemini-(?P<v>[0-9.]+)-carbon"]), 1)
    check("no match keeps patterns empty of a pick", listing("opencode", oc, [r"openrouter/z-ai/glm-(?P<v>[0-9.]+)-pro"]), 1, resolved=None)
    check("empty opencode listing", listing("opencode", "\n", [r"p/m"]), 4)

    check("grok error bullet", listing("grok", "- error: catalog unavailable\n", [r"grok-(?P<v>[0-9.]+)"]), 4)
    check("grok error row inside the section", listing("grok", "Available models:\n  - error: catalog unavailable\n", [r"grok-(?P<v>[0-9.]+)"]), 4)
    check("grok valid sibling-only listing", listing("grok", grok, [r"grok-code-(?P<v>[0-9.]+)"]), 1)
    check("opencode error text", listing("opencode", "Unauthorized\n", [r"openrouter/google/gemini-(?P<v>[0-9.]+)-carbon"]), 4)
    check("opencode error row with spaces", listing("opencode", "Error: x/y failed\n", [r"x/y"]), 4)
    check("opencode valid sibling-only listing", listing("opencode", "openrouter/google/gemini-5-titanium\n",
                                                       [r"openrouter/google/gemini-(?P<v>[0-9.]+)-carbon"]), 1)
    check("opencode nested and @cf rows", listing("opencode", "cloudflare-workers-ai/@cf/zai-org/glm-5.3\nopenrouter/~z-ai/glm-latest\n",
                                                 [r"cloudflare-workers-ai/@cf/zai-org/glm-(?P<v>[0-9.]+)"]), 0,
          "cloudflare-workers-ai/@cf/zai-org/glm-5.3")

    def access(programs):
        entry = {"slug": "gpt-7-sol", "visibility": "list"}
        if programs != "absent":
            entry["available_access_programs"] = {"cyber": programs}
        return json.dumps({"models": [entry]})
    want = ["--access-program", "daybreak_blue"]
    check("access program string is invalid", listing("codex", access("not_daybreak_blue"), [sol], want), 4)
    check("access program map is invalid", listing("codex", access({"daybreak_blue": False}), [sol], want), 4)
    check("access program list of non-strings is invalid", listing("codex", access([1]), [sol], want), 4)
    check("access program null means none", listing("codex", access(None), [sol], want), 1)
    check("access program absent means none",
          listing("codex", json.dumps({"models": [{"slug": "gpt-7-sol", "visibility": "list"}]}), [sol], want), 1)
    check("access program list", listing("codex", access(["standard", "daybreak_blue"]), [sol], want), 0, "gpt-7-sol")
    check("access program metadata is not read without the option", listing("codex", access("odd"), [sol]), 0, "gpt-7-sol")

    check("bad regex", listing("opencode", oc, ["(unclosed"]), 64)
    check("misspelled version group", listing("opencode", "example/model-2\nexample/model-3\n", [r"example/model-(?P<version>[0-9]+)"]), 64)
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
    with tempfile.TemporaryDirectory() as tmp:
        project = os.path.join(os.path.realpath(tmp), "project")
        os.mkdir(project)
        stubs = {}
        for name, body in (("show", 'import os\nprint("openrouter/stub/cwd-%s-pwd-%s" % (os.path.basename(os.getcwd()), os.path.basename(os.environ["PWD"])))\n'),
                           ("slow", "import time\ntime.sleep(5)\n")):
            stub_dir = os.path.join(os.path.realpath(tmp), name)
            os.mkdir(stub_dir)
            path = os.path.join(stub_dir, "opencode")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("#!%s\n%s" % (sys.executable, body))
            os.chmod(path, 0o755)
            stubs[name] = stub_dir
        old_path = os.environ["PATH"]
        try:
            for name, extra, want in (("show", [], 0), ("slow", ["--timeout", "1"], 4)):
                os.environ["PATH"] = stubs[name] + os.pathsep + old_path
                out = io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                    code = main(["--cli", "opencode", "--dir", project, "--pattern", "openrouter/stub/cwd-project-pwd-project"] + extra)
                assert code == want, ("public CLI stub", name, code, out.getvalue())
                if want == 0:
                    assert json.loads(out.getvalue())["resolved"] == "openrouter/stub/cwd-project-pwd-project", out.getvalue()
        finally:
            os.environ["PATH"] = old_path
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
