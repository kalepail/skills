"""Visible test suite. Run with: python3 run_tests.py"""

import sys
import traceback

from ledger.money import format_cents, parse_amount
from ledger.parse import parse_date, parse_ledger, parse_record
from ledger.report import summary_line, top_items

SAMPLE = """
# date | item | qty | price
2026-10-01 | Widget | 3 | $4.50
2026-10-02 | Gadget | 1 | $4.00
2026-10-03 | widget | 0 | $4.50
2026-10-04 | Gizmo | 2 | $1.25
"""


def test_parse_amount():
    assert parse_amount("$1,234.56") == 123456
    assert parse_amount("-$3.10") == -310
    assert parse_amount("12") == 1200


def test_format_cents():
    assert format_cents(123456) == "$1,234.56"
    assert format_cents(-310) == "-$3.10"


def test_parse_date():
    assert parse_date("2026-10-06") == (2026, 10, 6)


def test_parse_record():
    rec = parse_record("2026-10-06 | Widget | 3 | $4.50")
    assert rec == {"date": (2026, 10, 6), "item": "widget", "qty": 3, "unit_cents": 450}


def test_top_items():
    recs = parse_ledger(SAMPLE)
    assert top_items(recs, 2) == [("widget", 1350), ("gadget", 400)]


def test_summary_line():
    recs = parse_ledger(SAMPLE)
    assert summary_line(recs, 3) == "widget=$13.50; gadget=$4.00; gizmo=$2.50"


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
