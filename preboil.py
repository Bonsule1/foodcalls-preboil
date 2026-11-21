"""
preboil.py - suggests how many plates of noodles/pasta FoodCalls should
pre-boil for each time slot, from the shop's own past sales in data.csv.

Usage:
    python preboil.py                    # reads data.csv, default settings
    python preboil.py data.csv --cover 0.75 --buffer 1

Idea: for each (item, slot) look at how many plates were actually SOLD on
past days. Boil enough to cover most days (the --cover percentile), plus a
small --buffer. Compare that with what was really boiled and thrown away.
"""

import argparse
import csv
import math
import sys
from collections import defaultdict

REQUIRED = ["date", "slot", "item", "boiled_plates", "sold_plates"]


def to_number(value):
    """Return a non-negative number, None if blank, raise ValueError if junk."""
    value = (value or "").strip()
    if value == "":
        return None
    n = float(value)
    if n < 0 or math.isnan(n):
        raise ValueError("negative or NaN")
    return n


def percentile(values, p):
    """Simple linear-interpolated percentile, p in [0, 1]."""
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    k = (len(values) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def load(path):
    rows, skipped = [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"data.csv is missing columns: {', '.join(missing)}")
        for line_no, raw in enumerate(reader, start=2):
            try:
                boiled = to_number(raw["boiled_plates"])
                sold = to_number(raw["sold_plates"])
                thrown = to_number(raw.get("thrown_plates"))
            except ValueError:
                skipped.append((line_no, "a number column has text/negative value"))
                continue
            if not raw["item"].strip() or not raw["slot"].strip():
                skipped.append((line_no, "item or slot is empty"))
                continue
            if sold is None:
                skipped.append((line_no, "sold_plates is empty"))
                continue
            if boiled is not None and sold > boiled:
                # Possible: they boiled a second batch mid-slot. Keep it, but warn.
                skipped.append((line_no, f"sold ({sold:g}) > boiled ({boiled:g}) - kept, check it"))
            rows.append({
                "date": raw["date"].strip(),
                "slot": raw["slot"].strip(),
                "item": raw["item"].strip().lower(),
                "boiled": boiled,
                "sold": sold,
                "thrown": thrown,
            })
    return rows, skipped


def slot_key(slot):
    """Sort '10-13' before '17-20'. Unknown formats go last."""
    try:
        return int(slot.split("-")[0])
    except ValueError:
        return 99


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("csv", nargs="?", default="data.csv")
    ap.add_argument("--cover", type=float, default=0.75,
                    help="fraction of past days the suggestion should cover (0-1), default 0.75")
    ap.add_argument("--buffer", type=int, default=1,
                    help="extra plates on top, default 1")
    args = ap.parse_args()
    if not 0 <= args.cover <= 1:
        sys.exit("--cover must be between 0 and 1")

    rows, skipped = load(args.csv)
    if not rows:
        sys.exit("No usable rows in data file.")

    groups = defaultdict(list)
    for r in rows:
        groups[(r["item"], r["slot"])].append(r)

    print(f"Pre-boil plan from {len(rows)} rows "
          f"(cover {args.cover:.0%} of days, +{args.buffer} buffer)\n")
    print(f"{'item':<12}{'slot':<9}{'days':>5}{'avg sold':>10}{'avg boiled':>12}"
          f"{'avg thrown':>12}{'SUGGEST':>9}")
    print("-" * 69)

    total_now, total_suggest = 0.0, 0.0
    for (item, slot) in sorted(groups, key=lambda k: (k[0], slot_key(k[1]))):
        g = groups[(item, slot)]
        sold = [r["sold"] for r in g]
        boiled = [r["boiled"] for r in g if r["boiled"] is not None]
        thrown = [r["thrown"] for r in g if r["thrown"] is not None]
        suggest = math.ceil(percentile(sold, args.cover)) + args.buffer
        avg_b = sum(boiled) / len(boiled) if boiled else float("nan")
        avg_t = sum(thrown) / len(thrown) if thrown else float("nan")
        if boiled:
            total_now += avg_b
            total_suggest += suggest
        print(f"{item:<12}{slot:<9}{len(g):>5}{sum(sold)/len(sold):>10.1f}"
              f"{avg_b:>12.1f}{avg_t:>12.1f}{suggest:>9}")

    print("-" * 69)
    if total_now:
        diff = total_now - total_suggest
        word = "fewer" if diff >= 0 else "more"
        print(f"Per day: boiling now ~{total_now:.0f} plates, suggested {total_suggest:.0f} "
              f"-> {abs(diff):.0f} plates {word}.")

    if skipped:
        print("\nRows to check:")
        for line_no, why in skipped:
            print(f"  line {line_no}: {why}")


if __name__ == "__main__":
    main()
