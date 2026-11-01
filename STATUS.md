# STATUS

**Project:** Mini-Course Author Guide
**Maintainer:** Asdale Dynamics, LLC · dylanasdale.github.io
**Last updated:** 2026-11-01

## What was built

A complete guide for turning one chapter of a book/manual into a small,
self-hosted course, in the house style: plain English, step by step, never
condescending, with real numbers and checkable promises.

- **11 Markdown documents in `docs/`** — the seven chapters promised by the
  project goal (promise-sized lesson; reader-finishable outline; recording
  without fancy gear; lesson pages & printables; platform-vs-marketplace fee
  math with a worked break-even example; kindly-worded refund policy and
  reply scripts; three-email launch/buyer drips on a plain newsletter) plus
  the lesson template, launch checklist, and glossary.
- **`build.py`** — a dependency-free (standard library only) build script
  that converts `docs/*.md` into a warm, styled static site in `site/`:
  `index.html` with hero + card TOC, one HTML page per document with
  header nav and prev/next pager, `styles.css`. The build **validates and
  fails loudly** on: a doc missing its `# Title`, a doc not registered in
  the build's page list, a broken internal link, or an index card missing.
- **`tests/test_build.py`** — 18 unittest cases covering the build, content,
  sources, and CLI (details under Verification).
- **`README.md`** — project overview, build/test/serve instructions, layout,
  positioning versus the sibling guides (selling-digital-products-guide and
  guide-writing-cookbook), credit to Asdale Dynamics, LLC.
- **`LICENSE`** — MIT, copyright line exactly: Copyright (c) 2026 Asdale
  Dynamics, LLC.

## How to run it

From the project root (Python 3.10+, no installs needed):

```sh
python3 build.py                                   # build site/ + validate
python3 build.py --check                           # docs validation only
python3 -m http.server 8000 --directory site       # preview at localhost:8000
python3 -m unittest discover -s tests -v           # run the test suite
```

## Verification results

Run on 2026-11-01, all passing:

- `python3 build.py` → `Built 12 pages into site` (11 doc pages + index).
- `python3 build.py --check` → `Docs check passed (11 pages).`
- `python3 -m unittest discover -s tests` → `Ran 18 tests ... OK`.

Coverage highlights: all pages exist and are well-formed HTML; every
internal link resolves; the index links every page; nav links every page;
pager starts/ends correctly; no unfilled `____` blanks outside pages where
blanks are the artifact (template, checklist, 01/07 exercises/drafts,
glossary quotes); glossary defines ≥15 terms including all key ones; the
launch checklist renders 40+ checkbox items; fee-math tables and figures
(`$47.28`, `$44.10`) render; no TODOs; no secret-shaped strings in sources
or output; LICENSE text matches the required exact copyright line; CLI
build/check exit 0, and a deliberately broken probe doc makes `--check`
exit 1 with a `BUILD ERROR`.

Bugs found and fixed during verification: table separator rows rendering as
data rows, list-item continuation (lazy-wrapped) lines escaping their `<li>`,
double `</li>` emission, and several garbled sentences/misphrasings in
chapters 03/05/06/07 and the checklist.

## Known gaps

- **Illustrative fee rates.** Chapter 05 uses clearly-labeled illustrative
  rates (Stripe-like 2.9% + $0.30, marketplace ~10%, platform ~$39/mo + 5%)
  to teach the arithmetic; readers are told to rerun the math with current
  real rates. No live pricing is fetched.
- **No fenced-code or nested-list content** in current docs, so those
  parser paths are exercised only lightly (fenced code is supported in the
  parser but untested with real content).
- **Videos/printables don't exist yet** — the guide teaches the reader to
  produce them; the repo itself ships no media.
- **Minimal coverage of EU VAT / cross-border specifics** — flagged in the
  fee math chapter as "check before launch," not calculated in depth.
- **No pagination/search on the site** — deliberate for an 11-page v1; the
  card index is the navigation.

## Sibling-project boundaries (repeated from README)

- selling-digital-products-guide: breadth of digital goods. Not here.
- guide-writing-cookbook: writing the manual itself. Not here.
