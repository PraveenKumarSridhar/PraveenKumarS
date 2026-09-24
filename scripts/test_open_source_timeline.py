#!/usr/bin/env python3
"""Check the rendered contribution timeline and its append-only authoring path."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


BUILD = Path(sys.argv.pop(1)).resolve()
ROOT = Path(__file__).resolve().parent.parent


class Timeline(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.inside = False
        self.current = None
        self.entries = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("id") == "open-source":
            self.inside = True
        elif self.inside and tag == "article":
            self.current = {"date": None, "text": "", "links": []}
        elif self.current is not None and tag == "time":
            self.current["date"] = attrs.get("datetime")
        elif self.current is not None and tag == "a":
            self.current["links"].append(attrs.get("href"))

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "article" and self.current is not None:
            self.entries.append(self.current)
            self.current = None
        elif tag == "section" and self.inside:
            self.inside = False


class OpenSourceTimelineTests(unittest.TestCase):
    def test_rendered_entries_follow_pr_events_newest_first(self):
        entries = Timeline((BUILD / "index.html").read_text()).entries
        self.assertEqual(
            [entry["date"] for entry in entries],
            ["2026-09-24", "2026-09-10", "2026-08-04", "2026-07-21"],
        )
        self.assertEqual(len(entries), 4)
        self.assertIn("Hindsight", entries[0]["text"])
        self.assertIn("Merged", entries[2]["text"])
        self.assertEqual(entries[0]["links"], ["https://github.com/vectorize-io/hindsight/pull/4745"])

    def test_newer_data_entry_appears_first_without_template_edit(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            output = Path(temporary) / "site"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "node_modules", "_site", ".artifacts"))
            data_file = source / "_data" / "contributions.yml"
            with data_file.open("a") as stream:
                stream.write("\n- date: '2026-10-01'\n  project: Test Engine\n  title: Preserve result IDs\n  description: Keeps result IDs available after parsing.\n  outcome: Submitted\n  pr: '#99'\n  url: https://github.com/example/test-engine/pull/99\n")
            subprocess.run(["bash", str(source / "scripts/build_site.sh"), str(output)], check=True, stdout=subprocess.DEVNULL)
            entries = Timeline((output / "index.html").read_text()).entries
            self.assertEqual(entries[0]["date"], "2026-10-01")
            self.assertIn("Test Engine", entries[0]["text"])
            self.assertEqual(entries[0]["links"], ["https://github.com/example/test-engine/pull/99"])
            self.assertEqual(len(entries), 5)


if __name__ == "__main__":
    unittest.main()
