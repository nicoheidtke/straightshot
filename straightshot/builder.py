"""
Core site building functionality for straightshot.
"""

import logging
import time
from pathlib import Path
from typing import Any

import jinja2

from straightshot.content_processor import (
    collect_site_languages,
    link_alternate_languages,
    load_content_files,
    validate_content,
)
from straightshot.custom_tags import process_custom_tags
from straightshot.models import (
    BuildResult,
    ContentFile,
    ContentProcessingConfig,
    SiteContext,
)
from straightshot.output_writer import (
    copy_static_assets,
    write_json_file,
    write_rendered_page,
)
from straightshot.templating import (
    create_jinja_environment,
    render_template,
)


def build_template_context(
    site_context: SiteContext, **additional_context: Any
) -> dict[str, Any]:
    """Build a standardized template context with site data and any additional context."""
    context = {"site": site_context, **additional_context}
    return context


def process_content(
    env: jinja2.Environment,
    site_context: SiteContext,
    content_config: ContentProcessingConfig,
    build_result: BuildResult,
    content_files: list[ContentFile],
) -> None:
    """Process and render content files."""
    logger = logging.getLogger(__name__)
    logger.info(f"Rendering {len(content_files)} content files...")

    for content_file in content_files:
        logger.debug(f"Processing content file: {content_file.path}")

        # Process custom tags first, passing the Jinja environment
        content_file.html = process_custom_tags(
            content_file.html,
            env,
            site_context,
            build_result,
        )
        try:
            rendered_html = render_template(
                env,
                "article.html",
                build_template_context(site_context, page=content_file),
            )
            relative_output_path = Path("content") / f"{content_file.slug}.html"
            if not write_rendered_page(
                content_config.output_dir,
                relative_output_path,
                rendered_html,
                build_result,
            ):
                build_result.success = False
        except jinja2.TemplateNotFound as e:
            error_msg = f"Template not found for content file {content_file.path}: {e}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False
        except jinja2.TemplateSyntaxError as e:
            error_msg = f"Template syntax error in article.html at line {e.lineno} (processing {content_file.path}): {e.message}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False
        except jinja2.TemplateRuntimeError as e:
            error_msg = f"Template runtime error in article.html (processing {content_file.path}): {e.message}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False
        except Exception as e:
            error_msg = f"Error rendering template for {content_file.path}: {e}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False


def _generate_article_index_data(
    env: jinja2.Environment, content_files: list[ContentFile]
) -> list[dict[str, Any]]:
    """Generates the list of dictionaries for the article index JSON."""
    article_index = []
    for article in content_files:
        slug_parts = article.slug.split("/")
        category = slug_parts[0] if len(slug_parts) > 1 else "general"
        topics = list(article.metadata.topics)
        article_index.append(
            {
                "slug": article.slug,
                "title": article.metadata.title,
                "description": article.metadata.description or "",
                "written": article.metadata.written.isoformat(),
                "topics": topics,
                "url": article.url,
                "category": category,
                "lang": article.metadata.lang,
                "content_id": article.content_id,
                "alternate_languages": list(article.alternate_languages.keys()),
            }
        )
    return article_index


def build_standalone_pages(
    env: jinja2.Environment,
    site_context: SiteContext,
    content_config: ContentProcessingConfig,
    build_result: BuildResult,
    article_index: list[dict[str, Any]],
) -> None:
    """Render all standalone pages as defined in the site configuration."""
    logger = logging.getLogger(__name__)

    logger.info(f"Rendering {len(site_context.standalone_pages)} standalone pages...")

    for page_cfg in site_context.standalone_pages:
        logger.debug(
            f"Rendering standalone page: {page_cfg.template} -> {page_cfg.output}"
        )

        context = build_template_context(
            site_context,
            articles=site_context.articles,
            topics=site_context.topics,
            article_index=article_index,
        )

        try:
            rendered = env.get_template(page_cfg.template).render(context)
            if not write_rendered_page(
                content_config.output_dir,
                page_cfg.output,
                rendered,
                build_result,
            ):
                build_result.success = False
        except jinja2.TemplateNotFound as e:
            error_msg = f"Template not found for standalone page: {e}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False
        except jinja2.TemplateSyntaxError as e:
            error_msg = f"Template syntax error in {page_cfg.template} at line {e.lineno}: {e.message}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False
        except jinja2.TemplateRuntimeError as e:
            error_msg = f"Template runtime error in {page_cfg.template}: {e.message}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False
        except Exception as e:
            error_msg = f"Failed to render standalone page {page_cfg.template}: {e}"
            logger.error(error_msg)
            build_result.errors.append(error_msg)
            build_result.success = False


def update_site_topics(
    content_files: list[ContentFile], site_context: SiteContext
) -> None:
    """Update the site_context.topics dictionary with topics from content files."""
    for content_file in content_files:
        for topic in content_file.metadata.topics:
            if topic not in site_context.topics:
                site_context.topics[topic] = []
            site_context.topics[topic].append(content_file)


def _find_navigation_target(
    current_file: ContentFile,
    content_files: list[ContentFile],
    current_index: int,
    direction: int,
    default_language: str,
) -> ContentFile | None:
    """Find the best navigation target, skipping alternate language versions."""
    current_lang = current_file.metadata.lang

    # Search in the specified direction (1 for next, -1 for previous)
    i = current_index + direction
    while 0 <= i < len(content_files):
        candidate = content_files[i]

        # Skip alternate language versions of the current article
        if current_file.content_id and candidate.content_id == current_file.content_id:
            i += direction
            continue

        # Found a different article - now find the best language version
        # If candidate is in the same language as current file, use it
        if candidate.metadata.lang == current_lang:
            return candidate

        # If candidate has an alternate language version in current language, use that
        if current_lang in candidate.alternate_languages:
            return candidate.alternate_languages[current_lang]

        # If current file is not in default language, try to get default language version
        if (
            current_lang != default_language
            and default_language in candidate.alternate_languages
        ):
            return candidate.alternate_languages[default_language]

        # Otherwise, use the candidate as-is
        return candidate

    return None


def compute_related_content_for_files(
    content_files: list[ContentFile], site_context: SiteContext
) -> None:
    """Compute previous/next and related content for each file."""
    default_language = site_context.language

    for i, file in enumerate(content_files):
        # Previous/Next navigation: chronological with language preference, skipping alternate versions
        file.previous = _find_navigation_target(
            file, content_files, i, -1, default_language
        )
        file.next = _find_navigation_target(file, content_files, i, 1, default_language)

        # Related content: topic-based, excluding alternate language versions
        topic_matches: dict[ContentFile, int] = {}
        for topic in file.metadata.topics:
            if topic in site_context.topics:
                for related_file in site_context.topics[topic]:
                    # Skip self
                    if related_file == file:
                        continue
                    # Skip alternate language versions of the same article
                    if file.content_id and related_file.content_id == file.content_id:
                        continue
                    topic_matches[related_file] = topic_matches.get(related_file, 0) + 1

        # Sort related content by number of matching topics (descending)
        file.related = [
            related_file
            for related_file, count in sorted(
                topic_matches.items(), key=lambda x: x[1], reverse=True
            )
        ]


def setup_build_environment(content_config: ContentProcessingConfig) -> None:
    """Set up the build environment by creating necessary directories."""
    logger = logging.getLogger(__name__)
    logger.info("Creating output directory...")
    content_config.output_dir.mkdir(parents=True, exist_ok=True)


def load_and_process_content(
    content_config: ContentProcessingConfig,
    site_context: SiteContext,
    build_result: BuildResult,
) -> list[ContentFile]:
    """Load content files from all configured directories and process them."""
    logger = logging.getLogger(__name__)
    logger.info("Loading site content...")

    content_files = []
    for directory in content_config.content_dirs:
        directory_name = directory.name if directory.name else str(directory)
        logger.info(f"Loading site content from {directory}...")
        dir_files = load_content_files(
            content_config, build_result, directory, site_context.language
        )
        content_files.extend(dir_files)
        logger.debug(f"Loaded {len(dir_files)} files from {directory_name}")

    content_files.sort(key=lambda x: x.metadata.written, reverse=True)
    logger.debug(f"Total content files loaded: {len(content_files)}")

    if not validate_content(build_result, content_files):
        logger.warning("Content validation failed.")
        build_result.success = False

    return content_files


def process_site_metadata(
    content_files: list[ContentFile], site_context: SiteContext
) -> None:
    """Process site-wide metadata including topics, languages, and related content."""
    logger = logging.getLogger(__name__)

    # Assign loaded articles to the site context
    site_context.articles = content_files

    # Collect all topics from content files and add them to the site context
    update_site_topics(site_context.articles, site_context)

    # Process multi-language support
    logger.info("Processing multi-language content...")
    link_alternate_languages(content_files)
    site_context.languages = collect_site_languages(content_files)

    # Calculate related content using site_context.topics
    logger.info("Computing related content...")
    compute_related_content_for_files(site_context.articles, site_context)


def generate_site_output(
    content_config: ContentProcessingConfig,
    site_context: SiteContext,
    content_files: list[ContentFile],
    build_result: BuildResult,
) -> None:
    """Generate all HTML output including content pages and standalone pages."""
    logger = logging.getLogger(__name__)
    logger.info("Generating site HTML...")

    # Create Jinja environment
    jinja_env = create_jinja_environment(
        content_config.templates_dir, site_context, content_config.content_root
    )

    # Process content files
    process_content(
        jinja_env,
        site_context,
        content_config,
        build_result,
        content_files,
    )

    # Generate article index JSON
    logger.info("Generating article index JSON...")
    article_index_data = _generate_article_index_data(jinja_env, site_context.articles)
    content_index_json_rel_path = Path("content") / "index.json"
    if not write_json_file(
        content_config.output_dir,
        content_index_json_rel_path,
        article_index_data,
        build_result,
    ):
        logger.error("Failed to write article index JSON file.")
        build_result.success = False

    # Copy static assets
    if not copy_static_assets(
        content_config.static_dir, content_config.output_dir, build_result
    ):
        logger.error("Failed to copy static assets.")
        build_result.success = False

    # Build standalone pages
    build_standalone_pages(
        jinja_env,
        site_context,
        content_config,
        build_result,
        article_index_data,
    )


def print_build_summary(build_result: BuildResult, elapsed_time: float) -> None:
    """Print a summary of the build results."""
    logger = logging.getLogger(__name__)
    logger.info(f"Build completed in {elapsed_time:.2f} seconds")
    logger.info(f"Processed: {build_result.files_processed} files")
    logger.info(f"Skipped: {build_result.files_skipped} files")
    if build_result.warnings:
        logger.warning(f"Warnings ({len(build_result.warnings)}):")
        for warning in build_result.warnings:
            logger.warning(f"- {warning}")
    if build_result.errors:
        logger.error(f"Errors ({len(build_result.errors)}):")
        for error in build_result.errors:
            logger.error(f"- {error}")


def build_site(
    site_context: SiteContext,
    content_config: ContentProcessingConfig,
) -> BuildResult:
    """Build the complete static site."""
    logger = logging.getLogger(__name__)

    start_time = time.time()
    build_result = BuildResult()

    try:
        # Setup
        setup_build_environment(content_config)

        # Load and validate content
        content_files = load_and_process_content(
            content_config, site_context, build_result
        )

        # Process site metadata
        process_site_metadata(content_files, site_context)

        # Generate output
        generate_site_output(content_config, site_context, content_files, build_result)

    except Exception as e:
        logger.error(f"Critical error during site build: {e}")
        build_result.errors.append(f"Critical build error: {e}")
        build_result.success = False

    # Final error check
    if build_result.errors:
        build_result.success = False

    elapsed_time = time.time() - start_time
    print_build_summary(build_result, elapsed_time)

    return build_result
