# Getting Started

This guide walks you through creating your first straightshot site step by step.

## Prerequisites

- Python 3.12 or higher
- A text editor or IDE

## Installation

Download and install straightshot from GitHub:

```sh
# Download from GitHub releases
# https://github.com/nicoheidtke/straightshot/releases

# Or install directly from GitHub
pip install git+https://github.com/nicoheidtke/straightshot.git
```

## Quick Start

### 1. Create the Directory Structure

Create a basic site structure:

```
my-site/
├── content/
│   ├── site.yaml           # Site configuration
│   ├── about.md           # About page content  
│   └── publish/           # Published articles
│       └── articles/
│           └── first-post.md
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page template
│   ├── article.html       # Article page template
│   └── about.html         # About page template
└── static/                # CSS, JS, images
    ├── css/
    │   └── main.css
    └── js/
        └── main.js
```

### 2. Basic Site Configuration

Create `content/site.yaml`:

```yaml
title: "My Blog"
description: "A blog about technology and life"
author: "Your Name"
url: "https://yourdomain.com"
language: "en"
base_url: "/"

standalone_pages:
  - template: "index.html"
    output_path: "index.html"
  - template: "about.html"
    output_path: "about.html" 
    content_source: "about.md"
```

### 3. Write Your First Article

Create `content/publish/articles/first-post.md`:

```yaml
---
title: "Welcome to My Blog"
written: 2024-01-15
description: "My first post using straightshot"
topics: welcome, meta
---

# Welcome to My Blog

This is my first post using straightshot! I'm excited to share my thoughts and experiences.

## Getting Started with straightshot

straightshot makes it easy to:

1. **Write in Markdown** - Focus on content, not formatting
2. **Organize content** - Simple directory structure
3. **Customize design** - Full control over templates and styling

Stay tuned for more posts!
```

### 4. Build Your Site

Run the build command:

```sh
straightshot build \
  --content-dir my-site/content \
  --templates-dir my-site/templates \
  --static-dir my-site/static \
  --output-dir my-site/output \
  --site-config my-site/content/site.yaml
```

### 5. Preview Your Site

Open `my-site/output/index.html` in your browser to see your site!

## Next Steps

Now that you have a basic site running:

1. **Customize your templates** - See [Templates & Theming](templates.md)
2. **Add more content** - See [Content Writing](content.md)
3. **Configure your site** - See [Site Configuration](configuration.md)

## Using the Example Site

The repository includes a complete example site at `example-site/`. You can:

1. **Study the structure** - See how a real site is organized
2. **Copy templates** - Use them as starting points for your own site
3. **Test locally** - Run `poetry poe example` to see it in action

The example site demonstrates all features and serves as both documentation and a working reference. See [Example Site Features](example-site.md) for details.
