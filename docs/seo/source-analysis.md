# praveenks.com --- SEO & Discoverability Plan

**Goal:** Make `praveenks.com` easy to discover through Google and AI
search, while establishing a strong association between **Praveen Kumar
Sridhar** and **AI agents, agent memory, agent evaluation, and knowledge
systems**.

## 1. Target Positioning

The primary topic graph should be:

> **Praveen Kumar Sridhar → AI Agents → Agent Memory → Agent Evaluation
> → Knowledge Systems**

General ML experience remains as credibility, but should support rather
than dominate this positioning.

### Primary topics

-   AI agents
-   Agent memory
-   Agent evaluation
-   Agent knowledge systems
-   Reliable / long-running agents

### Secondary topics

-   Context engineering
-   Memory provenance
-   Retrieval and RAG
-   LLM evaluation
-   Agent reliability
-   Honcho, Mem0, Hindsight
-   LangChain / LangSmith evaluation infrastructure

------------------------------------------------------------------------

# 2. Homepage

## Metadata

**Recommended title**

> Praveen Kumar Sridhar \| AI Agents, Agent Memory & Evaluation

**Recommended meta description**

> Machine learning engineer working on AI agents, agent memory,
> knowledge systems and evaluation. Experiments and technical notes on
> building reliable long-running agents.

## Hero

Recommended direction:

> **Building reliable AI agents that can remember, learn, and be
> evaluated.**

Supporting copy:

> I'm Praveen Kumar Sridhar, a machine learning engineer working on
> agent evaluation, memory and knowledge systems. I write technical
> notes and experiments about what happens when AI agents have to
> operate over time.

## Information hierarchy

1.  Hero / positioning
2.  Featured Lab Notes
3.  Current areas of exploration
4.  Selected projects / experiments
5.  Selected professional impact
6.  Experience
7.  Skills
8.  About / contact

The résumé should establish credibility without becoming the dominant
semantic content of the homepage.

------------------------------------------------------------------------

# 3. Build Topic Pillars

## Pillar 1: Agent Memory

Create:

`/agent-memory/`

Cover:

1.  What agent memory means
2.  Why agents need memory
3.  Types of memory
4.  Writing memories
5.  Retrieval
6.  Consolidation
7.  Forgetting
8.  Provenance and perspective
9.  Failure modes
10. Evaluating memory
11. Frameworks
12. Experiments
13. Further reading

Target concepts include **AI agent memory, LLM agent memory, long-term
agent memory, memory architecture, memory retrieval, memory provenance,
memory evaluation, Mem0, Honcho, and Hindsight**.

## Pillar 2: Agent Evaluation

Create:

`/agent-evaluation/`

Cover:

1.  Why agent evaluation differs from model evaluation
2.  Task success
3.  Trajectory evaluation
4.  Tool-use evaluation
5.  Knowledge evaluation
6.  Memory evaluation
7.  Reliability
8.  Online vs offline evaluation
9.  Human evaluation
10. Failure attribution
11. Evaluation integrity
12. Frameworks and tooling

## Pillar 3: Agent Knowledge

Eventually create:

`/agent-knowledge/`

Cover knowledge systems, agent RAG, memory vs RAG, knowledge retrieval,
and context engineering. Build this only after sufficient supporting
content exists.

------------------------------------------------------------------------

# 4. Flagship Resource

Highest-priority new article:

> **How to Evaluate AI Agent Memory: Metrics, Failure Modes &
> Benchmarks**

Suggested URL:

`/notes/evaluating-agent-memory/`

Cover:

-   Retrieval accuracy
-   Precision and recall
-   Temporal correctness
-   Stale-memory rate
-   Contradiction rate
-   Provenance correctness
-   Personalization correctness
-   Memory pollution
-   False-memory injection
-   Forgetting
-   Memory usefulness
-   Task-level impact
-   Multi-turn evaluation
-   Offline vs online evaluation
-   Dataset construction
-   Benchmark design

Make this a substantial technical resource with diagrams, examples,
experiments, and code where useful. Future memory articles should
naturally link to it.

------------------------------------------------------------------------

# 5. Improve Existing Titles

Combine editorial personality with explicit technical search intent.

Instead of:

> When Competence Attacks Its Measurement

Use:

> **When AI Agents Game Their Evaluations: Evaluation Integrity and
> Reward Hacking**

Keep *When Competence Attacks Its Measurement* as a subtitle if desired.

Instead of:

> Agent Memory Needs a Point of View

Use:

> **Agent Memory Needs a Point of View: Provenance and Perspective in
> Multi-Agent Systems**

Comparison articles should remain direct, for example:

> **Honcho vs Mem0: Architecture, Tradeoffs and Agent Memory Design**

------------------------------------------------------------------------

# 6. Internal Linking

Every article should belong to a topic cluster.

``` text
                         Agent Memory
                              |
          +-------------------+-------------------+
          |                   |                   |
     Architecture         Evaluation          Frameworks
          |                   |                   |
    Perspective         Memory Metrics       Honcho vs Mem0
          |                   |                   |
     Provenance          Benchmarks        Honcho -> Hindsight
```

Every new article should:

-   Link to its pillar page.
-   Link to 2--4 genuinely related Lab Notes.
-   Receive links from older relevant articles.
-   Link to foundational definitions rather than repeatedly explaining
    them.
-   Use descriptive anchor text.

Add breadcrumbs such as:

`Home → Lab Notes → Agent Memory → Article`

Implement `BreadcrumbList` structured data.

------------------------------------------------------------------------

# 7. Structured Data

## Person schema

Homepage JSON-LD should consistently identify Praveen with:

-   `@type: Person`
-   `name`
-   `url`
-   `image`
-   `jobTitle`
-   `sameAs` for LinkedIn, GitHub and X
-   `alumniOf`
-   `knowsAbout`

Suggested `knowsAbout` values:

-   AI Agents
-   Agent Memory
-   Agent Evaluation
-   Knowledge Systems
-   Large Language Models
-   Machine Learning

## Article schema

Every Lab Note should expose:

-   `BlogPosting` or `Article`
-   headline
-   description
-   author
-   datePublished
-   dateModified
-   image
-   mainEntityOfPage

Also use `WebSite`, `ProfilePage`, and `BreadcrumbList` where
appropriate.

------------------------------------------------------------------------

# 8. Technical SEO Checklist

-   [ ] Verify `robots.txt`.
-   [ ] Verify XML sitemap.
-   [ ] Submit sitemap to Google Search Console.
-   [ ] Verify canonical URLs.
-   [ ] Ensure HTTP redirects to HTTPS.
-   [ ] Keep `www` / non-`www` behavior consistent.
-   [ ] Verify correct HTTP status codes.
-   [ ] Ensure important pages are not accidentally `noindex`.
-   [ ] Use one clear H1 per page.
-   [ ] Maintain logical heading hierarchy.
-   [ ] Give every page a unique title.
-   [ ] Give important pages useful meta descriptions.
-   [ ] Add Open Graph metadata.
-   [ ] Add X/Twitter card metadata.
-   [ ] Expose article publication and modification dates.
-   [ ] Add meaningful image alt text where appropriate.
-   [ ] Compress images.
-   [ ] Verify mobile usability.
-   [ ] Monitor Core Web Vitals.
-   [ ] Ensure JavaScript does not hide important content from crawlers.
-   [ ] Monitor broken links and 404s.
-   [ ] Add breadcrumbs where useful.

------------------------------------------------------------------------

# 9. Search Console Feedback Loop

Track:

-   Indexed pages
-   Excluded/non-indexed pages
-   Queries
-   Impressions
-   Clicks
-   CTR
-   Average position
-   Pages receiving impressions
-   Sitemap status

Every month:

1.  Export queries.
2.  Find queries receiving impressions but few clicks.
3.  Find relevant queries ranking roughly positions 5--20.
4.  Improve the page answering those queries.
5.  Add useful sections for relevant query variants.
6.  Improve titles/descriptions when CTR is weak.
7.  Add internal links to pages close to ranking.

Do not create thin pages for every keyword variation.

------------------------------------------------------------------------

# 10. Content Strategy

Prioritize **original technical work** over generic SEO content.

The ideal loop:

``` text
Experiment
    ↓
Finding
    ↓
X post
    ↓
Lab Note
    ↓
Evergreen pillar
    ↓
Search traffic / citations / backlinks
```

## High-value article queue

### Agent Memory

1.  How to Evaluate AI Agent Memory
2.  Agent Memory Architecture: A Practical Guide
3.  RAG vs Agent Memory: Where Each Belongs
4.  Honcho vs Mem0 vs Hindsight
5.  What Should an AI Agent Remember?
6.  Memory Provenance in Multi-Agent Systems
7.  When Should an Agent Forget?
8.  Evaluating Long-Term Memory Across Multi-Turn Conversations
9.  Memory Pollution: How Bad Memories Compound
10. Building a Benchmark for Agent Memory

### Agent Evaluation

11. A Practical Guide to AI Agent Evaluation
12. Why LLM Evals Break for Agents
13. Evaluating Agent Trajectories, Not Just Final Answers
14. How Agents Can Game Their Own Evaluations
15. Failure Attribution in AI Agent Systems
16. Offline vs Online Agent Evaluation
17. Evaluating Tool-Using Agents
18. Building an Agent Evaluation Stack with LangSmith
19. Agent Eval Metrics That Actually Matter
20. Testing Reliability Across Long-Running Agent Tasks

------------------------------------------------------------------------

# 11. Make Experiments the Differentiator

Avoid relying on generic explainers such as "What Is AI Agent Memory?"

Prefer original work such as:

> **I Migrated 8,455 Agent Memories from Honcho to Hindsight. Here's
> What Broke.**

Structure experiments so they also answer broader technical questions.

Original experiments provide:

-   Unique data
-   Original charts
-   First-hand technical experience
-   Natural backlink opportunities
-   Better X content
-   Better AI-search citation potential
-   Evidence for evergreen guides

------------------------------------------------------------------------

# 12. Optimize for AI Search

Make articles easy for humans and retrieval systems to parse.

Preferred structure:

1.  Clear title
2.  Short summary
3.  Key findings
4.  Problem
5.  Method
6.  Results
7.  Interpretation
8.  Limitations
9.  Practical implications
10. Related work / links

Use explicit headings. Define important concepts. Include concrete
numbers and experimental details. Clearly distinguish observed results
from interpretation. Cite primary sources and expose code/data where
appropriate.

------------------------------------------------------------------------

# 13. Entity Identity

Use the same identity consistently across:

-   Website
-   GitHub
-   LinkedIn
-   X
-   arXiv / research profiles where applicable
-   Event/conference bios
-   Guest posts
-   Project repositories

Preferred full name:

> **Praveen Kumar Sridhar**

Where appropriate, associate it with:

> AI agents, agent memory and agent evaluation.

------------------------------------------------------------------------

# 14. Backlinks

Do not buy links or prioritize generic SEO directories.

Earn links through useful technical work:

-   GitHub repositories
-   Framework documentation
-   Research discussions
-   Technical newsletters
-   Hacker News
-   Relevant Reddit discussions
-   Conference/event pages
-   Technical communities
-   Open-source projects
-   Papers and technical reports

Original benchmarks, datasets, diagrams, tools, and experiments are
especially linkable.

------------------------------------------------------------------------

# 15. Distribution

Every substantial Lab Note should have a distribution package.

## X

Create several distinct surfaces from one article:

-   Launch post
-   Technical takeaway
-   Interesting chart/result
-   Follow-up observation
-   Relevant replies to existing discussions

Lead with the finding rather than repeatedly posting the same link.

## GitHub

When meaningful code exists:

1.  Create a clean repository.
2.  Write a useful README.
3.  Link the article from the README.
4.  Link the repository from the article.

## LinkedIn

Use a problem → experiment → unexpected result → engineering implication
structure, then link to the complete analysis.

------------------------------------------------------------------------

# 16. Measurement

## Search visibility

Track:

-   Organic impressions
-   Organic clicks
-   Ranking queries
-   Indexed technical pages
-   Queries in top 20
-   Queries in top 10

## Authority

Track:

-   Referring domains
-   Technical backlinks
-   GitHub stars/forks
-   Citations and mentions
-   Newsletter/community references
-   AI-search citations where observable

## Personal brand

Track branded queries such as:

-   Praveen Kumar Sridhar
-   Praveen AI agents
-   Praveen agent memory
-   Praveen agent evaluation

Also monitor referrals to X, GitHub and LinkedIn plus inbound technical,
speaking and community opportunities.

------------------------------------------------------------------------

# 17. First 30 Days

## Week 1 --- Foundation

-   [ ] Update homepage title.
-   [ ] Update homepage meta description.
-   [ ] Rewrite hero around agents/memory/evals.
-   [ ] Verify robots.txt.
-   [ ] Verify XML sitemap.
-   [ ] Set up/verify Google Search Console.
-   [ ] Submit sitemap.
-   [ ] Verify canonical tags.
-   [ ] Add/verify Person schema.
-   [ ] Add Article schema to Lab Notes.
-   [ ] Check indexing for every Lab Note.

## Week 2 --- Architecture

-   [ ] Create `/agent-memory/`.
-   [ ] Map every existing article to a topic cluster.
-   [ ] Add internal links between existing articles.
-   [ ] Add breadcrumbs.
-   [ ] Improve titles of editorially named articles.
-   [ ] Add article summaries/key findings.

## Week 3 --- Flagship

Publish:

> **How to Evaluate AI Agent Memory: Metrics, Failure Modes &
> Benchmarks**

Then:

-   [ ] Link it from the homepage.
-   [ ] Link it from `/agent-memory/`.
-   [ ] Link relevant older articles to it.
-   [ ] Create X launch content.
-   [ ] Create supporting diagrams.
-   [ ] Publish useful code/examples on GitHub where appropriate.

## Week 4 --- Distribution & Measurement

-   [ ] Review Search Console.
-   [ ] Record baseline metrics.
-   [ ] Identify early ranking queries.
-   [ ] Improve pages receiving impressions.
-   [ ] Publish one experiment-driven follow-up.
-   [ ] Begin targeted distribution of the flagship article.

------------------------------------------------------------------------

# 18. 60-Day Milestones

-   [ ] `/agent-memory/` is substantial.
-   [ ] Flagship memory-evaluation article is live.
-   [ ] 3--5 supporting memory articles exist.
-   [ ] Internal linking is systematic.
-   [ ] Article/schema metadata is standardized.
-   [ ] At least one experiment has accompanying code/data.
-   [ ] Search Console query mining has happened twice.
-   [ ] Existing articles have been updated using search data.
-   [ ] `/agent-evaluation/` outline is ready.
-   [ ] X routinely feeds relevant readers into Lab Notes.

------------------------------------------------------------------------

# 19. 90-Day Milestones

-   [ ] Launch `/agent-evaluation/`.
-   [ ] Have 8--12 high-quality interconnected technical pieces.
-   [ ] Build at least two substantial evergreen guides.
-   [ ] Publish multiple original experiments.
-   [ ] Establish a repeatable article → X → GitHub distribution
    process.
-   [ ] Track backlinks and referring domains.
-   [ ] Refresh articles beginning to rank.
-   [ ] Identify the topic cluster receiving the strongest search
    response.
-   [ ] Double down on that cluster for the following quarter.

------------------------------------------------------------------------

# 20. Priority Matrix

  Priority   Work                                        Expected Impact
  ---------- ------------------------------------------- ------------------------
  P0         Homepage positioning                        High
  P0         Search Console + indexing verification      High
  P0         Sitemap / canonical / schema verification   High
  P0         `/agent-memory/` pillar                     Very High
  P0         Agent-memory-evaluation flagship            Very High
  P1         Internal linking                            High
  P1         Existing article title improvements         Medium--High
  P1         Experiment-driven articles                  Very High
  P1         Article structured data                     Medium
  P1         `/agent-evaluation/` pillar                 High
  P2         Image / alt-text cleanup                    Low--Medium
  P2         Minor metadata polish                       Low--Medium
  P2         `/agent-knowledge/` pillar                  Medium initially
  P2         Broader backlink outreach                   Medium--High over time

------------------------------------------------------------------------

# 21. Publishing Checklist

Before publishing a Lab Note, answer:

1.  Which topic pillar does this strengthen?
2.  What real query or technical question does it answer?
3.  What is original about the article?
4.  Which existing pages should link to it?
5.  Which pages should it link to?
6.  Is the title understandable without context?
7.  Does the introduction clearly explain the problem?
8.  Are claims supported by experiments or primary sources where
    possible?
9.  Is there a useful diagram, dataset, code artifact, or concrete
    example?
10. How will it be distributed through X, GitHub, LinkedIn, or relevant
    communities?

------------------------------------------------------------------------

# 22. North-Star Outcome

The site should evolve from:

> **A strong portfolio belonging to an experienced ML engineer**

into:

> **A recognizable technical resource for engineers working on AI agent
> memory, evaluation, knowledge systems, and long-running agent
> reliability.**

The long-term objective is that searches and AI queries about **agent
memory and agent evaluation** repeatedly surface useful work from
`praveenks.com`, while searches for **Praveen Kumar Sridhar** clearly
establish the same technical identity.
