from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "site" / "printables" / "pdf"
PDF_PATTERN = re.compile(r"\(([^)]+site/printables/pdf/[^)]+\.pdf)\)")


def find_pdf_links(path: Path) -> list[Path]:
    links: list[Path] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for match in PDF_PATTERN.finditer(text):
        link = match.group(1)
        target = (path.parent / link).resolve()
        links.append(target)
    return links


def main():
    markdown_files = list(ROOT.glob("**/*.md"))
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

    if missing:
        print("Broken PDF links detected:\n")
        for md_path, issues in missing.items():
            print(f"- {md_path}:")
            for issue in issues:
                print(f"  • {issue}")
        print("\nHint: ritual PDFs are gitignored; run `python scripts/generate_printable_pdfs.py` to place fresh copies before publishing.")
        raise SystemExit(1)

    referenced = {link.relative_to(ROOT) for md in markdown_files for link in find_pdf_links(md)}
    orphaned = [path.relative_to(ROOT) for path in PDF_DIR.glob("*.pdf") if path.relative_to(ROOT) not in referenced]

    print("All referenced PDF links exist.")
    if orphaned:
        print("Orphaned PDFs (not linked in markdown):")
        for pdf in sorted(orphaned):
            print(f"- {pdf}")
    else:
        print("All PDFs are linked from markdown.")


if __name__ == "__main__":
    main()
