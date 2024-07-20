"""
straightshot Static Site Generator

Main entry point that orchestrates CLI parsing and site building.
"""

import logging
import shutil
import sys
import traceback
from pathlib import Path

from straightshot.builder import build_site
from straightshot.cli import setup_args, validate_build_args
from straightshot.config import load_site_context_from_path
from straightshot.docs_utils import discover_documentation_files, get_doc_content
from straightshot.models import ContentProcessingConfig, SiteContext


def show_documentation(doc_name: str = "features") -> None:
    """Display documentation from the package."""
    # Discover available documentation
    docs_map = discover_documentation_files()

    if not docs_map:
        print("No documentation files found.")
        print()
        print("You can find the documentation online at:")
        print("https://github.com/nicoheidtke/straightshot/tree/main/docs")
        return

    # Handle the requested document
    if doc_name not in docs_map:
        print(f"Unknown documentation: {doc_name}")
        print("Available documentation:")
        for name in sorted(docs_map.keys()):
            print(f"  - {name}")
        print()
        print("You can also find the documentation online at:")
        print("https://github.com/nicoheidtke/straightshot/tree/main/docs")
        return

    doc_content = get_doc_content(docs_map[doc_name])

    if doc_content:
        print(doc_content)
    else:
        print(f"Documentation file not found: {doc_name}")
        print("Available documentation:")
        for name in sorted(docs_map.keys()):
            print(f"  - {name}")
        print()
        print("You can also find the documentation online at:")
        print("https://github.com/nicoheidtke/straightshot/tree/main/docs")


def setup_logging(verbose: bool) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def load_config(site_config_path: Path, base_url_override: str | None) -> SiteContext:
    """Load site configuration from file with optional base URL override."""
    logger = logging.getLogger(__name__)
    try:
        site_context = load_site_context_from_path(site_config_path)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Error loading site configuration: {e}")
        sys.exit(1)
    if base_url_override is not None:
        logger.info(
            f"Overriding base_url with command-line value: '{base_url_override}'"
        )
        site_context.base_url = base_url_override
        site_context.__post_init__()  # re-normalize
    return site_context


def main() -> None:
    """Main entry point for the straightshot CLI."""
    try:
        args = setup_args()

        # Handle docs command
        if args.command == "docs":
            show_documentation(args.doc_name)
            return

        # Handle build command (default)
        if args.command == "build":
            validate_build_args(args)
            setup_logging(args.verbose)

            logger = logging.getLogger(__name__)

            if args.clean and args.output_dir.exists():
                logger.info(f"Cleaning output directory: {args.output_dir}")
                shutil.rmtree(args.output_dir)

            logger.info("Loading site config...")
            site_context = load_config(args.site_config, args.base_url)

            content_dirs = [args.content_dir / "publish"] + (
                [args.content_dir / "drafts"] if args.drafts else []
            )
            content_config = ContentProcessingConfig(
                content_root=args.content_dir,
                content_dirs=content_dirs,
                static_dir=args.static_dir,
                templates_dir=args.templates_dir,
                output_dir=args.output_dir,
            )

            logger.info("Building site...")
            result = build_site(site_context, content_config)

            if not result.success:
                logger.error(f"Build failed with {len(result.errors)} errors")
                sys.exit(1)

            sys.exit(0)

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error building site: {e}")
        print(traceback.format_exc())
        sys.exit(-1)


if __name__ == "__main__":
    main()
