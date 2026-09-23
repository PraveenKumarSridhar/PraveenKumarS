# SEO baseline and verification record

Recorded September 23, 2026. Source baseline: `origin/main` at `e2af5a25e97dc5ea8eea4bf1bcec883243b5dc08`. The button/copy PR #23 is merged; rejected metadata PR #24 is closed and excluded from this branch.

## Before changes

- Seven generated HTML routes: homepage, Notes index, and five notes. All seven pass canonical, unique head title/description, social metadata, JSON-LD, internal link/asset/fragment, and single-H1 checks. Body SVG titles are deliberately excluded from head-title extraction.
- Five notes pass the existing image preflight. The Muse note's JSON-LD uses the supported ImageObject form; the other notes use image URL strings.
- The production homepage, Notes index, robots.txt, sitemap.xml, and feed.xml return HTTP 200. HTTP homepage redirects to HTTPS. A deliberately nonexistent route returns 404.
- The production sitemap contains seven HTML URLs plus the resume PDF. Robots allows crawling and names the HTTPS sitemap.
- `www.praveenks.com` does not resolve. Apex A/AAAA records resolve to GitHub Pages. No DNS changes made by this work.
- Mobile `nav.top` was hidden at widths below 680px. Homepage reveal CSS left 20 content blocks at opacity zero when JavaScript was disabled or IntersectionObserver was unavailable.
- The homepage had no direct article cards. The new browser checks initially reported 50 failed assertions across repeated viewport/page cases, not 50 distinct defects.

## Foundation milestone checks

Commands and toolchain are documented in `README.md`. The pinned Pages build image contains Ruby 3.3.5, Jekyll 3.10.0, and jekyll-seo-tag 2.8.0. Browser tests use Playwright 1.62.1 with its matching Chromium.

| Check | Observed result |
| --- | --- |
| Pages production build and existing image validation | Pass, five notes |
| Generated output audit | Pass, seven HTML pages |
| Validator sensitivity tests | 11 pass, including nine intentional corruptions and SVG-title/ImageObject controls |
| Main browser matrix | 294 assertions pass across all seven pages at 320/390/768/1440px, plus no-JS/missing-observer and actual-font checks |
| Real Jekyll collection fixtures | 0 notes hides the empty section; 1 renders one link; 4 renders newest three; special characters remain text |
| Long-title fixture browser matrix | 258 assertions pass across six synthetic pages |
| Preservation comparison | All five note bodies, metadata and JSON-LD unchanged; homepage capability/impact/work/projects/skills/education/contact body sections unchanged |
| Visual inspection | Desktop and mobile homepage/featured-writing screenshots checked; theme and typography retained, text readable, links visible |

Local screenshots and detailed logs are development artifacts, excluded from publication. CI retains screenshots as a downloadable Actions artifact. The browser matrix blocks analytics, tests missing web fonts, and separately captures the normal loaded fonts. It checks real navigation and visible keyboard focus. It is Chromium coverage, not a claim about every browser or assistive technology.

## Search Console

Authenticated access to the domain property was verified after the user completed setup. The pre-existing HTTP sitemap submission from 2018 was marked “Couldn't fetch”. The current `https://praveenks.com/sitemap.xml` was submitted and then reported **Sitemap processed successfully**, last read September 23, 2026, with eight discovered entries. Discovery does not establish indexing.

Private performance/indexing observations are kept outside Git under `.artifacts/seo/`. The initial complete performance window is August 25 through September 21, 2026, Web search, with no country/device filter. Query rows are unavailable at this volume, so branded versus non-branded performance cannot yet be calculated. The page-index report is dated September 20 and predates the latest note and new sitemap submission. Recheck after Google processes the newly discovered URLs.

## Editorial review of the homepage

Self-review, 0-2 each: question answered 2; original evidence/examples 1; claim support 2; scanability 2; useful links 2. Total 9/10, no zero. The homepage states the technical focus and points to existing original work. It does not itself add an experiment, which is why the evidence dimension is 1. Employment facts and the article claims are inherited from existing public content. Headline/intro and card titles were visually reviewed at desktop/mobile sizes.

## Remaining scope

The foundation milestone is not the whole SEO program. Continue the ordered content-linking, schema, guide, and reproducible evaluation tasks in the implementation plan. Rankings, indexing of all notes, field Core Web Vitals, future Search Console windows, DNS changes, and public distribution are separate evidence or authorization dependencies. Nothing has been merged or deployed by this branch.
