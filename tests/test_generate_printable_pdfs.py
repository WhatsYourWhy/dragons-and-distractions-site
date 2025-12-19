from pathlib import Path

import pytest

from scripts.generate_printable_pdfs import NAV_MARKER, cleaned_lines


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
