# Contributing to LSP MATLAB Server

Thank you for your interest in contributing! This guide will help you get started.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Workflow](#workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Code of Conduct

Be respectful, inclusive, and constructive. We welcome contributions from everyone.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of LSP protocol
- Knowledge of MATLAB syntax (helpful but not required)

### First Contribution

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/matlab_lsp_server.git
cd matlab_lsp_server
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install in editable mode
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt
```

### 4. Verify Setup

```bash
# Run tests
pytest

# Check version
python server.py --version
```

---

## Workflow

### Branch Naming

Use descriptive branch names:

- `feat/completion-snippets` - New feature
- `fix/diagnostics-async` - Bug fix
- `docs/installation-guide` - Documentation
- `refactor/parser-optimization` - Code refactoring
- `test/hover-coverage` - Test additions

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting (no code change)
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance

**Examples:**

```
feat(completion): add code snippet support

Implement code snippets for function completions
including parameter placeholders.

Closes #123
```

```
fix(parser): handle nested function parsing correctly

Previously, nested functions were parsed as top-level.
Now they're correctly identified.

Fixes #45
```

### Pull Request Process

1. Update documentation
2. Add/update tests
3. Run quality checks
4. Commit changes
5. Push to branch
6. Create pull request

**PR Title:** Should follow commit message format

**PR Description:** Include:
- What changes were made
- Why they were made
- How they were tested
- Related issues

---

## Coding Standards

### Python Style

Follow PEP 8:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

### Type Hints

Use type hints for all public functions:

```python
from typing import List, Optional

def get_functions(
    code: str,
    include_nested: bool = False
) -> List[FunctionInfo]:
    """Extract function definitions from code."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def analyze_file(
    file_path: str,
    rules: Optional[Dict[str, bool]] = None
) -> DiagnosticResult:
    """Analyze a MATLAB file for errors and warnings.

    Args:
        file_path: Path to the .m file to analyze
        rules: Diagnostic rules to apply

    Returns:
        DiagnosticResult containing found diagnostics

    Raises:
        FileNotFoundError: If file doesn't exist
        AnalysisError: If analysis fails
    """
    pass
```

### Async/Await

LSP is async by nature. Use `async def` for handlers:

```python
@server.feature("textDocument/completion")
async def handle_completion(
    params: CompletionParams
) -> CompletionResult:
    """Handle completion requests."""
    result = await some_async_operation()
    return result
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run specific test
pytest tests/unit/test_parser.py::test_parse_function

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v
```

### Writing Tests

Use pytest with descriptive names:

```python
import pytest
from src.parser.matlab_parser import MatlabParser

def test_parse_simple_function():
    """Test parsing of a simple function definition."""
    parser = MatlabParser()
    code = "function x = foo(a, b) end"
    result = parser.parse(code)

    assert len(result.functions) == 1
    assert result.functions[0].name == "foo"
    assert result.functions[0].parameters == ["a", "b"]
```

### Test Structure

```
tests/
├── conftest.py           # Pytest fixtures
├── unit/                 # Unit tests
│   ├── test_parser.py
│   ├── test_analyzer.py
│   └── test_handlers.py
└── integration/          # Integration tests
    ├── test_server.py
    └── test_mlint_integration.py
```

### Fixtures

Use `conftest.py` for shared fixtures:

```python
import pytest

@pytest.fixture
def sample_matlab_code():
    """Provide sample MATLAB code for testing."""
    return """
    function x = test(a, b)
        x = a + b;
    end
    """

@pytest.fixture
def parser():
    """Provide configured parser instance."""
    return MatlabParser()
```

---

## Submitting Changes

### Before Submitting

Run all quality checks:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/

# Run tests
pytest

# Check coverage (should be >70%)
pytest --cov=src
```

### Pre-commit Hooks (Optional)

Install pre-commit hooks for automatic checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Now hooks run automatically on commit
```

### Creating Pull Request

1. Go to [GitHub Pull Requests](https://github.com/yourusername/matlab_lsp_server/pulls)
2. Click "New Pull Request"
3. Select your branch
4. Fill in PR template:
   - Description of changes
   - Testing performed
   - Related issues
5. Submit

### PR Review Process

- Maintainers will review your PR
- Address feedback with new commits
- Once approved, PR will be merged
- You'll be credited in CHANGELOG

---

## Reporting Bugs

### Before Reporting

1. Search [existing issues](https://github.com/yourusername/matlab_lsp_server/issues)
2. Check [FAQ in README](README.md#troubleshooting)
3. Reproduce the bug with latest version

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows 11, Ubuntu 22.04]
 - Python Version: [e.g. 3.11.5]
 - MATLAB Version: [e.g. R2023b]
 - Editor: [e.g. VS Code 1.85.0]
 - Server Version: [e.g. 0.1.0]

**Additional context**
Add any other context about the problem here.

**Logs**
[Attach debug logs from running with `--verbose`]
```

### Get Debug Logs

```bash
# Enable verbose logging
export LSP_LOG_LEVEL=DEBUG  # Linux/macOS
set LSP_LOG_LEVEL=DEBUG     # Windows

# Run server
python -m matlab_lsp --stdio --verbose > debug.log 2>&1
```

---

## Suggesting Features

### Before Suggesting

1. Search [existing issues](https://github.com/yourusername/matlab_lsp_server/issues)
2. Check [ROADMAP](README.md#roadmap)
3. Consider if it's a core LSP feature

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear and concise description of what the problem is.
Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

---

## Development Resources

### Key Documentation

- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [lsprotocol Types](https://lsprotocol.readthedocs.io/)
- [MATLAB Documentation](https://www.mathworks.com/help/matlab/)

### Code Structure

```
src/
├── protocol/         # LSP lifecycle (initialize, shutdown, exit)
├── handlers/         # LSP method handlers
│   ├── completion.py
│   ├── hover.py
│   ├── diagnostics.py
│   └── ...
├── parser/           # MATLAB code parser
│   ├── matlab_parser.py
│   └── models.py
├── analyzer/         # Code analyzers
│   ├── base_analyzer.py
│   └── mlint_analyzer.py
├── features/         # Feature management
│   └── feature_manager.py
└── utils/           # Utilities
    ├── cache.py
    ├── logging.py
    ├── config.py
    └── ...
```

### MCP Tools Used

This project uses MCP (Model Context Protocol) tools for development:

- **context7 MCP** - Library documentation (pygls, lsprotocol)
- **z_ai MCP** - Code generation and analysis
- **z_ai_tools MCP** - Image and diagram analysis
- **DuckDuckGo MCP** - Web search and research
- **Filesystem MCP** - File operations

---

## Recognition

Contributors will be recognized in:
- CHANGELOG.md (for each release)
- README.md (contributors section)
- GitHub contributors list

Thank you for contributing! 🎉

---

## Questions?

- Check [Documentation](README.md)
- Search [Issues](https://github.com/yourusername/matlab_lsp_server/issues)
- Create [Discussion](https://github.com/yourusername/matlab_lsp_server/discussions)
