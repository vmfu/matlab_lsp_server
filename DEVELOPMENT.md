# LSP MATLAB Server Development Guide

Guide for developing and extending LSP MATLAB Server.

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/matlab_lsp_server.git
cd matlab_lsp_server
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Pre-commit Hooks

```bash
pre-commit install
```

### 4. Verify Installation

```bash
python -c "import src.server; print('Installation successful')"
pytest --version
```

## Project Structure

```
matlab_lsp_server/
├── src/                    # Source code
├── tests/                   # Tests
├── docs/                    # Documentation (planned)
├── CHANGELOG.md             # Version history
├── README.md                # Project overview
├── ARCHITECTURE.md          # Design documentation
├── DEVELOPMENT.md           # This file
├── TODO.md                  # Development tasks
├── pyproject.toml           # Project config
├── requirements.txt           # Dependencies
└── .pre-commit-config.yaml  # Code quality hooks
```

## Development Workflow

### Feature Development

1. **Plan**
   - Review ARCHITECTURE.md
   - Check feature compatibility
   - Plan handler integration

2. **Implement**
   - Create handler in `src/handlers/`
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
   - Update README.md
   - Add to CHANGELOG.md
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
```

## Adding LSP Handlers

### 1. Create Handler File

```python
# src/handlers/my_handler.py
from lsprotocol.types import (
    MyParams,
    MyResult,
)
from pygls.server import LanguageServer

from ..handlers.base import BaseHandler
from ..utils.logging import get_logger

logger = get_logger(__name__)


class MyHandler(BaseHandler):
    """Handler for my LSP feature."""

    def handle_my_feature(
        self,
        server: LanguageServer,
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

```python
# server.py
from src.handlers.my_handler import get_my_handler

# Initialize handler
my_handler = get_my_handler()

# Register LSP method
@server.feature("myFeature")
def my_feature_handler(ls, params):
    return my_handler.handle_my_feature(ls, params)
```

### 3. Add Feature Capability

```python
# src/features/feature_manager.py
def configure_my_feature(self, enable: bool = True):
    """Configure my feature."""
    if enable:
        self._capabilities.my_feature_provider = True
        logger.debug("My feature enabled")
    else:
        self._capabilities.my_feature_provider = None
        logger.debug("My feature disabled")
```

### 4. Create Tests

```python
# tests/unit/test_my_handler.py
import pytest
from pygls.server import LanguageServer

from src.handlers.my_handler import MyHandler, get_my_handler


def test_my_handler_initialization():
    """Test MyHandler can be initialized."""
    handler = MyHandler()
    assert handler is not None


def test_get_my_handler():
    """Test getting global MyHandler instance."""
    handler1 = get_my_handler()
    handler2 = get_my_handler()
    assert handler1 is handler2
```

## Parser Development

### Adding New MATLAB Syntax

1. **Update Parser Models**

```python
# src/parser/models.py
@dataclass
class NewStructureInfo:
    """Info about new MATLAB structure."""
    name: str
    line: int
    # Add more fields as needed
```

2. **Add Regex Pattern**

```python
# src/parser/matlab_parser.py
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
# src/parser/matlab_parser.py
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

## Performance Optimization

### 1. Caching

```python
# src/utils/performance.py
from src.utils.performance import create_lru_symbol_table_cache

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
from src.utils.performance import Debouncer

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
python -m cProfile -s time src/server.py > profile.txt

# Profile specific function
python -m cProfile -s time -o profile.prof -m src.parser
```

## Debugging

### Enable Debug Logging

```bash
export LSP_LOG_LEVEL=DEBUG
python -m src.server --stdio
```

### Log Output

Logs are written to:
- Console (stdout/stderr)
- Optional: File (configure in `src/utils/logging.py`)

### Common Issues

#### Handler Not Called
- Check handler registration in `server.py`
- Verify capability is advertised
- Check LSP client supports feature

#### No Completion Suggestions
- Verify SymbolTable is populated
- Check parser is extracting symbols
- Enable DEBUG logging

#### Diagnostics Not Showing
- Check mlint integration
- Verify diagnostics publishing
- Check file path handling

#### Performance Issues
- Check cache size
- Reduce cache TTL
- Profile with cProfile

## Testing

### Unit Tests

```bash
# Run specific test
pytest tests/unit/test_parser.py::test_parse_function

# Run with output
pytest -v --tb=short

# Run with coverage
pytest --cov=src.tests/unit/test_parser.py --cov-report=html
```

### Integration Tests

```bash
# Create test file
# tests/integration/test_full_workflow.py

# Run integration tests
pytest tests/integration/
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

## Continuous Integration

### Pre-commit Hooks

Hooks run before each commit:

- **black** - Format Python code
- **isort** - Sort imports
- **flake8** - Lint Python code
- **yamllint** - Validate YAML files

### Manual Hook Run

```bash
pre-commit run --all-files
pre-commit run --files src/parser.py
```

## Release Process

### 1. Update Version

```python
# src/server.py
__version__ = "0.2.0"  # Bump version
```

### 2. Update CHANGELOG

```markdown
## [0.2.0] - YYYY-MM-DD

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
git commit -m "chore(release): bump version to 0.2.0"
git tag v0.2.0
git push origin master
git push --tags
```

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
   - Update README.md if needed
   - Add to CHANGELOG.md
   - Comment complex code

### Pull Request Process

1. Create feature branch
2. Implement feature
3. Add tests (>80% coverage)
4. Update documentation
5. Submit PR with description

## Common Commands

```bash
# Development
pytest --cov=src
black src/
isort src/
flake8 src/

# Git
git status
git add .
git commit -m "message"
git push

# Server
python -m src.server --stdio
```

## Troubleshooting

### Import Errors

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```

### Test Failures

```bash
# Run single test
pytest tests/unit/test_parser.py::test_parse_function -v

# Debug with pdb
pytest --pdb tests/unit/test_parser.py::test_parse_function
```

### Server Not Starting

```bash
# Check dependencies
pip list

# Verify Python version
python --version

# Enable debug logging
export LSP_LOG_LEVEL=DEBUG
```

## Resources

### LSP Documentation
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [VS Code Extension API](https://code.visualstudio.com/api)

### MATLAB Documentation
- [MATLAB Documentation](https://www.mathworks.com/help/)
- [MATLAB Syntax](https://www.mathworks.com/help/matlab/ref/)
- [Class Definitions](https://www.mathworks.com/help/matlab/ref/classdef.html)

### Python Tools
- [pytest](https://docs.pytest.org/)
- [black](https://black.readthedocs.io/)
- [flake8](https://flake8.pycqa.org/)
- [isort](https://pycqa.github.io/isort/)

## Support

### Getting Help

- Check ARCHITECTURE.md for design decisions
- Review existing handlers for patterns
- Enable DEBUG logging for detailed output
- Check GitHub Issues for known problems

### Reporting Bugs

1. Include error message
2. Provide reproduction steps
3. Include environment details (OS, Python version)
4. Attach logs if possible
5. Create issue in GitHub

## Best Practices

### 1. Always Add Tests
- Target >80% code coverage
- Test both success and failure cases
- Test with real .m files

### 2. Use Logging
- Log important operations
- Use appropriate log levels
- Include context in log messages

### 3. Handle Errors Gracefully
- Catch exceptions properly
- Log error details
- Return appropriate LSP responses

### 4. Optimize Performance
- Cache expensive operations
- Avoid redundant parsing
- Use async for I/O operations

### 5. Follow Style Guide
- Use black for formatting
- Follow PEP 8
- Keep functions focused and small
- Add docstrings to public functions

## Next Steps

### For New Contributors

1. Read ARCHITECTURE.md
2. Study existing handlers
3. Pick a task from TODO.md
4. Implement and test
5. Submit PR

### For Maintainers

1. Review PRs promptly
2. Ensure CI/CD passes
3. Update documentation
4. Release new versions regularly
5. Monitor performance

## License

See LICENSE file for details.
