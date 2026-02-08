# Changelog

All notable changes to MATLAB LSP Server project.
## [0.2.1] - 2026-02-09

### Bug Fixes
- Fix package structure for proper PyPI installation
- Update imports for pygls 2.0 compatibility
- Remove non-existent InitializeResultServerInfoType import
- Fix entry point to use correct module path

### Documentation
- Update INSTALL.md to match README and INTEGRATION.md
- Update all commands to use 'matlab-lsp' instead of 'python -m matlab_lsp'
- Update version to 0.2.1 in all documentation
- Update DEVELOPMENT.md with correct imports and structure
- Update CONTRIBUTING.md with correct URLs and commands
- Document auto-discovery feature

### Changed
- Update pygls imports from 'pygls.server' to 'pygls.lsp.server'
- Change server_info to use dict instead of InitializeResultServerInfoType

---


## [0.2.0] - 2026-02-08

### Features
- **Improved MATLAB Auto-Discovery**: Enhanced path handling for better MATLAB installation detection across different platforms
- **Auto-Configuration**: Server now auto-generates `.matlab-lsprc.json` configuration on first run

### Performance
- **Faster mlint Search**: mlint is now searched only in `bin/` directories, avoiding full filesystem scans
- **Optimized Path Resolution**: Improved path handling for `matlabPath` configuration option

### Bug Fixes
- **Fixed mlint.bat References**: Removed non-existent `mlint.bat` from search paths (MATLAB only provides `mlint.exe`)
- **Graceful Empty Path Handling**: Better handling when `matlabPath` is not configured or empty

### Documentation
- **Simplified README Configurations**: Streamlined editor configuration examples with minimal required settings
- **Added 7 CLI Editor Configurations**: VS Code, Neovim, Vim, Emacs, TUI Crush, OpenCode CLI, Claude Code LSP / cclsp
- **Cleaned Up Documentation**: Removed 11 unused documentation files to reduce repository clutter
- **Improved Config Documentation**: Updated docs to reflect implemented configuration options

### Cleanup
- **Removed Outdated Files**:
  - `index.html` (empty file)
  - `create_release.py` (outdated script)
  - `src/matlab_server.py` (old duplicate implementation)
  - `mlint.bat` and `mlint.sh` (manual linting scripts)
- **Removed User-Specific Configs**: `.crush.json` and `.bat` files are no longer tracked

# Changelog

All notable changes to the MATLAB LSP Server project.

## [0.1.0] - 2026-02-07

### Important Notice

**Package Rename:** The package has been renamed from `lsp-matlab-for-windows` to `matlab-lsp-server` to better reflect its cross-platform capabilities.

- **Old Package:** `lsp-matlab-for-windows`
- **New Package:** `matlab-lsp-server`

**Installation:**
```bash
# Old package name (deprecated)
pip install lsp-matlab-for-windows

# New package name (use this!)
pip install matlab-lsp-server
```

See [MIGRATION.md](MIGRATION.md) for detailed migration instructions.

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
