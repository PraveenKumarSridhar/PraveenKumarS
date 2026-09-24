# Publishing an article

## Flow

1. Write and iterate outside `_notes` until the article is ready for review.
2. Add `_notes/your-article-slug.md` on a branch. Keep files directly in `_notes`, without subdirectories or other file formats. Keep the slug stable after publication.
3. Open a pull request. The `Site checks` workflow runs automatically on PR updates and main pushes.
4. Review the article and CI screenshots. Fix failing checks before merging.
5. After merge, verify the live article, Notes listing and social preview. Search Console discovery/indexing can lag deployment.

## Required front matter

```yaml
---
title: "Your article title"
description: "An accurate summary of this article."
date: YYYY-MM-DD
tags: [topic]
---
```

Replace the placeholders before running checks. Add the article body below the closing delimiter. The shared template supplies the page H1, author, navigation, breadcrumbs, canonical URL and social metadata. Use H2/H3 headings in the body when useful. No required opening, TL;DR, section sequence, word count or keyword density.

Optional fields:

- `last_modified_at: YYYY-MM-DD` for a substantive revision, never automatically set to today's date.
- `image: /assets/your-image.png`, or an image mapping with `path` and `alt`. Omit the field to use the existing default social card. Empty overrides fail.

Images in the body need alt attributes and existing local files. Decorative images may use empty alt text. Descriptive alt text quality is a human review task.

## What fails CI

| Stage | Rejected conditions |
| --- | --- |
| Source contract | Missing/duplicate YAML fields, empty title/description/body, invalid dates, update before publication, invalid tags or slug, duplicate route, bypassing shared layout or publication settings |
| Image preflight | Empty/malformed social-image override or missing local asset |
| Generated output | Source article absent from build/index; duplicate metadata; wrong canonical; missing author/article/breadcrumb schema; inconsistent dates/headline/image; multiple H1s; broken internal links/fragments/assets; missing image alt attributes; accidental noindex |
| Discovery | Missing sitemap entry; incorrect newest-ten feed coverage; blocked robots policy |
| Browser | Chromium and WebKit mobile clipping/overflow, hidden navigation/content, broken writing button, failed images, JavaScript errors, obscured table-of-contents targets, inaccessible table scrolling |

The source contract rejects `permalink`, `canonical_url`, `published`, `draft`, and `sitemap` overrides. These can silently alter the route or discoverability, and Jekyll collections do not share every post-draft behavior. Keep unfinished writing outside `_notes`; handle genuine route/indexing exceptions as an explicit reviewed change to the contract.

Tests discover new note files and generated pages automatically. A temporary fixture article exercises the entire build and proves that losing its output or index link is detected. Fixtures never enter the actual site's source or deployment.

## Run locally

```sh
bash scripts/build_site.sh /tmp/article-preview
python3 scripts/check_site.py /tmp/article-preview
python3 scripts/test_site_checks.py /tmp/article-preview
python3 scripts/test_new_article.py
node scripts/check_browser.cjs /tmp/article-preview .artifacts/browser
SITE_BROWSER=webkit node scripts/check_browser.cjs /tmp/article-preview .artifacts/browser/webkit
```

The build runs the Ruby contract tests, validates note metadata/images, then builds Jekyll. It uses the pinned Pages container, so no new local Ruby dependency is needed. CI uploads screenshots for 14 days.

## What remains human

Argument, voice, factual support, originality, permission to publish and whether the piece is worth reading. A green check does not approve editorial content, verify every external source, or guarantee indexing/ranking.

Repository merge enforcement is a separate GitHub setting. The workflow exposes the `site` status check. Require that check in the main-branch rules to prevent merging failures; it is not enforced merely by adding this file.

## AI-readable index

`/llms.txt` is generated at build time from the existing site description and every published note’s title, description and canonical URL, newest first. It links to the existing HTML articles. No manual duplicate list is needed. CI checks coverage, titles and nonempty descriptions, including the temporary new-article and seventeen-note fixtures. This optional index does not change crawler permissions or guarantee AI citations.
