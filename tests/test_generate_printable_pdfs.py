from pathlib import Path

from pypdf import PdfReader

from scripts import generate_printable_pdfs as pdfs


def test_parse_printable_extracts_intro_and_sections():
    printable = pdfs.parse_printable(Path("site/printables/single-task-oath-card.md"))

    assert printable.title == "Single-Task Oath"
    assert printable.hero_intro
    assert printable.sections
    assert printable.sections[0].title == "How to use it"


def test_build_pdf_creates_readable_output(tmp_path: Path):
    printable = pdfs.parse_printable(Path("site/printables/rejection-wisp-reply-scaffold.md"))
    output = tmp_path / "reply-scaffold.pdf"

    pdfs.build_pdf(printable, output)

    assert output.exists()
    assert output.stat().st_size > 0
    assert len(PdfReader(str(output)).pages) >= 1
