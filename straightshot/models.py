"""
Data models for the site generator.
"""

from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

DEFAULT_DATE_FORMAT = "%Y-%m-%d"  # Default date format for the site
REQUIRED_FRONTMATTER = ["title", "written", "topics"]
OPTIONAL_FRONTMATTER = ["description", "disabled", "image", "lang", "id"]


class StandalonePageConfig(BaseModel):
    """Configuration for a standalone page generated from a template."""

    template: (
        str  # Path to the Jinja2 template file, relative to the templates directory.
    )
    output: Path  # Output path for the rendered file, relative to the output directory.


class Metadata(BaseModel):
    """Content file metadata from frontmatter."""

    title: str
    written: date
    topics: List[str]
    description: Optional[str] = None
    disabled: bool = False
    image: Optional[str] = None
    lang: str = "en"
    id: Optional[str] = (
        None  # Unique identifier for the content, can be used for multi-language support
    )


class ContentFile(BaseModel):
    """Represents a markdown content file."""

    path: Path
    slug: str
    reference_slug: str  # The slug matching the file structure (underscores preserved)
    url: str
    html: str
    metadata: Metadata
    # Navigation
    previous: Optional["ContentFile"] = None
    next: Optional["ContentFile"] = None
    related: List["ContentFile"] = Field(default_factory=list)
    # Multi-language support
    alternate_languages: Dict[str, "ContentFile"] = Field(default_factory=dict)
    content_id: Optional[str] = None  # Identifier for matching content across languages

    def __hash__(self) -> int:
        """Make ContentFile hashable by using the slug as the hash value."""
        return hash(self.slug)

    def __eq__(self, other: Any) -> bool:
        """Compare ContentFile objects based on their slugs."""
        if not isinstance(other, ContentFile):
            return False
        return self.slug == other.slug


class SiteContext(BaseModel):
    """Site-wide context for templates and configuration."""

    # --- Configuration fields (from former SiteConfig) ---
    title: str
    description: str
    author: str
    url: str
    language: str = "en"
    date_format: str = DEFAULT_DATE_FORMAT
    custom_tags: Dict[str, str] = Field(default_factory=dict)
    theme: Dict[str, Any] = Field(default_factory=dict)
    social: Dict[str, str] = Field(default_factory=dict)
    seo: Dict[str, Any] = Field(default_factory=dict)
    base_url: str = "/"
    current_year: int = Field(default_factory=lambda: datetime.now().year)
    standalone_pages: List[StandalonePageConfig] = Field(default_factory=list)
    data: Dict[str, Any] = Field(
        default_factory=dict
    )  # User-defined data from YAML/JSON includes

    # --- Runtime context fields ---
    articles: List[ContentFile] = Field(default_factory=list)
    topics: Dict[str, List[ContentFile]] = Field(default_factory=dict)
    languages: List[str] = Field(default_factory=list)  # All languages found in content

    def __post_init__(self) -> None:
        # Normalize base_url
        if not self.base_url.startswith("/"):
            self.base_url = "/" + self.base_url
        if self.base_url != "/" and not self.base_url.endswith("/"):
            self.base_url += "/"


class BuildResult(BaseModel):
    """Result of a site build operation."""

    success: bool = True
    files_processed: int = 0
    files_skipped: int = 0
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class ContentProcessingConfig(BaseModel):
    """Configuration for content processing and loading."""

    content_root: Path
    content_dirs: List[Path]
    templates_dir: Path
    static_dir: Path
    output_dir: Path
    required_frontmatter: List[str] = Field(
        default_factory=lambda: REQUIRED_FRONTMATTER.copy()
    )
    optional_frontmatter: List[str] = Field(
        default_factory=lambda: OPTIONAL_FRONTMATTER.copy()
    )
