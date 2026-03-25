---
layout: hub
title: "Monster Index"
description: "Browse every monster in the bestiary with short hooks, first rituals, and fast tools—or filter the list when you know part of the name or feeling."
hero_title: "Map the Monsters"
hero_intro: "Start with the monster that matches your current stuck point, or use the guided chooser if you want plain-language routing first."
show_breadcrumbs: false
---

{% assign monsters = site.monsters | sort: "order" %}

<div class="section-callout">
  Need the fastest path? <a href="{{ '/choose-your-monster/' | relative_url }}">Choose Your Monster</a> routes you to one ritual and one tool without the full lore pass.
</div>

<section class="landing-section">
  <div class="section-heading">
    <p class="section-heading__eyebrow">Use the map, not the whole dungeon</p>
    <h2>How to use the bestiary without getting lost in it</h2>
    <p>These monster pages are here to help you recognize the pattern, grab one useful move, and stop before browsing turns into another avoidance side quest.</p>
  </div>
  <div class="landing-grid landing-grid--compact">
    <article class="landing-card">
      <h3>Want plain-language routing first?</h3>
      <p>Start with <a href="{{ '/choose-your-monster/' | relative_url }}">Choose Your Monster</a> if you know the feeling but not the creature name yet.</p>
    </article>
    <article class="landing-card">
      <h3>Want the shortest practical version?</h3>
      <p>Go to the <a href="{{ '/spellbook/' | relative_url }}">Spellbook</a> or the <a href="{{ '/site/' | relative_url }}">tool cabinet</a> if you need action before lore.</p>
    </article>
    <article class="landing-card">
      <h3>Want the full pattern and examples?</h3>
      <p>Use the cards below when you want the whole write-up, matching rituals, and a better sense of what is actually happening today.</p>
    </article>
  </div>
</section>

<section class="landing-section">
  <div class="section-heading">
    <p class="section-heading__eyebrow">Browse the full bestiary</p>
    <h2>Pick the monster that feels most true right now</h2>
    <p>Each card gives you the monster, one true hook line, one first ritual, and one fast tool so you can choose without opening every page.</p>
  </div>
  {% include monster-index-filter.html %}
  <div class="monster-grid monster-grid--index">
    {% for monster in monsters %}
    {% assign monster_hook = monster.you_might_be_here_if | first %}
    {% capture monster_search %}{{ monster.name }} {{ monster.plain_name | default: "" }} {{ monster.tagline }} {{ monster_hook }}{% for badge in monster.badges %} {{ badge }}{% endfor %}{% endcapture %}
    <article class="monster-card monster-card--index" data-search="{{ monster_search | strip | downcase | escape }}" style="--monster-accent: {{ monster.accent_color | default: '#c8900a' }};">
      {% if monster.sigil %}
      <figure class="monster-card__media monster-card__media--sigil monster-card__media--index">
        <img class="monster-card__media-image monster-card__media-image--sigil" src="{{ monster.sigil | relative_url }}" alt="" loading="lazy" decoding="async">
      </figure>
      {% endif %}
      <div class="monster-card__body">
        <p class="monster-card__eyebrow">{{ monster.plain_name | default: monster.tagline }}</p>
        <p class="monster-card__name"><a href="{{ monster.url | relative_url }}">{{ monster.name }}</a></p>
        <p class="monster-card__tagline">{{ monster.tagline }}</p>
        {% if monster_hook %}
        <p class="monster-card__hook">{{ monster_hook }}</p>
        {% endif %}
        {% if monster.badges %}
        <div class="monster-card__meta">
          {% for badge in monster.badges %}
          <span class="monster-card__badge">{{ badge }}</span>
          {% endfor %}
        </div>
        {% endif %}
        <div class="monster-card__actions">
          <a class="monster-card__action monster-card__action--primary" href="{{ monster.url | relative_url }}">Open monster page</a>
          {% if monster.start_here_ritual %}
          <a class="monster-card__action" href="{{ monster.start_here_ritual.url | relative_url }}">{{ monster.start_here_ritual.label }}</a>
          {% endif %}
          {% if monster.featured_printable %}
          <a class="monster-card__action" href="{{ monster.featured_printable.url | relative_url }}">{{ monster.featured_printable.label }}</a>
          {% endif %}
        </div>
      </div>
    </article>
    {% endfor %}
  </div>
</section>
