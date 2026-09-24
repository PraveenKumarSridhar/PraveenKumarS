#!/usr/bin/env python3
"""Exercise the local preview command through its HTTP response."""
import select
import subprocess
import sys
import time
import unittest
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / "scripts" / "preview_site.py"


class PreviewSiteTests(unittest.TestCase):
    def test_source_directory_is_rejected(self):
        result = subprocess.run(
            [sys.executable, str(PREVIEW), "--site-dir", str(ROOT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rendered Jekyll site", result.stderr)

    def test_preview_builds_and_serves_rendered_homepage(self):
        process = subprocess.Popen(
            [sys.executable, str(PREVIEW), "--port", "0"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        try:
            deadline = time.monotonic() + 45
            url = None
            while time.monotonic() < deadline and process.poll() is None:
                if select.select([process.stdout], [], [], 1)[0]:
                    line = process.stdout.readline().strip()
                    if line.startswith("Preview: "):
                        url = line.removeprefix("Preview: ")
                        break
            self.assertIsNotNone(url, "preview did not publish a local URL")
            with urlopen(url, timeout=5) as response:
                html = response.read().decode("utf-8")
            self.assertTrue(html.lstrip().lower().startswith("<!doctype html>"))
            self.assertIn('id="open-source"', html)
            self.assertNotIn("{% seo", html)
            self.assertNotIn("layout: null", html)
        finally:
            process.terminate()
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()


if __name__ == "__main__":
    unittest.main()
