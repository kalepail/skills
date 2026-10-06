"""Hidden tests, copied in by the grader after the agent finishes."""

import sys
import traceback

from ledger.money import format_cents, parse_amount
from ledger.parse import parse_date, parse_ledger
from ledger.report import summary_line, top_items


def test_format_small_negative():
    assert format_cents(-5) == "-$0.05"
    assert format_cents(-100) == "-$1.00"
    assert format_cents(0) == "$0.00"
    assert format_cents(-123456789) == "-$1,234,567.89"


def test_format_roundtrip():
    for s in ["$0.01", "-$0.99", "$10.00", "-$1,000.50"]:
        assert format_cents(parse_amount(s)) == s, s


def test_dates_varied():
    assert parse_date("2026-01-31") == (2026, 1, 31)
    assert parse_date(" 1999-12-01 ") == (1999, 12, 1)


def test_top_ties_by_name():
    recs = parse_ledger("""
2026-10-01 | pear | 1 | $2.00
2026-10-01 | apple | 2 | $1.00
2026-10-01 | fig | 1 | $5.00
2026-10-01 | date | 4 | $0.50
""")
    assert top_items(recs, 4) == [("fig", 500), ("apple", 200), ("date", 200), ("pear", 200)]
    assert top_items(recs, 1) == [("fig", 500)]


def test_summary_negative_refund():
    recs = parse_ledger("""
2026-10-01 | widget | 1 | $3.00
2026-10-02 | refund | 1 | -$0.40
""")
    assert summary_line(recs, 2) == "widget=$3.00; refund=-$0.40"


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
