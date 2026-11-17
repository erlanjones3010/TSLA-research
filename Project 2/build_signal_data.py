"""Download the point-in-time 10-year Treasury yield (DGS10) from ALFRED.

For every quarter-end date in data/prices.csv, this asks ALFRED for the DGS10
vintage that existed on that date and keeps the latest observation dated
before it. The result is saved to data/dgs10_asof.csv so the app runs offline.

Run once (needs internet):  python build_signal_data.py
"""

import csv
import io
import time
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
ALFRED = ("https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10"
          "&vintage_date={d}&cosd=2020-01-01")


def quarter_end_dates():
    with open(HERE / "data" / "prices.csv", newline="") as f:
        dates = [row["Date"] for row in csv.DictReader(f)]
    return [d for d in dates if int(d[5:7]) in (3, 6, 9, 12)]


def latest_known(decision_date):
    """Latest DGS10 observation dated strictly before the decision date, from the vintage on that date."""
    url = ALFRED.format(d=decision_date)
    req = urllib.request.Request(url, headers={"User-Agent": "FIN43900-project2"})
    for attempt in range(3):
        try:
            text = urllib.request.urlopen(req, timeout=90).read().decode()
            break
        except OSError:
            if attempt == 2:
                raise
            time.sleep(3)
    return parse_vintage(text, decision_date)


def parse_vintage(text, decision_date):
    """From one ALFRED vintage CSV, return (observation_date, value) of the latest
    observation dated strictly before the decision date."""
    rows = list(csv.reader(io.StringIO(text)))[1:]
    best = None
    for obs_date, value in rows:
        if value in ("", ".") or obs_date >= decision_date:
            continue
        if best is None or obs_date > best[0]:
            best = (obs_date, float(value))
    return best


def main():
    out = []
    for d in quarter_end_dates():
        obs_date, value = latest_known(d)
        out.append({"decision_date": d, "vintage_date": d, "observation_date": obs_date,
                    "dgs10_percent": value, "source": "ALFRED DGS10",
                    "downloaded": date.today().isoformat()})
        print(d, obs_date, value)
        time.sleep(0.5)
    with open(HERE / "data" / "dgs10_asof.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"Saved {len(out)} rows to data/dgs10_asof.csv")


if __name__ == "__main__":
    main()
