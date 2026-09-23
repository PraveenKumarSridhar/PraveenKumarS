# Local performance samples

September 23, 2026. Chromium 151.0.7922.34 through pinned Playwright. Three cold-cache samples per route/profile, compared with untouched main e2af5a2. Raw numeric samples are in `performance-samples.csv`.

Conditions: local uncompressed HTTP server; mobile 390px, 1.6 Mbps, 150 ms latency, 4x CPU slowdown; desktop 1440px, 10 Mbps, 40 ms latency, no CPU slowdown. External requests blocked, fallback fonts and reduced motion. Observe through one second after load. `encodedBytes` totals observed encoded document/resource bodies, excluding protocol overhead. LCP is the last observed candidate; CLS is the sum of shifts without recent input during this short window, not the field session-window metric.

These samples isolate local rendering and payload changes. They do not measure production hosting, actual web-font latency, real-device variability or search rankings. No field Core Web Vitals data was available in Search Console.

| Version | Profile | Route | Median LCP ms | Maximum observed shift sum | Median encoded KiB |
| --- | --- | --- | --- | --- | --- |
| baseline | mobile | `/` | 268 | 0.0000 | 29.4 |
| baseline | mobile | `/notes/` | 272 | 0.0000 | 9.9 |
| baseline | mobile | `/notes/muse-memory-investigation/` | 288 | 0.0211 | 414.6 |
| baseline | desktop | `/` | 76 | 0.0000 | 29.4 |
| baseline | desktop | `/notes/` | 80 | 0.0000 | 9.9 |
| baseline | desktop | `/notes/muse-memory-investigation/` | 88 | 0.0000 | 414.6 |
| SEO before lazy loading | mobile | `/` | 304 | 0.0000 | 33.4 |
| SEO before lazy loading | mobile | `/notes/` | 264 | 0.0000 | 11.0 |
| SEO before lazy loading | mobile | `/notes/muse-memory-investigation/` | 292 | 0.0155 | 416.5 |
| SEO before lazy loading | mobile | `/agent-memory/` | 296 | 0.0168 | 26.8 |
| SEO before lazy loading | mobile | `/notes/evaluating-agent-memory/` | 296 | 0.0156 | 29.2 |
| SEO before lazy loading | desktop | `/` | 84 | 0.0000 | 33.4 |
| SEO before lazy loading | desktop | `/notes/` | 88 | 0.0000 | 11.0 |
| SEO before lazy loading | desktop | `/notes/muse-memory-investigation/` | 84 | 0.0005 | 416.5 |
| SEO before lazy loading | desktop | `/agent-memory/` | 84 | 0.0000 | 26.8 |
| SEO before lazy loading | desktop | `/notes/evaluating-agent-memory/` | 84 | 0.0000 | 29.2 |
| Muse with lazy loading | mobile | `/notes/muse-memory-investigation/` | 288 | 0.0155 | 33.8 |
| Muse with lazy loading | desktop | `/notes/muse-memory-investigation/` | 84 | 0.0005 | 33.8 |

## Change justified by the measurement

The Muse page loaded about 416.5 KiB before lazy loading. Two below-the-fold diagrams account for most of it. Adding native `loading="lazy"` and `decoding="async"` lowers observed initial payload to 33.8 KiB in this setup, about 92%. Their bytes and dimensions are unchanged; the browser matrix scrolls to both and awaits successful decoding. This delays transfer until needed rather than reducing total bytes for a reader who scrolls through the article. LCP remains similar because the diagrams are below the initial viewport.

Homepage payload grows by about 4 KiB to include real article links and identity data. Three lab samples do not establish a meaningful production timing change. No new production library or render-blocking dependency was introduced.

Open image PR #17 covers `assets/social-card.png`, `apple-touch-icon.png` and `favicon.svg`; those files were left untouched. Social-card assets are metadata references rather than inline page images. Their optimization should be evaluated with that existing PR, not duplicated here.

## Reproduce

```sh
node scripts/sample_performance.cjs /tmp/praveen-seo-discovery /tmp/performance.json / /notes/ /notes/muse-memory-investigation/
```

Use the same browser, machine and build conditions for comparisons. Run the normal browser checks separately, since these samples do not exercise scrolling or keyboard behavior.

The guide and evaluation article were subsequently removed at user request. Their earlier samples above are historical, not current routes.
