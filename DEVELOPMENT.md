# Development Guide

This guide covers development tasks and workflows for straightshot contributors.

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/nicoheidtke/straightshot.git
   cd straightshot
   ```

2. Install dependencies:
   ```sh
   poetry install
   ```

## Development Tasks

straightshot uses [Poe the Task Runner](https://poethepoet.natn.io/) for common development tasks. All tasks are defined in `pyproject.toml`.

### Available Tasks

```bash
# List available poe options and available tasks
poetry poe

# Code formatting
poetry poe format

# Code quality checks
poetry poe lint          # Run linting checks
poetry poe type_check    # Run type checking 
poetry poe test          # Run tests
poetry poe check         # Run all checks (lint, type-check, test)

# Build and packaging
poetry poe package       # Build the package
poetry poe all          # Format, check, and package

# Example site
poetry poe example_build # Build the example site
poetry poe example_serve # Serve the example site locally
poetry poe example       # Build and serve the example site
```

### VS Code Integration

These tasks can also be run directly from VS Code using the configured tasks (which invoke Poe behind the scenes). Use `Ctrl+Shift+P` and search for "Run Task" to access them.

## Project Structure

- `straightshot/` - Main package source code
- `example-site/` - Example site for testing and demonstration
- `docs/` - Documentation files
- `tests/` - Test suite (currently minimal)

## Code Quality

The project uses:
- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Pytest** for testing

All code should pass the quality checks before committing:
```sh
poetry poe check
```

## Testing the Example Site

The example site serves as both documentation and a test of the generator:

```sh
# Build and serve locally
poetry poe example

# Or run steps separately
poetry poe example_build
poetry poe example_serve
```

This will build the example site and serve it at `http://localhost:8080/`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information about the current project status and contribution guidelines.
