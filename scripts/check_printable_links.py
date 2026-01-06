from __future__ import annotations

"""Validate printable links point at generated PDF artifacts.

This checker currently scans Markdown files for PDF links expressed as:
- Standard Markdown links (e.g., ``[text](./printables/pdf/file.pdf)``)
- Inline HTML anchors (``<a href="...">``), including simple Liquid
  ``relative_url`` filters wrapped in ``{{ }}``

It resolves those links relative to the Markdown source, verifies that the
targets live under ``site/printables/pdf/``, and asserts that certain pages
carry specific ritual links. A small YAML bridge pulls expected printable URLs
from ``_data/printables.yml`` for ``site/index.md``. Broader template parsing
for HTML, Liquid, or other data files is not implemented yet.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "site" / "printables" / "pdf"
PRINTABLE_PDF_PARTS = ("site", "printables", "pdf")
YAML_PDF_PREFIX = "/site/printables/pdf/"
SITE_INDEX_RELATIVE_PREFIX = "./printables/pdf/"
LIQUID_RELATIVE_URL_PATTERN = re.compile(
    r"""\{\{\s*["'](?P<path>[^"']+)["']\s*(\|\s*relative_url\s*)?\}\}"""
)


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
    for link in find_link_targets(text):
        normalized = normalize_link_target(link)
        if not normalized.lower().endswith(".pdf"):
            continue

        target = resolve_link_target(normalized, path)
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


def find_html_links(html: str) -> Iterable[str]:
    anchor_pattern = re.compile(
        r"""href\s*=\s*(?P<quote>["'])?(?P<href>\{\{.*?\}\}|[^"' >]+)(?P=quote)?""",
        re.IGNORECASE,
    )
    for match in anchor_pattern.finditer(html):
        yield match.group("href")


def find_link_targets(text: str) -> Iterable[str]:
    yield from find_md_links(text)
    yield from find_html_links(text)


def normalize_link_target(raw_link: str) -> str:
    stripped = raw_link.strip()
    liquid_match = LIQUID_RELATIVE_URL_PATTERN.fullmatch(stripped)
    if liquid_match:
        return liquid_match.group("path")
    return stripped


def resolve_link_target(link: str, source: Path) -> Path:
    if link.startswith("/site/"):
        return (ROOT / link.lstrip("/")).resolve()

    target = Path(link)
    if target.is_absolute():
        return target.resolve()

    return (source.parent / target).resolve()


def extract_yaml_pdf_links(yaml_path: Path) -> list[str]:
    """Extract PDF links from a YAML data file (e.g., _data/printables.yml)."""
    if not yaml:
        return []
    
    if not yaml_path.exists():
        return []
    
    try:
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        links = []
        if isinstance(data, list):
            for group in data:
                if isinstance(group, dict) and "printables" in group:
                    for item in group["printables"]:
                        if isinstance(item, dict):
                            for key in ["ink_pdf", "art_pdf"]:
                                if key in item and item[key]:
                                    links.append(item[key])
        return links
    except (yaml.YAMLError, FileNotFoundError, UnicodeDecodeError):
        return []


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
    
    # For site/index.md, also check YAML data file
    if check.path == Path("site/index.md"):
        yaml_path = ROOT / "_data" / "printables.yml"
        yaml_links = extract_yaml_pdf_links(yaml_path)
        # Convert absolute paths from YAML to relative paths from site/index.md
        for link in yaml_links:
            # YAML links are like /site/printables/pdf/filename.pdf
            # site/index.md needs ./printables/pdf/filename.pdf
            if link.startswith(YAML_PDF_PREFIX):
                relative_link = SITE_INDEX_RELATIVE_PREFIX + link[len(YAML_PDF_PREFIX):]
                links.add(relative_link)

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
