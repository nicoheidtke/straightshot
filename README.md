# **Straightshot** - a static site generator

A Python-based static site generator for blogs. It transforms Markdown content with YAML frontmatter into a HTML.

**Straightshot** was created to provide a fun way for me to create and maintain my own blog.
Its like Hugo, but worse. But also simpler.

## Features

**Straightshot** offers a range of features for building static websites:
- Configuration-driven site generation
- Custom Jinja2 templates
- Markdown with YAML frontmatter
- Responsive, mobile-first design
- SEO optimization by default
- Minimal client-side code
- Draft and published content separation
- Simple CLI for building and maintaining it

## Installation

Download the latest release from GitHub:

```sh
# Download and install a package manually from the github releases page
https://github.com/nicoheidtke/straightshot/releases

# Install directly from GitHub
pip install git+https://github.com/nicoheidtke/straightshot.git
```

**Note**: No PyPI package is available yet - installation is currently only available from GitHub releases or source.

## Quick Start

Create a simple site structure:

```
my-site/
├── content/
│   ├── site.yaml           # Site configuration
│   ├── index.md           # Home page content
│   └── publish/           # Blog articles and content
│       ├── articles/
│       │   └── my-first-post.md
│       └── talks/
│           └── my-presentation.md
├── templates/
│   └── base.html          # Base template
└── static/                # CSS, JS, images
```

Add content with YAML frontmatter:

```yaml
---
title: Welcome to My Site
written: 2024-01-15
description: My awesome new website
topics: welcome, blog
---

# Welcome

This is my first post using straightshot!
```

**Blog articles** go in the `content/publish/` directory, organized by content type (e.g., `articles/`, `talks/`). Each Markdown file becomes a page on your site.

Build your site:

```sh
straightshot build \
  --content-dir my-site/content \
  --templates-dir my-site/templates \
  --static-dir my-site/static \
  --output-dir output \
  --site-config my-site/content/site.yaml
```

For detailed configuration and features, see the [Features Documentation](docs/features.md).

### Example Site

A complete example site is included in the repository at [`example-site/`](example-site/). This demonstrates:
- Site configuration and structure
- Template organization and inheritance
- Content organization with articles and talks
- Static asset management
- Data includes and navigation setup

You can use this as a starting point or reference for building your own site.

## Requirements

- Python 3.12 or higher

## Documentation

- **[Features Documentation](docs/features.md)**: An explanation of all features including Markdown processing, templating, media embeds, and configuration options
- **[Architecture Documentation](docs/architecture.md)**: Information about the internal design, build process, and technical decisions
- **[Development Guide](DEVELOPMENT.md)**: Development tasks, setup instructions, and contribution workflow
- **[Changelog](CHANGELOG.md)**: Version history and notable changes
- **[Contributing Guidelines](CONTRIBUTING.md)**: Current project status and contribution information

### Built-in CLI Help

You can also access documentation directly from the command line:

```sh
# Show features documentation (default)
straightshot docs

# Show specific documentation
straightshot docs features
straightshot docs architecture

# Get help on any command
straightshot --help
straightshot build --help
straightshot docs --help
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



