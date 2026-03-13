from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_chooser_template_prefers_card_art_with_sigil_fallback():
    template = (ROOT / "_includes" / "path-card.html").read_text(encoding="utf-8")

    assert "{% assign card_media = matched_monster.card_art | default: matched_monster.sigil %}" in template


def test_monster_index_prefers_card_art_with_sigil_fallback():
    template = (ROOT / "monsters" / "index.md").read_text(encoding="utf-8")

    assert "{% assign monster_media = monster.card_art | default: monster.sigil %}" in template
