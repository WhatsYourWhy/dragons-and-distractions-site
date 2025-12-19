from __future__ import annotations

"""Validate printable links point at generated PDF artifacts."""

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "site" / "printables" / "pdf"
PRINTABLE_PDF_PARTS = ("site", "printables", "pdf")


@dataclass
class LinkCheck:
    path: Path
    required_links: list[str]


CHECKS: list[LinkCheck] = [
    LinkCheck(
        path=Path("site/index.md"),
        required_links=[
            "./printables/pdf/single-task-oath-card-ink.pdf",
            "./printables/pdf/single-task-oath-card-art.pdf",
            "./printables/pdf/tide-mark-calendar-card-ink.pdf",
            "./printables/pdf/tide-mark-calendar-card-art.pdf",
            "./printables/pdf/tide-marks-buddy-ping-ink.pdf",
            "./printables/pdf/tide-marks-buddy-ping-art.pdf",
            "./printables/pdf/wake-invocation-checklist-ink.pdf",
            "./printables/pdf/wake-invocation-checklist-art.pdf",
        ],
    ),
    LinkCheck(
        path=Path("spellbook/index.md"),
        required_links=[
            "../site/printables/pdf/single-task-oath-card-ink.pdf",
            "../site/printables/pdf/single-task-oath-card-art.pdf",
            "../site/printables/pdf/tide-mark-calendar-card-ink.pdf",
            "../site/printables/pdf/tide-mark-calendar-card-art.pdf",
            "../site/printables/pdf/tide-marks-buddy-ping-ink.pdf",
            "../site/printables/pdf/tide-marks-buddy-ping-art.pdf",
            "../site/printables/pdf/wake-invocation-checklist-ink.pdf",
            "../site/printables/pdf/wake-invocation-checklist-art.pdf",
        ],
    ),
    LinkCheck(
        path=Path("spellbook/single-task-oath.md"),
        required_links=["../site/printables/pdf/single-task-oath-card-ink.pdf"],
    ),
    LinkCheck(
        path=Path("spellbook/tide-mark-calendar.md"),
        required_links=[
            "../site/printables/pdf/tide-mark-calendar-card-ink.pdf",
            "../site/printables/pdf/tide-marks-buddy-ping-ink.pdf",
        ],
    ),
    LinkCheck(
        path=Path("spellbook/wake-invocation.md"),
        required_links=["../site/printables/pdf/wake-invocation-checklist-ink.pdf"],
    ),
]


def find_pdf_links(path: Path) -> list[Path]:
    links: list[Path] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for link in find_md_links(text):
        if not link.lower().endswith(".pdf"):
            continue

        target = (path.parent / link).resolve()
        try:
            rel_target = target.relative_to(ROOT)
        except ValueError:
            # Outside the repository; it will be flagged later as broken.
            links.append(target)
            continue

        if rel_target.parts[:3] == PRINTABLE_PDF_PARTS:
            links.append(target)
    return links


def find_md_links(markdown: str) -> Iterable[str]:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for match in link_pattern.finditer(markdown):
        yield match.group(1)


def ensure_pdf_directory_exists(pdf_dir: Path) -> list[str]:
    if pdf_dir.exists():
        return []
    return [f"Missing PDF output directory: {pdf_dir}"]


def check_required_links(check: LinkCheck) -> list[str]:
    resolved_path = check.path if check.path.is_absolute() else ROOT / check.path

    if not resolved_path.exists():
        return [f"File not found: {resolved_path}"]

    content = resolved_path.read_text(encoding="utf-8")
    links = set(find_md_links(content))

    errors: list[str] = []
    for required in check.required_links:
        if required not in links:
            errors.append(f"{resolved_path}: missing link to {required}")

    return errors


def check_broken_pdf_links(markdown_files: list[Path]) -> list[str]:
    missing: dict[Path, list[str]] = {}

    for md_file in markdown_files:
        pdf_links = find_pdf_links(md_file)
        broken = []
        for target in pdf_links:
            try:
                target.relative_to(ROOT)
            except ValueError:
                broken.append(f"{target} (outside repo)")
                continue
            if not target.exists():
                broken.append(str(target.relative_to(ROOT)))
        if broken:
            missing[md_file.relative_to(ROOT)] = broken

    errors: list[str] = []
    for md_path, issues in missing.items():
        errors.append(f"{md_path}:")
        for issue in issues:
            errors.append(f"  • {issue}")

    return errors


def report_orphaned_pdfs(pdf_dir: Path, referenced: set[Path]) -> None:
    orphaned = [path.relative_to(ROOT) for path in pdf_dir.glob("*.pdf") if path.relative_to(ROOT) not in referenced]
    if orphaned:
        print("Orphaned PDFs (not linked in markdown):")
        for pdf in sorted(orphaned):
            print(f"- {pdf}")


def main() -> int:
    markdown_files = list(ROOT.glob("**/*.md"))
    errors: list[str] = []

    errors.extend(ensure_pdf_directory_exists(PDF_DIR))
    errors.extend(check_broken_pdf_links(markdown_files))

    for check in CHECKS:
        errors.extend(check_required_links(check))

    if errors:
        print("Broken PDF links detected:\n")
        for error in errors:
            print(error)
        print(
            "\nHint: ritual PDFs are gitignored; run `python scripts/generate_printable_pdfs.py` "
            "to place fresh copies before publishing."
        )
        return 1

    referenced = {link.relative_to(ROOT) for md in markdown_files for link in find_pdf_links(md)}
    print("All referenced PDF links exist.")
    if referenced:
        report_orphaned_pdfs(PDF_DIR, referenced)
    else:
        print("No PDF links found in markdown.")

    print("Printable links are pointing at build-generated PDFs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
