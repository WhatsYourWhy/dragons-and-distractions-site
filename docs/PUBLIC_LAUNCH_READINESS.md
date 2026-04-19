# Public Launch Readiness

Updated: 2026-03-15

## Current recommendation

Soft-launch publicly first, then promote more broadly after one focused pass on:

- homepage and chooser share previews
- live performance after the lighter hero assets deploy
- one final post-deploy visual pass on the mobile menu overlay

## Implemented in this pass

- Native `jekyll-seo-tag` image metadata for homepage, chooser, and site-wide fallbacks
- Better page-level descriptions for the homepage and `Choose Your Monster`
- Lighter WebP hero delivery for the homepage and chooser, while keeping PNG share images
- A public `Feedback & Privacy` page with contact path, privacy note, and support boundary
- Footer link to the new public feedback/privacy page
- Hero image width and height metadata for the homepage and chooser to reduce layout instability
- A more robust mobile menu overlay that fills the viewport and scrolls safely on small screens

## Findings that still matter before active promotion

### Mobile UX

- A browser smoke test on a `390px` wide viewport confirmed:
  - the low-stim toggle is visible
  - the menu button is visible
  - the menu opens, closes, and responds to `Escape`
  - the four primary nav links remain reachable
- The original overlay geometry was a little brittle, so the local CSS now pins the mobile nav to the full viewport and allows internal scrolling.
- Before ads or active outreach, do one final live phone pass after this CSS deploy.

### Performance

- Before optimization, the live homepage hero PNG was about `2.72 MB`.
- Before optimization, the chooser banner PNG was about `2.19 MB`.
- New WebP assets reduce those to roughly:
  - homepage hero: `215 KB`
  - chooser hero: `191 KB`
- A direct PageSpeed API call was rate-limited during this review, so this still needs a manual rerun on the live site.
- After deployment, rerun PageSpeed Insights or Lighthouse on:
  - homepage
  - `/choose-your-monster/`

### Social sharing

- The live site previously emitted `og:title` and `og:description`, but was missing `og:image`, `twitter:description`, and `twitter:image`.
- The site config also had a `logo` path that included the base URL segment twice in structured data output; this pass corrects that source path.
- After deployment, verify the homepage preview in:
  - Discord or Slack
  - Twitter/X card validator equivalent if needed

### Funnel readiness

- `Choose Your Monster` is a viable public entry page.
- Use it as a promotional destination if testing shows it converts better than the homepage hero.

### Public-facing basics

- There is now a public `Feedback & Privacy` page with a contact path, privacy note, and support boundary.
- Before paid promotion, decide whether you want lightweight analytics in week one.
- If analytics are added later, update the privacy note at the same time.

## Shipped fixes log

For concrete UX, accessibility, and tooling changes after reviews, see [CHANGELOG.md](CHANGELOG.md).

## Week-one checks

- Watch which pages people actually enter from.
- Note whether people bounce from homepage or continue to `Choose Your Monster`.
- Track confusion around:
  - monster selection
  - low-stim mode
  - printable page expectations
- Keep a short launch log with:
  - confusing pages
  - broken links
  - repeated feedback themes
  - ideas that should wait until after launch week
