from __future__ import annotations

"""Validate launch-critical content contracts for public-facing pages."""

from pathlib import Path
import sys


CURRENT_ROOT = Path(__file__).resolve().parent.parent
if str(CURRENT_ROOT) not in sys.path:
    sys.path.insert(0, str(CURRENT_ROOT))

from scripts.check_monster_metadata import ROOT, extract_front_matter


PAGE_DESCRIPTION_PATHS = (
    ROOT / "index.md",
    ROOT / "choose-your-monster.md",
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
)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return path.name


def _has_non_empty_description(path: Path) -> bool:
    data = extract_front_matter(path)
    value = data.get("description")
    return isinstance(value, str) and bool(value.strip())


def validate_page_descriptions(paths: tuple[Path, ...] = PAGE_DESCRIPTION_PATHS) -> list[str]:
    errors: list[str] = []

    for path in paths:
        if not path.exists():
            errors.append(f"{display_path(path)}: expected public page is missing")
            continue

        if not _has_non_empty_description(path):
            errors.append(f"{display_path(path)}: missing non-empty top-level description front matter")

    return errors


def main() -> int:
    errors = validate_page_descriptions()

    if errors:
        print("Launch-content validation problems detected:\n")
        for error in errors:
            print(error)
        return 1

    print("Launch-content validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
