"""Money helpers. All amounts are integer cents."""


def parse_amount(text):
    """Parse '$1,234.56', '-$3.10', '12' or '0.5' into integer cents."""
    s = text.strip()
    neg = s.startswith("-")
    s = s.lstrip("-").lstrip("$").replace(",", "")
    if "." in s:
        whole, frac = s.split(".")
        frac = (frac + "00")[:2]
    else:
        whole, frac = s, "00"
    cents = int(whole or "0") * 100 + int(frac)
    return -cents if neg else cents


def format_cents(cents):
    """Format integer cents as '$1,234.56'. Negative values look like '-$0.05'."""
    sign = "-" if cents < 0 else ""
    return f"{sign}${cents // 100:,}.{cents % 100:02d}"
