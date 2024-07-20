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

[youtube: VIDEO_ID_HERE]

Embed Google Slides:

[slides: SLIDES_ID_HERE]

## Images

![Alt text for your image](path/to/image.jpg)

## Blockquotes

> This is a blockquote. It's great for highlighting important points or quotes from other sources.

---

Horizontal rules like the one above can help separate content sections.

## Testing Tags

Let's test the tags here:

YouTube: {% youtube id="test_video_id" %}
Slides: {% slides id="test_slides_id" %}
Link to article: {% link article="articles/cpp_modern_practices" %}
Link to page: {% link page="about" %}
Site Meta (Author): {% site_meta key=author %}

This should cover the basics.

That's it! Save this file in the `content/publish/` directory with a `.md` extension to publish it.