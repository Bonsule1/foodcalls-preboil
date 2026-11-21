# FoodCalls pre-boil planner

**Place:** FoodCalls, near IIIT Allahabad, Prayagraj
**Person:** Navesh Gupta, owner
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

<!-- TODO: paste output of `python preboil.py` once data.csv is in -->

## What it gets wrong / don't trust it for

- **Too few days.** With about a week of data, one odd day (a fest, a holiday, an exam week) moves the suggestion a lot.
- **It doesn't know the calendar.** Exam days, holidays and weekends aren't separate unless you split them yourself.
- **Lost sales are invisible.** If noodles ran out at 6:30, "sold" is lower than real demand, so the tool will under-suggest for that slot.
- **Estimated rows are weaker than counted rows.** Rows with `source=owner_estimate` come from memory.
- It only answers "how much to boil". It doesn't solve seating (18 seats) or any other problem he mentioned.

## Demo video

<!-- TODO: link your 3-minute screen recording here -->
