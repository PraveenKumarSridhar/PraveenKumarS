#!/usr/bin/env python3
"""Build real collection edge cases without altering the author's notes."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parent.parent


class Writing(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.section = False
        self.card = False
        self.heading = False
        self.titles = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id') == 'writing':
            self.section = True
        if tag == 'a' and 'writing-card' in attrs.get('class', '').split():
            self.card = True
            self.links.append(attrs.get('href'))
        if self.card and tag == 'h3':
            self.heading = True
            self.titles.append('')

    def handle_data(self, text):
        if self.heading:
            self.titles[-1] += text

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.heading = False
        if tag == 'a':
            self.card = False


with tempfile.TemporaryDirectory(prefix='pk-writing-', dir='/tmp') as tmp:
    root = Path(tmp)
    source = root / 'source'
    shutil.copytree(SOURCE, source, ignore=shutil.ignore_patterns('.git', '.superpowers', 'node_modules', '_site', '.artifacts', '__pycache__'))
    notes = source / '_notes'
    shutil.rmtree(notes)
    notes.mkdir()
    for count in (0, 1, 4):
        title = 'Memory <systems> & evaluation: ' + 'a-long-technical-title-' * 8
        for index in range(count):
            (notes / f'case-{index}.md').write_text(f'---\ntitle: "{title} {index}"\ndescription: "An example with <tags> & quotes."\ndate: 2026-01-0{index+1}\n---\n\n## Example\n\nA synthetic authoring fixture.\n')
        output = root / f'output-{count}'
        result = subprocess.run(['bash', str(source / 'scripts/build_site.sh'), str(output)], capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
        page = Writing((output / 'index.html').read_text())
        expected = list(range(count - 1, max(-1, count - 4), -1))
        assert page.section == (count > 0), (count, 'empty writing section')
        assert page.links == [f'/notes/case-{i}/' for i in expected], (count, page.links)
        assert page.titles == [f'{title} {i}' for i in expected], (count, 'escaped title or ordering failed')
        for href in page.links:
            assert (output / href.lstrip('/') / 'index.html').is_file(), href
        print(f'PASS: {count} notes, {len(page.links)} real homepage links, escaped titles, newest first')
    # The four-note build also exercises pathological title lengths in the real responsive templates.
    subprocess.run(['node', str(SOURCE / 'scripts/check_browser.cjs'), str(output), str(SOURCE / '.artifacts/writing-fixtures')], check=True)
