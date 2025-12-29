---
layout: hub
title: "Monster Index"
hero_title: "🗺️ Monster Index"
hero_intro: "Each monster represents a real executive function challenge—named, described, and disarmed with humor, science, and ritual. Choose your foe to jump straight to its lore and counter-spells."
show_breadcrumbs: true
---

{% assign monsters = site.monsters | sort: "order" %}

<div class="monster-grid">
  {% for monster in monsters %}
  <a class="monster-card" href="{{ monster.url | relative_url }}">
    <div class="monster-card__header">
      <span class="monster-card__emoji">{{ monster.emoji }}</span>
      <div>
        <p class="monster-card__name">{{ monster.name }}</p>
        <p class="monster-card__tagline">{{ monster.tagline }}</p>
      </div>
    </div>
    <p class="monster-card__description">{{ monster.description }}</p>
    {% if monster.cta %}
    <span class="monster-card__cta cta-link">{{ monster.cta }}</span>
    {% endif %}
    {% if monster.badges %}
    <div class="monster-card__meta">
      {% for badge in monster.badges %}
      <span class="monster-card__badge">{{ badge }}</span>
      {% endfor %}
    </div>
    {% endif %}
  </a>
  {% endfor %}
</div>

More monsters await...
