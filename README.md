# Mini-Course Author Guide

**Turn one promise-sized lesson from your book into a small, self-hosted
course** — outlined at a reader-finishable pace, recorded without fancy gear,
sold after honest fee math, refunded kindly, and announced with a plain
newsletter instead of a giant tool.

Written in the same voice as everything else from [Asdale Dynamics, LLC](https://dylanasdale.github.io):
plain English, step by step, never condescending.

## What's inside

Eleven documents in [`docs/`](docs/), also published as a small static website:

| Doc | What it does |
| --- | --- |
| [00 — Start Here](docs/00-start-here.md) | The whole recipe on one napkin, plus positioning vs sibling guides |
| [01 — The Promise-Sized Lesson](docs/01-promise-sized-lesson.md) | Pick one lesson: one person, one finish line, both checkable |
| [02 — Outline at a Finishable Pace](docs/02-outline-at-pace.md) | Time-budget the outline so a tired reader actually finishes |
| [03 — Recording Without Fancy Gear](docs/03-record-without-fancy-gear.md) | Phone + laptop + quiet room; tolerances table; export settings |
| [04 — Lesson Pages & Printables](docs/04-lesson-pages-and-printables.md) | Page skeleton, checkpoints, one-job printables |
| [05 — Platform-vs-Marketplace Fee Math](docs/05-fee-math.md) | Worked $49 × 8 sales examples, break-even rule, decision rule |
| [06 — Refunds Handled Kindly](docs/06-refunds-with-grace.md) | Policy facts, paste-adapt refund policy, reply scripts |
| [07 — Drip Announcements](docs/07-drip-announcements.md) | Three-email launch drip + buyer welcome drip, plain newsletter |
| [Lesson template](docs/lesson-template.md) | Copy, fill the blanks, ship it |
| [Launch checklist](docs/launch-checklist.md) | The whole launch, checkbox by checkbox |
| [Glossary](docs/glossary.md) | Plain words: drip, break-even, restart command, and friends |

## How this guide is different

- **Selling Digital Products Guide** covers the *breadth* of digital goods.
  This guide does one product shape — a small self-hosted course — end to end.
- **Guide-Writing Cookbook** covers *writing the manual itself*. This guide
  assumes the manual exists and turns it into a taught experience.

## Requirements

Python 3.10+ (standard library only — no pip installs). Run scripts from the
project root.

## Build the site

```sh
python3 build.py            # builds ./site/ and validates it
python3 build.py --check    # validate docs without writing anything
python3 build.py --out /tmp/course-site
```

The build converts every document in `docs/` to a styled HTML page, generates
`index.html` and `styles.css`, and **fails loudly** if a document is missing a
title, an internal link is broken, or a promised page is absent.

Preview locally (no server needed by the site itself; any static host works):

```sh
python3 -m http.server 8000 --directory site
# then open http://localhost:8000
```

## Run the tests

```sh
python3 -m unittest discover -s tests -v
```

The tests build the site into a temp directory and verify: all pages exist and
are well-formed, every internal link resolves, the index links every page,
the glossary defines its promised terms, the checklist renders its checkboxes,
no placeholder blanks leaked outside the template, no stray "TODO"s, and no
secret-shaped strings anywhere. They also check the LICENSE line and run the
CLI end to end.

## Project layout

```
build.py            build script (markdown -> static site, with validation)
tests/test_build.py build + content tests
docs/               the guide, in Markdown
site/               generated static site (do not edit; run build.py)
```

Style notes for edits: write like a friend would, use real numbers, keep
promises checkable, and re-run `python3 build.py --check` and the tests
before committing.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
