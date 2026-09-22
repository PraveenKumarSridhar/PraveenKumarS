# PraveenkumarS


This repository contains the code for my portfolio website, [https://praveenks.com](https://praveenks.com) The original html, css, and php were acquired from a free themezy theme found [here](https://www.themezy.com/demos/151-ceevee-free-responsive-website-template). It was a lot of fun tweaking the HTML to make the template my own. I learned a lot about HTML and CSS in the process of making this site.

## Lab Notes

The blog lives at [/notes/](https://praveenks.com/notes/) and is rendered by GitHub Pages' built-in Jekyll. To publish a note:

1. Add a markdown file to `_notes/`, e.g. `_notes/my-note-title.md` (the filename becomes the URL slug):

   ```markdown
   ---
   title: My note title
   description: One-liner shown on the listing page.
   date: 2026-07-18
   tags: [agents, evals]
   image: /assets/social-card.png # optional social-card override
   ---

   ## First section

   Body in plain markdown. `##` headings become the "On this page" sidebar.
   ```

2. Run `ruby scripts/validate_note_images.rb`. Fix any reported image errors before previewing or publishing.
3. `git push`. GitHub Pages rebuilds in ~30 seconds.

Read time is computed from word count, the newest note is featured on the listing page, and the note template is `_layouts/note.html`.

GitHub Pages also generates:

- `/sitemap.xml` for crawler discovery
- `/feed.xml` as an Atom feed of Lab Notes
- canonical, Open Graph, X card, and JSON-LD metadata for every note

Every note should include a `title`, `description`, and `date`. The site-wide social card is used when `image` is omitted.


### Optional social images

Omit `image` to use `/assets/social-card.png`. A supplied root-relative local asset path overrides the Open Graph, X card, and JSON-LD image for that note. It does not add a hero image or listing thumbnail. The existing Jekyll SEO plugin also supports alternative text:

```yaml
image:
  path: /assets/my-note-card.png
  alt: A short description of the card.
```

Use a 1200 by 630 image and verify its readability at feed-preview size. The preflight uses Ruby's standard YAML library, checks that nonempty local paths exist, and exits with an error for missing assets or invalid values. It is an authoring check to run before a build, not a GitHub Pages plugin. External image URLs are outside this local validation contract.

Empty strings, null, empty mappings, and empty `image.path` values should be omitted. They do not all inherit the default correctly in the SEO plugin. To explicitly remove empty overrides from selected files, run:

```sh
ruby scripts/validate_note_images.rb --normalize-empty _notes/my-note-title.md
```

Without this option the preflight is read-only. With no file arguments it checks every note. Normalization preserves the rest of each note and makes no edits if any checked file has an error. Duplicate top-level `image` keys are rejected. Empty overrides in flow-style front matter must be removed manually to avoid altering adjacent fields. Review the diff, run the preflight again, then build the preview. A broken nonempty override must be corrected; crawlers cannot be promised a fallback.
