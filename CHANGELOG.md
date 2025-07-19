# Changelog

I hope to document notable changes to this project if it turns out somebody other than me is interested in it.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-07-19

### Changed
- Moved site.yaml to project root in example site for better organization
- **BREAKING**: Moved user documentation from root-level include to proper package data structure

### Fixed  
- **MAJOR**: Fixed documentation packaging so docs are properly accessible after `pip install`
- Resolved issue with documentation files not being available in installed packages
- Added proper `importlib.resources` support for accessing package documentation
- Added fallback methods for backward compatibility with different installation methods

## [0.2.0] - 2025-07-15

First public release!
