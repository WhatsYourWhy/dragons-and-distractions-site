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

Tip: run `python scripts/check_printable_links.py` after generating to verify every referenced PDF exists before pushing to Pages.
