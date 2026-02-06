# AGENTS.md

Guide for AI agents working on the LSP MATLAB Server for Windows project.

## Project Overview

This is a **MATLAB Language Server Protocol (LSP) implementation** for Windows, built with Python and the pygls framework. The server provides intelligent code editing capabilities for MATLAB files in LSP-compatible editors like TUI Crush, VS Code, Neovim, and Emacs.

**Key Technologies:**
- Python 3.10+
- pygls (LSP framework)
- MATLAB mlint.exe (static analysis)
- lsprotocol (LSP protocol types)

**Current Status:** Early development phase. Core server skeleton exists in `server.py`; most LSP features (diagnostics, completion, hover, definition, etc.) are planned but not yet implemented.

## Essential Commands

### Installation
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (includes testing tools)
pip install -r requirements-dev.txt

# Install in editable mode for development
pip install -e .
```

### Running the Server
```bash
# Run in stdio mode (for LSP clients like TUI Crush)
python server.py --stdio

# Run in TCP mode (for debugging)
python server.py --tcp --port 4389

# Run with verbose logging
python server.py --stdio --verbose

# Show version
python server.py --version
```

### Code Quality (from requirements-dev.txt)
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# All at once (run these in sequence)
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/
```

### Testing
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_parser.py::test_parse_function

# Run with verbose output
pytest -v
```

### MATLAB Linting
```bash
# Windows - Run mlint on all .m files in current directory
mlint.bat

# Windows - Run on specific files
mlint.bat file1.m file2.m

# Linux/Mac - Run mlint
bash mlint.sh file.m
```

**Note:** mlint scripts require MATLAB installed. The path to mlint.exe is configured in `.matlab-lsprc.json` or via `MATLAB_PATH` environment variable.

## Project Structure

**Current State** (as implemented):
```
lsp_matlab_for_windows/
├── server.py                 # Main LSP server entry point
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── mlint.bat                # Windows MATLAB lint script
├── mlint.sh                 # Linux/Mac MATLAB lint script
├── .matlab-lsprc.json       # Server configuration
├── .gitignore
├── index.html               # Empty HTML file
├── start_crush.bat          # Helper script
└── for_tests/               # Manual test files
    ├── .crush.json          # TUI Crush configuration for testing
    ├── test_lsp_detailed.m
    └── test_matlab_lsp_simple.m
```

**Planned Structure** (from ARCHITECTURE.md):
```
lsp_matlab_for_windows/
├── server.py
├── requirements.txt
├── requirements-dev.txt
├── src/
│   ├── protocol/           # LSP protocol handlers (initialize, shutdown, etc.)
│   ├── handlers/           # LSP method handlers
│   │   ├── completion.py   # textDocument/completion
│   │   ├── diagnostics.py  # textDocument/diagnostic
│   │   ├── hover.py        # textDocument/hover
│   │   ├── definition.py   # textDocument/definition
│   │   ├── references.py   # textDocument/references
│   │   ├── document_symbol.py
│   │   ├── code_action.py
│   │   └── formatting.py
│   ├── parser/             # MATLAB code parser
│   │   ├── matlab_parser.py
│   │   └── models.py
│   ├── analyzer/           # Code analyzers
│   │   ├── base_analyzer.py
│   │   └── mlint_analyzer.py
│   ├── features/           # LSP feature registration
│   └── utils/              # Utilities
│       ├── cache.py
│       ├── config.py
│       ├── logging.py
│       └── path_utils.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── docs/
```

## Code Patterns and Conventions

### Python Style
- Follow **PEP 8** strictly
- Use **type hints** throughout
- Async/await for LSP protocol methods (LSP is async by nature)
- Docstrings for all public functions and classes

### Class Naming
- LSP Server: `MatLSServer` (extends `LanguageServer` from pygls)
- Handlers: `*Handler` (e.g., `CompletionHandler`, `DiagnosticsHandler`)
- Parsers: `*Parser` (e.g., `MatlabParser`)
- Analyzers: `*Analyzer` (e.g., `MlintAnalyzer`)

### LSP Method Registration Pattern
From DEVELOPMENT.md, handlers should follow this pattern:

```python
from pygls.protocol import LanguageServerProtocol
from lsprotocol.types import (
    CompletionParams,
    CompletionResult
)

class YourFeatureHandler(BaseHandler):
    def __init__(self, protocol: LanguageServerProtocol):
        super().__init__(protocol)

    @property
    def method_name(self) -> str:
        return "textDocument/yourFeature"

    def handle(self, params: YourFeatureParams) -> YourFeatureResult:
        """Handle your LSP method"""
        # Implementation
        pass
```

### Configuration Pattern
Configuration is stored in `.matlab-lsprc.json`:
```json
{
  "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
  "maxDiagnostics": 100,
  "diagnosticRules": {
    "all": true,
    "unusedVariable": true,
    "missingSemicolon": false
  },
  "formatting": {
    "indentSize": 4,
    "insertSpaces": true
  },
  "completion": {
    "enableSnippets": true,
    "maxSuggestions": 50
  },
  "cache": {
    "enabled": true,
    "maxSize": 1000
  }
}
```

The `matlabPath` can also be set via `MATLAB_PATH` environment variable.

### Import Organization
- First-party imports (from the project)
- Third-party imports (pygls, lsprotocol, etc.)
- Standard library imports

Use `isort` to maintain consistent import order.

## Testing Approach

### Test Structure
```
tests/
├── conftest.py              # pytest fixtures
├── unit/                    # Unit tests (no external dependencies)
│   ├── test_parser.py
│   ├── test_analyzer.py
│   └── test_handlers.py
├── integration/             # Integration tests (may use mlint)
│   ├── test_server.py
│   └── test_mlint_integration.py
└── fixtures/
    └── matlab_samples/      # Sample .m files for testing
```

### Writing Tests
```python
# Unit test example
import pytest
from src.parser.matlab_parser import MatlabParser

def test_parse_function():
    parser = MatlabParser()
    result = parser.parse_file("function foo() end")

    assert len(result.functions) == 1
    assert result.functions[0].name == "foo"
```

### Async Tests
Since LSP is async, many tests need to be async:
```python
import pytest
from src.protocol.lifecycle import MatLSServer

@pytest.mark.asyncio
async def test_server_initialization():
    server = MatLSServer()
    result = await server.protocol.initialize(INIT_PARAMS)
    assert result.capabilities.text_document_sync
```

## Important Gotchas

### Windows-Specific Path Handling
- Project is Windows-focused; paths use backslashes in config
- Use double backslashes in JSON strings: `"C:\\Program Files\\MATLAB\\..."`
- Python code should use `os.path` or `pathlib.Path` for cross-platform compatibility

### MATLAB Dependency
- **MATLAB R2020b or newer is required** for mlint functionality
- The `mlint.exe` path must be configured correctly
- Without MATLAB, the server will have limited/no diagnostics functionality
- Future versions may include an alternative analyzer without MATLAB dependency

### LSP Async Nature
- All LSP handlers must be async methods
- Use `@pygls.feature()` decorator or the handler registration pattern
- Server communicates via JSON-RPC over stdin/stdout in stdio mode

### TCP Mode for Debugging
- Use `--tcp` mode instead of `--stdio` for easier debugging
- Can connect with telnet or send JSON-RPC messages manually
- Default TCP port is 4389

### Configuration Priority
Configuration resolution order:
1. `.matlab-lsprc.json` in project root
2. Environment variables (`MATLAB_PATH`)
3. Default values

### File Extension Association
- MATLAB files use `.m` extension
- File type can be `"matlab"` or `"m"` in LSP client configuration
- Root patterns: `.git`, `.matlab-lsprc.json`, `project.m`

## Architecture Highlights

### LSP Server Components
The server follows a layered architecture:

1. **Protocol Layer** - Handles LSP lifecycle (initialize, shutdown, exit)
2. **Features Manager** - Registers LSP capabilities
3. **Handlers** - Implement specific LSP methods
4. **MATLAB Parser** - Extracts symbols and structure from .m files
5. **Analyzer** - Calls mlint.exe for static analysis
6. **Symbol Table** - Stores indexed symbols for code navigation
7. **Cache Manager** - Optimizes performance with caching
8. **Config Manager** - Manages server settings

### Data Flow Examples

**Diagnostic Flow:**
```
Document Change (didChange)
  → Cache Check
  → Parse File
  → Run mlint
  → Parse Output
  → Convert to LSP Diagnostics
  → Publish Diagnostics
```

**Completion Flow:**
```
Completion Request
  → Get Cursor Position
  → Parse Context
  → Query Symbol Table
  → Filter Candidates
  → Rank Results
  → Return Completion Items
```

## Development Workflow

### Adding a New LSP Feature
1. Create handler in `src/handlers/`
2. Implement handler class extending `BaseHandler`
3. Register in `src/features/feature_manager.py`
4. Add unit tests in `tests/unit/test_handlers.py`
5. Update documentation (README.md, ARCHITECTURE.md if needed)

### Commit Convention
Use Conventional Commits:
- `feat:` - new features
- `fix:` - bug fixes
- `docs:` - documentation
- `refactor:` - refactoring
- `test:` - tests
- `chore:` - maintenance

Examples:
```bash
git commit -m "feat(diagnostics): add mlint error severity mapping"
git commit -m "fix(parser): handle nested function definitions"
git commit -m "docs: update installation instructions"
```

### Before Committing
1. Run tests: `pytest`
2. Format code: `black src/ tests/`
3. Sort imports: `isort src/ tests/`
4. Lint: `flake8 src/ tests/`
5. Type check: `mypy src/`

## Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | User-facing documentation, installation, usage |
| `ARCHITECTURE.md` | System architecture, components, data flows |
| `DEVELOPMENT.md` | Developer guide, contributing, conventions |
| `DOCUMENTATION.md` | API documentation (planned) |
| `INTEGRATION.md` | Integration with LSP clients (TUI Crush, VS Code, etc.) |
| `AGENTS.md` | This file - guide for AI agents |

## Key Dependencies

### Core Dependencies (requirements.txt)
- `pygls>=0.13.0` - LSP framework
- `lsprotocol>=2023.0.0` - LSP protocol types
- `aiofiles>=23.0.0` - Async file operations
- `pydantic>=2.0.0` - Data validation
- `cachetools>=5.3.0` - Caching utilities
- `colorlog>=6.7.0` - Colored logging

### Development Dependencies (requirements-dev.txt)
- `pytest>=7.4.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `black>=23.7.0` - Code formatter
- `flake8>=6.0.0` - Linter
- `isort>=5.12.0` - Import sorter
- `mypy>=1.4.0` - Type checker
- `sphinx>=7.1.0` - Documentation generator

## Known Issues and Limitations

### Current Linting Warnings (from server.py)
- Unused imports: `typing.Optional`, `pygls.protocol.LanguageServerProtocol`
- Long lines (E501): Lines 119, 123 exceed 79 characters

These should be cleaned up during implementation of actual LSP features.

### Roadmap Status
Based on README.md roadmap:

**Phase 1: Core (Current)**
- [x] Architecture and documentation
- [ ] Basic LSP server
- [ ] mlint integration
- [ ] Error diagnostics

**Phase 2-4: Planned**
- Completion, hover, definition, references
- Document symbols, code actions, formatting
- Workspace symbols, performance, testing

## External Resources

### Key Documentation
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [lsprotocol Types](https://lsprotocol.readthedocs.io/)
- [MATLAB Documentation](https://www.mathworks.com/help/matlab/)

### MCP Tools Used in Development
The project actively uses these MCP servers for development:
- **z_ai MCP** - Code generation and analysis
- **context7 MCP** - Library documentation (pygls, lsprotocol)
- **z_ai_tools MCP** - Image and diagram analysis
- **DuckDuckGo MCP** - Web search
- **Filesystem MCP** - File system operations

Example usage:
```bash
# Get pygls documentation
context7: /openlawlibrary/pygls
query: "How to create LSP handler for completion?"

# Search for existing implementations
agent: "Find MATLAB LSP server implementations on GitHub"
```

## Testing the Integration

### TUI Crush Integration
To test with TUI Crush, configure in `.crush.json`:
```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": [
        "C:/path/to/lsp_matlab_for_windows/server.py",
        "--stdio"
      ],
      "filetypes": ["matlab", "m"],
      "workspace": ["C:/path/to/matlab/project"]
    }
  }
}
```

See `INTEGRATION.md` for detailed integration instructions and troubleshooting.

### Manual Testing Files
The `for_tests/` directory contains MATLAB files for manual testing:
- `test_lsp_detailed.m` - Syntax error examples
- `test_matlab_lsp_simple.m` - Simple test cases

Use these to verify diagnostics, completion, and other features as they're implemented.
