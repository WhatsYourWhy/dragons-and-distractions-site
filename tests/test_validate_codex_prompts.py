from pathlib import Path

import scripts.validate_codex_prompts as checks


def test_validate_page_descriptions_accepts_non_empty_descriptions(tmp_path: Path):
    described = tmp_path / "described.md"
    described.write_text(
        "\n".join(
            [
                "---",
                'description: "Clear page summary."',
                "---",
            ]
        ),
        encoding="utf-8",
    )

    assert checks.validate_page_descriptions((described,)) == []


def test_validate_page_descriptions_rejects_missing_or_blank_descriptions(tmp_path: Path):
    missing = tmp_path / "missing.md"
    missing.write_text(
        "\n".join(
            [
                "---",
                'title: "Missing description"',
                "---",
            ]
        ),
        encoding="utf-8",
    )

    blank = tmp_path / "blank.md"
    blank.write_text(
        "\n".join(
            [
                "---",
                'description: "   "',
                "---",
            ]
        ),
        encoding="utf-8",
    )

    errors = checks.validate_page_descriptions((missing, blank))

    assert errors == [
        "missing.md: missing non-empty top-level description front matter",
        "blank.md: missing non-empty top-level description front matter",
    ]


def test_validate_page_descriptions_flags_missing_allowlisted_pages(tmp_path: Path):
    expected = tmp_path / "public-page.md"

    errors = checks.validate_page_descriptions((expected,))

    assert errors == ["public-page.md: expected public page is missing"]


def test_validate_page_descriptions_reports_missing_front_matter_delimiter(tmp_path: Path):
    page = tmp_path / "no_delimiter.md"
    page.write_text("# Title only\n", encoding="utf-8")

    errors = checks.validate_page_descriptions((page,))

    assert len(errors) == 1
    assert "no_delimiter.md" in errors[0]
    assert "invalid or unreadable YAML front matter" in errors[0]


def test_validate_page_descriptions_reports_invalid_yaml_in_front_matter(tmp_path: Path):
    page = tmp_path / "bad_yaml.md"
    page.write_text("---\nfoo: [\n---\n\nBody.\n", encoding="utf-8")

    errors = checks.validate_page_descriptions((page,))

    assert len(errors) == 1
    assert "bad_yaml.md" in errors[0]
    assert "invalid or unreadable YAML front matter" in errors[0]
