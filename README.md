# LSP MATLAB Server

Language Server Protocol (LSP) implementation for MATLAB code editing support in modern IDEs (VS Code, JetBrains, etc.).

## Overview

LSP MATLAB Server provides intelligent code editing features for MATLAB files (.m, .mlx):

- **Syntax highlighting** - Code structure analysis
- **Code completion** - Intelligent suggestions based on project symbols
- **Go-to-definition** - Navigate to function/variable definitions
- **Find-references** - Locate all usages of a symbol
- **Hover documentation** - Display symbol information on mouse hover
- **Document symbols** - Outline view of file structure
- **Quick fixes** - Automatic suggestions for common errors
- **Code formatting** - Automatic MATLAB code formatting
- **Workspace search** - Search symbols across entire project

## Features

### Essential Features (Phase 2)

#### Matlab Parser
Regex-based MATLAB code parser supporting:
- Function definitions (`function ... end`)
- Variable declarations (`global`, `persistent`)
- Comments (single-line `%` and block `%{ ... }%`)
- Class definitions (`classdef ... end`)
- Nested functions and methods
- Class properties

#### Symbol Table
In-memory code symbol indexing:
- Storage for functions, variables, classes, properties
- Search by name and URI
- Automatic update on file parsing
- Statistics tracking

#### Cache Manager
Performance optimization with result caching:
- In-memory cache with TTL (5 minutes default)
- Parsing result caching
- Mlint analysis caching
- File change invalidation

#### Code Completion
Intelligent code suggestions:
- Project symbols from SymbolTable
- Built-in MATLAB functions (sin, cos, sqrt, abs, zeros, ones, eye, size, length, disp, fprintf, input, keyboard, error, warning)
- MATLAB keywords (if, else, elseif, for, while, end, function, return, break, continue)
- Relevance ranking (exact > prefix > partial)
- Limited to 20 results

#### Hover Provider
Documentation display on cursor hover:
- Symbol search by position
- Symbol information display
- Markdown documentation
- Symbol kind emojis

#### Document Symbols
Hierarchical document structure:
- Classes > methods > functions hierarchy
- Nested function support
- LSP DocumentSymbol format

### Advanced Features (Phase 3)

#### Go-to-Definition
Navigate to symbol definitions:
- Symbol search by position
- Cross-file definition search
- LSP Location format

#### Find-All-References
Locate symbol usages:
- All references search
- includeDeclaration parameter
- Cross-file reference search

#### Code Actions
Quick fixes for errors:
- Undefined function suggestions
- Missing semicolon fixes
- Unused variable warnings
- End statement suggestions

#### Workspace Symbols
Project-wide symbol search:
- Fuzzy matching by query
- Symbol kind filtering
- Optimized search

### Polish Features (Phase 4)

#### Code Formatting
Automatic MATLAB code formatting:
- Configurable indentation
- End keyword alignment
- Operator and space formatting

#### Performance Optimizations
- LRU cache for symbol table
- Debouncing for operations
- Time measurement decorator
- Performance utilities

## Installation

### Requirements

- Python 3.10+
- pygls
- lsprotocol
- pytest (for development)
- pytest-cov (for development)

### Install from Source

```bash
git clone https://github.com/yourusername/lsp_matlab_for_windows.git
cd lsp_matlab_for_windows
pip install -e .
```

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest --cov=src
```

## Usage

### Starting the Server

```bash
python -m src.server --stdio
```

### VS Code Integration

Create `.vscode/settings.json`:

```json
{
  "matlab.lsp.path": "path/to/python",
  "matlab.lsp.args": ["-m", "src.server", "--stdio"]
}
```

### JetBrains Integration

Configure in Settings > Languages & Frameworks > MATLAB:

- **Language Server**: Custom
- **Server path**: `path/to/python`
- **Arguments**: `-m src.server --stdio`

## Project Structure

```
lsp_matlab_for_windows/
├── src/
│   ├── __init__.py
│   ├── server.py                 # Main LSP server
│   ├── parser/                   # MATLAB parser
│   │   ├── __init__.py
│   │   ├── matlab_parser.py
│   │   └── models.py
│   ├── handlers/                 # LSP handlers
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── completion.py
│   │   ├── hover.py
│   │   ├── definition.py
│   │   ├── references.py
│   │   ├── code_action.py
│   │   ├── document_symbol.py
│   │   ├── workspace_symbol.py
│   │   ├── formatting.py
│   │   └── diagnostics.py
│   ├── analyzer/                 # Code analyzers
│   │   ├── __init__.py
│   │   ├── base_analyzer.py
│   │   └── mlint_analyzer.py
│   ├── protocol/                 # LSP protocol
│   │   ├── __init__.py
│   │   ├── document_sync.py
│   │   └── lifecycle.py
│   ├── utils/                    # Utilities
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── symbol_table.py
│   │   ├── logging.py
│   │   ├── config.py
│   │   ├── performance.py
│   │   └── document_store.py
│   └── features/                 # Feature management
│       ├── __init__.py
│       └── feature_manager.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_parser.py
│   │   ├── test_cache.py
│   │   ├── test_symbol_table.py
│   │   ├── test_completion.py
│   │   ├── test_hover.py
│   │   ├── test_definition.py
│   │   ├── test_references.py
│   │   ├── test_code_action.py
│   │   ├── test_document_symbol.py
│   │   ├── test_workspace_symbol.py
│   │   ├── test_formatting.py
│   │   └── test_performance.py
│   ├── fixtures/
│   │   └── matlab_samples/
│   └── integration/
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── .pre-commit-config.yaml
└── README.md
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_parser.py
```

### Pre-commit Hooks

Project uses pre-commit hooks for code quality:

- **flake8** - Python linting
- **isort** - Import sorting
- **black** - Code formatting
- **yamllint** - YAML validation

Install hooks:
```bash
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

## LSP Capabilities

### Implemented Features

- ✅ `textDocument/completion` - Code completion
- ✅ `textDocument/hover` - Hover information
- ✅ `textDocument/documentSymbol` - Document outline
- ✅ `textDocument/definition` - Go-to-definition
- ✅ `textDocument/references` - Find-references
- ✅ `textDocument/codeAction` - Quick fixes
- ✅ `workspace/symbol` - Workspace search
- ✅ `textDocument/formatting` - Code formatting
- ✅ `textDocument/sync` - Document synchronization

### Synchronization

- ✅ `textDocument/didOpen` - File opened
- ✅ `textDocument/didClose` - File closed
- ✅ `textDocument/didChange` - Content changed
- ✅ `workspace/didChangeWorkspaceFolders` - Project changes

## Configuration

### Server Options

- `indent_size` - Indentation size (default: 4)
- `max_line_length` - Maximum line length (default: 80)
- `cache_ttl` - Cache time-to-live in seconds (default: 300)

### Logging

Configure logging level via environment variable:

```bash
export LSP_LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
python -m src.server --stdio
```

## Troubleshooting

### Common Issues

#### Completion not working
- Check SymbolTable is populated
- Verify parser is extracting symbols correctly
- Check logging for errors

#### Diagnostics not showing
- Ensure mlint integration is configured
- Check file path handling
- Verify diagnostics publishing

#### Performance issues
- Enable LRU caching
- Reduce cache TTL
- Check for memory leaks
- Profile with `python -m cProfile`

## Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines.

## License

MIT License - See LICENSE file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
