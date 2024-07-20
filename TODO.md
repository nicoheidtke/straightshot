# TODO - Features to Implement

## SEO & Performance Features

- **Robots.txt generation** - Automatic robots.txt file creation with sitemap reference
- **Sitemap frontmatter controls** - Support for `sitemap: false`, `changefreq`, `priority` in content frontmatter
- **Analytics integration** - Google Analytics 4 and Search Console verification support
- **Advanced robots configuration** - Custom robots rules and per-page robots control
- **Custom permalinks** - Support for `permalink` field in frontmatter to override URLs
- **URL pattern configuration** - Configurable URL patterns for different content types
- **HTML/CSS minification** - Built-in minification for performance optimization
- **SEO validation commands** - CLI commands to validate SEO compliance (`--validate-seo`)
- **Feed configuration** - Advanced RSS feed options (`max_items`, `include_content`, etc.)
- **Hreflang tags** - Automatic hreflang generation for multi-language content
- **Performance optimizations** - Lazy loading, resource preloading, image optimization

## Content Features

- **Enhanced markdown features** - Math notation, footnotes, task lists, custom containers, admonitions
- **Content validation** - Validate required frontmatter fields, dates, broken links, missing images
- **Draft system improvements** - Better draft/publish workflow and `draft` flag support
- **Advanced custom tags** - External link tags with metadata, more media embeds

## Multi-language Features

- **Automatic language linking** - Auto-detect and link translations based on filename patterns
- **Language-specific sitemaps** - Generate separate sitemaps for different languages
- **Translation discovery** - Automatic detection of translation relationships

## Template & Theming

- **Theme system** - Pluggable theme support beyond basic configuration
- **Template inheritance** - Better template organization and reuse
- **Component system** - Reusable template components

## Build & Development

- **Watch mode** - File watching for development with auto-rebuild
- **Development server** - Built-in development server with live reload
- **Build optimization** - Incremental builds and caching
- **Plugin system** - Extensible plugin architecture for custom functionality
