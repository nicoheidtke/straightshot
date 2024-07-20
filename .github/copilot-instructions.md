## Project Overview
straightshot is a Python-based static site generator with dynamic article loading capabilities. It transforms Markdown content with YAML frontmatter into a responsive, SEO-friendly website.

## Development Guidelines

### Project Documentation & Configuration
- Always consider `README.md`, `.gitignore`, `pyproject.toml` and `.vscode/tasks.json` when working on dev/build code and always update them as needed
- Always consider `docs/architecture.md` and `docs/features.md` when working on site generation features
- Maintain the `CHANGELOG.md` file to document notable changes which are visible for users
- Use LF line-endings for all files (see `.editorconfig`)

### Development Process
- Ask questions to get clarifications - especially if something is questionable from design or engineering perspective before implementing
- Discuss and provide options before altering architecture, dependencies or features
- After making changes, check for problems using: `poetry poe all`

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
