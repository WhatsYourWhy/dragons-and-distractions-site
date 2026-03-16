# Dragons & Distractions — Design System

> This document is the locked design brief for this site.
> Codex and all contributors: implement from this spec. Do not improvise font choices, color palettes, or layout structure without updating this file first.

---

## The Core Feeling

You crack open the site and feel like you found something in a dusty bookshop. A handbook someone actually used — coffee-stained margins, sketched notes, monster entries written in a careful scholarly hand. It's serious about its subject but never clinical. The fantasy framing isn't decoration, it's *the point*. You're not reading about ADHD. You're consulting a bestiary.

The tone is: **warm, grounded, slightly wry**. The monsters are real. The rituals work. The humor is in the naming, not the execution.

---

## Color System

| Token | Value | Usage |
|---|---|---|
| `--color-page-bg` | `#0a0804` | Page background. Deep charcoal with warm undertone. |
| `--color-surface` | `#130f09` | Card/container background. |
| `--color-surface-alt` | `#1a1208` | Alternate card surface. Parchment that's been handled. |
| `--color-border` | `#3d2e1a` | Warm dark brown. Edges of things. |
| `--color-text-base` | `#d4c9b0` | Body text. Aged cream, not white. |
| `--color-text-strong` | `#f0e8d5` | Headings. Brighter ivory. |
| `--color-text-muted` | `#9e9080` | Labels, captions, secondary text. |
| `--color-accent` | `#c8900a` | Amber mid. Borders on active elements, focus rings. |
| `--color-accent-light` | `#f5c842` | Candlelight gold. Links, hover glows, CTAs. |
| `--color-magic` | `#4cc8c8` | Spectral cyan. Rituals, spells, otherworldly elements. Used sparingly. |
| `--color-danger` | `#b22222` | Stamp red. Alerts, rejection, the Perfection Wyrm's ink. Rare. |

### Low-Stim Mode
A lighter cream palette for days when the dark grimoire is too intense. **Keep this feature.** It matters for the ADHD audience. Low-stim mode overrides the dark palette with warm off-whites and desaturated accents. It is not a bug; it is a feature.

---

## Typography

### Font Stack

| Role | Font | Weight | Notes |
|---|---|---|---|
| Display / H1 | **Fraunces** | 700+ | Tuscan serif. Soft, slightly playful, authoritative. Large scale, wide tracking, amber glow. |
| Headings H2–H4 | **Fraunces** | 600 | Same family, more restrained. |
| Body / Running text | **Lora** | 400/400i | Well-kerned reading serif. 16–18px. Comfortable for longer content. |
| UI / Nav / Labels | **Cinzel** | 400–600 | Engraved Roman. Small-caps, tracked wide. Gravitas without bulk. |
| Printable body | **Lora** | 400 | Clean, readable at print size. |

### Google Fonts Import
```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Lora:ital,wght@0,400;0,600;1,400&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
```

### Typographic Rules
- H1: Fraunces 700, `text-shadow: 0 0 40px rgba(200,144,10,0.4)` amber glow, color `--color-text-strong`
- H2–H4: Fraunces 600, color `--color-text-strong`, letter-spacing `-0.01em`
- Nav links: Cinzel 400, `text-transform: uppercase`, `letter-spacing: 0.08em`, color `--color-text-muted`
- Nav hover: color `--color-accent-light`, `text-shadow: 0 0 12px rgba(245,200,66,0.4)`
- Body: Lora 400, color `--color-text-base`, line-height 1.75
- Links: color `--color-accent-light`, hover: color `--color-magic`

---

## Page Structure

### Header
- Sticky, dark background with blur on scroll
- `background: rgba(10,8,4,0.9)`, `backdrop-filter: blur(18px)`
- Border-bottom: `1px solid --color-border`
- Site title: Fraunces display, color `--color-accent-light`, amber glow
- Navigation: Cinzel small-caps, minimal, right-aligned
- Mobile: hamburger collapses to full-screen dark overlay

### Hero / Landing Section
- Full-width image: use `Monster Slayer's Journal Cover Art.png` or the hero art
- Dark gradient overlay: `linear-gradient(180deg, rgba(10,8,4,0) 0%, rgba(10,8,4,0.9) 100%)`
- Site tagline in large Fraunces, centered, color `--color-text-strong`
- Two CTAs:
  - Primary: "Choose Your Monster" — gold filled button
  - Secondary: "Browse the Bestiary" — outline button, `--color-accent` border

### Monster Index
- Grid of cards (2-col tablet, 3-col desktop)
- Each card:
  - Left-border accent strip in that monster's color (see Monster Color Identity)
  - Monster name in Fraunces 600
  - Sigil/icon centered, large
  - One-line hook from `you_might_be_here_if[0]`
  - Hover: amber glow, slight lift (`translateY(-2px)`)

### Monster Detail Pages
- Full-width banner image with gradient overlay, monster name in huge Fraunces overlaid
- "Start Here" ritual block at top, prominent — not buried below lore
- Lore section in italic Lora, visually set apart (slightly indented, or bordered left)
- Practical tools/rituals in card format below
- Printable CTA at bottom with cyan accent

### Spellbook
- Two-column grid of ritual cards
- Each card: spell name in Fraunces, monster tag(s) in Cinzel small-caps, steps in numbered Lora list
- Ritual elements get `--color-magic` cyan accent treatment

### Printables
- **Lighter treatment — these are for printing**
- Light parchment background in print media, not dark
- Good typography, generous spacing
- Print CSS: hide nav, header, footer; white background; black text
- They are practical artifacts. Don't over-style.

### Footer
- Background: `#070502` (near-black)
- Border-top: `1px solid --color-border`
- Cinzel small-caps, color `--color-text-muted`
- Minimal: copyright, links, nothing more

---

## Texture & Atmosphere

- **Noise overlay on dark backgrounds:** `background-image: url("data:image/svg+xml,...")` or CSS grain at 4–6% opacity — makes flat digital color feel like paper
- **Card hover:** `box-shadow: 0 0 20px rgba(200,144,10,0.25)` — cards warm and lift on hover
- **Section dividers:** `hr` elements get a gold `✦` ornament centered via `::after`
- **Monster accent borders:** Each monster card/page uses its personality color as a left-border or accent ring — see Monster Color Identity table below

---

## Monster Color Identity

Each monster has one personality color used consistently on its card, detail page header, and any tags referencing it across the site. Store these as front matter in each monster's markdown file (`accent_color: "#6b5ae0"`), not hardcoded in CSS.

| Monster | Accent Color | Hex | Personality |
|---|---|---|---|
| Task Hydra | Indigo | `#6b5ae0` | Fractured, multi-headed, overwhelming |
| Temporal Shark | Deep teal | `#1a7a7a` | Cold, relentless, invisible until too late |
| Slumber Troll | Forest green | `#2d6b3a` | Heavy, immovable, warm and deceptive |
| Dopamine Goblin | Warm orange | `#d4721a` | Chaotic, flickering, irresistible |
| Cave Bear | Rust red | `#8b2a2a` | Retreating, protective, isolation-seeking |
| Perfection Wyrm | Dusty gold | `#a08020` | Obsessive, circling, never done |
| Rejection Wisp | Spectral cyan | `#4cc8c8` | Ghostly, social-static, dread-spreading |
| Sensory Storm | Silver-purple | `#7a5aa0` | Overwhelming, electric, input overload |
| Burnout Dragon | Ember | `#8b3a1a` | Depleted, resting, protecting the last coal |

---

## Implementation Rules for Codex

1. **Do not override `--color-page-bg` with a light background on `body {}`.** The dark palette is intentional.
2. **Do not replace the font stack** (Fraunces + Lora + Cinzel) without updating this file and the Google Fonts import in `_layouts/default.html`.
3. **Monster accent colors belong in front matter** (`accent_color` field), not hardcoded in stylesheet rules.
4. **The low-stim theme toggle stays.** It lives in `body.theme-low-stim` CSS overrides. Do not remove it.
5. **Printable pages get print-optimized CSS.** Light backgrounds, black text in `@media print`.
6. **No improvised color choices.** If a color isn't in this system, add it here first.
7. **Typography hierarchy is strict.** H1 = Fraunces 700. H2–H4 = Fraunces 600. Body = Lora. Nav/labels = Cinzel. Do not mix these up.

---

*Last updated: 2026-03-11. Design by Justin Shank. Brief compiled with Wyrd.*
