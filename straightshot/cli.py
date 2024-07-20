"""
Command-line interface for straightshot static site generator.
"""

import argparse
import sys
from pathlib import Path


def _get_docs_choices() -> list[str]:
    """Get available documentation choices, with fallback for import issues."""
    try:
        from straightshot.docs_utils import get_available_docs

        return get_available_docs()
    except ImportError:
        # Fallback if there are import issues
        return ["features", "architecture"]


def setup_args() -> argparse.Namespace:
    """Set up command-line argument parsing."""
    parser = argparse.ArgumentParser(description="straightshot static site generator")

    # Create subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command (default)
    build_parser = subparsers.add_parser("build", help="Build the static site")
    build_parser.add_argument(
        "--content-dir",
        type=Path,
        required=True,
        help="Path to the root content directory",
    )
    build_parser.add_argument(
        "--templates-dir",
        type=Path,
        required=True,
        help="Path to the templates directory",
    )
    build_parser.add_argument(
        "--static-dir",
        type=Path,
        required=True,
        help="Path to the static files directory",
    )
    build_parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Path to the output (build) directory",
    )
    build_parser.add_argument(
        "--site-config",
        type=Path,
        required=True,
        help="Path to the site configuration YAML file (e.g., site.yaml)",
    )
    build_parser.add_argument(
        "--drafts", action="store_true", help="Include draft articles"
    )
    build_parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    build_parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean output directory before building",
    )
    build_parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="Override the base_url specified in site.yaml. Use '/' for root.",
    )

    # Docs command
    docs_parser = subparsers.add_parser("docs", help="Show documentation")
    docs_choices = _get_docs_choices()
    docs_parser.add_argument(
        "doc_name",
        nargs="?",
        default="features"
        if "features" in docs_choices
        else docs_choices[0]
        if docs_choices
        else "features",
        choices=docs_choices,
        help="Documentation to display (default: features)",
    )

    # For backward compatibility, add the build arguments at the top level too
    parser.add_argument(
        "--content-dir",
        type=Path,
        help="Path to the root content directory",
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        help="Path to the templates directory",
    )
    parser.add_argument(
        "--static-dir",
        type=Path,
        help="Path to the static files directory",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Path to the output (build) directory",
    )
    parser.add_argument(
        "--site-config",
        type=Path,
        help="Path to the site configuration YAML file (e.g., site.yaml)",
    )
    parser.add_argument("--drafts", action="store_true", help="Include draft articles")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean output directory before building",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="Override the base_url specified in site.yaml. Use '/' for root.",
    )

    args = parser.parse_args()

    # For backward compatibility: if no command is specified but build args are provided, assume build
    if args.command is None and args.content_dir is not None:
        args.command = "build"
    elif args.command is None:
        args.command = "build"  # Default to build

    return args


def validate_build_args(args: argparse.Namespace) -> None:
    """Validate that required build arguments are present."""
    required_args = [
        "content_dir",
        "templates_dir",
        "static_dir",
        "output_dir",
        "site_config",
    ]
    missing_args = [arg for arg in required_args if getattr(args, arg) is None]
    if missing_args:
        print(
            f"Error: Missing required arguments for build: {', '.join(f'--{arg.replace("_", "-")}' for arg in missing_args)}"
        )
        print("Use 'straightshot build --help' for more information.")
        sys.exit(1)
