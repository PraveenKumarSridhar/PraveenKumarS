#!/usr/bin/env python3
"""Check the generated Pages site, not its Liquid source. Standard library only."""
import argparse
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
import json
import re
from html import unescape
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ORIGIN = "https://praveenks.com"
BASELINE_ROUTES = {
    "/", "/notes/", "/notes/agent-memory-needs-a-point-of-view/",
    "/notes/honcho-vs-mem0-two-memory-layers-two-architectures/",
    "/notes/when-competence-attacks-its-measurement/",
    "/notes/from-honcho-to-hindsight/", "/notes/muse-memory-investigation/",
}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.in_head = self.in_title = self.in_json = False
        self.title = ""
        self.h1 = ""
        self.in_h1 = False
        self.title_count = self.h1_count = 0
        self.meta = {}
        self.canonicals, self.refs, self.ids, self.schemas = [], [], [], []
        self.missing_alt = 0
        self.json_text = ""
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.append(a["name"])
        if tag == "head":
            self.in_head = True
        if tag == "title" and self.in_head:
            self.in_title = True
            self.title_count += 1
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
        if tag == "meta" and self.in_head:
            key = a.get("name", a.get("property", "")).lower()
            self.meta.setdefault(key, []).append(a.get("content", ""))
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonicals.append(a.get("href", ""))
        if tag in ("a", "link") and a.get("href"):
            self.refs.append(a["href"])
        if tag in ("img", "script", "source") and a.get("src"):
            self.refs.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.missing_alt += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_json = True
            self.json_text = ""

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.in_head = False
        if tag == "script" and self.in_json:
            self.schemas.append(json.loads(self.json_text))
            self.in_json = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1 += data
        if self.in_title:
            self.title += data
        if self.in_json:
            self.json_text += data


def route_for(path):
    value = "/" + path.as_posix()
    return value[:-10] if value.endswith("index.html") else value


def check_site(root, source_root=None):
    root = root.resolve()
    source_root = source_root or Path(__file__).resolve().parent.parent
    errors, pages, titles, descriptions = [], {}, [], []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def local_file(url):
        path = root / unquote(urlsplit(url).path).lstrip("/")
        if not path.resolve().is_relative_to(root):
            return None
        return path / "index.html" if path.is_dir() else path

    for name in ("docs", "scripts", "tests", "examples", "node_modules", "package.json", "package-lock.json", "README.md"):
        check(not (root / name).exists(), f"private/development file published: {name}")
    for path in sorted(root.rglob("*.html")):
        route = route_for(path.relative_to(root))
        try:
            source = path.read_text()
            check(source.lstrip().lower().startswith(("<!doctype html", "<html")), f"{route}: raw front matter or invalid document start")
            check("{% seo" not in source and "{{ site." not in source, f"{route}: unrendered Liquid")
            pages[route] = Page(source)
        except (ValueError, UnicodeError) as error:
            errors.append(f"{route}: invalid HTML/JSON-LD: {error}")
    for route in sorted(BASELINE_ROUTES - pages.keys()):
        errors.append(f"missing baseline route: {route}")

    source_routes = {"/notes/" + path.stem + "/" for pattern in ("*.md", "*.markdown") for path in (source_root / "_notes").glob(pattern)}
    for route in sorted(source_routes):
        check(route in pages, f"source article absent from build: {route}")
    if "/notes/" in pages:
        index_links = {urljoin(ORIGIN + "/notes/", ref) for ref in pages["/notes/"].refs}
        for route in sorted(source_routes):
            check(ORIGIN + route in index_links, f"article absent from Notes index: {route}")

    for route, page in pages.items():
        canonical = ORIGIN + route
        check(page.title_count == 1 and bool(page.title.strip()), f"{route}: needs one nonempty head title")
        check(page.h1_count == 1, f"{route}: expected one H1, got {page.h1_count}")
        check(page.canonicals == [canonical], f"{route}: wrong/duplicate canonical: {page.canonicals}")
        for key in ("description", "og:title", "og:description", "og:url", "og:image", "twitter:card", "twitter:title", "twitter:image"):
            values = page.meta.get(key, [])
            check(len(values) == 1 and bool(values[0].strip()), f"{route}: missing/duplicate/empty {key}")
        check(page.meta.get("og:url") == [canonical], f"{route}: og:url differs from canonical")
        check(page.meta.get("og:description") == page.meta.get("description"), f"{route}: description differs from OG")
        check(page.meta.get("og:image") == page.meta.get("twitter:image"), f"{route}: social images disagree")
        for key in ("robots", "googlebot"):
            check(not any("noindex" in x.lower() for x in page.meta.get(key, [])), f"{route}: {key} blocks indexing")
        titles.append(page.title.strip())
        descriptions.extend(page.meta.get("description", []))
        check(not page.missing_alt, f"{route}: {page.missing_alt} images lack alt attributes")
        check(len(page.ids) == len(set(page.ids)), f"{route}: duplicate HTML IDs")
        check(bool(page.schemas), f"{route}: missing JSON-LD")
        schemas = [node for item in page.schemas for node in (item.get("@graph", [item]) if isinstance(item, dict) else item)]
        check(all(isinstance(s, dict) for s in schemas), f"{route}: schema nodes must be objects")
        schemas = [s for s in schemas if isinstance(s, dict)]
        if route == "/":
            people = [s for s in schemas if s.get("@type") == "Person"]
            check(len(people) == 1, "homepage: expected one Person identity")
            for person in people:
                check(person.get("@id") == ORIGIN + "/#person" and person.get("url") == ORIGIN + "/", "homepage: conflicting Person identity")
                check(person.get("name") == "Praveen Kumar Sridhar", "homepage: Person name mismatch")
        if route.startswith("/notes/") and route != "/notes/":
            articles = [s for s in schemas if s.get("@type") in ("BlogPosting", "Article")]
            check(len(articles) == 1, f"{route}: expected exactly one article schema")
            crumbs = [s for s in schemas if s.get("@type") == "BreadcrumbList"]
            check(len(crumbs) == 1, f"{route}: expected one breadcrumb schema")
            for crumb in crumbs:
                expected = [(1, "Home", ORIGIN + "/"), (2, "Lab Notes", ORIGIN + "/notes/"), (3, page.h1, canonical)]
                actual = [(x.get("position"), x.get("name"), x.get("item")) for x in crumb.get("itemListElement", []) if isinstance(x, dict)]
                check(actual == expected, f"{route}: breadcrumb schema mismatch")
            for article in articles:
                check(article.get("headline") == page.h1, f"{route}: headline differs from H1")
                check(article.get("author", {}).get("url") == ORIGIN + "/#person", f"{route}: author identity mismatch")
                for field in ("headline", "description", "author", "datePublished", "dateModified", "image", "mainEntityOfPage"):
                    check(bool(article.get(field)), f"{route}: article missing {field}")
                check(article.get("mainEntityOfPage", {}).get("@id") == canonical, f"{route}: article mainEntityOfPage mismatch")
                check(article.get("url") == canonical, f"{route}: article URL mismatch")
                check(article.get("description") in page.meta.get("description", []), f"{route}: article description mismatch")
                image = article.get("image")
                image_url = image.get("url") if isinstance(image, dict) else image
                check(image_url in page.meta.get("og:image", []), f"{route}: article image mismatch")
                try:
                    check(datetime.fromisoformat(article["dateModified"]) >= datetime.fromisoformat(article["datePublished"]), f"{route}: modification predates publication")
                except (KeyError, TypeError, ValueError):
                    errors.append(f"{route}: invalid article date")
        for ref in page.refs + page.meta.get("og:image", []):
            url = urljoin(canonical, ref)
            parts = urlsplit(url)
            if parts.netloc != "praveenks.com" or parts.scheme not in ("http", "https"):
                continue
            target = local_file(url)
            check(target is not None and target.is_file(), f"{route}: broken local reference {ref}")
            if target and target.is_file() and parts.fragment and target.suffix == ".html":
                other = pages.get(route_for(target.relative_to(root)))
                check(other is not None and unquote(parts.fragment) in other.ids, f"{route}: missing fragment {ref}")

    for label, values in (("title", titles), ("description", descriptions)):
        for value, count in Counter(values).items():
            check(count == 1, f"duplicate {label}: {value}")
    try:
        sitemap = ET.parse(root / "sitemap.xml")
        urls = [el.text for el in sitemap.findall(".//{*}loc")]
        check(len(urls) == len(set(urls)), "duplicate sitemap URLs")
        html_urls = {ORIGIN + route for route in pages}
        check(html_urls.issubset(set(urls)), f"pages absent from sitemap: {sorted(html_urls - set(urls))}")
        for url in urls:
            target = local_file(url)
            check(url.startswith(ORIGIN + "/") and target is not None and target.is_file(), f"invalid sitemap URL: {url}")
        feed = ET.parse(root / "feed.xml")
        entries = feed.findall("{*}entry")
        feed_urls = {el.attrib.get("href") for entry in entries for el in entry.findall("{*}link") if el.attrib.get("rel", "alternate") == "alternate"}
        # jekyll-feed 0.17 defaults to ten newest notes; _config.yml leaves this limit unchanged.
        note_routes = [route for route in pages if route.startswith("/notes/") and route != "/notes/"]
        note_routes.sort(key=lambda route: pages[route].meta.get("article:published_time", [""])[0], reverse=True)
        # At the tenth-entry boundary, equally dated notes have no chronological priority.
        cutoff = pages[note_routes[min(9, len(note_routes) - 1)]].meta.get("article:published_time", [""])[0] if note_routes else ""
        required_notes = {ORIGIN + route for route in note_routes if pages[route].meta.get("article:published_time", [""])[0] > cutoff}
        eligible_notes = {ORIGIN + route for route in note_routes if pages[route].meta.get("article:published_time", [""])[0] >= cutoff}
        check(len(feed_urls) == min(10, len(note_routes)) and required_notes <= feed_urls <= eligible_notes,
              "feed does not match newest notes (including date ties at the ten-entry boundary)")
        for url in feed_urls:
            check(url in html_urls, f"feed points to absent page: {url}")
        robots = (root / "robots.txt").read_text()
        check(f"Sitemap: {ORIGIN}/sitemap.xml" in robots, "robots.txt lacks production sitemap")
        check(not any(line.split("#", 1)[0].strip().lower() == "disallow: /" for line in robots.splitlines()), "robots.txt blocks the whole site")
    except (OSError, ET.ParseError, TypeError) as error:
        errors.append(f"sitemap/feed/robots: {error}")
    try:
        llms = (root / "llms.txt").read_text()
        check(llms.startswith("# ") and "\n> " in llms, "llms.txt lacks heading or summary")
        check("{{" not in llms and "{%" not in llms, "llms.txt contains unrendered Liquid")
        entries = re.findall(r"^- \[([^\n]+)\]\((https://[^\s)]+)\)(?:: (.*))?$", llms, re.M)
        urls = [url for _, url, _ in entries]
        expected = {ORIGIN + route for route in pages}
        check(set(urls) == expected and len(urls) == len(expected), "llms.txt links do not match published pages")
        for title, url, description in entries:
            route = url.removeprefix(ORIGIN)
            if route in pages and route.startswith("/notes/") and route != "/notes/":
                check(unescape(title) == pages[route].h1, f"llms.txt title mismatch: {route}")
                check(bool(description.strip()), f"llms.txt missing description: {route}")
    except OSError as error:
        errors.append(f"llms.txt: {error}")
    return errors, {route: {"title": page.title, "description": page.meta.get("description"), "canonical": page.canonicals} for route, page in pages.items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    if not args.site.is_dir():
        parser.error("site output directory does not exist")
    errors, pages = check_site(args.site.resolve(), args.source.resolve())
    if args.report:
        args.report.write_text(json.dumps({"pages": pages, "errors": errors}, indent=2) + "\n")
    for error in errors:
        print("FAIL: " + error, file=sys.stderr)
    print(f"Checked {len(pages)} HTML pages: {len(errors)} failure(s).")
    sys.exit(bool(errors))
