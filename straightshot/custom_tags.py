"""
Custom tag processing for straightshot articles.
"""

import re
from typing import Dict

import jinja2  # Import jinja2

from straightshot.models import (
    BuildResult,
    ContentFile,
    SiteContext,
)


def parse_tag_args(args_str: str) -> dict[str, str]:
    args_pattern = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\\\']*)\'|([^\s%]+))')
    args = {}
    for arg_match in args_pattern.finditer(args_str):
        key = arg_match.group(1)
        value = arg_match.group(2) or arg_match.group(3) or arg_match.group(4)
        args[key] = value
    return args


def process_link_tag(
    args: Dict[str, str],
    reference_content_map: Dict[str, ContentFile],  # Use reference map
    site_context: SiteContext,
    env: jinja2.Environment,
) -> str:
    """Process the {% link %} tag."""
    target_slug = args.get("article")
    if not target_slug:
        return "<!-- Link tag error: Missing 'article' argument -->"

    # Lookup using the reference slug map
    target_content = reference_content_map.get(target_slug)

    if not target_content:
        return f"<a href=\"#\">Article '{target_slug}' not found</a>"

    template = env.get_template("tags/link.html")
    context = {
        "url": f"{site_context.base_url.rstrip('/')}/{target_content.url}",
        "title": target_content.metadata.title,
        "args": args,  # Pass original args too
        "site": site_context,
    }
    return template.render(context)


def process_site_meta_tag(
    tag_context: dict[str, object],
    args: dict[str, str],
    site_context: SiteContext,
    build_result: BuildResult,
) -> None:
    key = args["key"]
    value = getattr(site_context, key, None)
    if value is not None:
        tag_context["value"] = str(value)
    else:
        value = getattr(site_context, key, None)
        if value is not None:
            tag_context["value"] = str(value)
        else:
            build_result.warnings.append(
                f"Custom tag 'site_meta' error: Key '{key}' not found in site context or config."
            )
            tag_context["value"] = f"[site_meta: {key} not found]"


def process_custom_tags(
    html_content: str,
    env: jinja2.Environment,  # Add Jinja environment parameter
    site_context: SiteContext,
    build_result: BuildResult,
) -> str:
    """Process custom {% tagname key="value" ... %} tags within HTML content."""

    # Build the reference_content_map for link lookups
    reference_content_map = {cf.reference_slug: cf for cf in site_context.articles}

    custom_tags_config = site_context.custom_tags
    tag_pattern = re.compile(r"{%\s*(\w+)\s*(.*?)\s*%}")

    def replace_tag(match: re.Match[str]) -> str:
        tag_name = match.group(1).strip()
        args_str = match.group(2).strip()
        original_tag = str(match.group(0))

        # Check if tag is defined in config *before* parsing args
        if tag_name not in custom_tags_config:
            build_result.warnings.append(
                f"Custom tag error: Unknown tag '{{% {tag_name} ... %}}'. "
                f"Ensure it's defined in site.yaml's 'custom_tags'."
            )
            # Return original tag to avoid breaking content
            return original_tag

        try:
            args = parse_tag_args(args_str)
        except ValueError as e:
            build_result.errors.append(
                f"Custom tag error: Failed to parse arguments for tag '{tag_name}': {e}"
            )
            return original_tag  # Return original tag on parse error

        template_path = custom_tags_config[tag_name]

        # Base context includes parsed args and site context
        tag_context = {
            "args": args,
            "site": site_context,
            "base_url": site_context.base_url,  # Keep base_url for convenience
        }

        # --- Call specific processors ONLY for tags needing complex logic ---
        if tag_name == "link":
            return process_link_tag(args, reference_content_map, site_context, env)
        elif tag_name == "site_meta" and "key" in args:
            # Populates tag_context['value']
            process_site_meta_tag(tag_context, args, site_context, build_result)

        # --- Render the tag using its template (for tags other than 'link') ---
        try:
            template = env.get_template(template_path)
            rendered_tag = template.render(tag_context)
            return rendered_tag
        except jinja2.TemplateNotFound:
            build_result.errors.append(
                f"Custom tag error: Template '{template_path}' not found for tag '{tag_name}'."
            )
            return original_tag  # Return original tag if template missing
        except Exception as e:
            build_result.errors.append(
                f"Custom tag error: Failed to render template '{template_path}' for tag '{tag_name}': {e}"
            )
            return original_tag  # Return original tag on render error

    processed_content = tag_pattern.sub(replace_tag, html_content)
    return processed_content
