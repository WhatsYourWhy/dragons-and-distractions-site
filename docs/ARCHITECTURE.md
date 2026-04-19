# Architecture

Short map of how **Dragons & Distractions** is built and where to change things.

## Stack

- **Jekyll** static site, deployed with **GitHub Actions** to **GitHub Pages** (see [.github/workflows/pages.yml](.github/workflows/pages.yml)).
- **Ruby / Bundler** for Jekyll and plugins (`Gemfile`); **Python** for printable PDF generation and repo checks (`requirements.txt`, `scripts/`, `tests/`).

## Content model

- **Pages:** Markdown at repo root and under `monsters/`, `spellbook/`, `site/`, `codex/`, `art/`, etc. Front matter selects layout and SEO fields (`title`, `description`, hero images).
- **Collection `monsters`:** Source files in `_monsters/`; built URLs under `/monsters/:name/` per `_config.yml`.
- **Data:** `_data/chooser_paths.yml` drives the Choose Your Monster oracle; `_data/nav_links.yml`, `_data/printables.yml`, etc. support navigation and tool listings.

## Presentation

- **Layouts:** `_layouts/default.html` (shell, theme script, nav, main, footer), `hub.html` (marketing/landing pages with hero `<picture>`), `monster.html`, `printable.html`, `page.html`.
- **Includes:** `_includes/oracle.html` (symptom chooser + client script), `path-card.html`, `site-banner.html`, `monster-masthead.html`, `monster-index-filter.html`, etc.
- **Styles:** `assets/design.css` (primary UI), `assets/main.scss` → `main.css`. Design intent and constraints: [DESIGN.md](DESIGN.md).

## Hub hero images

- Optional front matter: `hero_image` (fallback `img` src), `hero_image_webp`, `hero_image_avif`, `hero_image_width`, `hero_image_height`, `hero_image_alt`. AVIF/WebP sources render only when set.

## Python tooling

- `scripts/generate_printable_pdfs.py` — generates ink/art PDFs (artifacts typically gitignored under `site/printables/pdf/`).
- `scripts/check_printable_links.py`, `scripts/check_monster_metadata.py` — CI validation.
- `pytest` exercises scripts and fixtures under `tests/`.

## CI pipeline (summary)

1. Install Python deps; regenerate printables; run link + metadata checks.
2. `bundle exec jekyll build` → `_site/`.
3. Deploy `_site/` to Pages.

## Accessibility notes

- **Monster index sigils** use `alt=""` because adjacent text names the monster; sigils repeat visual identity already described. If a sigil is treated as meaningful on its own, add short alt in the collection front matter and wire it in `monsters/index.md`.
- **Low Stim** is exposed as a **switch** (`aria-checked`) in the site banner; oracle choices remain **toggle buttons** with `aria-pressed` and paired `aria-controls` / panels.

## Related docs

- [README.md](README.md) — local run, scripts, deployment.
- [DESIGN.md](DESIGN.md) — visual and tone contracts.
- [PUBLIC_LAUNCH_READINESS.md](PUBLIC_LAUNCH_READINESS.md) — launch checklist and live verification.
- [CHANGELOG.md](CHANGELOG.md) — shipped changes.
