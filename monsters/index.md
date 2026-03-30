---
layout: hub
title: "Monster Index"
description: "Browse every monster in the bestiary with short hooks, first rituals, and fast tools - or filter the list when you know part of the name or feeling."
hero_title: "Map the Monsters"
hero_intro: "Start with the monster that matches your current stuck point, or use the guided chooser if you want plain-language routing first."
show_breadcrumbs: false
---

{% assign monsters = site.monsters | sort: "order" %}

<div class="monster-grid">
  {% for monster in monsters %}
  <article class="monster-card">
    <a class="monster-card__body" href="{{ monster.url | relative_url }}">
      {% if monster.sigil %}
      <figure class="monster-card__sigil-frame">
        <img class="monster-card__sigil" src="{{ monster.sigil | relative_url }}" alt="{{ monster.name }} sigil">
      </figure>
      {% endif %}
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
  </article>
  {% endfor %}
</div>

<div class="section-callout">Need the fastest path? <a href="{{ '/choose-your-monster/' | relative_url }}">Choose Your Monster</a> routes you to one ritual and one tool without the full lore pass.</div>
