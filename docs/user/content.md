# Content & Writing

Learn how to create and organize content for your straightshot site using Markdown with YAML frontmatter, multi-language support, and topic organization.

## Content Structure

straightshot organizes content in a logical directory structure:

```
content/
├── site.yaml              # Site configuration
├── about.md               # Static pages
├── data/                  # Site data files
├── drafts/                # Unpublished content
├── publish/               # Published content
│   ├── articles/          # Blog posts
│   └── talks/             # Presentations
└── static/                # Assets (CSS, JS, images)
```

## Writing Articles

### Basic Article Structure

Every article is a Markdown file with YAML frontmatter:

```markdown
---
title: "Getting Started with Python"
written: 2024-01-15
description: "A beginner's guide to Python programming"
topics: python, programming, tutorial
---

# Getting Started with Python

Python is a powerful, easy-to-learn programming language...
```

### Required Frontmatter

The minimal frontmatter for an article:

```yaml
---
title: "Your Article Title"
written: 2024-01-15
description: "Brief description for SEO and summaries"
---
```

### Available Fields

```yaml
---
title: "Advanced Python Patterns"
written: 2024-01-15
description: "Explore advanced Python programming patterns"
topics: python, patterns, advanced
language: en
disabled: false
image: path/to/image.jpg
id: unique-content-id
---
```

## Multi-language Content

Create language versions using matching `id` fields in frontmatter. See [Multi-language Support](multi-language.md) for detailed configuration.

```yaml
---
title: "Guía de Python"
lang: es
id: python-guide  # Links to other language versions
---
```

## Topic Organization

### Adding Topics

Organize content with topics for filtering and discovery:

```yaml
---
title: "Modern Web Development"
topics: webdev, javascript, frontend, react
---
```

Topics can be:
- **Comma-separated string**: `topics: webdev, javascript, frontend`
- **YAML list**: 
  ```yaml
  topics:
    - webdev
    - javascript
    - frontend
  ```

### Topic Features

Topics enable several automatic features:

- **Site-wide topic collection** - All topics are available in templates via `site.topics`
- **Topic clouds** - Display popular topics with article counts
- **Related articles** - Automatic suggestions based on shared topics

Access topic data in templates:
```html
<!-- All topics with counts -->
{% for topic, articles in site.topics|dictsort %}
  {{ topic }}: {{ articles|length }} articles
{% endfor %}

<!-- Topic links -->
<a href="{{ url_for('blog') }}?topic={{ topic }}">{{ topic }}</a>
```

## Content Types

### Blog Articles

Place regular blog posts in `content/publish/articles/`:

```markdown
---
title: "The Future of Web Development"
written: 2024-02-01
description: "Exploring upcoming trends in web development"
topics: webdev, trends, future
---
```

### Talks and Presentations

Store presentation content in `content/publish/talks/`:

```markdown
---
title: "Building Scalable APIs"
written: 2024-01-20
topics: api, scaling, backend
---

{% slides %}
https://docs.google.com/presentation/d/1abc123def456/edit
{% endslides %}
```

### Static Pages

Create standalone pages in the `content/` root:

```markdown
---
title: "About Me"
description: "Learn more about the author"
template: "about.html"
---

# About Me

I'm a software developer passionate about...
```

## Markdown Features

straightshot uses [markdown-it-py](https://markdown-it-py.readthedocs.io/) with:

- **CommonMark** standard support
- **Tables** extension enabled
- **Syntax highlighting** via Pygments for code blocks
- **Typographer** for smart quotes and dashes

### Code Blocks

Syntax highlighting works for many languages:

````markdown
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
````

### Tables

Standard Markdown table syntax:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Data 1   | Value 1  |
| Row 2    | Data 2   | Value 2  |
```

## Custom Tags

Embed rich content with custom tags using `key=value` syntax:

### YouTube Videos

```markdown
{% youtube id="dQw4w9WgXcQ" %}
```

### Slides

```markdown
{% slides id="your_presentation_id" %}
```

### Article Links

```markdown
{% link article="articles/python-guide" %}
```

### Site Metadata

```markdown
{% site_meta key="author" %}
```

Custom tags are configured in `site.yaml` and use templates in `templates/tags/`.

## Drafts and Publishing

### Working with Drafts

Place unpublished content in `content/drafts/`:

```markdown
---
title: "Work in Progress Article"
written: 2024-02-01
disabled: true
---
```

### Publishing Workflow

1. Write new articles in `content/drafts/`
2. Review and edit content
3. Move completed articles to appropriate publish directory
4. Run `straightshot build` to generate the site

## Content Organization Tips

### File Naming

Use consistent naming conventions:

- `kebab-case-titles.md` for articles
- Language suffixes for translations: `article.es.md`
- Descriptive names that match your content

### Metadata Consistency

- Write clear, specific titles under 60 characters
- Create compelling descriptions under 160 characters  
- Use consistent topic names across articles
- Include accurate publication dates in ISO format
