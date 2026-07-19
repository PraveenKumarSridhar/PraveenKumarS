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
   ---

   ## First section

   Body in plain markdown. `##` headings become the "On this page" sidebar.
   ```

2. `git push`. GitHub Pages rebuilds in ~30 seconds.

Read time is computed from word count, the newest note is featured on the listing page, and the note template is `_layouts/note.html`.