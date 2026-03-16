from __future__ import annotations

"""Validate the repo contracts introduced while working through CODEX_PROMPTS.md."""

from pathlib import Path
import re
import sys

CURRENT_ROOT = Path(__file__).resolve().parent.parent
if str(CURRENT_ROOT) not in sys.path:
    sys.path.insert(0, str(CURRENT_ROOT))

from scripts.check_monster_metadata import ROOT, extract_front_matter


HOMEPAGE_PATH = ROOT / "index.md"
SPELLBOOK_INDEX = ROOT / "spellbook" / "index.md"
MONSTER_INDEX = ROOT / "monsters" / "index.md"
HEADER_INCLUDES = (
    ROOT / "_includes" / "site-header.html",
    ROOT / "_includes" / "header-nav.html",
    ROOT / "_includes" / "site-banner.html",
)
EXPECTED_HOMEPAGE_ACTIONS = [
    {"label": "Choose Your Monster", "url": "/choose-your-monster/", "style": "primary"},
    {"label": "Browse the Bestiary", "url": "/monsters/", "style": "secondary"},
]
EXPECTED_RITUAL_KEYS = (
    "task-hydra",
    "temporal-shark",
    "slumber-troll",
    "cave-bear",
    "dopamine-goblin",
    "perfection-wyrm",
    "rejection-wisp",
    "sensory-storm",
    "burnout-dragon",
)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return path.name


def validate_homepage_hero(path: Path = HOMEPAGE_PATH) -> list[str]:
    data = extract_front_matter(path)
    errors: list[str] = []

    if data.get("hero_variant") != "cover":
        errors.append(f"{display_path(path)}: hero_variant must be 'cover'")
    if data.get("hero_image") != "/assets/generated/homepage-hero-web.png":
        errors.append(f"{display_path(path)}: hero_image must point to /assets/generated/homepage-hero-web.png")

    actions = data.get("hero_actions")
    if actions != EXPECTED_HOMEPAGE_ACTIONS:
        errors.append(
            f"{display_path(path)}: hero_actions must exactly match the homepage CTA contract"
        )

    return errors


def validate_spellbook_directory(path: Path = SPELLBOOK_INDEX) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    keys = tuple(re.findall(r'data-ritual-key="([^"]+)"', text))

    if keys != EXPECTED_RITUAL_KEYS:
        errors.append(
            f"{display_path(path)}: ritual directory keys must exactly match {', '.join(EXPECTED_RITUAL_KEYS)}"
        )

    if text.count('class="ritual-library__card"') != len(EXPECTED_RITUAL_KEYS):
        errors.append(
            f"{display_path(path)}: ritual directory must render {len(EXPECTED_RITUAL_KEYS)} ritual cards"
        )

    return errors


def validate_monster_index_template(path: Path = MONSTER_INDEX) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    required_snippets = (
        '{% assign monster_hook = monster.you_might_be_here_if | first %}',
        'style="--monster-accent: {{ monster.accent_color | default: \'#c8900a\' }};"',
        '{{ monster.sigil | relative_url }}',
        'class="monster-card__hook"',
    )

    for snippet in required_snippets:
        if snippet not in text:
            errors.append(f"{display_path(path)}: missing monster index contract snippet: {snippet}")

    return errors


def validate_header_markup(paths: tuple[Path, ...] = HEADER_INCLUDES) -> list[str]:
    errors: list[str] = []
    required_snippets = (
        "js-theme-toggle",
        "js-menu-toggle",
        "site-banner__menu-toggle",
        "site-navigation",
    )

    for path in paths:
        text = path.read_text(encoding="utf-8")
        if path.name == "site-banner.html":
            for snippet in required_snippets:
                if snippet not in text:
                    errors.append(f"{display_path(path)}: missing header contract snippet: {snippet}")
            continue

        if "{% include site-banner.html" not in text:
            errors.append(f"{display_path(path)}: must render the shared site-banner include")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_homepage_hero())
    errors.extend(validate_spellbook_directory())
    errors.extend(validate_monster_index_template())
    errors.extend(validate_header_markup())

    if errors:
        print("CODEX prompt validation problems detected:\n")
        for error in errors:
            print(error)
        return 1

    print("CODEX prompt validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
