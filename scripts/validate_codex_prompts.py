from __future__ import annotations

"""Validate launch-critical content contracts and CODEX-era layout checks."""

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
EXPECTED_HOMEPAGE_HERO_IMAGES = frozenset(
    {
        "/assets/generated/homepage-hero-web.png",
        "/assets/generated/homepage-hero-web.webp",
    }
)
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
    ROOT / "codex" / "index.md",
    ROOT / "spellbook" / "index.md",
    ROOT / "spellbook" / "single-task-oath.md",
    ROOT / "spellbook" / "tide-mark-calendar.md",
    ROOT / "spellbook" / "wake-invocation.md",
    ROOT / "site" / "index.md",
    ROOT / "site" / "printables" / "burnout-dragon-minimum-viable-day.md",
    ROOT / "site" / "printables" / "perfection-wyrm-done-is-better.md",
    ROOT / "site" / "printables" / "rejection-wisp-reply-scaffold.md",
    ROOT / "site" / "printables" / "sensory-storm-reset-card.md",
    ROOT / "site" / "printables" / "single-task-oath-card.md",
    ROOT / "site" / "printables" / "tide-mark-calendar-card.md",
    ROOT / "site" / "printables" / "tide-marks-buddy-ping.md",
    ROOT / "site" / "printables" / "wake-invocation-checklist.md",
    ROOT / "art" / "index.md",
)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return path.name


def _has_non_empty_description(data: dict[str, object]) -> bool:
    value = data.get("description")
    return isinstance(value, str) and bool(value.strip())


def _markdown_body_after_front_matter(path: Path) -> str:
    """Return file content after the closing YAML front matter delimiter, or full text if none."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[index + 1 :])
    return text


def validate_homepage_hero(path: Path = HOMEPAGE_PATH) -> list[str]:
    """CODEX cover+CTA contract when ``hero_actions`` is set; else hub-style hero fields + body CTA."""
    errors: list[str] = []
    if not path.exists():
        return [f"{display_path(path)}: homepage missing"]

    try:
        data = extract_front_matter(path)
    except ValueError as exc:
        return [
            f"{display_path(path)}: invalid or unreadable YAML front matter ({exc})"
        ]
    except yaml.YAMLError as exc:
        return [
            f"{display_path(path)}: invalid or unreadable YAML front matter ({exc})"
        ]

    hero_actions = data.get("hero_actions")
    if isinstance(hero_actions, list):
        if data.get("hero_variant") != "cover":
            errors.append(f"{display_path(path)}: hero_variant must be 'cover'")
        hero_image = data.get("hero_image")
        if hero_image not in EXPECTED_HOMEPAGE_HERO_IMAGES:
            errors.append(
                f"{display_path(path)}: hero_image must point to one of "
                f"{', '.join(sorted(EXPECTED_HOMEPAGE_HERO_IMAGES))}"
            )
        if hero_actions != EXPECTED_HOMEPAGE_ACTIONS:
            errors.append(
                f"{display_path(path)}: hero_actions must exactly match the homepage CTA contract"
            )
        return errors

    for key in ("hero_title", "hero_intro", "hero_image"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"{display_path(path)}: missing non-empty '{key}' in front matter"
            )

    hero_image = data.get("hero_image")
    hero_image_stripped = hero_image.strip() if isinstance(hero_image, str) else ""
    if hero_image_stripped and hero_image_stripped not in EXPECTED_HOMEPAGE_HERO_IMAGES:
        errors.append(
            f"{display_path(path)}: hero_image must point to one of "
            f"{', '.join(sorted(EXPECTED_HOMEPAGE_HERO_IMAGES))}"
        )

    body = _markdown_body_after_front_matter(path)
    if "Choose Your Monster" not in body:
        errors.append(
            f"{display_path(path)}: homepage body must include the Choose Your Monster CTA"
        )

    return errors


def validate_spellbook_directory(path: Path = SPELLBOOK_INDEX) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    keys = tuple(re.findall(r'data-ritual-key="([^"]+)"', text))

    if keys != EXPECTED_RITUAL_KEYS:
        errors.append(
            f"{display_path(path)}: ritual directory keys must exactly match "
            f"{', '.join(EXPECTED_RITUAL_KEYS)}"
        )

    if text.count('class="ritual-library__card"') != len(EXPECTED_RITUAL_KEYS):
        errors.append(
            f"{display_path(path)}: ritual directory must render "
            f"{len(EXPECTED_RITUAL_KEYS)} ritual cards"
        )

    return errors


def validate_monster_index_template(path: Path = MONSTER_INDEX) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    required_snippets = (
        "{% assign monster_hook = monster.you_might_be_here_if | first %}",
        "style=\"--monster-accent: {{ monster.accent_color | default: '#c8900a' }};\"",
        "{{ monster.sigil | relative_url }}",
        'class="monster-card__hook"',
    )

    for snippet in required_snippets:
        if snippet not in text:
            errors.append(
                f"{display_path(path)}: missing monster index contract snippet: {snippet}"
            )

    return errors


def validate_monster_filter_include(path: Path = MONSTER_FILTER_INCLUDE) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    required_snippets = (
        'document.readyState === "loading"',
        'document.addEventListener("DOMContentLoaded", initMonsterIndexFilter, { once: true })',
        "initMonsterIndexFilter();",
    )

    for snippet in required_snippets:
        if snippet not in text:
            errors.append(
                f"{display_path(path)}: missing monster filter init guard snippet: {snippet}"
            )

    return errors


def validate_page_descriptions(paths: tuple[Path, ...] = PAGE_DESCRIPTION_PATHS) -> list[str]:
    errors: list[str] = []

    for path in paths:
        if not path.exists():
            errors.append(f"{display_path(path)}: expected public page is missing")
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

        if not _has_non_empty_description(data):
            errors.append(
                f"{display_path(path)}: missing non-empty top-level description front matter"
            )

    return errors


def validate_header_markup(paths: tuple[Path, ...] = HEADER_INCLUDES) -> list[str]:
    """Check banner snippets and that header partials include ``site-banner`` (no YAML parsing)."""
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
                    errors.append(
                        f"{display_path(path)}: missing header contract snippet: {snippet}"
                    )
            continue

        if "{% include site-banner.html" not in text:
            errors.append(
                f"{display_path(path)}: must render the shared site-banner include"
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
        print("Launch-content validation problems detected:\n")
        for error in errors:
            print(error)
        return 1

    print("Launch-content validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
