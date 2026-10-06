"""Reporting over parsed ledger records."""

from .money import format_cents


def line_total(rec):
    return rec["qty"] * rec["unit_cents"]


def totals_by_item(records):
    """Return {item: total_cents} summed over all records."""
    totals = {}
    for rec in records:
        totals[rec["item"]] = totals.get(rec["item"], 0) + line_total(rec)
    return totals


def top_items(records, n):
    """Return the n items with the largest total as [(item, total_cents), ...].

    Order is by total descending; ties are broken by item name ascending.
    """
    ranked = sorted(totals_by_item(records).items(), key=lambda kv: kv[1])
    return ranked[:n]


def summary_line(records, n=3):
    """Return 'widget=$13.50; gadget=$4.00' for the top n items."""
    return "; ".join(f"{item}={format_cents(t)}" for item, t in top_items(records, n))
