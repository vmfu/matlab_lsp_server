# LSP MATLAB Server Development Guide

Guide for developing and extending MATLAB LSP Server.

---

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Running Tests](#running-tests)
- [Adding LSP Handlers](#adding-lsp-handlers)
- [Parser Development](#parser-development)
- [Performance Optimization](#performance-optimization)
- [Debugging](#debugging)
- [Testing](#testing)
- [Release Process](#release-process)
- [Contributing Guidelines](#contributing-guidelines)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)

---

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/vmfu/matlab_lsp_server.git
cd matlab_lsp_server
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Or install in editable mode
pip install -e .
```

### 3. Install Pre-commit Hooks

```bash
pre-commit install
```

### 4. Verify Installation

```bash
# Check version
matlab-lsp --version

# Run tests
pytest --version
```

---

## Project Structure

```
matlab_lsp_server/
├── src/                         # Source code
│   └── matlab_lsp_server/       # Main package
│       ├── __init__.py
│       ├── server.py              # Entry point (CLI)
│       ├── matlab_server.py       # LSP server class
│       ├── analyzer/              # Code analyzers
│       │   ├── __init__.py
│       │   ├── base_analyzer.py
│       │   └── mlint_analyzer.py
│       ├── features/              # LSP features
│       │   ├── __init__.py
│       │   └── feature_manager.py
│       ├── handlers/              # LSP method handlers
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── completion.py
│       │   ├── diagnostics.py
│       │   ├── hover.py
│       │   ├── definition.py
│       │   ├── references.py
│       │   ├── document_symbol.py
│       │   ├── code_action.py
│       │   ├── formatting.py
│       │   └── workspace_symbol.py
│       ├── parser/                # MATLAB parser
│       │   ├── __init__.py
│       │   ├── matlab_parser.py
│       │   └── models.py
│       ├── protocol/              # LSP protocol handlers
│       │   ├── __init__.py
│       │   ├── lifecycle.py
│       │   └── document_sync.py
│       └── utils/                # Utilities
│           ├── __init__.py
│           ├── cache.py
│           ├── config.py
│           ├── document_store.py
│           ├── logging.py
│           ├── performance.py
│           └── symbol_table.py
├── tests/                       # Tests
│   ├── unit/                    # Unit tests
│   ├── integration/              # Integration tests
│   └── fixtures/                # Test data
├── docs/                        # Documentation (planned)
├── CHANGELOG.md                 # Version history
├── README.md                    # Project overview
├── INSTALL.md                   # Installation guide
├── INTEGRATION.md              # Editor integration guide
├── ARCHITECTURE.md             # Design documentation
├── DEVELOPMENT.md               # This file
├── AGENTS.md                   # AI agent guide
├── TODO.md                     # Development tasks
├── pyproject.toml               # Project config
├── requirements.txt             # Dependencies
├── requirements-dev.txt         # Dev dependencies
├── .pre-commit-config.yaml      # Code quality hooks
└── for_tests/                  # Manual test files
```

---

## Development Workflow

### Feature Development

1. **Plan**
   - Review [ARCHITECTURE.md](ARCHITECTURE.md)
   - Check feature compatibility
   - Plan handler integration

2. **Implement**
   - Create handler in `src/matlab_lsp_server/handlers/`
   - Implement LSP methods
   - Add logging

3. **Test**
   - Create test file in `tests/unit/`
   - Write unit tests
   - Ensure >80% coverage

4. **Register**
   - Add to `FeatureManager`
   - Update capabilities
   - Test with real LSP client

5. **Document**
   - Update [README.md](README.md)
   - Add to [CHANGELOG.md](CHANGELOG.md)
   - Commit changes

### Code Style

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Run before commit
pre-commit run --all-files

# Type check
mypy src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_parser.py

# Run verbose
pytest -v --tb=short

# Run integration tests
pytest tests/integration/

# Run specific test
pytest tests/unit/test_parser.py::test_parse_function
```

---

## Adding LSP Handlers

### 1. Create Handler File

```python
# src/matlab_lsp_server/handlers/my_handler.py
from typing import Any

from lsprotocol.types import (
    MyParams,
    MyResult,
)
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.handlers.base import BaseHandler
from matlab_lsp_server.utils.logging import get_logger

logger = get_logger(__name__)


class MyHandler(BaseHandler):
    """Handler for my LSP feature."""

    @property
    def method_name(self) -> str:
        """Get the LSP method name this handler implements."""
        return "textDocument/myFeature"

    def handle(
        self,
        params: MyParams,
    ) -> MyResult:
        """Handle my LSP feature."""
        logger.debug("Handling my feature")

        # Implement logic here
        result = MyResult(...)

        return result


# Global instance
_my_handler = None

def get_my_handler() -> MyHandler:
    """Get global MyHandler instance."""
    global _my_handler
    if _my_handler is None:
        _my_handler = MyHandler()
        logger.debug("MyHandler instance created")
    return _my_handler
```

### 2. Register Handler

The `FeatureManager` automatically registers all handlers from the `handlers/` package. No manual registration is required in `server.py`.

However, if you need to manually control handler registration:

```python
# src/matlab_lsp_server/features/feature_manager.py
from matlab_lsp_server.handlers.my_handler import get_my_handler

# Initialize handler
my_handler = get_my_handler()

# FeatureManager will automatically discover and register
```

### 3. Add Feature Capability

```python
# LSP capabilities are automatically configured based on registered handlers

# To add server capabilities:
# Update ServerInfo in initialize method
```

### 4. Create Tests

```python
# tests/unit/test_my_handler.py
import pytest
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.handlers.my_handler import MyHandler, get_my_handler


def test_my_handler_initialization():
    """Test MyHandler can be initialized."""
    handler = MyHandler()
    assert handler is not None


def test_get_my_handler():
    """Test getting global MyHandler instance."""
    handler1 = get_my_handler()
    handler2 = get_my_handler()
    assert handler1 is handler2


def test_my_handler_method_name():
    """Test handler returns correct method name."""
    handler = MyHandler()
    assert handler.method_name == "textDocument/myFeature"
```

---

## Parser Development

### Adding New MATLAB Syntax

1. **Update Parser Models**

```python
# src/matlab_lsp_server/parser/models.py
from dataclasses import dataclass

@dataclass
class NewStructureInfo:
    """Info about new MATLAB structure."""
    name: str
    line: int
    # Add more fields as needed
```

2. **Add Regex Pattern**

```python
# src/matlab_lsp_server/parser/matlab_parser.py
import re
from typing import List

from matlab_lsp_server.parser.models import NewStructureInfo

def _parse_new_structure(self, lines: List[str]) -> List[NewStructureInfo]:
    """Parse new MATLAB structure."""
    structures = []

    for i, line in enumerate(lines):
        # Add regex pattern here
        match = re.match(r'your_pattern_here', line)

        if match:
            structure = NewStructureInfo(
                name=match.group(1),
                line=i + 1,
            )
            structures.append(structure)

    return structures
```

3. **Update Parse Method**

```python
# src/matlab_lsp_server/parser/matlab_parser.py
def parse_file(self, file_path: str) -> ParseResult:
    """Parse MATLAB file."""
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse existing structures
    functions = self._parse_functions(lines)
    # Add new structure parsing
    new_structures = self._parse_new_structure(lines)

    return ParseResult(
        file_path=file_path,
        functions=functions,
        new_structures=new_structures,
        # Add more fields
    )
```

---

## Performance Optimization

### 1. Caching

```python
# src/matlab_lsp_server/utils/performance.py
from matlab_lsp_server.utils.cache import create_lru_symbol_table_cache

# Create cache
symbol_cache = create_lru_symbol_table_cache(capacity=128)

# Use cache
result = symbol_cache.get(cache_key)
if result is None:
    result = expensive_operation()
    symbol_cache.put(cache_key, result)
```

### 2. Debouncing

```python
# src/matlab_lsp_server/utils/performance.py
from matlab_lsp_server.utils.performance import Debouncer

debouncer = Debouncer(delay=0.5)

@debouncer.debounce
def on_file_change():
    """Handle file change."""
    # Expensive operation
    parse_file(file_path)

# Call debounced
on_file_change()  # Will delay calls
```

### 3. Profiling

```bash
# Profile server
python -m cProfile -s time -m matlab_lsp_server.server > profile.txt

# Profile specific function
python -m cProfile -s time -o profile.prof -m matlab_lsp_server.parser
```

---

## Debugging

### Enable Debug Logging

```bash
# Run with verbose flag
matlab-lsp --stdio --verbose

# Or when running as module
python -m matlab_lsp_server.server --stdio --verbose
```

### Log Output

Logs are written to:
- Console (stdout/stderr)
- Colored output using colorlog

### Common Issues

#### Handler Not Called
- Check handler is in `src/matlab_lsp_server/handlers/`
- Verify FeatureManager discovers the handler
- Check LSP client supports feature
- Enable `--verbose` logging for details

#### No Completion Suggestions
- Verify SymbolTable is populated
- Check parser is extracting symbols
- Enable `--verbose` logging
- Check document is indexed

#### Diagnostics Not Showing
- Check mlint integration
- Verify diagnostics publishing
- Check file path handling
- Ensure MATLAB path is configured (if needed)

#### Performance Issues
- Check cache size
- Reduce cache TTL
- Profile with cProfile
- Check for redundant parsing

---

## Testing

### Unit Tests

```bash
# Run specific test
pytest tests/unit/test_parser.py::test_parse_function

# Run with output
pytest -v --tb=short

# Run with coverage
pytest --cov=src.matlab_lsp_server --cov-report=html

# Run specific test file
pytest tests/unit/test_parser.py
```

### Integration Tests

```bash
# Run integration tests
pytest tests/integration/

# Create integration test
# tests/integration/test_full_workflow.py
```

### Test Fixtures

Create test MATLAB files in `tests/fixtures/matlab_samples/`:

```matlab
% test_fixtures/simple_function.m
function result = simpleFunction(x)
    y = x * 2;
    result = y + 1;
end
```

### Testing LSP Integration

To test with a real LSP client:

1. Install server: `pip install -e .`
2. Configure your editor (see [INTEGRATION.md](INTEGRATION.md))
3. Open a test `.m` file
4. Trigger LSP features (completion, hover, go-to-definition)
5. Check logs with `--verbose`

---

## Continuous Integration

### Pre-commit Hooks

Hooks run before each commit:

- **black** - Format Python code
- **isort** - Sort imports
- **flake8** - Lint Python code
- **mypy** - Type check code

### Manual Hook Run

```bash
# Run all hooks
pre-commit run --all-files

# Run on specific files
pre-commit run --files src/matlab_lsp_server/parser.py
```

### CI/CD

GitHub Actions is configured for:
- Running tests on multiple Python versions
- Building package
- Publishing to PyPI on release

---

## Release Process

### 1. Update Version

Update version in all files:

```python
# pyproject.toml
[project]
version = "0.2.1"

# src/matlab_lsp_server/__init__.py
__version__ = "0.2.1"

# src/matlab_lsp_server/server.py
__version__ = "0.2.1"

# src/matlab_lsp_server/matlab_server.py
# Update server_info version

# src/matlab_lsp_server/protocol/lifecycle.py
# Update server_info version
```

### 2. Update CHANGELOG

```markdown
## [0.2.1] - 2025-02-09

### Added
- New feature description

### Changed
- Modified feature description

### Fixed
- Bug fix description
```

### 3. Tag and Push

```bash
git add -A
git commit -m "chore(release): bump version to 0.2.1"
git tag v0.2.1
git push origin master
git push --tags
```

### 4. Create GitHub Release

1. Go to https://github.com/vmfu/matlab_lsp_server/releases/new
2. Select tag `v0.2.1`
3. Set title `v0.2.1`
4. Write release notes
5. Click "Publish release"

GitHub Actions will automatically publish to PyPI.

---

## Contributing Guidelines

### Code Review

1. **Self-review**
   - Run `pre-commit run --all-files`
   - Run `pytest --cov=src`
   - Check code style

2. **Test with Real Files**
   - Test with actual .m files
   - Verify LSP client compatibility
   - Check performance

3. **Documentation**
   - Update [README.md](README.md) if needed
   - Add to [CHANGELOG.md](CHANGELOG.md)
   - Comment complex code

### Pull Request Process

1. Create feature branch
2. Implement feature
3. Add tests (>80% coverage)
4. Update documentation
5. Submit PR with description

---

## Common Commands

```bash
# Development
pytest --cov=src
black src/
isort src/
flake8 src/
mypy src/

# Git
git status
git add .
git commit -m "message"
git push

# Server
matlab-lsp --stdio

# Or as module
python -m matlab_lsp_server.server --stdio

# With verbose
matlab-lsp --stdio --verbose

# TCP mode (debugging)
matlab-lsp --tcp --port 4389
```

---

## Troubleshooting

### Import Errors

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .

# Check if using pygls 2.0
python -c "from pygls.lsp.server import LanguageServer; print('pygls 2.0 OK')"
```

### Test Failures

```bash
# Run single test
pytest tests/unit/test_parser.py::test_parse_function -v

# Debug with pdb
pytest --pdb tests/unit/test_parser.py::test_parse_function

# Run last failed test
pytest --lf
```

### Server Not Starting

```bash
# Check dependencies
pip list

# Verify Python version
python --version  # Must be 3.10+

# Check for pygls 2.0
python -c "import pygls; print(dir(pygls))"

# Enable debug logging
matlab-lsp --stdio --verbose
```

### Package Build Issues

```bash
# Clean build artifacts
rm -rf build/ dist/ src/*.egg-info/

# Rebuild
python -m build

# Check pyproject.toml
cat pyproject.toml
```

---

## Resources

### LSP Documentation
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [lsprotocol Documentation](https://lsprotocol.readthedocs.io/)

### Internal Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Design decisions and structure
- [AGENTS.md](AGENTS.md) - AI agent development guide
- [README.md](README.md) - Project overview and features
- [INSTALL.md](INSTALL.md) - Installation instructions
- [INTEGRATION.md](INTEGRATION.md) - Editor configuration guides

### MATLAB Documentation
- [MATLAB Documentation](https://www.mathworks.com/help/)
- [MATLAB Syntax](https://www.mathworks.com/help/matlab/ref/)
- [Class Definitions](https://www.mathworks.com/help/matlab/ref/classdef.html)

### Python Tools
- [pytest](https://docs.pytest.org/)
- [black](https://black.readthedocs.io/)
- [flake8](https://flake8.pycqa.org/)
- [isort](https://pycqa.github.io/isort/)
- [mypy](https://mypy.readthedocs.io/)

---

## Support

### Getting Help

- Check [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions
- Review existing handlers for patterns
- Enable `--verbose` logging for detailed output
- Check GitHub Issues for known problems
- Read [AGENTS.md](AGENTS.md) for MCP tool usage

### Reporting Bugs

1. Include error message
2. Provide reproduction steps
3. Include environment details (OS, Python version)
4. Attach logs if possible (with `--verbose`)
5. Create issue in [GitHub](https://github.com/vmfu/matlab_lsp_server/issues/new)

---

## Best Practices

### 1. Always Add Tests
- Target >80% code coverage
- Test both success and failure cases
- Test with real .m files
- Use fixtures for test data

### 2. Use Logging
- Log important operations
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Include context in log messages
- Use colorlog for colored output

### 3. Handle Errors Gracefully
- Catch exceptions properly
- Log error details
- Return appropriate LSP error responses
- Never crash the server

### 4. Optimize Performance
- Cache expensive operations
- Avoid redundant parsing
- Use async for I/O operations
- Profile with cProfile when needed

### 5. Follow Style Guide
- Use black for formatting
- Follow PEP 8
- Use type hints
- Keep functions focused and small
- Add docstrings to public functions

### 6. Use Correct Imports

**For pygls 2.0:**
```python
# Correct
from pygls.lsp.server import LanguageServer
from lsprotocol.types import InitializeParams

# Incorrect (pygls 1.x)
from pygls.server import LanguageServer
```

**For package imports:**
```python
# Correct
from matlab_lsp_server.handlers.base import BaseHandler
from matlab_lsp_server.utils.logging import get_logger

# Incorrect (old structure)
from src.handlers.base import BaseHandler
from ..utils.logging import get_logger
```

---

## Next Steps

### For New Contributors

1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Study existing handlers in `src/matlab_lsp_server/handlers/`
3. Pick a task from TODO.md
4. Implement and test
5. Submit PR with description

### For Maintainers

1. Review PRs promptly
2. Ensure CI/CD passes
3. Update documentation
4. Release new versions regularly
5. Monitor performance metrics
6. Respond to issues and discussions

---

## License

See LICENSE file for details.
