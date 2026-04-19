# CODEX Prompts Audit

Audit date: 2026-03-15

This file tracks the repo-truth pass against [CODEX_PROMPTS.md](/C:/Users/Justin/dragons-and-distractions-site/CODEX_PROMPTS.md), the implementation targets we actually used, and the evidence that now guards them.

| Prompt | Audit Status | Actual Targets | Resolution | Validation Evidence |
| --- | --- | --- | --- | --- |
| 1. Missing spellbook ritual pages | `done` | [spellbook/index.md](/C:/Users/Justin/dragons-and-distractions-site/spellbook/index.md), [scripts/check_monster_metadata.py](/C:/Users/Justin/dragons-and-distractions-site/scripts/check_monster_metadata.py) | Kept the one-page spellbook anchor model and enforced `start_here_ritual.url` resolution against real spellbook pages/anchors. | `python scripts/check_monster_metadata.py`, `tests/test_check_monster_metadata.py` |
| 2. Apply DESIGN.md theme | `partial` | [assets/design.css](/C:/Users/Justin/dragons-and-distractions-site/assets/design.css), [_layouts/hub.html](/C:/Users/Justin/dragons-and-distractions-site/_layouts/hub.html) | Finished the remaining active-theme gaps in the loaded design layer: cover hero, low-stim token alignment, card hover glow, divider ornament, noise overlay, and mobile nav styling. | `python scripts/validate_codex_prompts.py`, visual review checklist |
| 3. Monster index card grid | `partial` | [monsters/index.md](/C:/Users/Justin/dragons-and-distractions-site/monsters/index.md), [assets/design.css](/C:/Users/Justin/dragons-and-distractions-site/assets/design.css) | Normalized the index to accent-strip cards with centered sigils, Fraunces headings, and the first hook line. | `python scripts/validate_codex_prompts.py`, `tests/test_monster_card_art_templates.py` |
| 4. Burnout Dragon printable linkage | `partial` | [_monsters/burnout-dragon.md](/C:/Users/Justin/dragons-and-distractions-site/_monsters/burnout-dragon.md), [site/printables/burnout-dragon-minimum-viable-day.md](/C:/Users/Justin/dragons-and-distractions-site/site/printables/burnout-dragon-minimum-viable-day.md) | Kept the printable page and switched the featured monster CTA to the readable page-first flow. | `python scripts/check_monster_metadata.py`, `python scripts/check_printable_links.py` |
| 5. Spellbook full ritual listing | `partial` | [spellbook/index.md](/C:/Users/Justin/dragons-and-distractions-site/spellbook/index.md), [scripts/validate_codex_prompts.py](/C:/Users/Justin/dragons-and-distractions-site/scripts/validate_codex_prompts.py) | Added a dedicated 9-card ritual directory with monster tags, primary ritual names, and first-step previews, while keeping the longer cluster guide below. | `python scripts/validate_codex_prompts.py`, `tests/test_validate_codex_prompts.py` |
| 6. Homepage hero with CTAs | `partial` | [index.md](/C:/Users/Justin/dragons-and-distractions-site/index.md), [_layouts/hub.html](/C:/Users/Justin/dragons-and-distractions-site/_layouts/hub.html), [assets/design.css](/C:/Users/Justin/dragons-and-distractions-site/assets/design.css) | Converted the homepage hero into a cover image with the required overlay and exact CTA pair. | `python scripts/validate_codex_prompts.py`, visual review checklist |
| 7. Low-stim mode toggle | `stale wording` | [_layouts/default.html](/C:/Users/Justin/dragons-and-distractions-site/_layouts/default.html), [_includes/site-banner.html](/C:/Users/Justin/dragons-and-distractions-site/_includes/site-banner.html), [assets/design.css](/C:/Users/Justin/dragons-and-distractions-site/assets/design.css) | The feature already existed; refined the header label/copy and aligned the active low-stim palette to the locked brief. | `python scripts/validate_codex_prompts.py`, manual header/theme check |
| 8. Mobile nav hamburger | `partial` | [_includes/site-banner.html](/C:/Users/Justin/dragons-and-distractions-site/_includes/site-banner.html), [_layouts/default.html](/C:/Users/Justin/dragons-and-distractions-site/_layouts/default.html), [assets/design.css](/C:/Users/Justin/dragons-and-distractions-site/assets/design.css) | Added the hamburger, full-screen dark overlay nav, escape/outside-click close behavior, and shared header markup for both active include paths. | `python scripts/validate_codex_prompts.py`, `tests/test_validate_codex_prompts.py` |

## Runbook

- `python scripts/check_monster_metadata.py`
- `python scripts/check_printable_links.py`
- `python scripts/validate_codex_prompts.py`
- `pytest -q`

## Visual Sign-Off Checklist

- Homepage hero in default theme and low-stim theme
- Monster index at mobile, tablet, and desktop widths
- Spellbook ritual directory plus the cluster list below it
- Burnout Dragon monster page CTA to printable page and PDF backup link
- Mobile nav open, close on backdrop click, and close on `Esc`
- One printable page in browser and print preview
