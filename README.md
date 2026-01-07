# 🐉 Dragons & Distractions – Project Index

This project transforms ADHD and executive dysfunction into a playful, mythic toolkit. Each monster represents a cognitive challenge, and each artifact, spell, or quest offers real science-backed help.

## 🔧 Primary Use
- Website & resource hub
- Printable or digital decks/cards
- Community storytelling & submissions

## 🎯 Key Goals
- Normalize struggle through humor, science, and myth
- Give people better tools (with names, faces, stories)
- Offer rituals and quests instead of shame or rigidity

## 🗺️ Navigate This Project
- **Monsters**: Core creature files with triggers, lore, and tactics
- **Tools**: Spells, artifacts, rituals, and planning docs
- **Codex**: Philosophy, origin logic, tone tracking
- **Art**: Character images and prompts
- **Site**: Anything for upload, public use, or onboarding

## 📌 Status
🛠️ In development | 🐾 Play-focused | 💡 Ikigai-aligned

Feel free to add monsters, refine rituals, or log new ideas.
---

## 🛡️ Licensing & Use

This project is free to explore and use personally, but not for resale or commercialization.

If you'd like to collaborate, build with it, or bring it into a product or offering — let's talk.

> This is a gift, not a giveaway.  
> Respect the sword. Share the scroll.

See LICENSE file for full details.

## 🧾 Regenerating ritual printables

If you update any ritual text, keep the downloadable PDFs in sync:

1. Install the PDF dependency (Python 3.9+):
   ```bash
   pip install -r requirements.txt
   ```
2. Regenerate all ritual PDFs (ink-friendly + art headers):
   ```bash
   python scripts/generate_printable_pdfs.py
   ```
3. The files land in `site/printables/pdf/` and are linked from the Spellbook and Site Tools index.
   - The PDFs are **gitignored** to keep the repo text-only. Regenerate them locally (or in CI before publishing) so the links stay live on your built site.

Tip: run `python scripts/check_printable_links.py` after generating to verify every referenced PDF exists before pushing to Pages. The checker currently validates ritual PDF links inside Markdown files and inline HTML `<a>` tags (including simple Liquid `relative_url` filters) and folds in `_data/printables.yml` entries when checking `site/index.md`; it already enforces a handful of required ritual links. Broader HTML/Liquid template parsing can be added once implemented.

## 🚀 Publishing to GitHub Pages

This repo ships with a ready-to-go GitHub Actions workflow that builds the site and deploys it to Pages (including regenerated PDFs):

1. Enable **GitHub Pages** in the repo settings and choose **GitHub Actions** as the source.
2. Push to `main` (or `work`); the workflow at `.github/workflows/pages.yml` will:
   - Install Python and `fpdf2`
   - Regenerate the printable PDFs
   - Run the printable link checker
   - Build the site with GitHub's Jekyll runner into `_site/`
   - Upload `_site/` as the static site artifact
3. The `deploy` job publishes that artifact to the `github-pages` environment. Once it completes, the job output lists your live URL.

### Local development

Run Jekyll locally:
Ruby + Bundler + Jekyll required.

```bash
python scripts/generate_printable_pdfs.py
bundle exec jekyll serve --livereload --trace
```

Then open http://localhost:4000 in your browser; Jekyll will render the markdown pages and copy the regenerated PDFs into the `_site/` output.

For a lightweight static preview without Jekyll:

```bash
python scripts/generate_printable_pdfs.py
python -m http.server 4000
```

Then open http://localhost:4000 in your browser; the markdown files and PDFs will serve as static files.
