from pathlib import Path

import scripts.validate_codex_prompts as checks


def test_validate_homepage_hero_accepts_cover_cta_contract(tmp_path: Path):
    homepage = tmp_path / "index.md"
    homepage.write_text(
        "\n".join(
            [
                "---",
                'hero_variant: cover',
                'hero_image: "/assets/generated/homepage-hero-web.png"',
                "hero_actions:",
                '  - label: "Choose Your Monster"',
                '    url: "/choose-your-monster/"',
                '    style: "primary"',
                '  - label: "Browse the Bestiary"',
                '    url: "/monsters/"',
                '    style: "secondary"',
                "---",
            ]
        ),
        encoding="utf-8",
    )

    assert checks.validate_homepage_hero(homepage) == []


def test_validate_homepage_hero_rejects_wrong_ctas(tmp_path: Path):
    homepage = tmp_path / "index.md"
    homepage.write_text(
        "\n".join(
            [
                "---",
                'hero_variant: split',
                'hero_image: "/assets/generated/other.png"',
                "hero_actions:",
                '  - label: "Open a Tool"',
                '    url: "/site/"',
                '    style: "primary"',
                "---",
            ]
        ),
        encoding="utf-8",
    )

    errors = checks.validate_homepage_hero(homepage)

    assert any("hero_variant must be 'cover'" in error for error in errors)
    assert any("hero_image must point to /assets/generated/homepage-hero-web.png" in error for error in errors)
    assert any("hero_actions must exactly match the homepage CTA contract" in error for error in errors)


def test_validate_spellbook_directory_checks_exact_ritual_keys(tmp_path: Path):
    spellbook = tmp_path / "index.md"
    spellbook.write_text(
        "\n".join(
            [
                '<article class="ritual-library__card" data-ritual-key="task-hydra"></article>',
                '<article class="ritual-library__card" data-ritual-key="temporal-shark"></article>',
            ]
        ),
        encoding="utf-8",
    )

    errors = checks.validate_spellbook_directory(spellbook)

    assert any("ritual directory keys must exactly match" in error for error in errors)
    assert any("ritual directory must render 9 ritual cards" in error for error in errors)


def test_validate_monster_index_template_checks_contract(tmp_path: Path):
    template = tmp_path / "monsters-index.md"
    template.write_text(
        '{% assign monster_hook = monster.you_might_be_here_if | first %}\n'
        'style="--monster-accent: {{ monster.accent_color | default: \'#c8900a\' }};"\n'
        '{{ monster.sigil | relative_url }}\n'
        'class="monster-card__hook"\n',
        encoding="utf-8",
    )

    assert checks.validate_monster_index_template(template) == []


def test_validate_header_markup_requires_mobile_nav_and_theme_toggle(tmp_path: Path):
    header = tmp_path / "site-banner.html"
    header.write_text(
        "\n".join(
            [
                "js-theme-toggle",
                "js-menu-toggle",
                "site-banner__menu-toggle",
                "site-navigation",
            ]
        ),
        encoding="utf-8",
    )

    assert checks.validate_header_markup((header,)) == []
