# The World in One Day — Saturday 21 November 2026

[![rank](https://make.fun/badge/news-image-20261121/xenopatijaya/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/xenopatijaya/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)
[![competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)

A single 1024×1024 newspaper front page summing up **Saturday 21 November 2026** in one image — 36 verified stories across 6 continents, drawn entirely by code (PIL, no photos).

## What's on the page

- **Masthead** — "THE WORLD IN ONE DAY", Saturday 21 November 2026.
- **Stats strip** — 3 missiles downed over Riyadh · 372,000 evacuated as Cyclone Akvan passed · M6.7 quake shakes Peru · 117* Rahul's century in Wellington.
- **3 illustrated leads** — COP31 spills into overtime (Antalya), three missiles downed over Riyadh, Rahul's century puts India on top (Wellington).
- **10 illustrated feature cards** — Akvan aftermath, Kyiv counts the cost, missiles land in Poland, Denmark expels attaché, ICC map to 2035, $52M for schooling, SCO Forum day two, Trump: Putin "tired", Palisades fire guilty verdict, Peru M6.7.
- **World map** — dot-matrix continents with 13 numbered pins (1–13).
- **The day in brief (14–36)** — 23 more stories, each with its source.
- **DATE CHECK strip** — near-miss stories excluded because they happened on another day (Akvan landfall 20 Nov, ICJ Myanmar ruling 19 Nov, Pete Rose pardon 20 Nov, Sensex +898 close 20 Nov, JPMorgan/Visa/Mastercard disclosures 19 Nov, Hyundai Elantra reveal 19 Nov).
- **Method footer** — every story happened, or was first reported, on Sat 21 Nov 2026 in some time zone; sources are named on each item.

## How it is built

`draw.py` (Pillow) draws `entry.png` deterministically — two runs produce byte-identical output. `main.py` is a pure copy: it copies the committed `entry.png` to `MAKEFUN_OUTPUT_DIR` (default `/output`) and draws nothing.

```sh
python3 draw.py          # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/
```

## Competition

[news-image-20261121 — "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121) · free entry · $100 USDC, top 50 paid · closes 23 Nov 2026 00:00 UTC.
