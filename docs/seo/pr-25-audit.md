# PR 25 regression audit

Audited against main `e2af5a25e97dc5ea8eea4bf1bcec883243b5dc08` on 2026-09-23.

## Findings fixed

1. Article preflight only enumerated top-level Markdown. A nested article bypassed validation entirely, returning success with zero notes. The inventory now rejects nested files and unsupported formats, enforcing the documented flat collection. A regression test covers nested Markdown and HTML.
2. In WebKit at 320px, two overflowing article tables did not respond to arrow keys while focused. Shared table containers now handle unmodified left/right arrows. Native pointer/touch scrolling and server-rendered containers remain available.

The image test also raced WebKit lazy loading: `decode()` could reject while a source was being loaded. Tests now wait for completed images with nonzero intrinsic width. macOS WebKit keyboard tests use Option+Tab, the platform's link-navigation shortcut.

## Verification

- Pinned GitHub Pages build succeeds; seven HTML routes.
- All five original articles match main after removing only the two new lazy-image attributes.
- Original homepage hero and introduction retained; no new articles or positioning edits.
- Source contract: nine tests, twenty assertions.
- Output validator: seventeen deliberate-corruption tests.
- Real new-article and seventeen-note feed-rollover fixtures pass.
- Chromium and WebKit: 393 checks each, zero failures locally, at 320/390/768/1440px.
- Browser checks exercise navigation, breadcrumbs, writing button, table-of-contents targets, keyboard focus and horizontal table scrolling, image loading, overflow, no JavaScript and missing IntersectionObserver.
- Generated metadata, structured data, canonical/social URLs, local links/fragments/assets, sitemap/feed and private-file exclusions pass.
- Mobile homepage, Notes index and article screenshots visually inspected. CI retains desktop/mobile screenshots for all routes, including WebKit.
- Main requires the GitHub Actions site check, an up-to-date branch, and applies enforcement to administrators.

## Limits

This verifies the PR build. It has not been merged or deployed. Playwright WebKit is engine coverage, not a physical iPhone/Safari test. External websites and email delivery are not tested, and passing checks cannot establish search ranking or editorial quality. Live deployment smoke checks remain necessary after merge.
