#!/usr/bin/env python3
"""Prove future articles enter the real build, index, sitemap and feed automatically."""
from pathlib import Path
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

    # Cross the feed limit with same-day articles; sitemap/index must still contain all of them.
    for i in range(11):
        (fixture / '_notes' / f'feed-fixture-{i:02d}.md').write_text(f'---\ntitle: "Feed fixture {i}"\ndescription: "Unique temporary feed fixture {i}."\ndate: 2026-09-22\ntags: [testing]\n---\nBody.\n')
    subprocess.run(['bash', str(fixture / 'scripts/build_site.sh'), str(output)], check=True)
    errors, pages = check_site(output, fixture)
    assert not errors, errors
    assert len(pages) == 19, len(pages)
    print('PASS: 17 notes, all indexed/listed, newest-ten feed handles same-day ties.')
