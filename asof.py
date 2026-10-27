"""Lab 16: build an as-of card-spend panel and compare it with a naive panel."""

from collections import defaultdict
from datetime import date


# Edit this date to evaluate the data set at another point in time.
DECISION_DATE = date.fromisoformat("2026-03-31")

DATA = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published": "2026-03-10", "index": 111.0},
]


def row_numbers(rows):
    """Return row numbers in their original order for readable audit output."""
    return [record["row"] for record in rows]


def remove_exact_duplicates(rows):
    """Keep the first copy of each observation; row number is not part of identity."""
    seen = set()
    kept, removed = [], []
    for record in rows:
        identity = (record["ticker"], record["month"], record["published"], record["index"])
        if identity in seen:
            removed.append(record)
        else:
            seen.add(identity)
            kept.append(record)
    return kept, removed


def keep_latest_revision(rows):
    """For every ticker/month, retain its latest publication in the supplied rows."""
    latest = {}
    for record in rows:
        key = (record["ticker"], record["month"])
        if key not in latest or record["published"] > latest[key]["published"]:
            latest[key] = record
    kept = [record for record in rows if latest[(record["ticker"], record["month"])] is record]
    removed = [record for record in rows if latest[(record["ticker"], record["month"])] is not record]
    return kept, removed


def calculate_signals(panel):
    """Calculate the change into the latest available month for each ticker."""
    by_ticker = defaultdict(list)
    for record in panel:
        by_ticker[record["ticker"]].append(record)

    signals = {}
    for ticker, records in by_ticker.items():
        records.sort(key=lambda record: record["month"])
        previous, latest = records[-2:]
        change = (latest["index"] / previous["index"] - 1) * 100
        signals[ticker] = (change, latest["month"])
    return signals


def print_signals(label, signals):
    print(label)
    for ticker in sorted(signals):
        change, month = signals[ticker]
        month_name = date.fromisoformat(f"{month}-01").strftime("%B")
        print(f"  {ticker}: {change:+.2f}% {month_name}")


def main():
    # Rule 1: quarantine rows without tickers.
    valid_tickers = [record for record in DATA if record["ticker"]]
    quarantined = [record for record in DATA if not record["ticker"]]

    # Rule 2: remove exact duplicates after quarantine.
    deduplicated, duplicates = remove_exact_duplicates(valid_tickers)

    # Rule 3: remove publications unavailable on the decision date.
    available = [record for record in deduplicated if date.fromisoformat(record["published"]) <= DECISION_DATE]
    after_decision_date = [record for record in deduplicated if date.fromisoformat(record["published"]) > DECISION_DATE]

    # Rule 4: retain the newest then-available revision for each ticker/month.
    as_of_panel, older_revisions = keep_latest_revision(available)
    as_of_panel.sort(key=lambda record: record["row"])

    # The naive comparison skips only the decision-date restriction, not data cleanup.
    naive_panel, _ = keep_latest_revision(deduplicated)

    print(f"Decision date: {DECISION_DATE.isoformat()}")
    print("Row funnel")
    print(f"  Quarantined (no ticker): {row_numbers(quarantined)}")
    print(f"  Exact duplicate: {row_numbers(duplicates)}")
    print(f"  Published after decision date: {row_numbers(after_decision_date)}")
    print(f"  Older revision: {row_numbers(older_revisions)}")
    print(f"  Remaining: {row_numbers(as_of_panel)}")

    print("\nRemaining as-of panel")
    print("  Row  Ticker  Month    Published   Index")
    for record in as_of_panel:
        print(f"  {record['row']:>3}  {record['ticker']:<6}  {record['month']}  {record['published']}  {record['index']:.1f}")

    print()
    print_signals("As-of signals", calculate_signals(as_of_panel))
    print()
    print_signals("Naive signals (unrestricted publication dates)", calculate_signals(naive_panel))


if __name__ == "__main__":
    main()
