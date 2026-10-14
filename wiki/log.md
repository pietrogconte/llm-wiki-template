# Log

Append-only chronological log of every operation on the wiki (ingest, query, lint, setup). To see the last entries from a terminal: `grep "^## \[" wiki/log.md | tail -5`

## [2026-01-03] setup | Wiki created

Structure created from `llm-wiki-template`. Domain: home baking. Content in English. No MemPalace.

## [2026-01-10] ingest | 2026-01-10 Levain feeding diary

- New pages: [[2026-01-10 Levain feeding diary]], [[Sourdough bread]], [[Natural fermentation]].

## [2026-01-24] ingest | 2026-01-24 Hydration test 70 vs 75

- New pages: [[2026-01-24 Hydration test 70 vs 75]], [[Hydration]], [[Cast iron pot]], [[Fermentation temperature]]. ✅ 70% as the bread default.

## [2026-02-07] ingest | 2026-02-07 30-minute autolyse

- New page: [[Autolyse]]. Updated: [[Sourdough bread]].

## [2026-02-14] ingest | 2026-02-14 First Neapolitan pizza

- New pages: [[Neapolitan pizza]], [[Pizza stone]], [[Type 00 flour]], [[Home oven]], [[Maillard reaction]].

## [2026-02-21] ingest | 2026-02-21 00 flour and W value

- New page: [[Flour strength]]. Updated: [[Type 00 flour]].

## [2026-02-28] ingest | 2026-02-28 Oven thermometer

- Updated: [[Home oven]] (🔎 real temperature measured). Affects [[Neapolitan pizza]].

## [2026-03-07] ingest | 2026-03-07 High-hydration focaccia

- New page: [[Focaccia]]. Updated: [[Hydration]], [[Autolyse]].

## [2026-03-14] ingest | 2026-03-14 Cold fermentation

- Updated: [[Fermentation temperature]] (cold fermentation). Affects [[Focaccia]].

## [2026-03-20] query | Why did the pizza come out with a pale bottom?

Answered from [[Home oven]] and [[Pizza stone]]: the real oven runs ~20 °C below the dial. 💡 recorded in [[Neapolitan pizza]].

## [2026-04-04] ingest | 2026-04-04 First panettone

- New page: [[Panettone]]. Updated: [[Natural fermentation]], [[Flour strength]].

## [2026-04-18] ingest | 2026-04-18 Crust browning

- Updated: [[Maillard reaction]]. Affects [[Panettone]] (dark top).

## [2026-04-18] lint | Check

`python scripts/lint_wiki.py --strict`: 0 errors, 0 warnings. Semantic: [[Fermentation temperature]], [[Maillard reaction]] and [[Home oven]] became hubs (cited by all four projects).
