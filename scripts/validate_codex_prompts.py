from __future__ import annotations

"""Validate the repo contracts introduced while working through CODEX_PROMPTS.md."""

from pathlib import Path
import re
import sys

import yaml

CURRENT_ROOT = Path(__file__).resolve().parent.parent
if str(CURRENT_ROOT) not in sys.path:
    sys.path.insert(0, str(CURRENT_ROOT))

from scripts.check_monster_metadata import ROOT, extract_front_matter


HOMEPAGE_PATH = ROOT / "index.md"
SPELLBOOK_INDEX = ROOT / "spellbook" / "index.md"
MONSTER_INDEX = ROOT / "monsters" / "index.md"
MONSTER_FILTER_INCLUDE = ROOT / "_includes" / "monster-index-filter.html"
HEADER_INCLUDES = (
    ROOT / "_includes" / "site-header.html",
    ROOT / "_includes" / "header-nav.html",
    ROOT / "_includes" / "site-banner.html",
)
EXPECTED_HOMEPAGE_ACTIONS = [
    {"label": "Choose Your Monster", "url": "/choose-your-monster/", "style": "primary"},
    {"label": "Browse the Bestiary", "url": "/monsters/", "style": "secondary"},
]
EXPECTED_HOMEPAGE_HERO_IMAGES = {
    "/assets/generated/homepage-hero-web.png",
    "/assets/generated/homepage-hero-web.webp",
}
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
PAGE_DESCRIPTION_PATHS = (
    ROOT / "index.md",
    ROOT / "choose-your-monster.md",
    ROOT / "feedback.md",
    ROOT / "404.md",
    ROOT / "monsters" / "index.md",
    ROOT / "spellbook" / "index.md",
    ROOT / "spellbook" / "wake-invocation.md",
    ROOT / "spellbook" / "tide-mark-calendar.md",
    ROOT / "spellbook" / "single-task-oath.md",
    ROOT / "site" / "index.md",
    ROOT / "site" / "printables" / "wake-invocation-checklist.md",
    ROOT / "site" / "printables" / "single-task-oath-card.md",
    ROOT / "site" / "printables" / "sensory-storm-reset-card.md",
    ROOT / "site" / "printables" / "burnout-dragon-minimum-viable-day.md",
    ROOT / "site" / "printables" / "rejection-wisp-reply-scaffold.md",
    ROOT / "site" / "printables" / "tide-mark-calendar-card.md",
    ROOT / "site" / "printables" / "tide-marks-buddy-ping.md",
    ROOT / "site" / "printables" / "perfection-wyrm-done-is-better.md",
    ROOT / "codex" / "index.md",
    ROOT / "art" / "index.md",
)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return path.name


def validate_page_descriptions(paths: tuple[Path, ...] = PAGE_DESCRIPTION_PATHS) -> list[str]:
    errors: list[str] = []

    for path in paths:
        data = extract_front_matter(path)
        if not _has_non_empty_description(data):
            errors.append(f"{display_path(path)}: missing non-empty top-level description front matter")

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

        try:
            data = extract_front_matter(path)
        except ValueError as exc:
            errors.append(
                f"{display_path(path)}: invalid or unreadable YAML front matter ({exc})"
            )
            continue
        except yaml.YAMLError as exc:
            errors.append(
                f"{display_path(path)}: invalid or unreadable YAML front matter ({exc})"
            )
            continue

        value = data.get("description")
        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"{display_path(path)}: missing non-empty top-level description front matter"
            )

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_homepage_hero())
    errors.extend(validate_spellbook_directory())
    errors.extend(validate_monster_index_template())
    errors.extend(validate_monster_filter_include())
    errors.extend(validate_page_descriptions())
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
