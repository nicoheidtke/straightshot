"""
Configuration settings for the straightshot site generator.
"""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml

# Import SiteContext from models
from straightshot.models import SiteContext


class DataFileLoader(ABC):
    """Abstract base class for data file loaders."""

    @property
    @abstractmethod
    def directive_prefix(self) -> str:
        """The directive prefix for this loader (e.g., '$$include_yaml')."""
        pass

    @property
    @abstractmethod
    def file_format_name(self) -> str:
        """Human-readable name of the file format."""
        pass

    @abstractmethod
    def load(self, file_path: Path) -> Any:
        """
        Load and parse a data file.

        Args:
            file_path: Path to the file to load

        Returns:
            Parsed file content

        Raises:
            ValueError: If file parsing fails
        """
        pass


class YamlLoader(DataFileLoader):
    """Loader for YAML files."""

    @property
    def directive_prefix(self) -> str:
        return "$$include_yaml"

    @property
    def file_format_name(self) -> str:
        return "YAML"

    def load(self, file_path: Path) -> Any:
        """Load and parse a YAML file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(
                f"Invalid {self.file_format_name} in file {file_path}: {e}"
            ) from e


class JsonLoader(DataFileLoader):
    """Loader for JSON files."""

    @property
    def directive_prefix(self) -> str:
        return "$$include_json"

    @property
    def file_format_name(self) -> str:
        return "JSON"

    def load(self, file_path: Path) -> Any:
        """Load and parse a JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid {self.file_format_name} in file {file_path}: {e}"
            ) from e


# Registry of available loaders
_LOADERS = [YamlLoader(), JsonLoader()]
_LOADER_MAP = {loader.directive_prefix: loader for loader in _LOADERS}


def _process_includes(data: Any, content_root: Path) -> Any:
    """
    Recursively process $$include_* directives in data structure.

    Args:
        data: The data structure to process (dict, list, or any other type)
        content_root: Root directory for resolving file paths

    Returns:
        Processed data structure with includes resolved

    Raises:
        ValueError: If file loading fails or security constraints are violated
    """
    if isinstance(data, dict):
        return {
            key: _process_includes(value, content_root) for key, value in data.items()
        }
    elif isinstance(data, list):
        return [_process_includes(item, content_root) for item in data]
    elif isinstance(data, str):
        # Check if this string matches any loader directive
        for directive_prefix, loader in _LOADER_MAP.items():
            if data.startswith(f"{directive_prefix} "):
                file_path = data[len(directive_prefix) + 1 :].strip()
                return _load_include_file(file_path, content_root, loader)

    return data


def _load_include_file(
    file_path: str, content_root: Path, loader: DataFileLoader
) -> Any:
    """
    Load and parse a data file using the specified loader.

    Args:
        file_path: Relative path to the file
        content_root: Root directory for resolving paths
        loader: The data file loader to use

    Returns:
        Parsed file content

    Raises:
        ValueError: If file loading fails or security constraints are violated
    """
    logger = logging.getLogger(__name__)

    try:
        # Resolve the path relative to content root
        full_path = (content_root / file_path).resolve()

        # Security check: Ensure the resolved path is still within content root
        if not full_path.is_relative_to(content_root.resolve()):
            raise ValueError(f"Error: file path outside content root: {file_path}")

        if not full_path.is_file():
            raise ValueError(f"Error: data file not found: {file_path}")

        # Load and parse the file using the loader
        content = loader.load(full_path)
        logger.debug(f"Successfully loaded {loader.file_format_name} file: {file_path}")
        return content

    except Exception as e:
        raise ValueError(
            f"Error loading {loader.file_format_name} file {file_path}: {e}"
        ) from e


def load_site_context_from_path(config_path: Path) -> SiteContext:
    """Loads site configuration from a specified YAML file path and returns a SiteContext object."""
    logger = logging.getLogger(__name__)

    if not config_path.exists():
        raise FileNotFoundError(f"Site config file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {config_path}: {e}") from e
    except Exception as e:
        raise ValueError(f"Error reading file {config_path}: {e}") from e

    # Process $$include directives in the data section
    content_root = config_path.parent
    if "data" in config_data:
        logger.debug("Processing include directives in data section")
        try:
            config_data["data"] = _process_includes(config_data["data"], content_root)
        except ValueError as e:
            raise ValueError(
                f"Error processing includes in site configuration: {e}"
            ) from e

    try:
        # Use Pydantic's model_validate (v2) or parse_obj (v1) for mapping
        site_context = SiteContext.model_validate(config_data)
        site_context.__post_init__()  # Trigger validation and normalization if needed
        return site_context
    except Exception as e:
        raise ValueError(f"Invalid site configuration in {config_path}: {e}") from e
