# SEO Discoverability Implementation Plan

For execution: use superpowers:executing-plans, sequentially in this task. The user has authorized implementation. The button PR is already merged. Deliver SEO as a separate draft PR with sequential atomic commits; the user reviews and merges the completed SEO change.

**Goal:** Make Praveen Kumar Sridhar's technical work on agent memory, evaluation, and knowledge systems easier to discover, read, and connect, with measured search outcomes and no known site regressions.

**Architecture:** Keep GitHub Pages' existing Jekyll renderer, collections, SEO plugin, design tokens, and article URLs. Improve the homepage and content graph incrementally. Build the generated site in CI and test what readers and crawlers actually receive, including mobile and JavaScript-disabled browsers.

**Tech stack:** Jekyll 3.10, Liquid, HTML/CSS, existing vanilla JavaScript, jekyll-seo-tag 2.8, jekyll-sitemap, jekyll-feed. Python standard library for output validation; Playwright for browser regression checks. No new production runtime.

**Spec:** `docs/seo/source-analysis.md`, copied from the user's supplied analysis, plus the constraints and completion contract below. Baseline main: `e2af5a2`. PR #23 is merged; rejected PR #24 is closed and is not a dependency.

## Global constraints

- Execute tasks in order. One SEO draft PR with sequential commits. The user merges; do not merge or enable auto-merge.
- Preserve existing URLs, resume/download links, contact paths, experience facts, article bodies, theme, fonts, and the approved Notes heading and comma-separated obsession line unless a task explicitly changes them.
- A successful build is necessary but insufficient. Test generated output, browser behavior, and visual appearance.
- No claim of zero possible bugs or guaranteed rankings. Completion means the named gates passed, with remaining limits recorded.
- No invented experiments, personal experiences, employment claims, metrics, publication dates, backlinks, or Search Console data.
- New claims need primary sources or reproducible evidence. Historical observations must retain their dates and limits.
- Source plans, tests, and experiment drafts must not appear in the published site, sitemap, or feed.
- Do not change DNS, verification records, external profile bios, or send social posts/messages as an incidental code change. Prepare concrete changes for the user's review where access or publication authorization is required.
- Keep the source analysis's conditional 60/90-day content work in scope as gated follow-up work, not as thin pages created to satisfy a checklist.
- No em dashes in new prose. No keyword stuffing or unsubstantiated SEO impact estimates.

## Review focus

1. A reader on a 320px phone can reach Writing, Work, and Contact using a visible keyboard-accessible navigation path, with JavaScript off. Task 3 owns browser checks across all templates.
2. Failed or disabled JavaScript must not hide the homepage's writing, experience, or contact content. Task 3 owns visible-content tests, including reduced motion and a missing IntersectionObserver.
3. A crawler gets exactly one canonical, meaningful unique title/description, social tags, valid JSON-LD, and links resolving to real output. Task 1 owns the full generated-page audit; later tasks extend its contract.
4. Existing note URLs, feeds, anchor links, and image overrides remain intact. Task 1 records the route inventory; every subsequent task uses it. Task 4 owns article navigation tests.
5. Long titles, sparse collections, tables, and fonts that fail to load must not create clipped text or inaccessible links. Tasks 2/3 own browser overflow and fixture checks; article content tasks reuse them.

## Verification and evaluation contracts

**Engineering gate, each PR:** existing image preflight passes; Pages-compatible production build succeeds; all expected routes remain; no broken internal assets/links/fragments; no raw front matter or Liquid; canonical/OG/Twitter/JSON-LD agree; sitemap and feed match eligible content; private files absent. Browser checks at 320, 390, 768, and 1440px cover all seven current HTML pages, visible navigation, no page overflow, images loaded, no uncaught JavaScript errors, and no-JS reading. Add new routes to this matrix. Inspect screenshots of changed templates, with normal and reduced motion. Run `git diff --check` and review the entire diff against main.

**Gate sensitivity:** deliberately break a link, canonical, JSON-LD, or expected route in a temporary copy and confirm the output validator fails. Browser tests must first reproduce hidden mobile navigation and no-JS content. A green check that cannot detect its intended break is not accepted.

**Editorial evaluation:** score each changed/new page 0, 1, or 2 on question answered, original evidence/examples, claim support, scanability, and useful related links. Require at least 8/10, no zero, and no unsupported factual claims. Record reasons, not only scores. A self-review is editorial evidence, not proof of reader satisfaction.

**Search evaluation:** record Search Console Web performance, property, export date, date window, country/device filters, indexed/excluded URLs, and sitemap state. Track branded separately from non-branded queries. Compare matched complete 28-day windows after publication; report clicks, impressions, CTR (clicks/impressions), position by page/query cohort, and top-10/top-20 query counts. Note reporting lag, anonymized query omissions, small samples, and concurrent publications. Do not interpret average position changes as causal proof. Prioritize relevant queries around positions 5-20 with repeat impressions. Without authenticated access, record “unavailable”, not zero or “indexed”. Technical delivery can proceed; measurement tasks cannot be called complete.

**Release gate:** user reviews and merges the SEO PR after implementation and verification. Recheck remote main before opening and finishing the PR. Verify deployed routes/status/metadata after merge. If a regression is confirmed, prepare a revert PR for that PR's commit rather than overwrite unrelated main changes. Do not promote content before its canonical URL works.

## Ordered atomic tasks

### Task 1: Reproducible baseline and regression gate (SEO foundation milestone)

**Files:** create `scripts/check_site.py`, `scripts/check_browser.cjs`, `scripts/build_site.sh`, `package.json`, `package-lock.json`, `.github/workflows/site-checks.yml`, `.gitignore`, `docs/seo/baseline.md`; extend `README.md` and `_config.yml` exclusions.

**Interfaces:** `bash scripts/build_site.sh OUTPUT_DIR` creates production output; `python3 scripts/check_site.py OUTPUT_DIR` checks it; `node scripts/check_browser.cjs OUTPUT_DIR ARTIFACT_DIR` serves output on a temporary local port and checks Chromium. Browser runner requires the pinned development dependency `playwright`, not a production script.

- [ ] Record current main SHA, five note URLs, assets, title/canonical/schema baseline, existing authoring checks, and unresolved external data access.
- [ ] Build unmodified main using the cached official Pages build image with a digest pinned in `scripts/build_site.sh`. Validate images first. Run with source mounted read-only and output outside source or ignored/excluded.
- [ ] Implement generated-output checks using `html.parser`, `urllib.parse`, `json`, and `xml.etree.ElementTree`. Require the seven baseline routes and discover new HTML pages automatically. Check links against built files, fragments against target IDs, head metadata independently of body SVG titles, note BlogPosting fields, social assets, sitemap/feed coverage, and private-file exclusion.
- [ ] Prove failure sensitivity by mutating temporary copies of the build. Expected: nonzero for missing route, broken link, bad canonical, invalid JSON-LD, and leaked plan; unmodified baseline passes structural checks.
- [ ] Write browser tests before homepage fixes. Expected baseline failures: mobile nav hidden and homepage content opacity zero without JS. Capture baseline screenshots before editing.
- [ ] Add CI that installs the pinned development dependencies, builds with the same Pages image, runs both validators, and uploads screenshots on completion/failure. It must not deploy.
- [ ] Document exact commands, tool versions, scope, and known baseline issues. Commit the gate with the foundation fixes so the draft PR's checks are green.

Run: `bash scripts/build_site.sh /tmp/praveen-seo-check && python3 scripts/check_site.py /tmp/praveen-seo-check && node scripts/check_browser.cjs /tmp/praveen-seo-check /tmp/praveen-seo-browser`

Expected after Tasks 2/3: all gates pass. Baseline defects remain clearly distinguished from regressions.

### Task 2: Homepage positioning and discoverable writing (SEO foundation milestone)

**Files:** `index.html`, `_config.yml`; tests from Task 1.

**Interfaces:** Uses `site.notes` front matter already rendered in `/notes/`. Produces real HTML article links before the experience sections. Does not create a second source of article titles/descriptions.

- [ ] Set site tagline to `AI Agents, Agent Memory & Evaluation`; homepage description to `Praveen Kumar Sridhar works on AI agents, agent memory, and evaluation. Technical notes and experiments on building reliable agent systems.`
- [ ] Replace the greeting-only H1 with `Building AI agents that remember and hold up under evaluation.` Keep the existing role label and introduce the full name in the intro: `I'm Praveen Kumar Sridhar. I build AI agents for businesses at Meta and the evaluation frameworks that test whether they work. Here I write about agent memory, retrieval quality, and what makes agents reliable over time.` Verify this stays within existing public claims.
- [ ] Add a writing section immediately after the hero, before professional capabilities. Heading: `Notes on memory, agents, and evals.` Intro: `Experiments, architecture comparisons, and things I learned by inspecting how agents actually work.` Include a concise current-focus line using `site.obsession` and link to `/notes/`.
- [ ] Render three most recent notes with existing titles, descriptions, and publication dates. Use actual collection objects, escape displayed fields, and handle zero, one, and long-title cases without empty boxes or overflow.

```liquid
{% assign recent_notes = site.notes | sort: "date" | reverse %}
{% if recent_notes.size > 0 %}
  {% for note in recent_notes limit: 3 %}
  <a class="writing-card" href="{{ note.url | relative_url }}">
    <h3>{{ note.title | escape }}</h3>
    <p>{{ note.description | escape }}</p>
    <time datetime="{{ note.date | date_to_xmlschema }}">{{ note.date | date: "%b %-d, %Y" }}</time>
  </a>
  {% endfor %}
{% endif %}
```

- [ ] Reuse existing colors, typography, borders, and responsive spacing. Preserve the three hero actions and all existing section IDs, employment facts, and contact links.
- [ ] Validate all new links; compare the untouched article output and its social metadata to baseline. Check homepage title/hero consistency and visible writing at all four widths.
- [ ] Run editorial rubric and document the score and rationale. Commit as `feat: foreground agent work and technical writing`.

Expected: crawler-visible links to three real notes, full name and topic in HTML, unchanged note URLs and article content, no clipping at 320px.

### Task 3: Mobile and failed-script reading (SEO foundation milestone)

**Files:** `index.html`, `notes/index.html`, `_layouts/note.html`; `scripts/check_browser.cjs`.

**Interfaces:** Keep `nav.top` links and `header.bar` behavior across all templates; no new navigation library or click-dependent menu.

- [ ] Reproduce each baseline failure in the browser runner before changing CSS.
- [ ] Replace the mobile `display:none` rule with a wrapped, visible header navigation. Use natural header height on mobile and adequate link padding. Keep desktop layout intact.
- [ ] Make `.reveal` content visible by default. Use progressive enhancement only if the animation can fail open; the simplest safe choice is to remove the visibility dependency and observer animation. Respect reduced motion for smooth scrolling/transitions.
- [ ] Verify real clicks to Writing, Work, Contact, and a featured note; keyboard-focus visibility; no-JS access; no IntersectionObserver access; article TOC and table scrolling still work with JS.
- [ ] Capture before/after desktop/mobile screenshots and inspect visually. Run the entire build/output/browser gate. Commit as `fix: keep navigation and homepage content accessible`.

Expected: hidden-content tests turn green; no internal link or metadata regressions; no unexpected shifts at desktop width. This is the first reviewable commit milestone, including Tasks 1-3 and this plan. Continue the next tasks in the same draft PR.

### Task 4: Existing-note discovery and topic map (SEO discovery milestone)

**Files:** five existing `_notes/*.md`, `notes/index.html`, `_layouts/note.html`, `docs/seo/topic-map.md`; shared validators.

**Interfaces:** preserve all five current permalinks. Add visible related-reading links using existing URLs. Do not link to a future guide before it exists.

- [ ] Map POV note to provenance/perspective; Honcho-vs-Mem0 to architecture/frameworks; migration note to operational memory/retrieval; Muse note to memory/context assembly; competence note to evaluation integrity.
- [ ] Add 2-4 genuinely relevant links where supported, with an explicit reason per link. For the evaluation-integrity note, fewer links are acceptable if the relationship would otherwise be forced. Avoid automatic all-to-all linking.
- [ ] Expand the competence note's title to `When AI Agents Game Their Evaluations: Evaluation Integrity and Reward Hacking`; retain its original title as a subtitle if it improves the article. Expand the POV title to `Agent Memory Needs a Point of View: Provenance and Perspective in Multi-Agent Systems`. Preserve filenames and dates; set `last_modified_at` only for actual substantive edits.
- [ ] Add concise summaries only where absent; preserve original findings and private-source caveats. Add a visible Home > Lab Notes > current article breadcrumb, with a topic level only once that topic URL exists.
- [ ] Evaluate the reading path, link graph, metadata, feed, long titles, mobile layout, TOC and anchors; record rubric results. Commit the discovery milestone after its checks pass; continue Task 5.

Expected: each note has a clear topic and useful onward reading; all historical links resolve; no altered factual claims.

### Task 5: Identity, article dates, and breadcrumbs (SEO schema milestone)

**Files:** `_config.yml`, `index.html`, `_layouts/note.html`, new `_includes/person-schema.html` and `_includes/breadcrumbs.html` only if repetition warrants them; `scripts/check_site.py`.

**Interfaces:** retain `{% seo %}` as the owner of WebSite/BlogPosting metadata. Supplemental Person uses a stable `https://praveenks.com/#person` identifier; breadcrumbs must match visible links.

- [ ] Inspect actual emitted graph before extending it. Add Person using verified full name, homepage, visible professional role, Northeastern University, existing sameAs profiles, and supported knowsAbout topics. Do not use the generic social card as a portrait.
- [ ] Ensure note author resolves to the same identity; validate publication/modification dates, image override, mainEntityOfPage, and headline against visible content. Do not reset dates at every build.
- [ ] Add BreadcrumbList via `jsonify`-escaped values, matching the visible breadcrumb. Avoid duplicate Article or contradictory Person records.
- [ ] Extend validator with malformed/duplicate/conflicting-identity and date fixtures; check all notes. Use Google's Rich Results Test on deployable/public output after merge when available; local JSON parsing alone does not prove eligibility.
- [ ] Run full gates, commit the schema milestone, and continue Task 6; verify live after the SEO PR merges.

Expected: valid, consistent graph with evidence-backed fields; unchanged layout except intended breadcrumb/date presentation. No rich-result or ranking guarantee.

### Task 6: Substantive agent memory guide (SEO guide milestone)

**Files:** new `agent-memory/index.md`, a small page layout derived from the established note design if needed, homepage/Notes links, links in relevant existing notes; `docs/seo/content-review.md`.

**Interfaces:** `/agent-memory/` is a stable evergreen page, not a fake dated note. Reuse site styles and SEO machinery; add route to output/browser checks.

- [ ] Organize around the lifecycle: capture -> store -> retrieve -> inject -> influence behavior. Cover memory types, admission/writes, consolidation, forgetting, provenance/perspective, retrieval, failure modes, evaluation, frameworks, and experiments.
- [ ] Source framework statements from current primary documentation. Use dated existing notes as firsthand cases, keeping reported observations distinct from unverified runtime claims.
- [ ] Include one original worked example following a corrected user preference through write, supersession, retrieval, and answer use; a lifecycle diagram; an architecture decision table; explicit limitations and further reading.
- [ ] Link to relevant existing notes; update those notes and homepage to link back where useful. No links to the flagship until it is built.
- [ ] Score the editorial rubric, run all engineering gates, and commit the guide milestone. A list of definitions or links alone fails the substantial-guide gate.

Expected: a reader can design a memory lifecycle and identify where it can fail; examples and citations support each recommendation.

### Task 7: Reproducible memory-evaluation example (SEO experiment milestone)

**Files:** `examples/memory-evaluation/README.md`, `cases.jsonl`, `evaluate.py`, `test_evaluate.py`; exclude examples from rendered site until intentionally linked as source.

**Interfaces:** `python3 examples/memory-evaluation/evaluate.py --cases examples/memory-evaluation/cases.jsonl --predictions PATH` emits JSON metrics plus per-case errors. Dataset labels are independently hand-derived and versioned. No provider credentials or API calls required.

- [ ] Define fixtures for stable preference, corrected preference, date-sensitive fact, contradiction, provenance, privacy scope, irrelevant repetition, injected false memory, explicit forgetting, and relevant-memory abstention. Include multi-turn histories, queries, permitted evidence IDs, expected answer facts, and timestamps.
- [ ] Implement set-based precision/recall and separately report stale use, unsupported claims, scope violations, provenance correctness, and task correctness with explicit denominators. Empty expected/predicted sets and missing outputs need defined behavior and tests. Abstention is scored separately from successful answer.
- [ ] Add failing unit cases for wrong denominators, stale evidence, invalid IDs, missing results, and timestamp ordering before implementing. No LLM judge used as ground truth.
- [ ] Run simple transparent baselines (latest-k, query-token overlap, corrected-state oracle) against the same cases. Label this a synthetic teaching example, not a framework benchmark or real-agent performance claim.
- [ ] Store exact command, dataset hash, outputs, limitations, and failure cases. Require deterministic reruns to match. Commit the experiment milestone with code review and unit plus site regression checks.

Expected: readers can reproduce the numbers and see why retrieval accuracy alone cannot establish useful memory. The oracle is an upper-bound fixture, not a production system.

### Task 8: Flagship memory-evaluation article (SEO flagship milestone)

**Files:** `_notes/evaluating-agent-memory.md`, related note links, `agent-memory/index.md`, homepage selection if needed; diagram assets with meaningful alt text.

**Interfaces:** stable `/notes/evaluating-agent-memory/`; consumes Task 7's committed cases/code/results. No new results invented during prose drafting.

- [ ] Write `How to Evaluate AI Agent Memory: Metrics, Failure Modes & Benchmarks`, covering all 17 topics in source analysis section 4.
- [ ] Explain retrieval precision/recall, temporal correctness, stale/contradictory/false memories, provenance, personalization, pollution, forgetting, usefulness, task impact, multi-turn histories, offline/online evaluation, dataset construction, and benchmark design.
- [ ] Include metric definitions and denominators, the reproducible synthetic example, a diagram, observed failures, primary sources, limitations, and a practical experiment checklist. Separate retrieval exposure from actual answer influence.
- [ ] Independently recompute every published number from the checked-in results; validate code links and alt text. Run editorial rubric and technical gates.
- [ ] Connect the article from homepage, guide, and relevant old notes. Prepare X and LinkedIn distribution drafts under excluded `docs/seo/distribution/`; do not post. Commit the flagship milestone, complete the whole-PR review, then verify the live canonical after user merge.

Expected: reproducible evidence, clear limitations, connected reading paths, no unsupported claim of framework superiority.

### Task 9: Remaining technical and measurement work (account actions now; measured follow-up fixes if needed)

**Files:** only files justified by audit findings; `docs/seo/measurement.md` and `docs/seo/baseline.md` track evidence. Private exports stay outside Git.

**Interfaces:** Search Console property `sc-domain:praveenks.com` or verified URL-prefix equivalent; production sitemap `https://praveenks.com/sitemap.xml`.

- [ ] Confirm Search Console access, record indexing status per important URL, and verify sitemap submission. Use user-provided authenticated access, never infer indexing from HTTP 200.
- [ ] Verify HTTP -> HTTPS and apex/www behavior. If www is desired, present the exact CNAME/Pages setting for user review, then test redirect chains and TLS after the authorized change. DNS absence is not proof of an apex ranking penalty.
- [ ] Measure mobile/desktop lab performance and inspect image sizes. Optimize assets only where measured weight or rendering issues warrant it; retain existing image PR #17 overlap awareness. Compare dimensions, visual quality, LCP/CLS and transfer sizes before/after.
- [ ] Record field Core Web Vitals if available; a small site may have no CrUX sample. Do not substitute a single Lighthouse score for field performance.
- [ ] Run matched 28-day evaluations after deployment, then repeat monthly. Report actual direction/magnitude and uncertainty. Fix pages with evidenced query mismatch or poor CTR; avoid arbitrary keyword variants.

Expected: measured account state and documented technical changes. Missing access and elapsed observation windows remain explicit dependencies, not completed checkboxes.

### Task 10: Evaluation guide, follow-ups, and distribution (conditional 60/90-day work)

**Files:** `agent-evaluation/index.md`, new `_notes/` articles supported by experiments, `docs/seo/editorial-calendar.md`, distribution drafts; later `/agent-knowledge/` only if justified.

**Interfaces:** reuse completed guides, schema, note layout, dataset methodology, and search measurement definitions.

- [ ] Use the evaluation-integrity note plus flagship and follow-up experiment as the evidence base for `/agent-evaluation/`. Cover task success, trajectories, tools, knowledge/memory, reliability, online/offline/human evaluation, attribution, integrity, and tooling. Require the same rubric and engineering gates.
- [ ] Rank the source analysis's article queue by a concrete unanswered question, available original evidence, and observed search demand when available. Publish supporting pieces only when they add evidence; 8-12 articles is a planning target, not a quality shortcut.
- [ ] Prepare consistent full-name/topic bios and source-repository links for the user's review. Prepare launch/takeaway/chart/follow-up drafts per substantial article; public posts and outreach require explicit authorization and a live canonical.
- [ ] Track relevant referring domains, citations, observable AI-search mentions, and technical inquiries without fabricating attribution. Review after two monthly Search Console exports and choose the next topic based on evidence.
- [ ] Build `/agent-knowledge/` only after unique supporting material exists. Otherwise record why it remains gated and retain the scope.

Expected: useful interconnected content and a repeatable measured publishing process. External publication, user merge gates, and future observation windows cannot be completed by local code alone.

## Spec coverage and completion audit

| Source sections | Deliverable |
| --- | --- |
| 1-2 positioning/homepage | Task 2 |
| 3 topic pillars | Tasks 6 and 10 |
| 4 flagship | Tasks 7-8 |
| 5-6 titles/internal links | Task 4, then guide/article backlinks in 6/8 |
| 7 schema | Task 5 |
| 8 technical checklist | Tasks 1/3/5/9 |
| 9 measurement | Task 9 plus evaluation contract |
| 10-12 original content/experiments/AI readability | Tasks 6-8/10 and editorial rubric |
| 13-15 identity/backlinks/distribution | Tasks 5/8/10, external actions gated |
| 16 metrics | Task 9 and evaluation contract |
| 17 first 30 days | Tasks 1-9, sequential implementation and access dependencies |
| 18-19 60/90 days | Task 10 and two monthly measurement cycles |
| 20 priorities | Homepage/gates first, links then substantial guides and original evaluation |
| 21 publishing checklist | Editorial rubric plus engineering/release gates |
| 22 outcome | Measured over time; no guarantee from implementation alone |

Before marking the overall goal complete, inspect each task's committed files, actual test results, review state, merge/deployment evidence, external-access requirements, and search observation windows. Mark each as complete, incomplete, or waiting on a named dependency. Do not equate the first milestone or a green build with the full SEO program being complete.

## Authoritative guidance

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide): useful content, readable organization, descriptive links, and the time needed to evaluate changes.
- [Google Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article): supported article metadata and visible-content consistency.
- [GitHub Pages dependency versions](https://pages.github.com/versions/): compatibility baseline for the local build.
