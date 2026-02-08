# LSP MATLAB Server

A lightweight, fast, and cross-platform Language Server Protocol (LSP) implementation for MATLAB files.

**Version:** 0.2.0 | **License:** MIT | **Python:** 3.10+

📖 **[See INTEGRATION.md](INTEGRATION.md) for detailed editor configuration guides and advanced options.**

---

## Quick Install

```bash
pip install matlab-lsp-server
```

That's it! The server is now ready to use.

*For detailed editor integration guides and advanced configuration, see [INTEGRATION.md](INTEGRATION.md).*

### Command-Line Options

```bash
# Run in stdio mode (for LSP clients)
python -m matlab_lsp --stdio

# Run in TCP mode (for debugging)
python -m matlab_lsp --tcp --port 4389

# Enable verbose logging
python -m matlab_lsp --stdio --verbose

# Disable automatic config creation
python -m matlab_lsp --stdio --no-init-config
```

**Options:**
- `--stdio` - Run in stdio mode (default for LSP clients)
- `--tcp` - Run in TCP mode (for debugging)
- `--port PORT` - Port for TCP mode (default: 4389)
- `--host HOST` - Host for TCP mode (default: 127.0.0.1)
- `-v, --verbose` - Enable verbose logging
- `--no-init-config` - Disable automatic `.matlab-lsprc.json` creation
- `--version` - Show version information

### Configuration Methods

You can configure the server in multiple ways (priority order):

1. **Editor Settings** (highest) - Pass settings via LSP client
2. **Config File** - `.matlab-lsprc.json` in project root
3. **Environment Variables** - `MATLAB_PATH`
4. **Auto-Discovery** - Automatically finds MATLAB in standard locations

#### Quick Editor Configuration

**VS Code (`.vscode/settings.json`):**
```json
{
  "languageserver": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab_lsp", "--stdio"],
      "filetypes": ["matlab", "m"],
      "rootPatterns": [".git", ".matlab-lsprc.json"]
    }
  }
}
```

**Neovim (nvim-lspconfig):**
```lua
require('lspconfig').matlab_lsp.setup({
  cmd = {'python', '-m', 'matlab_lsp', '--stdio'},
  filetypes = {'matlab', 'm'},
  root_dir = require('lspconfig.util').root_pattern('.git', '.matlab-lsprc.json', 'project.m')
})
```

**Vim (vim-lsp):**
```vim
" .vimrc
autocmd BufRead,BufNewFile *.m set filetype=matlab

if executable('python')
  au User lsp_setup call lsp#register_server({
    \ 'name': 'matlab-lsp',
    \ 'cmd': {server_info->['python', '-m', 'matlab_lsp', '--stdio']},
    \ 'whitelist': ['matlab', 'm']
    \ })
endif
```

**Emacs (lsp-mode):**
```elisp
;; init.el
(use-package lsp-mode
  :config
  (lsp-register-client
    (make-lsp-client
      :new-connection (lsp-stdio-connection '("python" "-m" "matlab_lsp" "--stdio"))
      :major-modes '(matlab-mode)
      :server-id 'matlab-lsp)))

(use-package matlab-mode
  :config
  (add-hook 'matlab-mode-hook #'lsp))
```

**TUI Crush (`.crush.json`):**
```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab_lsp", "--stdio"],
      "filetypes": ["matlab", "m"],
      "root_markers": [".git", ".matlab-lsprc.json", "project.m"]
    }
  }
}
```

**OpenCode CLI (`.opencode.json`):**
```json
{
  "lsp": {
    "matlab": {
      "command": ["python", "-m", "matlab_lsp", "--stdio"],
      "extensions": [".m"]
    }
  }
}
```

**Claude Code LSP / cclsp (`cclsp.json`):**
```json
{
  "servers": [
    {
      "extensions": ["m"],
      "command": ["python", "-m", "matlab_lsp", "--stdio"],
      "rootDir": "."
    }
  ]
}
```

*See [INTEGRATION.md](INTEGRATION.md) for detailed configuration and advanced options.*

---

## Why This Over Official MathWorks LSP?

| Feature | This Server | MathWorks LSP |
|---------|-------------|---------------|
| **Lightweight** | Pure Python, no Java required | Java-based, heavy |
| **Startup Time** | < 1 second | 5-10 seconds |
| **Memory Usage** | ~50MB | 500MB+ |
| **MATLAB Required** | Optional (standalone analyzer) | Required |
| **Configuration** | Simple JSON file | Complex JSON/registry |
| **Cross-Platform** | Windows, Linux, macOS | Windows only |
| **Customization** | Fully configurable | Limited |

### Key Advantages:

1. **Fast & Lightweight** - Starts instantly, uses minimal resources
2. **No MATLAB Dependency** - Works with standalone analyzer when MATLAB isn't installed
3. **Cross-Platform** - Works on Windows, Linux, and macOS
4. **Simple Setup** - One `pip install` and you're done
5. **Flexible** - Highly configurable with JSON config file
6. **Open Source** - MIT licensed, community-driven

---

## Features

### Core LSP Features
- **Code Completion** - Smart suggestions for functions, variables, and classes
- **Hover Documentation** - Show function signatures and documentation inline
- **Go to Definition** - Jump to function/class definitions instantly
- **Find References** - Locate all usages of symbols
- **Document Symbols** - Outline view of your code structure
- **Workspace Symbols** - Search symbols across entire project
- **Code Formatting** - Auto-format MATLAB code with configurable style
- **Diagnostics** - Real-time error and warning detection
- **Quick Fixes** - Automatic suggestions for common issues

### MATLAB Support
- **Regex Parser** - Fast and robust MATLAB syntax parsing
- **Function Extraction** - Extract all function definitions
- **Class Parsing** - Support for `classdef`, properties, methods
- **Nested Functions** - Handle nested and local functions
- **Variable Tracking** - Track global and persistent variables
- **Comment Extraction** - Parse documentation from comments

### Performance
- **LRU Caching** - Fast symbol lookups with O(1) complexity
- **Debouncing** - Optimized document analysis
- **In-Memory Index** - Quick project-wide symbol search
- **Async Operations** - Non-blocking diagnostics and analysis

*For complete feature documentation and configuration options, see [INTEGRATION.md](INTEGRATION.md).*

---

## Quick Start

### 1. Install

```bash
# Using pip (recommended)
pip install matlab-lsp-server

# Or from source
git clone https://github.com/yourusername/matlab_lsp_server.git
cd matlab_lsp_server
pip install -e .
```

### 2. Configure Your Editor

#### TUI Crush

Create or edit `~/.crush.json`:

```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab-lsp", "--stdio"],
      "filetypes": ["m"],
      "root_markers": [".git", ".matlab-lsprc.json"]
    }
  }
}
```

#### VS Code

Create `.vscode/settings.json`:

```json
{
  "languageserver": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab-lsp", "--stdio"],
      "filetypes": ["matlab", "m"],
      "rootPatterns": [".git", ".matlab-lsprc.json"]
    }
  }
}
```

Or install the MATLAB extension and configure it to use this server.

#### Neovim

Add to `init.lua` or `init.vim`:

```lua
require('lspconfig').matlab_lsp.setup({
  cmd = {"python", "-m", "matlab-lsp", "--stdio"},
  filetypes = {"matlab", "m"},
  root_dir = require('lspconfig.util').root_pattern(
    ".git", ".matlab-lsprc.json"
  ),
})
```

### 3. Open a MATLAB File

Open any `.m` file in your editor. The LSP server will automatically start and provide:
- Syntax error highlighting
- Code completion
- Hover documentation
- Go-to-definition
- And more!

*For more editor configurations (Emacs, Vim, OpenCode, cclsp), see [INTEGRATION.md](INTEGRATION.md).*

---

## Configuration

Copy the example configuration file to your project root:

```bash
cp .matlab-lsprc.json.example .matlab-lsprc.json
```

**Note:** The server automatically creates `.matlab-lsprc.json` with default settings on first run if it doesn't exist. You can skip this step and edit the auto-generated file later.

Then edit `.matlab-lsprc.json` with your settings:

**What happens if `matlabPath` stays empty?**
- Server starts normally without errors
- Basic LSP features work (completion, hover, go to definition, etc.)
- Diagnostics from MATLAB's mlint analyzer will be unavailable
- Server tries to find MATLAB in standard locations
- Server logs a warning: "MlintAnalyzer is NOT available!"

**Auto-Discovery on First Run:**
On first startup, the server automatically searches for MATLAB in:
1. System PATH (recursive search, finds even in bin/win64/)
2. Standard installation paths:
   - Windows: `C:/Program Files/MATLAB`, `D:/Program Files/MATLAB`, etc.
   - macOS: `/Applications/MATLAB_R*.app`
   - Linux: `/usr/local/MATLAB`, `/opt/MATLAB`, `~/MATLAB`
3. If found, `matlabPath` is auto-filled in `.matlab-lsprc.json`

**To enable full diagnostics:**
1. Set `matlabPath` in `.matlab-lsprc.json`
2. Or set `MATLAB_PATH` environment variable
3. Or ensure MATLAB is in system PATH

**Handling MATLAB Reinstallation:**
If you reinstall MATLAB to a different location:
- Server will detect the old path is invalid
- Automatically searches for new MATLAB location
- Falls back to basic LSP features if MATLAB not found
- Update `matlabPath` in config to specify new location


```json
{
  "matlabPath": "C:/Program Files/MATLAB/R2023b"
}
```

**That's it!** All other settings use sensible defaults. For more configuration options, see [INTEGRATION.md](INTEGRATION.md).

### Environment Variables

You can also configure using environment variables:

```bash
# MATLAB installation path
export MATLAB_PATH="C:/Program Files/MATLAB/R2023b"
```

---

## Installation Methods

### Method 1: pip install (Recommended)

```bash
pip install matlab-lsp-server
matlab-lsp --stdio
```

### Method 2: Install from Source

```bash
git clone https://github.com/yourusername/matlab_lsp_server.git
cd matlab_lsp_server
pip install -e .
python server.py --stdio
```

### Method 3: Download Release

1. Download from [Releases](https://github.com/yourusername/matlab_lsp_server/releases)
2. Extract the archive
3. Run: `python server.py --stdio`

---

## Platform-Specific Notes

### Windows
- Requires Python 3.10+
- MATLAB R2020b or later recommended for mlint integration
- Works with PowerShell, Command Prompt, Git Bash

### Linux
- Requires Python 3.10+
- Tested on Ubuntu, Debian, Fedora
- MATLAB R2020b or later recommended
- Works with Octave's mlint alternative (experimental)

### macOS
- Requires Python 3.10+ (from python.org or Homebrew)
- MATLAB R2020b or later recommended
- Tested on macOS 11+ (Big Sur and later)

---

## Running the Server

### stdio Mode (for LSP clients)

```bash
python server.py --stdio
# or
matlab-lsp --stdio
```

### TCP Mode (for debugging)

```bash
python server.py --tcp --port 4389
# Connect with telnet or nc
telnet localhost 4389
```

### Verbose Logging

```bash
python server.py --stdio --verbose
```

### Show Version

```bash
python server.py --version
# Output: MATLAB LSP Server v0.2.0
```

---

## Troubleshooting

### "mlint not found"
1. Install MATLAB R2020b or later
2. Set `MATLAB_PATH` environment variable
3. Or configure in `.matlab-lsprc.json`
4. Server will use standalone analyzer (limited features)

### "No diagnostics shown"
1. Check log level is set to INFO or DEBUG
2. Verify MATLAB path is correct
3. Try running server with `--verbose`

### "Slow performance"
1. Enable caching (default: enabled)
2. Reduce `maxSuggestions` in config
3. Close unused documents
4. Use a fast disk (SSD recommended)

### Get Debug Logs

```bash
# Use the --verbose flag
python -m matlab_lsp --stdio --verbose

# Or from source
python server.py --stdio --verbose
```

*For more troubleshooting tips and configuration options, see [INTEGRATION.md](INTEGRATION.md).*

---

## Development

### Project Structure

```
matlab_lsp_server/
├── server.py              # Main entry point
├── requirements.txt        # Dependencies
├── pyproject.toml        # Package config
├── src/
│   ├── protocol/         # LSP lifecycle handlers
│   ├── handlers/         # LSP method handlers
│   ├── parser/           # MATLAB parser
│   ├── analyzer/         # Code analyzers
│   ├── features/         # Feature management
│   └── utils/           # Utilities
└── tests/              # Unit and integration tests
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_parser.py::test_parse_function
```

---

## Documentation

- [Installation Guide](INSTALL.md) - Detailed installation instructions
- [Architecture](ARCHITECTURE.md) - Design decisions and structure
- [Development](DEVELOPMENT.md) - Developer guide
- [Contributing](CONTRIBUTING.md) - How to contribute
- [CHANGELOG](CHANGELOG.md) - Version history
- [FAQ](#troubleshooting) - Common issues and solutions

---

## Version: 0.2.0

### What's Included

- ✅ Full LSP implementation (9+ features)
- ✅ MATLAB parser (regex-based)
- ✅ Code completion with ranking
- ✅ Hover documentation
- ✅ Go-to-definition with cross-file support
- ✅ Find references
- ✅ Document symbols with hierarchy
- ✅ Workspace symbols with fuzzy search
- ✅ Code formatting with configurable style
- ✅ Diagnostics via mlint
- ✅ Quick fixes for common errors
- ✅ Cross-platform support (Windows, Linux, macOS)
- ✅ Standalone analyzer (no MATLAB required)
- ✅ LRU caching for performance
- ✅ Configurable via JSON or environment

### Known Limitations

- .mlx files (Live Scripts) not supported
- Octave compatibility is experimental
- Some advanced MATLAB features may not be parsed correctly
- mlint required for full diagnostics (standalone analyzer is limited)

---

## Requirements

### Minimum
- Python 3.10 or higher
- 50MB RAM
- 10MB disk space

### Recommended (for full features)
- MATLAB R2020b or later
- 100MB RAM
- 50MB disk space
- SSD drive for better performance

### Optional
- MATLAB R2023b (for latest features)
- Git (for installation from source)

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Author

**Vladimir M. Funtikov**

## Links

- **GitHub:** https://github.com/yourusername/matlab_lsp_server
- **PyPI:** https://pypi.org/project/matlab-lsp-server/
- **Issues:** https://github.com/yourusername/matlab_lsp_server/issues

---

**LSP MATLAB Server v0.2.0**
**Fast. Lightweight. Cross-Platform.**
