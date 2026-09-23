# Search measurement procedure

Property: `sc-domain:praveenks.com`. Search type: Web. Keep country/device unrestricted for the headline comparison; break down those cohorts separately when sample size supports it.

1. Before publishing, record a complete 28-day window with its exact dates and last-update timestamp. Save property totals, pages, queries, indexed/excluded URLs and reasons, and sitemap status privately. Empty query rows mean unavailable data, not zero non-branded traffic.
2. Record the merge SHA, deployment date, changed URLs, and any simultaneous new articles. The technical baseline is in `baseline.md`; the private initial measurement is outside Git under `.artifacts/seo/`.
3. After 28 complete days of post-deployment data, compare like-for-like windows. Report absolute counts with CTR = clicks / impressions; stratify branded queries, topic queries, device, and country when available. Page/query totals can differ from property totals because of Search Console aggregation and privacy filtering.
4. Treat average position and top-10/top-20 query counts as descriptive measures, not causal effects. Small denominators, new URLs, reporting lag, seasonality, and simultaneous publishing weaken inference. Do not invent targets without a usable baseline.
5. Prioritize pages repeatedly shown for relevant queries around positions 5-20. Inspect whether the page actually answers the query before editing copy. Evaluate low CTR alongside position and intent. Avoid creating near-duplicate pages for keyword variants.
6. Recheck URL Inspection for every important new or changed canonical. “Discovered”, “submitted”, and “indexed” are different states. Use the exact reason Google reports; successful local HTTP requests alone do not prove indexing.
7. Record field Core Web Vitals only if Google has sufficient data. Keep reproducible lab tests separate from field data. Attribute a performance change only to measurements with comparable settings.
8. Review again in the next monthly window. Keep article/experiment quality gates independent of traffic so an early low-volume signal does not drive low-quality content.

The domain property and current HTTPS sitemap submission have been verified. No recurring automation has been created. Future measurement windows remain scheduled work in the plan, not completed evaluation results.
