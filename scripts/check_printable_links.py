from __future__ import annotations

"""Validate printable links point at generated PDF artifacts.

This checker scans Markdown and HTML files for PDF links expressed as:
- Standard Markdown links (e.g., ``[text](./printables/pdf/file.pdf)``)
- Inline HTML anchors (``<a href="...">``) that appear in Markdown/HTML
  sources, including Liquid ``relative_url`` filters wrapped in ``{{ }}``

It resolves those links relative to the source file, verifies that the targets
live under ``site/printables/pdf/``, and asserts that certain pages carry
specific ritual links. YAML data files are also scanned so data-driven printables
stay covered by the link checker.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable, TypeAlias

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "site" / "printables" / "pdf"
PRINTABLE_PDF_PARTS = ("site", "printables", "pdf")
PRINTABLE_PAGE_PARTS = ("site", "printables")
MONSTER_DIR = "_monsters"
YAML_PDF_PREFIX = "/site/printables/pdf/"
SITE_INDEX_RELATIVE_PREFIX = "./printables/pdf/"
LIQUID_RELATIVE_URL_PATTERN = re.compile(
    r"""\{\{\s*["'](?P<path>[^"']+)["']\s*(\|\s*relative_url\s*)?\}\}"""
)
URL_SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")

SKIPPED_PATH_PARTS = frozenset(
    {
        ".git",
        ".claude",
        "tmp",
        ".pytest_cache",
        ".venv",
        "venv",
        "vendor",
        ".bundle",
        "_site",
        "__pycache__",
    }
)

LinkTarget: TypeAlias = Path | str


@dataclass
class LinkCheck:
    path: Path
    required_links: list[str]


CHECKS: list[LinkCheck] = [
    LinkCheck(
        path=Path("site/index.md"),
        required_links=[
            "./printables/pdf/single-task-oath-card-ink.pdf",
            "./printables/pdf/tide-mark-calendar-card-ink.pdf",
            "./printables/pdf/tide-marks-buddy-ping-ink.pdf",
            "./printables/pdf/wake-invocation-checklist-ink.pdf",
            "./printables/pdf/perfection-wyrm-done-is-better-ink.pdf",
            "./printables/pdf/rejection-wisp-reply-scaffold-ink.pdf",
            "./printables/pdf/sensory-storm-reset-card-ink.pdf",
            "./printables/pdf/burnout-dragon-minimum-viable-day-ink.pdf",
        ],
    ),
    LinkCheck(
        path=Path("spellbook/index.md"),
        required_links=[
            "../site/printables/pdf/single-task-oath-card-ink.pdf",
            "../site/printables/pdf/tide-mark-calendar-card-ink.pdf",
            "../site/printables/pdf/tide-marks-buddy-ping-ink.pdf",
            "../site/printables/pdf/wake-invocation-checklist-ink.pdf",
            "../site/printables/pdf/perfection-wyrm-done-is-better-ink.pdf",
            "../site/printables/pdf/rejection-wisp-reply-scaffold-ink.pdf",
            "../site/printables/pdf/sensory-storm-reset-card-ink.pdf",
            "../site/printables/pdf/burnout-dragon-minimum-viable-day-ink.pdf",
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


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def display_outside_target(target: LinkTarget) -> str:
    if isinstance(target, str):
        return target
    raw = str(target)
    normalized = raw.replace("\\", "/")
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]+:/", normalized) or normalized.startswith("//"):
        return normalized
    return raw


def iter_content_files(root: Path) -> list[Path]:
    """Markdown and HTML under root, excluding tooling and cache directories."""
    paths: list[Path] = []
    for pattern in ("**/*.md", "**/*.html"):
        for path in sorted(root.glob(pattern)):
            try:
                rel = path.relative_to(root)
            except ValueError:
                continue
            if SKIPPED_PATH_PARTS.intersection(rel.parts):
                continue
            paths.append(path)
    return paths


def find_pdf_links(path: Path, *, include_non_printables: bool = False) -> list[LinkTarget]:
    links: list[LinkTarget] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for link in find_link_targets(text):
        normalized = normalize_link_target(link)
        if not normalized.lower().endswith(".pdf"):
            continue

        target = resolve_link_target(normalized, path)
        if isinstance(target, str):
            links.append(target)
            continue

        try:
            rel_target = target.relative_to(ROOT)
        except ValueError:
            links.append(target)
            continue

        if include_non_printables or rel_target.parts[:3] == PRINTABLE_PDF_PARTS:
            links.append(target)
    return links


def find_printable_page_links(path: Path) -> list[Path]:
    links: list[Path] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for link in find_link_targets(text):
        normalized = normalize_link_target(link)
        if normalized.lower().endswith(".pdf"):
            continue

        target = resolve_link_target(normalized, path)
        if isinstance(target, str):
            continue

        try:
            rel_target = target.relative_to(ROOT)
        except ValueError:
            continue

        if rel_target.parts[:2] != PRINTABLE_PAGE_PARTS:
            continue
        if len(rel_target.parts) < 3 or rel_target.parts[2] == "pdf":
            continue
        if target.suffix.lower() != ".html":
            continue

        links.append(target)
    return links


def find_md_links(markdown: str) -> Iterable[str]:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for match in link_pattern.finditer(markdown):
        yield match.group(1)


def find_html_links(html: str) -> Iterable[str]:
    anchor_pattern = re.compile(
        r"""href\s*=\s*(?P<quote>["'])?(?P<href>\{\{.*?\}\}|[^"' >]+)(?P=quote)?""",
        re.IGNORECASE | re.DOTALL,
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


def resolve_link_target(link: str, source: Path) -> LinkTarget:
    if URL_SCHEME_PATTERN.match(link) or link.startswith("//"):
        return link

    if link.startswith("/site/"):
        return (ROOT / link.lstrip("/")).resolve()

    if link.startswith(("/", "\\")):
        return Path(link)

    target = Path(link)
    if target.is_absolute():
        return target

    return (source.parent / target).resolve()


def extract_yaml_pdf_links(yaml_path: Path) -> list[str]:
    """Extract PDF links from nested YAML structures."""
    if not yaml:
        return []

    if not yaml_path.exists():
        return []

    def walk(node) -> list[str]:
        if isinstance(node, dict):
            links: list[str] = []
            for value in node.values():
                links.extend(walk(value))
            return links
        if isinstance(node, list):
            links: list[str] = []
            for item in node:
                links.extend(walk(item))
            return links
        if isinstance(node, str) and node.lower().endswith(".pdf"):
            return [node]
        return []

    try:
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return walk(data)
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
    links: set[LinkTarget] = set()
    for link in find_link_targets(content):
        normalized = normalize_link_target(link)
        links.add(resolve_link_target(normalized, resolved_path))

    if check.path == Path("site/index.md"):
        yaml_path = ROOT / "_data" / "printables.yml"
        yaml_links = extract_yaml_pdf_links(yaml_path)
        for link in yaml_links:
            if link.startswith(YAML_PDF_PREFIX):
                relative_link = SITE_INDEX_RELATIVE_PREFIX + link[len(YAML_PDF_PREFIX):]
                links.add(resolve_link_target(relative_link, resolved_path))

    errors: list[str] = []
    for required in check.required_links:
        required_target = resolve_link_target(required, resolved_path)
        if required_target not in links:
            errors.append(f"{resolved_path}: missing link to {required}")

    return errors

def check_broken_pdf_links(
    content_files: list[Path], *, require_existing_pdfs: bool = True
) -> list[str]:
    missing: dict[str, list[str]] = {}

    for md_file in content_files:
        pdf_links = find_pdf_links(md_file, include_non_printables=True)
        printable_page_links = find_printable_page_links(md_file)
        broken = []
        for target in pdf_links:
            if isinstance(target, str):
                broken.append(f"{display_outside_target(target)} (outside repo)")
                continue

            try:
                rel_target = target.relative_to(ROOT)
            except ValueError:
                broken.append(f"{display_outside_target(target)} (outside repo)")
                continue

            if rel_target.parts[:3] != PRINTABLE_PDF_PARTS:
                broken.append(f"{display_path(ROOT / rel_target)} (unexpected location)")
                continue

            if require_existing_pdfs and not target.exists():
                broken.append(display_path(ROOT / rel_target))

        if (
            MONSTER_DIR in md_file.relative_to(ROOT).parts
            and not pdf_links
            and not printable_page_links
        ):
            broken.append("missing printable link for monster entry")

        if broken:
            try:
                missing[md_file.relative_to(ROOT)] = broken
            except ValueError:
                missing[md_file] = broken

    errors: list[str] = []
    for md_path, issues in missing.items():
        errors.append(f"{display_path(md_path)}:")
        for issue in issues:
            errors.append(f"  • {issue}")

    return errors


def check_yaml_pdf_links(
    yaml_files: list[Path], *, require_existing_pdfs: bool = True
) -> list[str]:
    missing: dict[str, list[str]] = {}

    for yaml_file in yaml_files:
        pdf_links = extract_yaml_pdf_links(yaml_file)
        if not pdf_links:
            continue

        broken = []
        for link in pdf_links:
            target = resolve_link_target(link, yaml_file)
            if isinstance(target, str):
                broken.append(f"{display_outside_target(target)} (outside repo)")
                continue

            try:
                rel_target = target.relative_to(ROOT)
            except ValueError:
                broken.append(f"{display_outside_target(target)} (outside repo)")
                continue

            if rel_target.parts[:3] != PRINTABLE_PDF_PARTS:
                broken.append(f"{display_path(ROOT / rel_target)} (unexpected location)")
                continue

            if require_existing_pdfs and not target.exists():
                broken.append(display_path(ROOT / rel_target))

        if broken:
            missing[display_path(yaml_file)] = broken

    errors: list[str] = []
    for yaml_display, issues in missing.items():
        errors.append(f"{yaml_display}:")
        for issue in issues:
            errors.append(f"  • {issue}")

    return errors


def report_orphaned_pdfs(pdf_dir: Path, referenced: set[Path]) -> None:
    orphaned = [
        path.relative_to(ROOT)
        for path in pdf_dir.glob("*.pdf")
        if path.relative_to(ROOT) not in referenced
    ]
    if orphaned:
        print("Orphaned PDFs (not linked in content files):")
        for pdf in sorted(orphaned):
            print(f"- {display_path(pdf)}")


def main() -> int:
    content_files = iter_content_files(ROOT)
    data_files = sorted(ROOT.glob("_data/*.yml"))
    errors: list[str] = []
    pdfs_generated = any(PDF_DIR.glob("*.pdf"))

    errors.extend(ensure_pdf_directory_exists(PDF_DIR))
    errors.extend(
        check_broken_pdf_links(content_files, require_existing_pdfs=pdfs_generated)
    )
    errors.extend(
        check_yaml_pdf_links(data_files, require_existing_pdfs=pdfs_generated)
    )

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

    if not pdfs_generated:
        print("Printable PDF artifacts not found; skipping existence check.")
        return 0

    referenced: set[Path] = set()
    for md in content_files:
        for link in find_pdf_links(md):
            if isinstance(link, str):
                continue
            try:
                referenced.add(link.relative_to(ROOT))
            except ValueError:
                continue
    for data_file in data_files:
        for link in extract_yaml_pdf_links(data_file):
            resolved = resolve_link_target(link, data_file)
            if isinstance(resolved, str):
                continue
            try:
                referenced.add(resolved.relative_to(ROOT))
            except ValueError:
                continue

    print("All referenced PDF links exist.")
    if referenced:
        report_orphaned_pdfs(PDF_DIR, referenced)
    else:
        print("No PDF links found in markdown.")

    print("Printable links are pointing at build-generated PDFs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
