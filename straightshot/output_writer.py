"""
Handles writing rendered content and static files to the output directory.
"""

import json
import shutil
from pathlib import Path
from typing import Any

from straightshot.models import BuildResult


def write_rendered_page(
    output_dir: Path,
    relative_output_path: Path,
    content: str,
    build_result: BuildResult,
) -> bool:
    """Write rendered HTML content to a file in the output directory."""
    absolute_output_path = output_dir / relative_output_path
    try:
        absolute_output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(absolute_output_path, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except Exception as e:
        build_result.errors.append(
            f"Error writing file {absolute_output_path}: {str(e)}"
        )
        return False


def write_json_file(
    output_dir: Path, relative_output_path: Path, data: Any, build_result: BuildResult
) -> bool:
    """Write JSON data to a file in the output directory."""
    absolute_output_path = output_dir / relative_output_path
    try:
        absolute_output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(absolute_output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        build_result.errors.append(
            f"Error writing JSON file {absolute_output_path}: {e}"
        )
        return False


def copy_static_assets(
    static_dir: Path, output_dir: Path, build_result: BuildResult
) -> bool:
    """Copy static files from the static directory to the output directory."""
    static_output = output_dir / "static"

    if not static_dir.exists():
        build_result.warnings.append(
            f"Static directory not found, skipping copy: {static_dir}"
        )
        return True  # Not an error if static dir doesn't exist

    try:
        if static_output.exists():
            shutil.rmtree(static_output)
        shutil.copytree(static_dir, static_output, dirs_exist_ok=True)
        return True
    except Exception as e:
        build_result.errors.append(
            f"Error copying static files from {static_dir} to {static_output}: {str(e)}"
        )
        return False
