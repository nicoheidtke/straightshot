# Multi-language Support

straightshot supports multi-language content through automatic linking of articles with matching IDs and a template-based language switcher.

## Basic Setup

Create articles in different languages using the same `id` in frontmatter:

**English version** (`articles/architecture-patterns.md`):
```yaml
---
title: "Modern Software Architecture Patterns"
written: 2025-04-05
topics: architecture, design-patterns
description: "Exploring effective software architecture patterns"
lang: en
id: architecture_patterns
---
```

**French version** (`articles/architecture-patterns-fr.md`):
```yaml
---
title: "Modèles d'Architecture Logicielle Modernes"  
written: 2025-04-05
topics: architecture, design-patterns
description: "Explorer les modèles d'architecture logicielle"
lang: fr
id: architecture_patterns
---
```

Articles with matching `id` values are automatically linked as alternate language versions.

## Language Switcher Template

Create a template macro to display language alternatives:

```html
{% macro language_switcher(page) %}
{% if page.alternate_languages %}
<div class="language-switcher">
    {% for lang_code, alt_page in page.alternate_languages.items() %}
        <a href="{{ url_for(alt_page.url) }}">{{ lang_code.upper() }}</a>
    {% endfor %}
</div>
{% endif %}
{% endmacro %}
```

Use it in templates:
```html
{% import '_macros.html' as macros %}
{{ macros.language_switcher(page) }}
```

The `page.alternate_languages` dictionary contains all linked articles by language code.

## Navigation Behavior

The navigation system considers language versions:

- **Previous/next navigation** skips alternate language versions of the same article
- **Related articles** exclude alternate language versions  
- **Language preference** attempts to show same-language content when available

## Site Configuration

Set your site's default language in `site.yaml`:

```yaml
language: "en"  # Default language
```

The system automatically:
- Detects all languages used in content
- Makes language data available to templates via `site.languages`
- Uses the default language for URL generation

## Template Usage

Access language information in templates:

```html
<!-- Page language -->
<html lang="{{ page.metadata.lang|default(site.language) }}">

<!-- All site languages -->
{% for lang in site.languages %}
    <link rel="alternate" hreflang="{{ lang }}" href="...">
{% endfor %}

<!-- Article structured data -->
"inLanguage": "{{ page.metadata.lang|default(site.language) }}"
```

## Implementation Notes

- Language linking happens automatically during content processing
- No manual configuration needed beyond matching `id` fields
- The language switcher only appears when alternate versions exist
- Navigation skips alternate language versions to avoid duplicates

Multi-language support in straightshot is designed to be simple to use while providing the core functionality needed for international content.
