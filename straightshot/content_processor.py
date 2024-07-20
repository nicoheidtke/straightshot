"""
Content processor for handling markdown files and frontmatter.
"""

import os
import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

import frontmatter
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

from straightshot.models import (
    BuildResult,
    ContentFile,
    ContentProcessingConfig,
    Metadata,
)


def load_content_files(
    config: ContentProcessingConfig,
    build_result: BuildResult,
    directory: Path,
    default_language: str = "en",
) -> List[ContentFile]:
    """Load all markdown files in a directory."""
    content_files = []
    if not directory.exists():
        build_result.warnings.append(f"Content directory not found: {directory}")
        return []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".md", ".markdown")):
                file_path = Path(root) / file
                try:
                    content_file = load_content_file(
                        config, build_result, file_path, True, default_language
                    )
                    if content_file and not content_file.metadata.disabled:
                        content_files.append(content_file)
                        build_result.files_processed += 1
                    elif content_file and content_file.metadata.disabled:
                        build_result.files_skipped += 1
                        build_result.warnings.append(
                            f"Skipped disabled file: {file_path}"
                        )
                    else:
                        build_result.files_skipped += 1
                except Exception as e:
                    build_result.errors.append(
                        f"Error processing {file_path}: {str(e)}"
                    )
                    build_result.files_skipped += 1
    return content_files


def load_content_file(
    config: ContentProcessingConfig,
    build_result: BuildResult,
    file_path: Path,
    require_frontmatter: bool = True,
    default_language: str = "en",
) -> Optional[ContentFile]:
    """Load a single markdown file using python-frontmatter."""
    try:
        post = frontmatter.load(file_path, encoding="utf-8")
        metadata_dict = post.metadata
        markdown_content = post.content
        if require_frontmatter:
            metadata = parse_frontmatter(config, metadata_dict, file_path)
        else:
            metadata = Metadata(
                title=str(metadata_dict.get("title", "Untitled")),
                written=metadata_dict.get("written", date.today()),
                topics=metadata_dict.get("topics", []),
                description=metadata_dict.get("description"),
                disabled=bool(metadata_dict.get("disabled", False)),
                image=metadata_dict.get("image"),
                lang=metadata_dict.get("lang", "en"),
            )
        html_content = process_markdown_content(markdown_content)
        url_slug, reference_slug = generate_slugs(
            config, file_path, metadata, default_language
        )
        url = f"content/{url_slug}.html"
        content_id = generate_content_id(file_path, metadata)
        return ContentFile(
            path=file_path,
            slug=url_slug,
            reference_slug=reference_slug,
            url=url,
            html=html_content,
            metadata=metadata,
            content_id=content_id,
        )
    except Exception as e:
        error_type = type(e).__name__
        build_result.errors.append(
            f"Error processing {file_path} ({error_type}): {str(e)}"
        )
        return None


def validate_content(
    build_result: BuildResult, content_files: List[ContentFile]
) -> bool:
    """Validate all content files for required fields and duplicates."""
    valid = True
    slugs: dict[str, Path] = {}
    titles: dict[str, Path] = {}
    for content_file in content_files:
        if content_file.slug in slugs:
            build_result.errors.append(
                f"Duplicate slug '{content_file.slug}' in {content_file.path} and {slugs[content_file.slug]}"
            )
            valid = False
        else:
            slugs[content_file.slug] = content_file.path
        if content_file.metadata.title in titles:
            build_result.warnings.append(
                f"Duplicate title '{content_file.metadata.title}' in {content_file.path} and {titles[content_file.metadata.title]}"
            )
        else:
            titles[content_file.metadata.title] = content_file.path
    return valid


def parse_frontmatter(
    config: ContentProcessingConfig, data: Dict[str, Any], file_path: Path
) -> Metadata:
    """Parse the metadata dictionary (already loaded by python-frontmatter)."""
    if not isinstance(data, dict):
        raise ValueError("Frontmatter did not parse as a dictionary.")
    validate_required_fields(config, data, file_path)
    if "written" not in data:
        raise ValueError("Missing required frontmatter field: written")
    if "topics" not in data:
        raise ValueError("Missing required frontmatter field: topics")
    written_date = parse_written_date(data["written"])
    topics_list = parse_topics(data["topics"])
    metadata = Metadata(
        title=str(data.get("title", "Untitled")),
        written=written_date,
        topics=topics_list,
    )
    for field in config.optional_frontmatter:
        if field in data:
            setattr(metadata, field, data[field])
    metadata.disabled = bool(data.get("disabled", False))
    return metadata


def validate_required_fields(
    config: ContentProcessingConfig, data: Dict[str, Any], file_path: Path
) -> None:
    for field in config.required_frontmatter:
        if field not in data:
            raise ValueError(f"Missing required frontmatter field: {field}")


def parse_written_date(written: Any) -> date:
    if isinstance(written, str):
        try:
            return date.fromisoformat(written)
        except ValueError as e:
            raise ValueError(
                "Invalid date format in 'written' field. Expected ISO format 'YYYY-MM-DD'."
            ) from e
    elif isinstance(written, date):
        return written
    else:
        raise ValueError(
            f"Invalid type for 'written' field: {type(written)}. Expected string (YYYY-MM-DD) or date object."
        )


def parse_topics(topics: Any) -> List[str]:
    if isinstance(topics, str):
        return [topic.strip() for topic in topics.split(",") if topic.strip()]
    elif isinstance(topics, list):
        return [str(topic).strip() for topic in topics if str(topic).strip()]
    else:
        raise ValueError(
            f"Invalid type for 'topics' field: {type(topics)}. Expected string or list."
        )


def _slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    slug = text.lower().replace(" ", "-").replace("_", "-")
    slug = re.sub(r"[^a-z0-9/-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def generate_slugs(
    config: ContentProcessingConfig,
    file_path: Path,
    metadata: Optional["Metadata"] = None,
    default_language: str = "en",
) -> tuple[str, str]:
    """Generate both the URL-friendly (hyphenated) slug and the reference slug (underscores preserved)."""
    relative_path = Path(file_path.name)
    for content_dir in config.content_dirs:
        if file_path.is_relative_to(content_dir):
            relative_path = file_path.relative_to(content_dir)

    path_parts = list(relative_path.parts)
    filename_stem = Path(path_parts[-1]).stem

    # Use custom slug from frontmatter if provided, otherwise use filename
    if metadata and metadata.id:
        path_parts[-1] = metadata.id
    else:
        path_parts[-1] = filename_stem

    reference_slug = "/".join(path_parts)
    url_slug_parts = [_slugify(part) for part in path_parts]
    url_slug = "/".join(url_slug_parts)

    # Always include language in the URL slug
    if metadata and metadata.lang:
        url_slug = f"{metadata.lang}/{url_slug}"
    else:
        # Use the provided default language instead of hardcoded "en"
        url_slug = f"{default_language}/{url_slug}"

    return url_slug, reference_slug


def process_markdown_content(markdown_text: str) -> str:
    """Convert Markdown text to HTML using markdown-it-py and Pygments for code highlighting."""

    def pygments_highlight(code: str, lang: str, attrs: str) -> str:
        try:
            lexer = get_lexer_by_name(lang) if lang else TextLexer()
        except Exception:
            lexer = TextLexer()
        formatter = HtmlFormatter(nowrap=True, cssclass="highlight")
        highlighted = highlight(code, lexer, formatter)
        return f'<pre class="highlight"><code>{highlighted}</code></pre>'

    md = (
        MarkdownIt("commonmark", {"typographer": True})
        .enable("table")
        .disable("smartquotes")
    )
    md.options["highlight"] = pygments_highlight
    html_content = md.render(markdown_text)
    return str(html_content)


def generate_content_id(file_path: Path, metadata: Optional["Metadata"] = None) -> str:
    """Generate a content ID for matching articles across languages."""
    if metadata and metadata.id:
        # Use id from frontmatter as the base ID
        return metadata.id
    else:
        # Use filename without extension as the base ID
        return Path(file_path.name).stem


def link_alternate_languages(content_files: List[ContentFile]) -> None:
    """Link content files that represent the same article in different languages."""
    # Group content files by their content ID
    content_groups: Dict[str, List[ContentFile]] = {}

    for content_file in content_files:
        if content_file.content_id:
            if content_file.content_id not in content_groups:
                content_groups[content_file.content_id] = []
            content_groups[content_file.content_id].append(content_file)

    # Link alternate languages for each group
    for _, group in content_groups.items():
        if len(group) > 1:  # Only link if there are multiple language versions
            for content_file in group:
                for other_file in group:
                    if other_file != content_file:
                        content_file.alternate_languages[other_file.metadata.lang] = (
                            other_file
                        )


def collect_site_languages(content_files: List[ContentFile]) -> List[str]:
    """Collect all unique languages from content files."""
    languages = set()
    for content_file in content_files:
        languages.add(content_file.metadata.lang)
    return sorted(languages)
