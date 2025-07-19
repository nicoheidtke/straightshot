"""
Utility functions for documentation handling.
"""

from pathlib import Path


def _get_docs_root() -> Path | None:
    """Get the root documentation directory."""

    # All paths to check for documentation files
    try_paths = [
        Path(__file__).parent.parent / "docs" / "user",  # When in local development
        Path(__file__).parent / "docs" / "user",  # When installed as: tar.gz / sdist
        Path(__file__) / "docs" / "user",  # When installed as: .whl / wheel
    ]

    # Check each path in the try_paths list
    for path in try_paths:
        try:
            if path.exists():
                return path
        except OSError:
            continue

    return None


def discover_documentation_files() -> dict[str, str]:
    """Discover available documentation files and return a mapping of names to paths."""
    docs_root = _get_docs_root()
    if not docs_root:
        return {}

    docs_map = {}

    try:
        # Find all .md files in docs directory and subdirectories
        for md_file in docs_root.rglob("*.md"):
            # Create a logical name from the file path relative to docs root
            relative_path = md_file.relative_to(docs_root)

            # Convert path to a logical name
            # bla/foo.md -> "bla/foo"
            logical_name = str(relative_path.with_suffix("")).replace("\\", "/")
            docs_map[logical_name] = str(relative_path)

    except OSError:
        pass

    return docs_map


def get_available_docs() -> list[str]:
    """Get a list of available documentation names for CLI choices."""
    docs_map = discover_documentation_files()
    return sorted(docs_map.keys())


def get_doc_content(doc_path: str) -> str | None:
    """Get documentation content from package data or local development files."""
    docs_root = _get_docs_root()
    if not docs_root:
        return None

    try:
        doc_file = docs_root / doc_path
        if doc_file.exists() and doc_file.is_file():
            return doc_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        pass

    return None
