# Site Configuration

Configure your straightshot site through a main `site.yaml` file that controls site metadata, behavior, and data includes.

## Main Configuration File

### `site.yaml`

The central configuration file in your project root that defines your site:

```yaml
# Site configuration from `site.yaml`
title: "My Blog"
description: "Thoughts on software development and technology"  
author: "Jon Doe"
url: "https://myblog.com"
language: "en"  # optional, defaults to "en"
base_url: "/"   # optional, defaults to "/"

# Custom tags for rich content (see Content & Writing guide)
custom_tags:
  youtube: "tags/youtube.html"
  slides: "tags/slides.html"
  link: "tags/link.html"
  site_meta: "tags/site_meta.html"

# Standalone pages to generate
standalone_pages:
  - template: "index.html"
    output: "index.html"
  - template: "about.html"
    output: "about.html"
  - template: "blog_index.html"
    output: "blog/index.html"
  - template: "sitemap.xml"
    output: "sitemap.xml"
  - template: "feed.xml"
    output: "feed.xml"

# Social media links
social:
  twitter: "@your-handle"
  github: "your-username"
  linkedin: "your-profile"

# SEO settings (used in templates)
seo:
  keywords: "technology, programming, blog"
  twitter_card_type: "summary_large_image"
  default_image: "static/images/site-default.jpg"

# Theme customization (used in templates)
theme:
  primary_color: "#3b82f6"
  highlight_style: "github-dark"
  default_mode: "auto"  # auto, light, or dark
```

## Data Includes

### External Data Files

Include external YAML or JSON files using special directives:

```yaml
# In site.yaml
data:
  # Direct inline data
  build_info:
    version: "1.0.0"
    built_with: "straightshot"
  
  # Include external files
  navigation: $$include_yaml data/navigation.yaml
  config: $$include_json data/site-config.json
```

## Command Line Configuration

All arguments are required when using the build command:

```bash
# Basic build command
straightshot build \
  --content-dir content \
  --templates-dir templates \
  --static-dir static \
  --output-dir _site \
  --site-config site.yaml

# Additional options
straightshot build \
  --content-dir content \
  --templates-dir templates \
  --static-dir static \
  --output-dir _site \
  --site-config site.yaml \
  --drafts \           # Include draft articles
  --verbose \          # Enable verbose output  
  --clean \            # Clean output directory before building
  --base-url "/blog/"  # Override base URL from site.yaml
```

## Configuration Fields

### Required Fields

- `title` - Site title
- `description` - Site description  
- `author` - Site author
- `url` - Full site URL

### Optional Fields

- `language` - Site language (default: "en")
- `base_url` - Base URL path (default: "/")
- `date_format` - Date display format (default: "%Y-%m-%d")
- `custom_tags` - Custom tag template mapping
- `standalone_pages` - Pages to generate from templates
- `social` - Social media links
- `seo` - SEO metadata (passed to templates)
- `theme` - Theme customization data (passed to templates)
- `data` - Custom data for templates (supports includes)

## Accessing Configuration

### In Templates

Configuration is available through the `site` object:

```html
<!-- Basic site info -->
<title>{{ site.title }}</title>
<meta name="description" content="{{ site.description }}">
<meta name="author" content="{{ site.author }}">

<!-- Social links -->
{% for platform, handle in site.social.items() %}
<a href="https://{{ platform }}.com/{{ handle }}">{{ platform|title }}</a>
{% endfor %}

<!-- Custom data -->
{% for feature in site.data.config.features %}
<div class="feature">
  <h3>{{ feature.name }}</h3>
  <p>{{ feature.description }}</p>
</div>
{% endfor %}

<!-- Navigation from includes -->
<nav>
  {% for item in site.data.navigation.navigation %}
  <a href="{{ item.url }}">{{ item.title }}</a>
  {% endfor %}
</nav>
```

## Validation

straightshot validates configuration during build:

- Required fields are present
- File paths exist  
- YAML/JSON syntax is valid
- Include directives resolve correctly

Configuration provides a flexible way to customize your site while keeping templates clean and data organized.
