#!/usr/bin/env python3
"""Tests for the Mini-Course Author Guide build.

Run with:  python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

LICENSE_TEXT = """\
MIT License

Copyright (c) 2026 Asdale Dynamics, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def build_into_tmp():
    tmp = tempfile.TemporaryDirectory()
    out = Path(tmp.name) / "site"
    build.build(out)
    return tmp, out


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp, cls.out = build_into_tmp()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_index_and_all_pages_exist(self):
        names = {p.name for p in self.out.iterdir()}
        expected = {"index.html", "styles.css"} | {(f[:-3] + ".html") for f, _, _ in build.PAGES}
        for name in expected:
            self.assertIn(name, names, "missing site file: %s" % name)

    def test_pages_are_well_formed_html(self):
        for page in build.PAGES:
            text = (self.out / (page[0][:-3] + ".html")).read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", text)
            self.assertIn("</html>", text)
            self.assertIn("<h1>", text)
            self.assertIn("<title>", text)
            self.assertNotIn("<h6", text)  # parser only emits h1-h4

    def test_internal_links_resolve(self):
        self.assertEqual(build.find_bad_links(build.load_pages(), self.out), [])

    def test_index_links_every_page(self):
        index = (self.out / "index.html").read_text(encoding="utf-8")
        for page in build.load_pages():
            self.assertIn('href="%s.html"' % page.slug, index)

    def test_nav_links_every_page(self):
        for page in build.load_pages():
            rendered = (self.out / (page.slug + ".html")).read_text(encoding="utf-8")
            for other in build.load_pages():
                if other is not page:
                    self.assertIn('href="%s.html"' % other.slug, rendered,
                                  "%s nav should link %s" % (page.slug, other.slug))

    def test_prev_next_pager(self):
        first = build.load_pages()[0]
        rendered = (self.out / (first.slug + ".html")).read_text(encoding="utf-8")
        self.assertIn('<nav class="pager"><a class="next"', rendered)
        self.assertNotIn("<span>Previous</span>", rendered)
        last = build.load_pages()[-1]
        rendered = (self.out / (last.slug + ".html")).read_text(encoding="utf-8")
        self.assertIn("<span>Previous</span>", rendered)
        self.assertNotIn('class="next"', rendered)

    def test_no_unfilled_blanks_outside_template(self):
        # Pages where blanks are the artifact itself (fill-in forms, drafts, quotes.)
        skip = {"lesson-template", "01-promise-sized-lesson", "launch-checklist",
                "07-drip-announcements", "glossary"}
        for page in build.load_pages():
            if page.slug in skip:
                continue
            text = (self.out / (page.slug + ".html")).read_text(encoding="utf-8")
            self.assertNotIn("____", text, "%s still has unfilled blanks" % page.slug)

    def test_glossary_defines_key_terms(self):
        text = (self.out / "glossary.html").read_text(encoding="utf-8")
        terms = ["Drip", "Marketplace (storefront-builder)", "Mini-course",
                 "Printable", "Promise-sized lesson", "Refund window", "Self-hosted"]
        for term in terms:
            self.assertIn(term, text, "glossary missing term: %s" % term)
        # glossary defines at least 15 terms (bold paragraph entries)
        self.assertGreaterEqual(text.count("<strong"), 15)

    def test_checklist_renders_checkboxes(self):
        text = (self.out / "launch-checklist.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count('class="pace"'), 40)

    def test_fee_math_tables_render(self):
        text = (self.out / "05-fee-math.html").read_text(encoding="utf-8")
        self.assertIn("<table>", text)
        self.assertIn("$47.28", text)
        self.assertIn("$44.10", text)

    def test_no_placeholder_todo_left(self):
        for path in self.out.iterdir():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertNotIn("lorem ipsum", text.lower())

    def test_no_secrets_in_sources_or_site(self):
        secret_patterns = re.compile(
            r"(sk-[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{16}|api[_-]?key\s*[:=]\s*\S{8,}|"
            r"BEGIN (RSA |EC )?PRIVATE KEY)", re.I)
        for path in [self.out, ROOT / "docs", ROOT / "tests", ROOT / "build.py", ROOT / "README.md"]:
            if path.is_file():
                candidates = [path]
            elif path.is_dir():
                candidates = [c for c in path.rglob("*") if c.is_file()]
            else:
                candidates = []
            for c in candidates:
                text = c.read_text(encoding="utf-8", errors="ignore")
                self.assertIsNone(secret_patterns.search(text), "possible secret in %s" % c)


class SourceTests(unittest.TestCase):
    def test_license_exact_copyright_line(self):
        self.assertEqual((ROOT / "LICENSE").read_text(encoding="utf-8"), LICENSE_TEXT)

    def test_readme_credits_asdale(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)

    def test_docs_cover_all_chapters(self):
        """Every chapter promised on the napkin exists in docs/."""
        required = [
            "00-start-here.md", "01-promise-sized-lesson.md", "02-outline-at-pace.md",
            "03-record-without-fancy-gear.md", "04-lesson-pages-and-printables.md",
            "05-fee-math.md", "06-refunds-with-grace.md", "07-drip-announcements.md",
            "lesson-template.md", "launch-checklist.md", "glossary.md",
        ]
        for name in required:
            self.assertTrue((ROOT / "docs" / name).exists(), "missing docs/%s" % name)


class CliTests(unittest.TestCase):
    def test_cli_builds_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "build.py"), "--out", tmp],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("Built", proc.stdout)

    def test_cli_check_exits_zero(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "build.py"), "--check"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_cli_check_fails_on_broken_doc(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = ROOT / "docs"
            probe = docs / "zz-probe.md"
            probe.write_text("body without a title\n", encoding="utf-8")
            try:
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "build.py"), "--check"],
                    capture_output=True, text=True, cwd=str(ROOT),
                )
                self.assertEqual(proc.returncode, 1)
                self.assertIn("BUILD ERROR", proc.stderr)
            finally:
                probe.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
