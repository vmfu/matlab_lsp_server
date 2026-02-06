# Changelog

All notable changes to the LSP MATLAB Server project.

## [0.1.0] - 2026-02-07

### Added

#### Phase 1: Project Setup
- Project structure with Python packaging
- Dependencies: pygls, lsprotocol, pytest, pytest-cov
- Base configuration (pyproject.toml)
- Project documentation (README.md, TODO.md)

#### Phase 2: Essential Features
- **MatlabParser** - regex-based parser for MATLAB syntax
  - Function parsing (function/end)
  - Variable parsing (global/persistent)
  - Comment parsing (single-line and block)
  - Class parsing (classdef)
  - Nested function support
  - Class method support

- **SymbolTable** - code symbol indexing
  - Symbol storage (functions, variables, classes, properties)
  - Search by name and URI
  - Statistics tracking
  - Automatic update on parsing

- **CacheManager** - result caching
  - In-memory cache with TTL (5 minutes default)
  - Parsing result caching
  - Mlint analysis caching
  - File change invalidation
  - Statistics and logging

- **CompletionHandler** - code completion
  - Candidates from SymbolTable
  - Built-in MATLAB functions (sin, cos, sqrt, abs, zeros, ones, eye, size, length, disp, fprintf, input, keyboard, error, warning)
  - MATLAB keywords (if, else, elseif, for, while, end, function, return, break, continue)
  - Relevance ranking (exact > prefix > partial)
  - Limit to 20 results

- **HoverHandler** - documentation on hover
  - Symbol search by position
  - Symbol information display
  - Markdown documentation
  - Symbol kind emojis

- **DocumentSymbolHandler** - document structure
  - Hierarchical structure (classes > methods > functions)
  - LSP DocumentSymbol format
  - Nested function support

#### Phase 3: Advanced Features
- **DefinitionHandler** - go-to-definition
  - Symbol search by position
  - Cross-file definition search
  - LSP Location format

- **ReferencesHandler** - find-all-references
  - All references search
  - includeDeclaration parameter
  - Cross-file reference search

- **CodeActionHandler** - quick fixes
  - Quick fix generation for diagnostics
  - Support for undefined functions, missing semicolons, unused variables, end statements

- **WorkspaceSymbolHandler** - workspace-wide search
  - Fuzzy matching by query
  - Symbol kind filtering (Function, Variable, Class, etc.)
  - Optimized search

#### Phase 4: Polish
- **FormattingHandler** - code formatting
  - Automatic MATLAB code formatting
  - Indent support (config.indentSize)
  - End keyword alignment
  - Configurable style

- **Performance Optimizations**
  - LRU cache for SymbolTable
  - Debouncing for operations
  - Time measurement decorator
  - Performance utils module

- **Pre-commit Hooks**
  - flake8 for linting
  - isort for import sorting
  - black for formatting
  - yamllint for YAML files
  - Large file check
  - Merge conflict check

### Changed

- Updated project structure for LSP server
- Added comprehensive test suite (128+ tests)
- Implemented code coverage (~73%)

### Fixed

- Fixed parsing errors for nested functions
- Fixed symbol table indexing issues
- Fixed handler initialization problems
- Fixed test failures for edge cases

### Testing

- Unit tests: 128+ passed
- Integration tests: planned
- Code coverage: ~73%
- All handlers tested independently
