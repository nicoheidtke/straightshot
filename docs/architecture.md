# straightshot Architecture

This document outlines the design principles, technology choices, and build workflow of the straightshot static site generator.

## Design Philosophy

straightshot was designed with the following principles in mind:

1. **Simplicity First**: Easy to understand, configure, and maintain without complex tooling
2. **Performance by Default**: Generate fast-loading static pages with minimal client-side JavaScript
3. **Developer Experience**: Provide clear workflows and comprehensive documentation
4. **Extensibility**: Allow for customization through templates and configuration
5. **Progressive Enhancement**: Ensure content is accessible regardless of JavaScript availability
6. **SEO Optimization**: Built-in support for modern SEO best practices

## Technology Stack

### Core Technologies

- **Python 3.12+**: Modern Python with type hints and dataclasses
- **Markdown**: Content authoring with YAML frontmatter for metadata
- **Jinja2**: Powerful templating engine for HTML generation
- **Pygments**: Syntax highlighting for code blocks
- **Pydantic**: Data validation and settings management

### Content Processing

- **python-frontmatter**: YAML frontmatter parsing from Markdown files
- **mdit-py-plugins**: Enhanced Markdown processing capabilities
- **PyYAML**: Configuration file processing and data includes

## Build Workflow

The build process follows a straightforward pipeline that transforms your content and configuration into a static website:

### 1. Configuration Loading

The generator loads your site configuration from `site.yaml`, which includes:
- Site metadata (title, description, author)
- Build settings (base URL, date formats)
- Navigation and data includes
- Standalone page definitions

### 2. Content Discovery

The system scans your content directories to find:
- Published content in the `publish/` directory
- Draft content in the `drafts/` directory (when enabled)
- Special content files referenced by standalone pages

### 3. Content Processing

Each Markdown file undergoes:
- YAML frontmatter extraction for metadata
- Markdown-to-HTML conversion with syntax highlighting
- Content validation (required fields, date formats)
- Custom tag processing (YouTube embeds, slides, etc.)

### 4. Template Rendering

The generator creates HTML pages by:
- Setting up the Jinja2 environment with your templates
- Rendering content pages using appropriate templates
- Generating standalone pages (index, about, blog listings)
- Creating machine-readable outputs (sitemap, RSS feeds)

### 5. Asset Handling

Static assets are processed by:
- Copying all files from the `static/` directory
- Preserving directory structure and file permissions
- No modification or optimization (kept simple)

### 6. Output Generation

The final static site includes:
- HTML pages for all content
- JSON data files for dynamic features
- Static assets (CSS, JavaScript, images)
- SEO files (sitemap.xml, feed.xml)

## Template System

straightshot uses Jinja2 templates with a hierarchical approach:

- **Base Templates**: Common page structure and layout
- **Content Templates**: Specific layouts for articles, talks, etc.
- **Partial Templates**: Reusable components and macros
- **Special Templates**: Machine-readable formats (XML, JSON)

Templates have access to:
- Site configuration data
- Content metadata and body
- Navigation data
- Article indices and lists

## Content Organization

Content follows a structured approach:

- **Frontmatter**: YAML metadata at the top of each file
- **Content Types**: Articles, talks, and custom content types
- **Status Management**: Published vs. draft content separation
- **Topic Organization**: Tag-based content categorization

## Configuration-Driven Design

The generator emphasizes configuration over convention:

- **Site Behavior**: Controlled through `site.yaml`
- **Data Includes**: External YAML/JSON files for structured data
- **Template Selection**: Configurable template mapping
- **Build Options**: Command-line flags for build variations

This approach allows multiple users to create vastly different sites using the same generator while maintaining simplicity and consistency.
