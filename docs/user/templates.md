# Templates & Theming

straightshot uses Jinja2 templates to generate HTML from content. See the [Jinja2 documentation](https://jinja.palletsprojects.com/) for template syntax and features.

## Template Structure

### Core Templates

```
templates/
├── base.html           # Base layout template
├── index.html          # Home page template
├── blog_index.html     # Blog listing page
├── article.html        # Individual article template
├── about.html          # About page template
├── feed.xml            # RSS feed template
├── sitemap.xml         # Sitemap template
├── _macros.html        # Reusable template macros
└── tags/               # Custom tag templates
    ├── link.html
    ├── site_meta.html
    ├── slides.html
    └── youtube.html
```

### Template Inheritance

Templates use Jinja2's `{% extends %}` and `{% block %}` system for layout inheritance.

## Template Variables

### Global Variables

Available in all templates:

- `site` - Site configuration from `site.yaml`
- `site.topics` - Dictionary of topics and their articles
- `site.articles` - All published articles

### Page Variables

Available in content templates:

- `page.metadata` - Frontmatter from the content file
- `page.content` - Rendered HTML content
- `page.url` - Page URL path
- `page.slug` - Page filename without extension
- `page.language` - Content language

### Template Assignment

Specify templates in frontmatter:

```yaml
---
title: "Custom Page"
template: "custom.html"
---
```

## Custom Functions

### URL Generation

- `url_for(path)` - Generate relative URLs
- `absolute_url_for(path)` - Generate absolute URLs

### Date Formatting

- `date` filter - Format dates using Python strftime patterns

## Custom Tag Templates

Custom tags use templates in the `tags/` directory. Tag templates receive variables from the tag content and can render arbitrary HTML.

## Static Assets

Place CSS, JavaScript, and images in `static/` directory. Reference using `url_for()`:

```html
<link rel="stylesheet" href="{{ url_for('static/css/main.css') }}">
<script src="{{ url_for('static/js/main.js') }}"></script>
```
