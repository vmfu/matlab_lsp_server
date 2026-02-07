# LSP MATLAB Server v0.1.0 - Installation Guide

Guide for installing and running LSP MATLAB Server v0.1.0.

## Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **RAM**: 4GB recommended
- **Storage**: 100MB for source code + dependencies
- **IDE**: LSP-compatible editor (VS Code 1.60+, JetBrains 2022+)

### Check Python Version

```bash
python --version
# Should output: Python 3.10.x
```

## Installation

### Option 1: Quick Install (Recommended)

```bash
# Navigate to release directory
cd dist/release

# Install dependencies
pip install -r requirements.txt

# Verify installation
python run_server.py --version

# Expected output:
# LSP MATLAB Server v0.1.0
# Version: 0.1.0
# Python: 3.10.x
```

### Option 2: Development Install

```bash
# Clone repository (if not already done)
git clone https://github.com/yourusername/lsp_matlab_for_windows.git
cd lsp_matlab_for_windows

# Install in development mode
pip install -e .

# Verify installation
python -m src.server --version
```

## Running the Server

### Command Line Options

#### Check Version

```bash
cd dist/release
python run_server.py --version
# Or
python run_server.py -v

# Expected output:
# LSP MATLAB Server v0.1.0
# Version: 0.1.0
# Python: 3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)]
```

#### Standard I/O Mode (Recommended for IDEs)

```bash
cd dist/release
python run_server.py --stdio
```

#### TCP Mode (For Testing)

```bash
cd dist/release
python run_server.py --tcp 5050
```

#### Help

```bash
python run_server.py --help
```

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'src.server'"

**Cause**: Missing `server.py` in `dist/release/src/`

**Solution**:
```bash
# Check if server.py exists
ls dist/release/src/server.py

# If not, copy it from root
cp server.py dist/release/src/
```

#### 2. "ImportError: cannot import name '...'"

**Cause**: Python path issues

**Solution**:
```bash
# Install in development mode
pip install -e .

# Or check Python path
python -c "import sys; print(sys.path)"
```

#### 3. Server Starts Immediately

**Cause**: No LSP client connected (expected behavior)

**Solution**: Connect from IDE (VS Code, JetBrains)

#### 4. Completion Not Working

**Cause**: Symbol table not populated

**Solution**:
```bash
# Enable debug logging
export LSP_LOG_LEVEL=DEBUG
python run_server.py --stdio

# Check console for symbol table messages
```

#### 5. Diagnostics Not Showing

**Cause**: Mlint integration issues

**Solution**:
```bash
# Check .matlab-lsprc.json configuration
cat .matlab-lsprc.json

# Ensure matlabPath is correct
# (Optional - remove config file if issues)
```

## IDE Integration

### VS Code

1. **Install Extension**
   - Search for "LSP MATLAB Server" extension
   - Or create your own extension

2. **Configure Settings**
   Create `.vscode/settings.json`:

```json
{
  "matlab.lsp.path": "python",
  "matlab.lsp.args": ["run_server.py", "--stdio"]
}
```

   - OR with absolute path:
```json
{
  "matlab.lsp.path": "F:\\Projects\\lsp_matlab_for_windows\\dist\\release\\python",
  "matlab.lsp.args": ["run_server.py", "--stdio"]
}
```

3. **Restart VS Code**

### JetBrains (IntelliJ, PyCharm, etc.)

1. **Open Settings**
   - Go to Settings > Languages & Frameworks > MATLAB

2. **Configure Language Server**
   - **Language Server**: Custom
   - **Server Path**: `python` (or full path to python.exe)
   - **Arguments**: `run_server.py --stdio`

   - Example with full path:
     - Server Path: `C:\Python310\python.exe`
     - Arguments: `F:\Projects\lsp_matlab_for_windows\dist\release\run_server.py --stdio`

3. **Apply and Restart IDE**

### Other IDEs

Check your IDE's LSP settings for:
- **Language Server Protocol (LSP)** support
- **Custom LSP server** option
- Configure with `python run_server.py --stdio`

## Configuration

### Server Configuration

Server can be configured via `.matlab-lsprc.json` file (auto-generated in current directory).

Example configuration:

```json
{
  "matlabPath": "H:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
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

### Environment Variables

```bash
# Enable debug logging
set LSP_LOG_LEVEL=DEBUG

# Windows CMD
set LSP_LOG_LEVEL=DEBUG && python run_server.py --stdio

# PowerShell
$LSP_LOG_LEVEL="DEBUG"; python run_server.py --stdio
```

## Testing

### Test Installation

```bash
cd dist/release

# Test import
python -c "import server; print('Import successful')"

# Test version
python run_server.py --version

# Expected:
# LSP MATLAB Server v0.1.0
# Version: 0.1.0
```

### Test LSP Connection

1. **Start Server**
   ```bash
   cd dist/release
   python run_server.py --stdio
   ```

2. **Connect from IDE**
   - Open VS Code or JetBrains
   - Navigate to MATLAB file (.m)
   - Check LSP features work (completion, hover, etc.)

3. **Enable Debug**
   ```bash
   LSP_LOG_LEVEL=DEBUG python run_server.py --stdio
   ```

## Features Overview

### Implemented Features

#### Code Intelligence
- ✅ **Code Completion** - Intellisense for MATLAB functions and variables
- ✅ **Hover Documentation** - Display function/variable information
- ✅ **Go-to-Definition** - Navigate to symbol definitions
- ✅ **Find-All-References** - Locate all symbol usages
- ✅ **Document Symbols** - Outline view of file structure
- ✅ **Workspace Symbols** - Search symbols across entire project

#### Code Quality
- ✅ **Quick Fixes** - Automatic suggestions for common errors
- ✅ **Diagnostics** - Linting and error detection
- ✅ **Code Formatting** - Automatic MATLAB code formatting

#### Performance
- ✅ **LRU Caching** - Fast symbol lookups
- ✅ **Debouncing** - Optimized operations
- ✅ **In-memory Index** - Quick symbol search

## Directory Structure (Release)

```
dist/release/
├── src/                    # Source code
│   ├── __init__.py
│   ├── server.py         # LSP server
│   ├── parser/           # MATLAB parser
│   ├── handlers/         # LSP handlers
│   ├── utils/            # Utilities
│   ├── analyzer/          # Code analyzers
│   ├── features/           # Feature management
│   └── protocol/           # LSP protocol
├── run_server.py           # Server launcher script
├── requirements.txt          # Python dependencies
├── pyproject.toml          # Project configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── README.md               # This file (Installation Guide)
├── INSTALL.md              # Quick Installation
├── VERSION.md              # Version information
├── CHANGELOG.md            # Version history
├── ARCHITECTURE.md         # Design documentation
├── DEVELOPMENT.md          # Development guide
├── TODO.md                 # Development tasks (all completed ✅)
└── RELEASE_NOTES.md        # Release notes
```

## Support

### Getting Help

1. **Review Documentation**
   - README.md (this file) - Installation guide
   - ARCHITECTURE.md - Design decisions
   - DEVELOPMENT.md - Development guide

2. **Enable Debug Logging**
   ```bash
   LSP_LOG_LEVEL=DEBUG python run_server.py --stdio
   ```

3. **Check Logs**
   - Review console output for errors
   - Look for "ERROR" or "WARNING" messages

### Reporting Bugs

1. **Include Information**
   - Error message and stack trace
   - Reproduction steps
   - Environment details (OS, Python version)
   - IDE version (VS Code, JetBrains)

2. **Create Issue**
   - Go to GitHub repository
   - Create new issue with bug report
   - Attach logs if possible

3. **Example Issue**
   ```
   **Title**: Completion not working for nested functions

   **Description**:
   When I have nested functions, code completion doesn't show symbols from outer functions.

   **Environment**:
   - OS: Windows 10
   - Python: 3.10.4
   - IDE: VS Code 1.85.1
   - MATLAB: R2023b

   **Steps to Reproduce**:
   1. Create .m file with nested functions
   2. Open in VS Code
   3. Type in nested function
   4. Try completion (Ctrl+Space)

   **Logs**:
   [Attach debug logs with LSP_LOG_LEVEL=DEBUG]
   ```

## Next Steps

### For Users

1. **Install Server** - Follow installation guide
2. **Configure IDE** - Set up LSP client
3. **Test Features** - Try completion, hover, definition
4. **Customize Settings** - Configure formatting, cache, etc.

### For Developers

1. **Review Source Code** - Study implementation
2. **Read Architecture** - Understand design decisions
3. **Extend Features** - Add new LSP features
4. **Contribute** - Submit pull requests

## License

MIT License - See LICENSE file for details.

---

**Version**: 0.1.0
**Last Updated**: 2026-02-07
**Status**: First Stable Release
