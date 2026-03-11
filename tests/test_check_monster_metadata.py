from pathlib import Path

import scripts.check_monster_metadata as checks


def configure_temp_repo(monkeypatch, tmp_path: Path) -> Path:
    monster_dir = tmp_path / "_monsters"
    monster_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(checks, "ROOT", tmp_path)
    monkeypatch.setattr(checks, "MONSTER_DIR", monster_dir)
    return tmp_path


def monster_front_matter(**overrides) -> str:
    data = {
        "name": "The Test Monster",
        "plain_name": "test paralysis",
        "emoji": "T",
        "tagline": "A test foe",
        "description": "A short description.",
        "challenge_summary": "A plain-language summary.",
        "you_might_be_here_if": ["One", "Two"],
        "start_here_ritual": {
            "label": "Test Ritual",
            "url": "/spellbook/test-ritual.html",
            "description": "Try the ritual first.",
        },
        "featured_printable": {
            "label": "Test Card",
            "url": "/site/printables/pdf/test-card-ink.pdf",
            "description": "Use the printable fast.",
        },
        "support_boundary": "A grounding boundary.",
        "cta": "Start now",
        "badges": ["Printable included"],
        "quick_links": [{"label": "Lore", "url": "#lore"}],
        "order": 1,
        "tags": ["adhd", "monster"],
    }
    data.update(overrides)

    import yaml

    return f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n\n# Test Monster\n"


def test_extract_front_matter_parses_mapping(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    monster = root / "_monsters" / "test.md"
    monster.write_text(monster_front_matter(), encoding="utf-8")

    data = checks.extract_front_matter(monster)

    assert data["name"] == "The Test Monster"
    assert data["start_here_ritual"]["url"] == "/spellbook/test-ritual.html"


def test_validate_monster_file_reports_missing_required_fields(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    monster = root / "_monsters" / "broken.md"
    monster.write_text(
        monster_front_matter(
            plain_name="",
            you_might_be_here_if=[],
            featured_printable={"label": "Card", "url": "", "description": ""},
        ),
        encoding="utf-8",
    )

    errors = checks.validate_monster_file(monster)

    assert f"_monsters{Path.sep}broken.md: missing non-empty 'plain_name'" in errors
    assert f"_monsters{Path.sep}broken.md: 'you_might_be_here_if' must be a non-empty list" in errors
    assert (
        f"_monsters{Path.sep}broken.md: 'featured_printable.url' must be a non-empty string"
        in errors
    )


def test_validate_monster_file_requires_expected_url_prefixes(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    monster = root / "_monsters" / "wrong-links.md"
    monster.write_text(
        monster_front_matter(
            start_here_ritual={
                "label": "Wrong",
                "url": "/monsters/task-hydra/",
                "description": "Nope",
            },
            featured_printable={
                "label": "Wrong",
                "url": "/assets/card.pdf",
                "description": "Nope",
            },
        ),
        encoding="utf-8",
    )

    errors = checks.validate_monster_file(monster)

    assert (
        f"_monsters{Path.sep}wrong-links.md: 'start_here_ritual.url' must point into /spellbook/"
        in errors
    )
    assert (
        f"_monsters{Path.sep}wrong-links.md: 'featured_printable.url' must point into /site/printables/"
        in errors
    )


def test_validate_monster_collection_reports_duplicate_identity_fields(monkeypatch, tmp_path):
    root = configure_temp_repo(monkeypatch, tmp_path)
    first = root / "_monsters" / "first.md"
    second = root / "_monsters" / "second.md"
    first.write_text(monster_front_matter(order=1), encoding="utf-8")
    second.write_text(
        monster_front_matter(name="The Test Monster", plain_name="test paralysis", order=1),
        encoding="utf-8",
    )

    errors = checks.validate_monster_collection([first, second])

    assert any("duplicate name 'The Test Monster'" in error for error in errors)
    assert any("duplicate plain_name 'test paralysis'" in error for error in errors)
    assert any("duplicate order '1'" in error for error in errors)
