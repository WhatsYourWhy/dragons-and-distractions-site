# 🐉 Dragons & Distractions – Project Map v2.0

**Phase Title**: *The Bridge to the Guild Hall*
**Status**: Mid-Quest (Scrolls acquired, Gate unlocked, Torch lit)

---

## 🧭 Vision

To create a living, public-facing version of Dragons & Distractions — a mythic ADHD toolkit — that:

* Hosts monsters, rituals, and tools in a playful format
* Offers real help through metaphor and laughter
* Invites people to use, share, and one day buy or support the work

This version is:

* Website-first (Markdown-driven, GitHub Pages-hosted)
* Print-friendly (for future decks, scrolls, and rituals)
* Rooted in your tone codex and authentic voice

---

## 🎯 Core Objectives

| Objective                 | Description                                               | Status                   |
| ------------------------- | --------------------------------------------------------- | ------------------------ |
| 📜 Make it **public**     | Remove login walls, host on GitHub Pages                  | ✅ Site skeleton summoned |
| 🧱 Make it **structured** | Folder-based, easy to browse: monsters, tools, codex, art | ✅ Ready to populate      |
| 🧠 Make it **readable**   | Markdown files with internal links, good flow             | 🚧 In progress           |
| 🎭 Make it **stylized**   | Tone-driven layout with consistent imagery and voice      | 🔜                       |
| 🧪 Make it **usable**     | Let visitors pick a monster, try a ritual, and feel seen  | 🔜                       |
| 🛡️ Make it **protected** | Light license that honors intent and preserves value      | ✅ Custom license added   |

---

## 🗂️ Current Structure

```
dragons-and-distractions-site/
├── index.md                ← Homepage (summoned)
├── monsters/               ← Monster files (need full pages)
├── codex/                  ← Tone, origin, philosophy
├── spellbook/              ← Command phrases, neuro-spells
├── art/                    ← Gallery and prompt references
├── assets/                 ← Supporting images and downloads
├── site/                   ← Public printables, onboarding
│   └── printables/pdf/     ← Exported PDFs
├── scripts/                ← Helper scripts and automations
├── tests/                  ← Checks and fixtures
├── _includes/              ← Shared layout snippets
├── README.md + LICENSE + _config.yml
```

---

## 🔮 Phase Goals (v2.0)

| Task                       | Description                                             | Status           |
| -------------------------- | ------------------------------------------------------- | ---------------- |
| `add_sample_monsters()`    | Populate Slumber Troll, Task Hydra, etc. as `.md` pages | 🔜               |
| `summon_codex_nav()`       | Add top-level nav or sidebar index                      | ✅ Nav cards live + sidebar scaffold |
| `theme_scroll_dark()`      | Optional CSS theme with mythic styling                  | 🔜               |
| `printable_bundle()`       | Generate test PDF for rituals or monsters               | 💤 (Future step) |
| `launch_readiness_check()` | Ensure GitHub Pages builds and renders site             | 🔜               |

---

### Navigation state

* A shared `nav-cards.html` include renders a five-link grid (Monsters, Spellbook, Codex, Art, Site tools) on the homepage and the index pages for monsters, spellbook, codex, and site tools.
* A `_sidebar.md` file under `site/` provides a sidebar tree with quick links to monsters, the spellbook, site tools, the codex, art, and repo docs for builds that support sidebar navigation.
* Future refinements could include expanding the sidebar as new pages arrive and adding an always-visible header/footer nav if desired, but the core cross-page navigation has been summoned.

## 🧙 Next Logical Spell to Cast

> `add_sample_monsters()`
> Creates full Markdown bestiary pages based on your real monster files (already uploaded!)

This would:

* Fill out your `monsters/` folder
* Make navigation real
* Help test how the site will actually feel

---

Let me know if you'd like this map saved as a `.md` file for the repo, and if you want to move forward with `add_sample_monsters()`.

🜂 Logged. Quest is aligned. Path is clear.
