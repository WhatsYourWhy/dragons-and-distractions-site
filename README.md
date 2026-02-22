# Dragons & Distractions

Jekyll site + content repo for monster-themed ADHD support pages and printable ritual cards.

## What is in this repo
- Jekyll content/pages (`index.md`, `monsters/`, `spellbook/`, `site/`, `_layouts/`, `_includes/`).
- Monster source entries in `_monsters/`.
- Printable markdown sources in `site/printables/*.md`.
- PDF tooling:
  - `scripts/generate_printable_pdfs.py` generates `*-ink.pdf` and `*-art.pdf` into `site/printables/pdf/`.
  - `scripts/check_printable_links.py` validates PDF links referenced in markdown/html.

## Local usage
### 1) Install dependencies
```bash
pip install -r requirements.txt
bundle install
```

### 2) Generate printable PDFs
```bash
python scripts/generate_printable_pdfs.py
```

### 3) Validate printable links
```bash
python scripts/check_printable_links.py
```

### 4) Run the site locally
```bash
bundle exec jekyll serve --livereload --trace
```
Open `http://localhost:4000`.

## GitHub Pages deployment
`.github/workflows/pages.yml` runs on pushes to `main` and `work` and does this:
1. Install Python deps from `requirements.txt`.
2. Regenerate printable PDFs.
3. Run printable link checks.
4. Build Jekyll site to `_site/`.
5. Deploy to GitHub Pages.

## Notes
- `site/printables/pdf/*.pdf` artifacts are gitignored and are expected to be generated during local work or CI.
- The link checker scans markdown + html files for `.pdf` links (including inline anchors and simple Liquid `relative_url` patterns).

## License
See `LICENSE`.
