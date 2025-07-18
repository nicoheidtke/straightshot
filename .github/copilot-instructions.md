## Project Overview
straightshot is a Python-based static site generator with dynamic article loading capabilities. It transforms Markdown content with YAML frontmatter into a responsive, SEO-friendly website.

## Development Guidelines

### Project Documentation & Configuration
- Always consider `README.md`, `.gitignore`, `pyproject.toml` and `.vscode/tasks.json` when working on dev/build code and always update them as needed
- Always consider `docs/dev/architecture.md` and `docs/user/_overview.md` when working on site generation features
- Maintain the `CHANGELOG.md` file to document notable changes which are visible for users
- Use LF line-endings for all files (see `.editorconfig`)

### Development Process
- Ask questions to get clarifications - especially if something is questionable from design or engineering perspective before implementing
- Discuss and provide options before altering architecture, dependencies or features
- After making changes, check for problems using a fitting build tasks from `pyproject.toml` or `.vscode/tasks.json`

### Maintenance 
When asked to perform a `maintenance routine`, run these steps:
- Update dependencies in `pyproject.toml` to latest versions using `poetry update`
- Scan for dead code and remove it
- Check for code quality issues using `ruff` and `mypy`
- Run all tests and ensure they pass
- Ensure the build process works as expected and the `pyproject.toml` build tasks are up-to-date and aligned with `.vscode/tasks.json`
- Ensure the example site builds and runs correctly
- Update the `CHANGELOG.md` with a new version entry based on the recent git history and the changes made.
- Ensure all internal and external documentation is up-to-date with the latest changes. 
- All links to internal and external documentation are valid.

### Release Preparation
When asked to perform a `release preparation`, follow these steps:
- Update the version in `pyproject.toml` to the next version (e.g. `0.1.0` to `0.2.0`). Ask for the next version number if not specified.
- Update the `CHANGELOG.md` with a new version entry, including a summary of changes
- Commit the changes with a message like `Bump version to 0.2.0`
- Tag the commit with `git tag -a v0.2.0 -m "Release version 0.2.0"`
- Do not pull or push anything. This is done manually.

### Code Quality & Refactoring Principles
- Minimize redundancy and maximize code reuse
- Prefer less code over more code - eliminate dead code and unnecessary complexity
- Look for opportunities to simplify code through conceptual/architectural improvements
- Maintain consistency and order throughout the codebase
- Keep files and functions reasonably sized and focused
- Actively refactor when code becomes too long or complex

## Programming Rules

### Code Organization & Architecture
- Look for code and configuration that can be reused or refactored to be made reusable, but maintain architectural boundaries
- Recognize three kinds of code:
  - **State manipulation:** Load and save state, various kinds of I/O, model data
  - **Algorithms:** Pure functions that transform input into output
  - **Orchestration/Logic:** Higher level logic, expression of system architecture, orchestrating state and algorithm relations

### Code Structure & Dependencies
- Use classes only for self-contained state and resources (data models, files etc)
- Use dependency injection in orchestration over hidden dependencies
- Algorithms should be pure functions (as much as possible in Python)
- Avoid large parameter lists (> 4) - group related parameters into data classes/models
- Avoid dict types when a data class can be used for better readability, type-safety, error messages and auto-completion
- Avoid creating large functions (more than ~10 loops or conditions)
- Do not nest functions unless they are small

### Naming Conventions
- **State manipulation:** Use verbs like `load_`, `save_`, `fetch_`, `read_`, `write_`, `update_`, `delete_`
  - Examples: `load_config`, `save_content_file`
- **Algorithms (pure functions):** Use verbs like `compute_`, `transform_`, `validate_`, `parse_`, `generate_`, `filter_`, `sort_`
  - Examples: `validate_content`, `generate_slug`
- **Orchestration/Logic:** Use verbs like `build_`, `perform_`, `run_`, `process_`, `orchestrate_`, `execute_`
  - Examples: `build_site`, `perform_deployment`

### Architecture Guidelines
- Site generation should be configuration driven to accommodate multiple users with varying site styles and complexity

## Web Design Principles

- Mobile-first responsive design
- Support both JavaScript and non-JavaScript environments when reasonable
- Preserve responsive design and dark/light mode functionality
- Minimal client-side code
- SEO optimization by default

## Documentation & Help
- Remember to update documentation when making changes to features or architecture.
- Do not use boastful language in documentation. Do not exagerate to make this project seem better or more mature than it is.
