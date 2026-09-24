#!/usr/bin/env python3
"""Prove future articles enter the real build, index, sitemap and feed automatically."""
from pathlib import Path
from datetime import datetime, timedelta
import sys
import xml.etree.ElementTree as ET
import shutil
import subprocess
import tempfile
from check_site import check_site

source = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='pk-article-', dir='/tmp') as tmp:
    root = Path(tmp)
    fixture = root / 'source'
    shutil.copytree(source, fixture, ignore=shutil.ignore_patterns('.git', '.superpowers', '.artifacts', 'node_modules', '_site', '__pycache__'))
    (fixture / '_notes/future-article-fixture.md').write_text('''---
title: "Fixture: memory & retrieval"
description: "A temporary technical publishing fixture, never a published article."
date: 2026-09-22
tags: [testing]
---

An arbitrary opening paragraph. No prescribed editorial structure.

## A section

A [link to the Notes index](/notes/).
''')
    output = root / 'site'
    subprocess.run(['bash', str(fixture / 'scripts/build_site.sh'), str(output)], check=True)
    errors, pages = check_site(output, fixture)
    assert not errors, errors
    route = '/notes/future-article-fixture/'
    assert route in pages
    index = output / 'notes/index.html'
    index.write_text(index.read_text().replace('href="' + route + '"', 'href="/notes/"'))
    assert any('article absent from Notes index: ' + route in e for e in check_site(output, fixture)[0])
    (output / route.lstrip('/') / 'index.html').unlink()
    assert any('source article absent from build: ' + route in e for e in check_site(output, fixture)[0])
    print('PASS: new article renders with metadata, index, sitemap and feed; missing page and index-link failures detected.')

    # Use a date newer than the actual feed, so this stays meaningful as the site grows.
    original_feed = ET.parse(output / 'feed.xml')
    entries = original_feed.findall('{*}entry')
    previous_feed_urls = {entry.find('{*}link').attrib['href'] for entry in entries}
    newest = max(datetime.fromisoformat(entry.find('{*}published').text.replace('Z', '+00:00')) for entry in entries)
    rollover_date = (newest + timedelta(days=1)).date().isoformat()
    # Cross the feed limit with same-day articles; sitemap/index/llms must retain every note.
    for i in range(11):
        (fixture / '_notes' / f'feed-fixture-{i:02d}.md').write_text(f'---\ntitle: "Feed fixture {i}"\ndescription: "Unique temporary feed fixture {i}."\ndate: {rollover_date}\ntags: [testing]\n---\nBody.\n')
    subprocess.run(['bash', str(fixture / 'scripts/build_site.sh'), str(output)], check=True)
    errors, pages = check_site(output, fixture)
    assert not errors, errors
    source_routes = {'/notes/' + path.stem + '/' for path in (fixture / '_notes').iterdir() if path.suffix in ('.md', '.markdown')}
    built_routes = {route for route in pages if route.startswith('/notes/') and route != '/notes/'}
    assert built_routes == source_routes, (built_routes, source_routes)
    new_entries = ET.parse(output / 'feed.xml').findall('{*}entry')
    new_feed_urls = {entry.find('{*}link').attrib['href'] for entry in new_entries}
    assert len(new_feed_urls) == 10
    assert not previous_feed_urls & new_feed_urls, 'Older articles should have rotated out of the feed'
    # Run the corruption suite against the grown site too: its mutations must not depend
    # on a particular article still being present in the newest-ten feed.
    subprocess.run([sys.executable, str(fixture / 'scripts/test_site_checks.py'), str(output)], check=True)
    print(f'PASS: {len(source_routes)} notes retained in index/sitemap/llms; older feed entries rotate out; regression suite passes on expanded site.')
