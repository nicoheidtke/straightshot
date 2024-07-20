"""
Handles Jinja2 environment setup, context creation, and template rendering to strings.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import frontmatter
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from straightshot.content_processor import process_markdown_content
from straightshot.models import SiteContext


def _register_filters(env: Environment, site_context: SiteContext) -> None:
    """Register custom Jinja filters."""

    # --- Filters ---
    def format_date(date: datetime, format_string: str | None = None) -> str:
        fmt = format_string if format_string is not None else site_context.date_format
        return date.strftime(fmt)

    env.filters["date"] = format_date

    def now_filter(format_string: str | None = None) -> str:
        fmt = format_string if format_string is not None else site_context.date_format
        return datetime.now().strftime(fmt)

    env.filters["now"] = now_filter


def _register_globals(
    env: Environment, site_context: SiteContext, content_root: Path
) -> None:
    """Register custom Jinja global functions."""
    logger = logging.getLogger(__name__)

    # --- Globals ---
    def url_for(path: str) -> str:
        base_url = site_context.base_url
        if not path:
            return base_url
        return base_url.rstrip("/") + "/" + path.lstrip("/")

    env.globals["url_for"] = url_for

    def absolute_url_for(path: str) -> str:
        domain = site_context.url.rstrip("/")
        relative_url = url_for(path)
        return f"{domain}{relative_url}"

    env.globals["absolute_url_for"] = absolute_url_for

    def _include_markdown(relative_path_str: str) -> str | Markup:
        """
        Reads a Markdown file relative to the content root, strips frontmatter,
        processes the content, and returns safe HTML or an error comment string.
        """
        try:
            # Resolve the path relative to the content root
            markdown_file_path = (content_root / relative_path_str).resolve()

            # Security check: Ensure the resolved path is still within the content root
            if not markdown_file_path.is_relative_to(content_root.resolve()):
                logger.warning(
                    f"Attempted to include markdown file outside content root: {relative_path_str}"
                )
                return "<!-- Error: Invalid path -->"

            if not markdown_file_path.is_file():
                logger.warning(
                    f"Markdown file not found for inclusion: {markdown_file_path}"
                )
                return f"<!-- Error: Markdown file not found: {relative_path_str} -->"

            # Load using frontmatter to separate content from metadata
            post = frontmatter.load(markdown_file_path, encoding="utf-8")
            markdown_content = post.content  # Use only the content part

            # Process markdown content
            html_content = process_markdown_content(markdown_content)
            # Return as Markup to prevent double escaping, suppress Bandit warning
            return Markup(html_content)  # noqa: S704
        except Exception as e:
            logger.error(f"Error including markdown file {relative_path_str}: {e}")
            # Return plain string, not Markup
            return f"<!-- Error processing markdown: {relative_path_str} -->"

    env.globals["include_markdown"] = _include_markdown


def create_jinja_environment(
    templates_dir: Path, site_context: SiteContext, content_root: Path
) -> Environment:
    """Create and configure the Jinja2 environment."""
    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    _register_filters(env, site_context)
    _register_globals(env, site_context, content_root)

    return env


def render_template(
    env: Environment, template_name: str, context: Dict[str, Any]
) -> str:
    """Render a template to a string."""
    template = env.get_template(template_name)
    full_context = {**context}
    if (
        "site" not in full_context and "page" in context
    ):  # Add site context if rendering a page
        # This assumes 'page' context implies needing 'site' context, adjust if needed
        # A better approach might be to always ensure 'site' is passed explicitly
        # from the orchestration layer. For now, mimic old behavior.
        pass  # The orchestration layer should now explicitly pass 'site' if needed.

    return template.render(full_context)
