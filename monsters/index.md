---
layout: hub
title: "Monster Index"
hero_title: "ðŸ—ºï¸ Monster Index"
hero_intro: "Start with the monster that matches your current stuck point, or use the guided chooser if you want plain-language routing first."
show_breadcrumbs: true
---

{% assign monsters = site.monsters | sort: "order" %}

<div class="monster-grid">
  {% for monster in monsters %}
  <article class="monster-card">
    <a class="monster-card__body" href="{{ monster.url | relative_url }}">
      <div class="monster-card__header">
        <span class="monster-card__emoji">{{ monster.emoji }}</span>
        <div>
          <p class="monster-card__name">{{ monster.name }}</p>
          <p class="monster-card__tagline">{{ monster.tagline }}</p>
        </div>
      </div>
      <p class="monster-card__description">{{ monster.challenge_summary | default: monster.description }}</p>
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
    {% if monster.quick_links %}
    <div class="monster-card__quick-links" aria-label="Quick links for {{ monster.name }}">
      {% for link in monster.quick_links %}
      {% assign link_href = link.url %}
      {% assign first_char = link_href | slice: 0, 1 %}
      {% if first_char == "#" %}
      {% assign link_href = monster.url | append: link_href %}
      {% endif %}
      <a class="monster-card__quick-link quick-actions__item" href="{{ link_href | relative_url }}">
        {% if link.emoji %}
        <span class="quick-actions__emoji" aria-hidden="true">{{ link.emoji }}</span>
        {% endif %}
        <span class="quick-actions__text">{{ link.label }}</span>
      </a>
      {% endfor %}
    </div>
    {% endif %}
  </article>
  {% endfor %}
</div>

More monsters await...

<div class="section-callout">Need the fastest path? <a href="{{ '/choose-your-monster/' | relative_url }}">Choose Your Monster</a> routes you to one ritual and one tool without the full lore pass.</div>
