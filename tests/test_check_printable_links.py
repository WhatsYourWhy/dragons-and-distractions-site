from dataclasses import replace
from pathlib import Path

import scripts.check_printable_links as checks


def configure_temp_repo(monkeypatch, tmp_path: Path) -> Path:
    monkeypatch.setattr(checks, "ROOT", tmp_path)
    monkeypatch.setattr(checks, "PDF_DIR", tmp_path / "site" / "printables" / "pdf")
    return tmp_path


def test_find_pdf_links_resolves_relative_pdf_directory(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    pdf_dir = root / "site" / "printables" / "pdf"
    pdf_dir.mkdir(parents=True)
    target_pdf = pdf_dir / "demo.pdf"
    target_pdf.touch()

    md_file = root / "site" / "printables" / "overview.md"
    md_file.parent.mkdir(parents=True, exist_ok=True)
    md_file.write_text(
        "\n".join(
            [
                "[printable](./pdf/demo.pdf)",
                "[non-printable](./pdf/demo.txt)",
                "[other](../not-tracked.pdf)",
            ]
        ),
        encoding="utf-8",
    )

    links = checks.find_pdf_links(md_file)

    assert links == [target_pdf]


def test_find_pdf_links_detects_html_anchor_with_relative_url(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    pdf_dir = root / "site" / "printables" / "pdf"
    pdf_dir.mkdir(parents=True)
    target_pdf = pdf_dir / "html.pdf"
    target_pdf.touch()

    md_file = root / "_monsters" / "html-link.md"
    md_file.parent.mkdir(parents=True, exist_ok=True)
    md_file.write_text(
        '<a href="{{ "/site/printables/pdf/html.pdf" | relative_url }}">Download</a>',
        encoding="utf-8",
    )

    links = checks.find_pdf_links(md_file)

    assert links == [target_pdf]


def test_find_pdf_links_detects_html_anchor_site_root_path(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    pdf_dir = root / "site" / "printables" / "pdf"
    pdf_dir.mkdir(parents=True)
    target_pdf = pdf_dir / "plain.html.pdf"
    target_pdf.touch()

    html_file = root / "site" / "printables" / "html-plain.html"
    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.write_text(
        '<a href="/site/printables/pdf/plain.html.pdf">Plain PDF</a>',
        encoding="utf-8",
    )

    links = checks.find_pdf_links(html_file)

    assert links == [target_pdf]


def test_find_pdf_links_resolves_site_root_links_to_repo_root(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    pdf_dir = root / "site" / "printables" / "pdf"
    pdf_dir.mkdir(parents=True)
    target_pdf = pdf_dir / "absolute.pdf"
    target_pdf.touch()

    md_file = root / "site" / "printables" / "absolute.md"
    md_file.write_text(
        "[printable](/site/printables/pdf/absolute.pdf)", encoding="utf-8"
    )

    links = checks.find_pdf_links(md_file)

    assert links == [target_pdf]


def test_check_required_links_passes_with_all_expected_links(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    template = checks.CHECKS[0]
    link_check = replace(template, path=root / template.path)
    link_check.path.parent.mkdir(parents=True)
    link_check.path.write_text(
        "\n".join(f"[{index}]({link})" for index, link in enumerate(link_check.required_links)),
        encoding="utf-8",
    )

    assert checks.check_required_links(link_check) == []


def test_check_required_links_accepts_yaml_links(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    template = checks.CHECKS[0]
    link_check = replace(template, path=template.path)
    (root / link_check.path).parent.mkdir(parents=True, exist_ok=True)
    (root / link_check.path).write_text("Welcome to the site", encoding="utf-8")

    data_dir = root / "_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    data_dir.joinpath("printables.yml").write_text(
        "\n".join(
            [
                "- printables:",
                "    - ink_pdf: /site/printables/pdf/single-task-oath-card-ink.pdf",
                "      art_pdf: /site/printables/pdf/single-task-oath-card-art.pdf",
                "    - ink_pdf: /site/printables/pdf/tide-mark-calendar-card-ink.pdf",
                "      art_pdf: /site/printables/pdf/tide-mark-calendar-card-art.pdf",
                "    - ink_pdf: /site/printables/pdf/tide-marks-buddy-ping-ink.pdf",
                "      art_pdf: /site/printables/pdf/tide-marks-buddy-ping-art.pdf",
                "    - ink_pdf: /site/printables/pdf/wake-invocation-checklist-ink.pdf",
                "      art_pdf: /site/printables/pdf/wake-invocation-checklist-art.pdf",
            ]
        ),
        encoding="utf-8",
    )

    assert checks.check_required_links(link_check) == []


def test_check_required_links_reports_missing_entry(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    template = checks.CHECKS[0]
    missing_link = template.required_links[0]
    link_check = replace(template, path=root / template.path)
    link_check.path.parent.mkdir(parents=True)
    link_check.path.write_text(
        "\n".join(f"[{index}]({link})" for index, link in enumerate(link_check.required_links[1:])),
        encoding="utf-8",
    )

    errors = checks.check_required_links(link_check)

    assert errors == [f"{link_check.path}: missing link to {missing_link}"]


def test_check_broken_pdf_links_flags_missing_pdf(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    pdf_dir = root / "site" / "printables" / "pdf"
    pdf_dir.mkdir(parents=True)

    present_pdf = pdf_dir / "present.pdf"
    present_pdf.touch()

    valid_markdown = root / "site" / "printables" / "good.md"
    valid_markdown.parent.mkdir(parents=True, exist_ok=True)
    valid_markdown.write_text("[good](./pdf/present.pdf)", encoding="utf-8")

    missing_markdown = root / "site" / "printables" / "missing.md"
    missing_markdown.write_text("[missing](./pdf/missing.pdf)", encoding="utf-8")

    errors = checks.check_broken_pdf_links([valid_markdown, missing_markdown])

    assert errors == [
        "site/printables/missing.md:",
        "  • site/printables/pdf/missing.pdf",
    ]


def test_check_broken_pdf_links_flags_links_outside_repo(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    external_md = root / "site" / "printables" / "nested" / "deep" / "external.md"
    external_md.parent.mkdir(parents=True, exist_ok=True)

    absolute_pdf = Path("/absolute/outside.pdf")
    parent_traversing_pdf = root.parent / "outside.pdf"
    external_md.write_text(
        "\n".join(
            [
                f"[absolute]({absolute_pdf})",
                "[parent](../../../../../outside.pdf)",
            ]
        ),
        encoding="utf-8",
    )

    errors = checks.check_broken_pdf_links([external_md])

    assert errors == [
        "site/printables/nested/deep/external.md:",
        f"  • {absolute_pdf} (outside repo)",
        f"  • {parent_traversing_pdf} (outside repo)",
    ]


def test_check_broken_pdf_links_flags_external_html_pdf(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    html_file = root / "site" / "printables" / "external.html"
    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.write_text(
        '<a href="https://example.com/printable.pdf">External</a>',
        encoding="utf-8",
    )

    errors = checks.check_broken_pdf_links([html_file])

    assert errors == [
        "site/printables/external.html:",
        "  • https:/example.com/printable.pdf (outside repo)",
    ]


def test_check_broken_pdf_links_reports_missing_monster_pdf(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    monster_md = root / "_monsters" / "missing.md"
    monster_md.parent.mkdir(parents=True, exist_ok=True)
    monster_md.write_text(
        '<a href="{{ "/site/printables/pdf/missing.pdf" | relative_url }}">Missing PDF</a>',
        encoding="utf-8",
    )

    errors = checks.check_broken_pdf_links([monster_md])

    assert errors == [
        "_monsters/missing.md:",
        "  • site/printables/pdf/missing.pdf",
    ]


def test_check_broken_pdf_links_parses_html_files(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    html_file = root / "_includes" / "cta.html"
    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.write_text(
        '<a href="{{ "/site/printables/pdf/missing.pdf" | relative_url }}">Download</a>',
        encoding="utf-8",
    )

    errors = checks.check_broken_pdf_links([html_file])

    assert errors == [
        "_includes/cta.html:",
        "  • site/printables/pdf/missing.pdf",
    ]


def test_check_broken_pdf_links_flags_monster_missing_printable(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    monster_md = root / "_monsters" / "missing-anchor.md"
    monster_md.parent.mkdir(parents=True, exist_ok=True)
    monster_md.write_text("No printable here.", encoding="utf-8")

    errors = checks.check_broken_pdf_links([monster_md])

    assert errors == [
        "_monsters/missing-anchor.md:",
        "  • missing printable PDF link for monster entry",
    ]
