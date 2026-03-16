from pathlib import Path

import pytest

import scripts.generate_printable_pdfs as printable_pdfs


NAV_MARKER = printable_pdfs.NAV_MARKERS[0]
cleaned_lines = printable_pdfs.cleaned_lines


@pytest.mark.parametrize("nav_line", [NAV_MARKER, f"## {NAV_MARKER}"])
def test_cleaned_lines_ignores_quick_navigation_sections(nav_line: str, tmp_path: Path):
    markdown = tmp_path / "demo.md"
    markdown.write_text(
        "\n".join(
            [
                "# Title",
                "Lead-in sentence.",
                nav_line,
                "- link one",
                "- link two",
                "Post-navigation content",
            ]
        ),
        encoding="utf-8",
    )

    lines = list(cleaned_lines(markdown))

    assert lines == ["Title", "Lead-in sentence."]


def test_cleaned_lines_skips_front_matter_and_download_links(tmp_path: Path):
    markdown = tmp_path / "demo.md"
    markdown.write_text(
        "\n".join(
            [
                "---",
                'title: "Demo"',
                "ink_pdf: /site/printables/pdf/demo-ink.pdf",
                "---",
                "",
                "Lead-in sentence.",
                "**Downloads:** [Ink-friendly PDF](./pdf/demo-ink.pdf)",
                "",
                "## Section",
                "- item one",
            ]
        ),
        encoding="utf-8",
    )

    lines = list(cleaned_lines(markdown))

    assert lines == ["Lead-in sentence.", "", "Section", "item one"]


def test_get_fpdf_dependencies_raises_helpful_error_when_missing(monkeypatch):
    real_import = __import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "fpdf" or name.startswith("fpdf."):
            raise ModuleNotFoundError("No module named 'fpdf'")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr("builtins.__import__", fake_import)

    with pytest.raises(SystemExit, match="Missing dependency 'fpdf2'"):
        printable_pdfs.get_fpdf_dependencies()
