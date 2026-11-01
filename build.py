#!/usr/bin/env python3
"""Build the Mini-Course Author Guide static site from docs/ markdown.

No third-party dependencies. Usage:

    python3 build.py                # build site/ and validate
    python3 build.py --out /tmp/x   # build into a custom directory
    python3 build.py --check        # validate docs only, no files written

Validation fails the build (nonzero exit) if a document is missing a title,
an internal link is broken, or the site is missing expected files.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
DEFAULT_OUT = ROOT / "site"

SITE_TITLE = "Mini-Course Author Guide"
SITE_TAGLINE = "Turn one promise-sized lesson from your book into a small, self-hosted course."
FOOTER = (
    "Mini-Course Author Guide · MIT License · "
    "Copyright (c) 2026 Asdale Dynamics, LLC · "
    '<a href="https://dylanasdale.github.io">dylanasdale.github.io</a>'
)

CSS = """\
:root {
  --paper: #faf6ef;
  --ink: #2b2723;
  --soft: #5c544b;
  --accent: #b5542d;
  --accent-soft: #f3e2d6;
  --card: #fffdf9;
  --border: #e5dbcc;
  --code-bg: #f0e9dd;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 18px/1.65 Georgia, "Times New Roman", serif;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
a:hover { color: #8a3d1e; }
.wrap { max-width: 46rem; margin: 0 auto; padding: 0 1.4rem; }
code, pre {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.82em;
  background: var(--code-bg);
  border-radius: 4px;
}
code { padding: 0.1em 0.35em; }
pre { padding: 0.9em 1.1em; overflow-x: auto; line-height: 1.5; }
pre code { padding: 0; background: none; font-size: 0.95rem; }

.site-header { border-bottom: 4px double var(--border); background: var(--card); }
.site-header .wrap { padding: 1.6rem 1.4rem 1.1rem; }
.brand {
  font-size: 1.35rem; font-weight: bold; color: var(--ink);
  text-decoration: none; letter-spacing: 0.01em;
}
.brand:hover { color: var(--accent); }
.tagline { margin: 0.15rem 0 0.9rem; color: var(--soft); font-style: italic; font-size: 0.98rem; }
.nav { display: flex; flex-wrap: wrap; gap: 0.2rem 0.9rem; font-size: 0.92rem; }
.nav a { color: var(--soft); text-decoration: none; }
.nav a:hover { color: var(--accent); text-decoration: underline; }

main .wrap { padding-top: 2.2rem; padding-bottom: 2.6rem; }
h1, h2, h3 { line-height: 1.25; font-weight: bold; }
h1 { font-size: 1.9rem; margin: 0 0 1.2rem; color: #1f1c19; }
h2 { font-size: 1.4rem; margin: 2.2rem 0 0.7rem; border-bottom: 1px solid var(--border); padding-bottom: 0.25rem; }
h3 { font-size: 1.15rem; margin: 1.7rem 0 0.5rem; }
h4 { font-size: 1.02rem; margin: 1.4rem 0 0.4rem; }
p { margin: 0.8rem 0; }
ul, ol { padding-left: 1.5rem; }
li { margin: 0.35rem 0; }
li.pace { list-style: none; margin-left: -1.45rem; padding-left: 1.45rem; }
li.pace::before { content: "\\2610\\2009"; color: var(--accent); }
li.pace.done::before { content: "\\2611\\2009"; }
blockquote {
  margin: 1.2rem 0; padding: 0.6rem 1.2rem;
  border-left: 4px solid var(--accent-soft);
  background: var(--accent-soft); border-radius: 0 8px 8px 0;
  color: #4a3c31;
}
blockquote p { margin: 0.3rem 0; }
hr { border: none; border-top: 1px dashed var(--border); margin: 2rem 0; }

table { border-collapse: collapse; width: 100%; margin: 1.2rem 0; font-size: 0.93rem; }
th, td { border: 1px solid var(--border); padding: 0.45rem 0.7rem; text-align: left; vertical-align: top; }
th { background: var(--accent-soft); }

.hero { text-align: left; padding: 2.2rem 0 1rem; }
.hero h1 { font-size: 2.2rem; margin-bottom: 0.6rem; }
.hero p.lede { font-size: 1.15rem; color: var(--soft); max-width: 38rem; }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr)); gap: 1rem; margin: 1.6rem 0; }
.card {
  display: block; background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 0.95rem 1.1rem; text-decoration: none; color: var(--ink);
}
.card:hover { border-color: var(--accent); box-shadow: 0 2px 8px rgba(90, 60, 30, 0.08); }
.card .num { display: block; color: var(--accent); font-size: 0.8rem; font-weight: bold;
  letter-spacing: 0.06em; text-transform: uppercase; }
.card .t { display: block; font-weight: bold; margin-top: 0.2rem; }
.card .d { display: block; color: var(--soft); font-size: 0.85rem; margin-top: 0.25rem; }
.note { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
  padding: 1rem 1.3rem; }

.pager { display: flex; justify-content: space-between; gap: 1rem; margin-top: 2.5rem;
  padding-top: 1rem; border-top: 1px solid var(--border); font-size: 0.95rem; }
.pager a { text-decoration: none; }
.pager .next { text-align: right; margin-left: auto; }
.pager span { display: block; font-size: 0.78rem; color: var(--soft); text-transform: uppercase;
  letter-spacing: 0.07em; }

footer { border-top: 4px double var(--border); background: var(--card); }
footer .wrap { padding: 1.3rem 1.4rem 1.6rem; color: var(--soft); font-size: 0.88rem; }
footer a { color: var(--soft); }

@media print {
  .site-header, .pager, footer { display: none; }
  body { background: #fff; }
}
"""

# (doc filename, nav label, card blurb). Order defines page order everywhere.
PAGES = [
    ("00-start-here.md", "Start Here", "The recipe on one napkin."),
    ("01-promise-sized-lesson.md", "1 · The Promise", "Pick one lesson, one person, one finish line."),
    ("02-outline-at-pace.md", "2 · The Outline", "Pace it so a tired reader actually finishes."),
    ("03-record-without-fancy-gear.md", "3 · Recording", "Phone, laptop, quiet room. That's the studio."),
    ("04-lesson-pages-and-printables.md", "4 · Pages & Printables", "Hand-deliver value before anyone buys."),
    ("05-fee-math.md", "5 · Fee Math", "Platform vs marketplace, on paper, in five minutes."),
    ("06-refunds-with-grace.md", "6 · Refunds", "A policy you are proud to publish."),
    ("07-drip-announcements.md", "7 · The Drip", "Three plain emails beat a giant tool."),
    ("lesson-template.md", "Template", "Copy, fill the blanks, ship it."),
    ("launch-checklist.md", "Checklist", "The whole launch, checkbox by checkbox."),
    ("glossary.md", "Glossary", "Plain words for plain people."),
]

HOME_INTRO = """\
# Turn your book into a small course you own.

**You wrote the manual.** It already helps people. This guide walks you — in
plain English, step by step, never condescending — through turning *one
slice* of it into a promise-sized lesson:

- outlined at a pace a tired reader can finish,
- recorded with the phone and laptop you already own,
- sold after five minutes of honest fee math,
- refunded kindly,
- and announced with a quiet newsletter drip instead of a huge tool.

No film crew. No course platform subscription eating your margin. Everything
ships as plain files — Markdown in, static HTML out — that you host wherever
you like and back up in one folder."""

HOME_OUTRO = """\
## How this is different

- **Selling Digital Products Guide** covers the *breadth* of digital goods.
  This guide does one product shape — a small self-hosted course — end to end.
- **Guide-Writing Cookbook** covers *writing the manual itself*. This guide
  assumes the manual exists and turns it into a taught experience.

Begin at [Start Here](00-start-here.html), or jump to the piece you need.
Everything here is MIT licensed; make it yours."""


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- markdown


def inline(text: str) -> str:
    """Render inline markdown (code, links, bold, italics) to HTML."""
    out = []
    for chunk in re.split(r"(`[^`]+`)", text):
        if chunk.startswith("`") and chunk.endswith("`") and len(chunk) > 2:
            out.append("<code>" + html.escape(chunk[1:-1]) + "</code>")
            continue
        for tok in re.split(r"(\[[^\]]*\]\([^)\s]+\))", chunk):
            m = re.fullmatch(r"\[([^\]]*)\]\(([^)\s]+)\)", tok)
            if m:
                out.append(
                    '<a href="%s">%s</a>'
                    % (html.escape(m.group(2), quote=True), emphasis(m.group(1)))
                )
            else:
                out.append(emphasis(tok))
    return "".join(out)


def emphasis(text: str) -> str:
    out = []
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*)", text):
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            out.append("<strong>" + html.escape(tok[2:-2]) + "</strong>")
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            out.append("<em>" + html.escape(tok[1:-1]) + "</em>")
        else:
            out.append(html.escape(tok))
    return "".join(out)


def _list_item_to_html(raw: str) -> tuple[str, str]:
    """Convert one bullet line to (li attributes, inner HTML). Callers open/close <li>."""
    m = re.match(r"^[-*]\s+(.*)$", raw)
    if m:
        body = m.group(1)
        if body.startswith("[ ] "):
            return ' class="pace"', inline(body[4:])
        if body.startswith("[x] "):
            return ' class="pace done"', inline(body[4:])
        return "", inline(body)
    m = re.match(r"^\d+\.\s+(.*)$", raw)
    if m:
        return "", inline(m.group(1))
    return "", inline(raw)


def _list_kind(raw: str) -> str | None:
    if re.match(r"^[-*]\s+\S", raw):
        return "ul"
    if re.match(r"^\d+\.\s+\S", raw):
        return "ol"
    return None


def markdown_to_html(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    para: list[str] = []
    quote: list[str] = []
    table: list[list[str]] | None = None
    list_kind: str | None = None
    li_open = False
    list_blank = False
    code: list[str] | None = None

    def close_li():
        nonlocal li_open
        if li_open:
            out.append("</li>")
            li_open = False

    def flush_list():
        nonlocal list_kind, list_blank
        close_li()
        if list_kind:
            out.append("</%s>" % list_kind)
            list_kind = None
        list_blank = False

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []

    def flush_quote():
        nonlocal quote
        if quote:
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            quote = []

    def flush_table():
        nonlocal table
        if table:
            head, *rows = table
            parts = ["<table><thead><tr>"]
            parts += ["<th>" + inline(c) + "</th>" for c in head]
            parts.append("</tr></thead><tbody>")
            for row in rows:
                parts.append("<tr>" + "".join("<td>" + inline(c) + "</td>" for c in row) + "</tr>")
            parts.append("</tbody></table>")
            out.append("".join(parts))
            table = None

    def flush_all():
        flush_para()
        flush_quote()
        flush_table()
        flush_list()

    def is_table_separator(cells: list[str]) -> bool:
        return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)

    for line in lines:
        stripped = line.rstrip()

        if code is not None:
            if stripped.startswith("```") and len(stripped) < 7:
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = None
            else:
                code.append(line)
            continue

        if stripped.startswith("```"):
            flush_all()
            code = []
            continue

        # table rows
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            if is_table_separator(cells):
                continue  # header/body separator: parsed implicitly, never rendered
            if len(cells) >= 2:
                flush_quote()
                if table is None:
                    flush_para()
                    flush_list()
                    table = [cells]
                else:
                    table.append(cells)
                continue

        flush_table()

        if stripped == "":
            flush_para()
            flush_quote()
            if li_open:
                list_blank = True  # a blank may separate <li> paragraphs or end the list
            continue

        if stripped == "---":
            flush_all()
            out.append("<hr>")
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            flush_all()
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level))
            continue

        if stripped.startswith(">"):
            flush_para()
            flush_list()
            quote.append(stripped.lstrip(">").strip())
            continue

        kind = _list_kind(stripped)
        if kind:
            flush_para()
            flush_quote()
            if list_kind != kind:
                flush_list()
                out.append("<%s>" % kind)
                list_kind = kind
            elif li_open:
                close_li()
            list_blank = False
            attrs, body = _list_item_to_html(stripped)
            out.append("<li%s>%s" % (attrs, body))
            li_open = True
            continue

        # lazy continuation of an open list item (wrapped or indented text,
        # with no intervening blank line)
        if list_kind and li_open and not list_blank:
            out.append(inline(stripped.strip()))
            continue

        flush_list()
        para.append(stripped)

    flush_para()
    flush_quote()
    flush_table()
    flush_list()
    return "\n".join(out)


# ------------------------------------------------------------------ build


class Page:
    def __init__(self, filename: str, nav: str, blurb: str, title: str, body_html: str):
        self.filename = filename
        self.slug = filename[:-3]  # strip .md
        self.nav = nav
        self.blurb = blurb
        self.title = title
        self.body_html = body_html


def load_pages() -> list[Page]:
    pages = []
    for filename, nav, blurb in PAGES:
        path = DOCS_DIR / filename
        if not path.exists():
            raise BuildError("missing document: docs/%s" % filename)
        md = path.read_text(encoding="utf-8")
        m = re.match(r"^#\s+(.+)$", md, re.M)
        if not m:
            raise BuildError("docs/%s has no '# Title' heading" % filename)
        title = m.group(1).strip()
        pages.append(Page(filename, nav, blurb, title, markdown_to_html(md)))
    return pages


def page_shell(pages: list[Page], page: Page, body: str) -> str:
    idx = pages.index(page)
    nav_items = ['<a href="index.html">Home</a>'] + [
        '<a href="%s.html">%s</a>' % (p.slug, p.nav) for p in pages
    ]
    prev_html = next_html = ""
    if idx > 0:
        prev_html = '<a href="%s.html"><span>Previous</span>%s</a>' % (
            pages[idx - 1].slug, html.escape(pages[idx - 1].title))
    if idx < len(pages) - 1:
        next_html = '<a class="next" href="%s.html"><span>Next</span>%s</a>' % (
            pages[idx + 1].slug, html.escape(pages[idx + 1].title))
    return PAGE_TMPL % dict(
        title=html.escape(page.title),
        desc=html.escape(SITE_TAGLINE, quote=True),
        brand=SITE_TITLE,
        tagline=html.escape(SITE_TAGLINE),
        nav=" ".join(nav_items),
        body=body,
        prev=prev_html,
        next=next_html,
        footer=FOOTER,
    )


PAGE_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s · %(brand)s</title>
<meta name="description" content="%(desc)s">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">%(brand)s</a>
    <p class="tagline">%(tagline)s</p>
    <nav class="nav">%(nav)s</nav>
  </div>
</header>
<main>
  <div class="wrap">
    <article>
%(body)s

<nav class="pager">%(prev)s%(next)s</nav>
    </article>
  </div>
</main>
<footer><div class="wrap"><p>%(footer)s</p></div></footer>
</body>
</html>
"""

INDEX_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(brand)s</title>
<meta name="description" content="%(desc)s">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">%(brand)s</a>
    <p class="tagline">%(tagline)s</p>
    <nav class="nav"><a href="00-start-here.html">Start Here</a><a href="05-fee-math.html">Fee Math</a><a href="launch-checklist.html">Checklist</a><a href="glossary.html">Glossary</a></nav>
  </div>
</header>
<main>
  <div class="wrap">
    <section class="hero">
%(intro)s
    </section>
    <section>
      <div class="cards">
%(cards)s
      </div>
      <div class="note">
%(outro)s
      </div>
    </section>
  </div>
</main>
<footer><div class="wrap"><p>%(footer)s</p></div></footer>
</body>
</html>
"""


def render_index(pages: list[Page]) -> str:
    cards = []
    for p in pages:
        cards.append(
            '<a class="card" href="%s.html"><span class="num">%s</span>'
            '<span class="t">%s</span><span class="d">%s</span></a>'
            % (p.slug, html.escape(p.nav), html.escape(p.title), html.escape(p.blurb))
        )
    return INDEX_TMPL % dict(
        brand=SITE_TITLE,
        desc=html.escape(SITE_TAGLINE, quote=True),
        tagline=html.escape(SITE_TAGLINE),
        intro=markdown_to_html(HOME_INTRO),
        cards="\n".join(cards),
        outro=markdown_to_html(HOME_OUTRO),
        footer=FOOTER,
    )


def find_bad_links(pages: list[Page], out_dir: Path) -> list[str]:
    """Internal links in generated HTML must resolve to files we generate."""
    bad = []
    wanted = {"index.html", "styles.css"} | {p.slug + ".html" for p in pages}
    rendered = [("index.html", render_index(pages))]
    rendered += [(p.slug + ".html", page_shell(pages, p, p.body_html)) for p in pages]
    for name, content in rendered:
        for href in re.findall(r'(?:href|src)="([^"]+)"', content):
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = href.split("#")[0]
            if path and (path not in wanted or not (out_dir / path).exists()):
                bad.append("%s -> %s" % (name, href))
    return bad


def validate(pages: list[Page], out_dir: Path | None) -> list[str]:
    errors = []
    by_filename = {p.filename for p in pages}
    docfiles = {p.name for p in DOCS_DIR.glob("*.md")}
    for extra in sorted(docfiles - by_filename):
        errors.append("docs/%s is not listed in build.py PAGES" % extra)
    for page in pages:
        if page.title.lower() in {"", "untitled", "title"}:
            errors.append("docs/%s has a placeholder title" % page.filename)
    if out_dir is not None:
        bad_links = find_bad_links(pages, out_dir)
        errors += bad_links
        index_pages = {p.slug for p in pages}
        for slug in re.findall(r'class="card" href="([a-z0-9-]+)\.html"', render_index(pages)):
            index_pages.discard(slug)
        if index_pages:
            errors.append("index page missing cards for: %s" % ", ".join(sorted(index_pages)))
    return errors


def build(out_dir: Path) -> None:
    pages = load_pages()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "styles.css").write_text(CSS, encoding="utf-8")
    (out_dir / "index.html").write_text(render_index(pages), encoding="utf-8")
    for p in pages:
        (out_dir / (p.slug + ".html")).write_text(
            page_shell(pages, p, p.body_html), encoding="utf-8")

    errors = validate(pages, out_dir)
    if errors:
        for e in errors:
            print("BUILD ERROR: " + e, file=sys.stderr)
        raise BuildError("%d validation error(s); site not trusted" % len(errors))

    print("Built %d pages into %s" % (len(pages) + 1, out_dir))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    parser.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = parser.parse_args(argv)

    out_dir = Path(args.out).resolve()
    try:
        if args.check:
            pages = load_pages()
            errors = validate(pages, None)
            if errors:
                for e in errors:
                    print("BUILD ERROR: " + e, file=sys.stderr)
                return 1
            print("Docs check passed (%d pages)." % len(pages))
            return 0
        build(out_dir)
        return 0
    except BuildError as exc:
        print("BUILD FAILED: %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
