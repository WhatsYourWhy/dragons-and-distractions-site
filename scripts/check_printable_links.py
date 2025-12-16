"""Validate printable links point at generated PDF artifacts.

This helper keeps the public-facing links aimed at build outputs instead of
tracked Markdown sources. It does **not** require the PDFs to exist locally;
the build pipeline is responsible for producing them in `site/printables/pdf/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable


@dataclass
class LinkCheck:
    path: Path
    required_links: list[str]


CHECKS: list[LinkCheck] = [
    LinkCheck(
        path=Path("site/index.md"),
        required_links=[
            "./printables/pdf/single-task-oath-card.pdf",
            "./printables/pdf/tide-mark-calendar-card.pdf",
            "./printables/pdf/tide-marks-buddy-ping.pdf",
            "./printables/pdf/wake-invocation-checklist.pdf",
        ],
    ),
    LinkCheck(
        path=Path("spellbook/index.md"),
        required_links=[
            "../site/printables/pdf/single-task-oath-card.pdf",
            "../site/printables/pdf/tide-mark-calendar-card.pdf",
            "../site/printables/pdf/tide-marks-buddy-ping.pdf",
            "../site/printables/pdf/wake-invocation-checklist.pdf",
        ],
    ),
    LinkCheck(
        path=Path("spellbook/single-task-oath.md"),
        required_links=["../site/printables/pdf/single-task-oath-card.pdf"],
    ),
    LinkCheck(
        path=Path("spellbook/tide-mark-calendar.md"),
        required_links=[
            "../site/printables/pdf/tide-mark-calendar-card.pdf",
            "../site/printables/pdf/tide-marks-buddy-ping.pdf",
        ],
    ),
    LinkCheck(
        path=Path("spellbook/wake-invocation.md"),
        required_links=["../site/printables/pdf/wake-invocation-checklist.pdf"],
    ),
]


def find_md_links(markdown: str) -> Iterable[str]:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for match in link_pattern.finditer(markdown):
        yield match.group(1)


def ensure_pdf_directory_exists(pdf_dir: Path) -> list[str]:
    if pdf_dir.exists():
        return []
    return [f"Missing PDF output directory: {pdf_dir}"]


def check_required_links(check: LinkCheck) -> list[str]:
    if not check.path.exists():
        return [f"File not found: {check.path}"]

    content = check.path.read_text(encoding="utf-8")
    links = set(find_md_links(content))

    errors: list[str] = []
    for required in check.required_links:
        if required not in links:
            errors.append(f"{check.path}: missing link to {required}")

    legacy_links = [
        link
        for link in links
        if link.startswith("../site/printables/") and link.endswith(".md")
    ]
    if legacy_links:
        formatted = ", ".join(sorted(legacy_links))
        errors.append(f"{check.path}: update printable links to PDFs (found {formatted})")

    return errors


def main() -> int:
    errors: list[str] = []

    errors.extend(ensure_pdf_directory_exists(Path("site/printables/pdf")))

    for check in CHECKS:
        errors.extend(check_required_links(check))

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Printable links are pointing at build-generated PDFs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
