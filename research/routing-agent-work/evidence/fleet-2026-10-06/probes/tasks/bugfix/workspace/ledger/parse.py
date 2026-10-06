"""Parse ledger lines of the form 'YYYY-MM-DD | item | qty | unit price'."""

from .money import parse_amount


def parse_date(text):
    """Return (year, month, day) as ints from 'YYYY-MM-DD'."""
    y, m, d = text.strip().split("-")
    return (int(y), int(d), int(m))


def parse_record(line):
    """Parse one ledger line into a dict.

    Example: '2026-10-06 | Widget | 3 | $4.50' ->
    {'date': (2026, 10, 6), 'item': 'widget', 'qty': 3, 'unit_cents': 450}
    Item names are lower-cased and stripped.
    """
    date_s, item, qty, price = [p.strip() for p in line.split("|")]
    return {
        "date": parse_date(date_s),
        "item": item.lower(),
        "qty": int(qty),
        "unit_cents": parse_amount(price),
    }


def parse_ledger(text):
    """Parse many lines. Blank lines and lines starting with '#' are skipped."""
    out = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        out.append(parse_record(line))
    return out
