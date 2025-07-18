# Example Site Features

The included example site demonstrates several advanced features that you can adapt for your own site.

## Interactive Elements

- **Topic filtering** - JavaScript-based filtering with URL parameter support (`?topic=webdev`)
  - Filter by multiple topics simultaneously
  - URL parameter persistence for shareable filtered views
  - Clear filters button and topic selection state display
- **Infinite scroll** - Dynamic article loading as users scroll
  - Viewport-aware loading for optimal performance
  - Responsive batch sizing based on screen size
- **Dark/light mode** - Theme switcher with localStorage persistence
  - System preference detection on first visit
  - Manual toggle with smooth transitions
- **Language switcher** - Multi-language article navigation
  - Circular flag icons with current language highlighting
  - Skip alternate language versions in main navigation

## Enhanced UI

- **Share menus** - Social sharing buttons with copy-to-clipboard
  - Twitter, LinkedIn, Reddit sharing links
  - Copy-to-clipboard with visual feedback
  - Dropdown menu with keyboard accessibility
- **Responsive design** - Mobile-first layout with CSS Grid/Flexbox
  - Orange/black/white color scheme with dark mode support
  - CSS custom properties for theming
  - Smooth hover animations and transitions
- **Code block enhancements** - Copy buttons and syntax highlighting
  - One-click code copying with visual feedback
  - Pygments syntax highlighting for multiple languages
- **Progressive enhancement** - Works without JavaScript
  - All core functionality accessible without JS
  - JavaScript adds convenience and visual polish

## Template Structure

- **Base template** with common layout and SEO meta tags
- **Macros** for reusable components:
  - Language switcher with circular flag-style buttons and current language highlighting
  - Share menus with dropdown functionality and accessibility features
- **Custom tags** for rich content (YouTube, slides, links)
- **Structured data** for search engine optimization

### Language Switcher Implementation

The example site's language switcher displays all languages including the current one:

```html
{% macro language_switcher(page) %}
{% if page.alternate_languages %}
<div class="language-switcher">
    {% set all_languages = [page.metadata.lang] + (page.alternate_languages.keys() | list) %}
    {% for lang_code in all_languages | sort %}
        {% if lang_code == page.metadata.lang %}
            <span class="lang-current lang-btn">{{ lang_code.upper() }}</span>
        {% else %}
            <a href="{{ url_for(page.alternate_languages[lang_code].url) }}" 
               class="lang-link lang-btn">{{ lang_code.upper() }}</a>
        {% endif %}
    {% endfor %}
</div>
{% endif %}
{% endmacro %}
```

## JavaScript Implementation

The example site's `main.js` includes:

- **Article rendering** - Dynamic card generation from JSON data
- **Infinite scroll** - Viewport calculations and batch loading
- **Topic filtering** - URL parameter handling and visual state management
- **Theme management** - localStorage persistence and system preference detection
- **Share functionality** - Clipboard API with fallback support

These features demonstrate straightshot's capabilities but are not required - use what fits your needs.
