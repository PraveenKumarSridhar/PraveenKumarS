#!/usr/bin/env python3
"""Prove the validator rejects realistic corruptions of a real generated site."""
from pathlib import Path
import shutil
import json
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from check_site import check_site

BUILD = Path(sys.argv.pop(1)).resolve()


class RegressionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "site"
        shutil.copytree(BUILD, self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def corrupt_home(self, old, new):
        file = self.root / "index.html"
        source = file.read_text()
        self.assertIn(old, source)
        file.write_text(source.replace(old, new, 1))

    def fails_with(self, text):
        errors, _ = check_site(self.root)
        self.assertTrue(any(text in error for error in errors), errors)

    def test_valid_site_passes_including_image_object_override(self):
        self.assertEqual(check_site(self.root)[0], [])

    def test_llms_missing_file(self):
        (self.root / "llms.txt").unlink()
        self.fails_with("llms.txt:")

    def test_llms_missing_article(self):
        file = self.root / "llms.txt"
        file.write_text("\n".join(line for line in file.read_text().splitlines() if '/notes/muse-memory-investigation/' not in line))
        self.fails_with("llms.txt links do not match")

    def test_llms_stale_title(self):
        file = self.root / "llms.txt"
        file.write_text(re.sub(r"^- \[.*?\](\(https://praveenks.com/notes/muse-memory-investigation/\))", r"- [Stale title]\1", file.read_text(), flags=re.M))
        self.fails_with("llms.txt title mismatch")

    def mutate_schema(self, route, kind, change):
        file = self.root / route / "index.html"
        def edit(match):
            obj = json.loads(match.group(1))
            return '<script type="application/ld+json">' + json.dumps(change(obj) if obj.get("@type") == kind else obj) + '</script>'
        file.write_text(re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', edit, file.read_text(), flags=re.S))

    def test_conflicting_person_identity_is_rejected(self):
        self.mutate_schema("", "Person", lambda x: dict(x, **{"@id": "https://example.com/person"}))
        self.fails_with("conflicting Person identity")

    def test_wrong_article_author_is_rejected(self):
        self.mutate_schema("notes/agent-memory-needs-a-point-of-view", "BlogPosting", lambda x: dict(x, author={"url": "https://example.com/person"}))
        self.fails_with("author identity mismatch")

    def test_breadcrumb_mismatch_is_rejected(self):
        self.mutate_schema("notes/agent-memory-needs-a-point-of-view", "BreadcrumbList", lambda x: dict(x, itemListElement=[]))
        self.fails_with("breadcrumb schema mismatch")

    def test_modification_before_publication_is_rejected(self):
        self.mutate_schema("notes/agent-memory-needs-a-point-of-view", "BlogPosting", lambda x: dict(x, dateModified="2020-01-01T00:00:00+00:00"))
        self.fails_with("modification predates publication")

    def test_duplicate_identity_is_rejected(self):
        self.corrupt_home('</head>', '<script type="application/ld+json">{"@type":"Person"}</script></head>')
        self.fails_with("expected one Person identity")

    def test_missing_old_note_is_rejected(self):
        (self.root / "notes/agent-memory-needs-a-point-of-view/index.html").unlink()
        self.fails_with("missing baseline route")

    def test_broken_internal_link_is_rejected(self):
        self.corrupt_home('</body>', '<a href="/missing-page/">Missing</a></body>')
        self.fails_with("broken local reference")

    def test_broken_fragment_is_rejected(self):
        self.corrupt_home('</body>', '<a href="/notes/#not-an-id">Missing</a></body>')
        self.fails_with("missing fragment")

    def test_wrong_canonical_is_rejected(self):
        self.corrupt_home('rel="canonical" href="https://praveenks.com/"', 'rel="canonical" href="http://localhost/"')
        self.fails_with("wrong/duplicate canonical")

    def test_duplicate_canonical_is_rejected(self):
        self.corrupt_home('</head>', '<link rel="canonical" href="https://praveenks.com/" /></head>')
        self.fails_with("wrong/duplicate canonical")

    def test_invalid_json_is_rejected(self):
        self.corrupt_home('<script type="application/ld+json">', '<script type="application/ld+json">BROKEN')
        self.fails_with("invalid HTML/JSON-LD")

    def test_noindex_is_rejected(self):
        self.corrupt_home('</head>', '<meta name="robots" content="noindex" /></head>')
        self.fails_with("blocks indexing")

    def test_raw_front_matter_is_rejected(self):
        self.corrupt_home('<!DOCTYPE html>', '---\nlayout: null\n---\n<!DOCTYPE html>')
        self.fails_with("raw front matter")

    def test_private_plan_leak_is_rejected(self):
        (self.root / "docs").mkdir()
        (self.root / "docs/plan.md").write_text("Private plan")
        self.fails_with("private/development file published")

    def test_missing_existing_note_in_feed_is_rejected(self):
        file = self.root / "feed.xml"
        tree = ET.parse(file)
        feed = tree.getroot()
        entries = feed.findall("{*}entry")
        self.assertTrue(entries, "The built feed must contain an entry to remove")
        feed.remove(entries[0])
        tree.write(file, encoding="unicode", xml_declaration=True)
        self.fails_with("feed does not match newest notes")

    def test_body_svg_title_does_not_corrupt_head_title(self):
        self.corrupt_home('</body>', '<svg><title>Chart title</title></svg></body>')
        self.assertEqual(check_site(self.root)[0], [])


if __name__ == "__main__":
    unittest.main()
