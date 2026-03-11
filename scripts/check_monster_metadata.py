from __future__ import annotations

"""Validate monster entry front matter for required product fields."""

from pathlib import Path
import sys
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
MONSTER_DIR = ROOT / "_monsters"
FRONT_MATTER_DELIMITER = "---"
REQUIRED_STRING_FIELDS = (
    "name",
    "plain_name",
    "emoji",
    "tagline",
    "description",
    "challenge_summary",
    "cta",
    "support_boundary",
)
REQUIRED_LIST_FIELDS = (
    "you_might_be_here_if",
    "badges",
    "tags",
)
REQUIRED_LINK_GROUPS = {
    "start_here_ritual": ("label", "url", "description"),
    "featured_printable": ("label", "url", "description"),
}


def extract_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith(FRONT_MATTER_DELIMITER):
        raise ValueError("missing opening front matter delimiter")

    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_DELIMITER:
        raise ValueError("missing opening front matter delimiter")

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == FRONT_MATTER_DELIMITER:
            closing_index = index
            break

    if closing_index is None:
        raise ValueError("front matter is not properly delimited")

    raw_front_matter = "\n".join(lines[1:closing_index])
    data = yaml.safe_load(raw_front_matter.strip())
    if not isinstance(data, dict):
        raise ValueError("front matter must parse to a mapping")
    return data


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_monster_file(path: Path) -> list[str]:
    try:
        data = extract_front_matter(path)
    except ValueError as exc:
        return [f"{path.relative_to(ROOT)}: {exc}"]

    errors: list[str] = []
    rel_path = path.relative_to(ROOT)

    for field in REQUIRED_STRING_FIELDS:
        if not _is_non_empty_string(data.get(field)):
            errors.append(f"{rel_path}: missing non-empty '{field}'")

    for field in REQUIRED_LIST_FIELDS:
        value = data.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{rel_path}: '{field}' must be a non-empty list")
            continue
        if not all(_is_non_empty_string(item) for item in value):
            errors.append(f"{rel_path}: '{field}' must contain only non-empty strings")

    order = data.get("order")
    if not isinstance(order, int):
        errors.append(f"{rel_path}: 'order' must be an integer")

    for field, nested_fields in REQUIRED_LINK_GROUPS.items():
        value = data.get(field)
        if not isinstance(value, dict):
            errors.append(f"{rel_path}: '{field}' must be a mapping")
            continue
        for nested_field in nested_fields:
            if not _is_non_empty_string(value.get(nested_field)):
                errors.append(
                    f"{rel_path}: '{field}.{nested_field}' must be a non-empty string"
                )

    ritual_url = data.get("start_here_ritual", {}).get("url")
    if _is_non_empty_string(ritual_url) and not str(ritual_url).startswith("/spellbook/"):
        errors.append(f"{rel_path}: 'start_here_ritual.url' must point into /spellbook/")

    printable_url = data.get("featured_printable", {}).get("url")
    if _is_non_empty_string(printable_url) and not str(printable_url).startswith(
        "/site/printables/"
    ):
        errors.append(
            f"{rel_path}: 'featured_printable.url' must point into /site/printables/"
        )

    quick_links = data.get("quick_links")
    if quick_links is not None:
        if not isinstance(quick_links, list) or not quick_links:
            errors.append(f"{rel_path}: 'quick_links' must be a non-empty list when present")
        else:
            for index, link in enumerate(quick_links):
                if not isinstance(link, dict):
                    errors.append(f"{rel_path}: 'quick_links[{index}]' must be a mapping")
                    continue
                if not _is_non_empty_string(link.get("label")):
                    errors.append(f"{rel_path}: 'quick_links[{index}].label' is required")
                if not _is_non_empty_string(link.get("url")):
                    errors.append(f"{rel_path}: 'quick_links[{index}].url' is required")

    return errors


def validate_monster_collection(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    names: dict[str, Path] = {}
    plain_names: dict[str, Path] = {}
    orders: dict[int, Path] = {}

    for path in paths:
        file_errors = validate_monster_file(path)
        errors.extend(file_errors)
        if file_errors:
            continue

        data = extract_front_matter(path)
        rel_path = path.relative_to(ROOT)

        name = data["name"]
        if name in names:
            errors.append(
                f"{rel_path}: duplicate name '{name}' also used by {names[name].relative_to(ROOT)}"
            )
        else:
            names[name] = path

        plain_name = data["plain_name"]
        if plain_name in plain_names:
            errors.append(
                f"{rel_path}: duplicate plain_name '{plain_name}' also used by "
                f"{plain_names[plain_name].relative_to(ROOT)}"
            )
        else:
            plain_names[plain_name] = path

        order = data["order"]
        if order in orders:
            errors.append(
                f"{rel_path}: duplicate order '{order}' also used by {orders[order].relative_to(ROOT)}"
            )
        else:
            orders[order] = path

    return errors


def main() -> int:
    monster_files = sorted(MONSTER_DIR.glob("*.md"))
    errors = validate_monster_collection(monster_files)

    if errors:
        print("Monster metadata problems detected:\n")
        for error in errors:
            print(error)
        return 1

    print("Monster metadata looks consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
