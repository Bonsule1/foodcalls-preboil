# FoodCalls pre-boil planner

**Place:** FoodCalls, near IIIT Allahabad, Prayagraj
**Person:** Nivesh Gupta, owner
**Date of fieldwork:** 20 Nov 2026

FoodCalls boils noodles and pasta in advance so the after-class rush (5-8 pm) gets served fast.
Whatever is left goes bad and gets thrown away, and the owner decides the quantity by guess.
This tool reads the shop's own records (`data.csv`) and suggests how many plates to boil for
each item in each time slot.

- Problem and research: [research.md](research.md)
- Visit, conversation and data notes: [fieldwork.md](fieldwork.md)
- Reflection: [reflection.md](reflection.md)

## How to run

Needs Python 3 (no extra libraries).

```
python preboil.py                         # uses data.csv
python preboil.py data.csv --cover 0.9    # cover 90% of past days instead of 75%
python preboil.py data.csv --buffer 2     # keep 2 spare plates instead of 1
```

### data.csv columns

| column | meaning |
|---|---|
| date | day of the record |
| slot | time slot, e.g. `17-20` |
| item | noodles / pasta / maggi ... |
| boiled_plates | plates boiled before the slot (blank if unknown) |
| sold_plates | plates sold in the slot (required) |
| thrown_plates | plates thrown away (blank if unknown) |
| source | `counted`, `register` or `owner_estimate` |
| notes | anything odd about that row |

## How it decides

For every item and slot, it looks at the plates sold on past days and takes the value that covers
`--cover` of those days (75th percentile by default), then adds `--buffer` plates. It then compares
that with what was really boiled.

Bad rows (text in a number column, empty item or slot, missing sold count) are skipped and listed
under "Rows to check". A row where more was sold than boiled is kept but flagged, because it
usually means a second batch was boiled.

## Real output

`python preboil.py` on the current `data.csv` (estimate rows, see below):

```
Pre-boil plan from 56 rows (cover 75% of days, +1 buffer)
Rows by source: estimate=56

item        slot      days  avg sold  avg boiled  avg thrown  SUGGEST
---------------------------------------------------------------------
noodles     10-13        7       1.0           -           -        2
noodles     13-17        7       2.9           -           -        4
noodles     17-20        7       7.3           -           -        9
noodles     20-22        7       2.0           -           -        3
pasta       10-13        7       0.4           -           -        2
pasta       13-17        7       1.4           -           -        3
pasta       17-20        7       4.0           -           -        6
pasta       20-22        7       1.3           -           -        3
---------------------------------------------------------------------
```

Reading it: before 5 pm, boil about 9 plates of noodles and 6 of pasta. In the 10 am-5 pm slots only 2-4 are needed.

## What it gets wrong / don't trust it for

- **Too few days.** With about a week of data, one odd day (a fest, a holiday, an exam week) moves the suggestion a lot.
- **It doesn't know the calendar.** Exam days, holidays and weekends aren't separate unless you split them yourself.
- **Lost sales are invisible.** If noodles ran out at 6:30, "sold" is lower than real demand, so the tool will under-suggest for that slot.
- **The current data is an estimate, not a count.** All 56 rows are built from the owner's spoken figures (~20 noodle/pasta customers a day, rush 5-8 pm), split into slots by me. See [fieldwork.md](fieldwork.md#data-datacsv). Treat the suggestions as a starting point until real counts replace them.
- **No waste numbers yet.** `boiled_plates` and `thrown_plates` are blank, so it can't yet say how many plates would be saved.
- **The buffer dominates small slots.** Pasta 10-13 averages 0.4 plates but gets a suggestion of 2. For tiny slots, "boil when ordered" is probably better.
- It only answers "how much to boil". It doesn't solve seating (18 seats) or any other problem he mentioned.

## Demo video

<!-- TODO: link your 3-minute screen recording here -->
