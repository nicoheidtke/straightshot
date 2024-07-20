---
title: Your Post Title Here
written: 2025-04-12
topics: topic1, topic2, topic3
description: A brief description of your post (will appear in meta tags and search results)
# Optional fields below:
# disabled: true (uncomment to disable this post)
# image: path/to/featured-image.jpg
# lang: en
---

# Your Post Title

This is where you write your post content. Everything below the frontmatter (the area between the `---` lines) will be processed as Markdown.

## Headings Are Easy

Use standard Markdown syntax for formatting:

- **Bold text** for emphasis
- *Italic text* for subtle emphasis
- [Links](https://example.com) to other websites
- Lists (like this one)

### Code Blocks with Syntax Highlighting

```python
def hello_world():
    print("Hello, World!")
    return True
```

## Media Embedding

Embed YouTube videos:

{% youtube id="dQw4w9WgXcQ" %}

Embed Google Slides:

{% slides id="YOUR_PRESENTATION_ID_HERE" %}

## Custom Tags

Link to another article (using its slug):

{% link article="articles/modern_architecture_patterns" %}

Link to a standalone page (like 'about'):

{% link page="about" %}

Display site configuration data:

Site Title: {% site_meta key="title" %}
Author: {% site_meta key="author" %}

## Images

![Alt text for your image](path/to/image.jpg)

## Blockquotes

> This is a blockquote. It's great for highlighting important points or quotes from other sources.

---

Horizontal rules like the one above can help separate content sections.

That's it! Save this file in the `content/publish/` directory with a `.md` extension to publish it.