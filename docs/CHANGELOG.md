# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Optional hub hero AVIF source via page front matter `hero_image_avif` in `_layouts/hub.html` (WebP and fallbacks unchanged when unset).
- Monster index client-side filter (`_includes/monster-index-filter.html`) with live status for screen readers.
- Global “Back to top” control (fixed button, respects `prefers-reduced-motion`, hidden when mobile nav overlay is open).
- `CHANGELOG.md` and `ARCHITECTURE.md` for release notes and system orientation.

### Changed

- Choose Your Monster oracle scrolls the active result into view after selection (narrow vs wide `block` behavior; honors reduced motion).
- Low-stimulus theme palette and oracle index styling adjusted for stronger text and control contrast (WCAG AA target for normal text).
- Low Stim header control now uses `role="switch"` and `aria-checked` instead of `aria-pressed`.
- Oracle choice buttons use visible `:focus-visible` rings; theme toggle gains a dedicated `:focus-visible` outline.
- Hub pages: `description` and hero `width`/`height` for Spellbook, Printables (site index), Codex, and Monster Index; Art index `description`.
- `<main id="main-content">` uses `tabindex="-1"` so focus can move to content after “Back to top”.

### Documentation

- `PUBLIC_LAUNCH_READINESS.md` links to this changelog for shipped remediation work.
