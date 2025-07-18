# SEO & Performance

## Meta Tags

Template blocks in `base.html` and `article.html` generate:

- Page titles (`<title>` tag)
- Meta descriptions (`<meta name="description">`)
- Canonical URLs (`<link rel="canonical">`)
- Open Graph tags (`<meta property="og:*">`)
- Twitter Card tags (`<meta name="twitter:*">`)

## Structured Data

JSON-LD structured data is generated via template blocks:

- Website schema (homepage)
- BlogPosting schema (articles)

## Sitemap

XML sitemap template (`sitemap.xml`) generates `/sitemap.xml` with:

- All published articles and pages
- Static modification dates and priorities

Configured via `site.yaml`:

```yaml
standalone_pages:
  - template: sitemap.xml
    output: sitemap.xml
```

## RSS Feed

RSS feed template (`feed.xml`) generates `/feed.xml` with:

- Recent articles (last 15)
- Article topics as categories

Configured via `site.yaml`:

```yaml
standalone_pages:
  - template: feed.xml
    output: feed.xml
```

## URLs

- Clean URLs without file extensions
- Slug-based paths derived from filenames

## Multi-language

- `lang` attribute on `<html>` element
- Language metadata field in frontmatter
- Filename-based language detection (`.es.md`, `.fr.md`)

## Performance

Static site generation provides:

- Pre-built HTML files
- No server-side processing
- CDN compatibility
