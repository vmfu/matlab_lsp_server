# Installation Guide

Complete installation instructions for MATLAB LSP Server on Windows, Linux, and macOS.

---

## Table of Contents

- [Quick Install](#quick-install)
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Quick Install

The fastest way to get started:

```bash
pip install matlab-lsp-server
```

That's it! Now [configure your editor](#editor-configuration) and start coding.

For detailed editor integration guides, see [INTEGRATION.md](INTEGRATION.md).

---

## System Requirements

### Minimum Requirements
- **Python:** 3.10 or higher
- **RAM:** 50MB
- **Disk:** 10MB free space
- **OS:** Windows 10+, Linux, or macOS 11+

### Recommended Requirements (for full features)
- **Python:** 3.10 or higher
- **RAM:** 100MB
- **Disk:** 50MB free space
- **MATLAB:** R2020b or later (optional)
- **Storage:** SSD recommended

### Optional Requirements
- **MATLAB R2023b** - For latest mlint features
- **Git** - For installing from source
- **Virtual Environment** - Recommended for isolation

---

## Installation Methods

### Method 1: pip install (Recommended)

**Best for:** Most users, quick setup, production use

```bash
# Install from PyPI
pip install matlab-lsp-server

# Verify installation
matlab-lsp --version

# Run server
matlab-lsp --stdio
```

#### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv matlab-lsp-env

# Activate on Windows
matlab-lsp-env\Scripts\activate

# Activate on Linux/macOS
source matlab-lsp-env/bin/activate

# Install
pip install matlab-lsp-server
```

---

### Method 2: Install from Source

**Best for:** Developers, testing latest features, contributing

```bash
# Clone repository
git clone https://github.com/vmfu/matlab_lsp_server.git
cd matlab_lsp_server

# Install in editable mode
pip install -e .

# Verify installation
matlab-lsp --version

# Run server
matlab-lsp --stdio
```

---

### Method 3: Download Release

**Best for:** Offline installation, specific version, no Git

1. Go to [Releases page](https://github.com/vmfu/matlab_lsp_server/releases)
2. Download latest release (`.tar.gz` or `.zip`)
3. Extract the archive:
   ```bash
   # Linux/macOS
   tar -xzf matlab_lsp_server_v*.tar.gz

   # Windows
   # Right-click and extract
   ```
4. Navigate to extracted directory
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run server:
   ```bash
   matlab-lsp --stdio
   ```

---

## Platform-Specific Instructions

### Windows

#### Prerequisites
1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. (Optional) Install MATLAB R2020b or later

#### Installation

```bash
# Open Command Prompt or PowerShell
pip install matlab-lsp-server

# Or from PowerShell
python -m pip install matlab-lsp-server
```

#### MATLAB Path Configuration

**Option 1: Auto-discovery (Recommended)**

The server automatically detects MATLAB in standard locations:
- `C:/Program Files/MATLAB/`
- `D:/Program Files/MATLAB/` (and other drives)
- Searches for `mlint.exe` recursively

No configuration needed for most setups!

**Option 2: Environment Variable**
```cmd
setx MATLAB_PATH "C:\Program Files\MATLAB\R2023b"
```

**Option 3: Config File**

The server automatically creates `.matlab-lsprc.json` on first run with auto-detected MATLAB path. You can edit it:

```json
{
  "matlabPath": "C:/Program Files/MATLAB/R2023b"
}
```

#### Troubleshooting
- If `pip` not found: Add Python to PATH and restart terminal
- If scripts not found: Reinstall Python with "Add to PATH" checked
- If mlint not found: Server will use standalone analyzer (basic features work)

---

### Linux

#### Prerequisites
1. Install Python 3.10+:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 python3-pip python3-venv

   # Fedora
   sudo dnf install python3 python3-pip

   # Arch
   sudo pacman -S python python-pip
   ```
2. (Optional) Install MATLAB R2020b or later

#### Installation

```bash
# Create virtual environment
python3 -m venv matlab-lsp-env
source matlab-lsp-env/bin/activate

# Install server
pip install matlab-lsp-server
```

#### MATLAB Path Configuration

**Option 1: Auto-discovery (Recommended)**

The server automatically detects MATLAB in standard locations:
- `/usr/local/MATLAB/`
- `/opt/MATLAB/`
- `~/MATLAB/`
- Searches for `mlint` recursively

No configuration needed for most setups!

**Option 2: Environment Variable**
```bash
export MATLAB_PATH="/usr/local/MATLAB/R2023b"
echo 'export MATLAB_PATH="/usr/local/MATLAB/R2023b"' >> ~/.bashrc
```

**Option 3: Config File**

The server automatically creates `.matlab-lsprc.json` on first run.

#### Octave Support (Experimental)

If you have Octave instead of MATLAB:
```bash
# Install Octave
sudo apt install octave  # Debian/Ubuntu
sudo dnf install octave  # Fedora

# Use Octave's mlint alternative
# Note: Limited features compared to MATLAB's mlint
```

---

### macOS

#### Prerequisites
1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/)
   - Do NOT use system Python (too old)
   - OR use Homebrew: `brew install python@3.11`
2. (Optional) Install MATLAB R2020b or later

#### Installation

```bash
# Create virtual environment
python3 -m venv matlab-lsp-env
source matlab-lsp-env/bin/activate

# Install server
pip install matlab-lsp-server
```

#### MATLAB Path Configuration

**Option 1: Auto-discovery (Recommended)**

The server automatically detects MATLAB in standard locations:
- `/Applications/MATLAB_R*.app`
- `/Applications/MATLAB.app`
- Searches for `mlint` recursively

No configuration needed for most setups!

**Option 2: Environment Variable**
```bash
export MATLAB_PATH="/Applications/MATLAB_R2023b.app"
echo 'export MATLAB_PATH="/Applications/MATLAB_R2023b.app"' >> ~/.zshrc
```

**Option 3: Config File**

The server automatically creates `.matlab-lsprc.json` on first run.

---

## Configuration

### Automatic Configuration

The server automatically creates `.matlab-lsprc.json` with default settings on first run if it doesn't exist. You can start using the server immediately and edit the auto-generated configuration file later.

To disable automatic configuration, use `--no-init-config` flag:

```bash
matlab-lsp --stdio --no-init-config
```

### Configuration Priority

MATLAB LSP Server supports multiple configuration methods with the following priority order:

1. **Editor Settings** (highest) - Passed via LSP client during initialization
2. **Config File** - `.matlab-lsprc.json` in project root
3. **Environment Variables** - `MATLAB_PATH`, `MATLAB_LSP_*`
4. **Auto-Discovery** - Automatically finds MATLAB in standard locations
5. **Default Values** - Built-in defaults

**Note:** Settings from higher priority sources override those from lower priority sources.

### Configuration Options

The server supports both nested and flat configuration structures:

**Option 1: Nested structure (recommended)**
```json
{
  "matlab": {
    "matlabPath": "C:/Program Files/MATLAB/R2023b",
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
}
```

**Option 2: Flat structure (also supported)**
```json
{
  "matlabPath": "C:/Program Files/MATLAB/R2023b",
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

### Complete Configuration Options Reference

| Option | Type | Default | Description |
|---------|-------|----------|-------------|
| `matlabPath` | string | auto | Path to MATLAB installation (can be empty for auto-discovery) |
| `maxDiagnostics` | integer | 100 | Max diagnostics per file (range: 0-1000) |
| `diagnosticRules.all` | boolean | true | Enable all rules |
| `diagnosticRules.unusedVariable` | boolean | true | Check unused variables |
| `diagnosticRules.missingSemicolon` | boolean | false | Check missing semicolons |
| `formatting.indentSize` | integer | 4 | Indentation size |
| `formatting.insertSpaces` | boolean | true | Use spaces (vs tabs) |
| `completion.enableSnippets` | boolean | true | Enable code snippets |
| `completion.maxSuggestions` | integer | 50 | Max completion items |
| `cache.enabled` | boolean | true | Enable caching |
| `cache.maxSize` | integer | 1000 | Max cache entries |

### Behavior Without MATLAB

If `matlabPath` is not configured or left empty:

**What works:**
- ✅ All basic LSP features (completion, hover, go to definition)
- ✅ Symbol extraction and code navigation
- ✅ Syntax highlighting (provided by editor)
- ✅ Document symbols and workspace symbols

**What doesn't work:**
- ❌ MATLAB mlint diagnostics (error/warning checking)
- ❌ Advanced code analysis from MATLAB

**How mlint is located:**
1. Checks configured `matlabPath` in `.matlab-lsprc.json`
   - Validates path exists before using
   - If invalid, continues searching (handles reinstallation)
2. Checks `MATLAB_PATH` environment variable
3. Searches in system PATH (recursive search)
   - Finds mlint even in `bin/win64/` subdirectories
   - Searches up to 3 levels deep from PATH entries
4. Checks standard installation paths:
   - Windows: `C:/Program Files/MATLAB`, `D:/...`, `H:/...` (multiple drives)
   - macOS: `/Applications/MATLAB_R*.app`, `/Applications/MATLAB.app`
   - Linux: `/usr/local/MATLAB`, `/opt/MATLAB`, `~/MATLAB`, `/usr/share/matlab`

**Auto-Discovery on First Run:**
When `.matlab-lsprc.json` is created, the server:
- Searches for MATLAB automatically
- Fills `matlabPath` if found
- Leaves empty if not found (basic features still work)

If mlint is not found, the server logs: `"MlintAnalyzer is NOT available!"`

### Environment Variables

You can also configure using environment variables:

```bash
# MATLAB path
export MATLAB_PATH="/usr/local/MATLAB/R2023b"

# Configuration options (prefix: MATLAB_LSP_)
export MATLAB_LSP_MAX_DIAGNOSTICS="100"
export MATLAB_LSP_DIAGNOSTIC_RULES_ALL="true"
```

| Environment Variable | Config Option | Example |
|-------------------|----------------|---------|
| `MATLAB_PATH` | `matlabPath` | `export MATLAB_PATH="/usr/local/MATLAB/R2023b"` |
| `MATLAB_LSP_MAX_DIAGNOSTICS` | `maxDiagnostics` | `export MATLAB_LSP_MAX_DIAGNOSTICS="50"` |
| `MATLAB_LSP_DIAGNOSTIC_RULES_ALL` | `diagnosticRules.all` | `export MATLAB_LSP_DIAGNOSTIC_RULES_ALL="true"` |

---

## Editor Configuration

For detailed editor integration guides, see [INTEGRATION.md](INTEGRATION.md).

### Quick Examples

**TUI Crush (`.crush.json`):**
```json
{
  "lsp": {
    "matlab": {
      "command": "matlab-lsp",
      "args": ["--stdio"],
      "filetypes": ["matlab", "m"],
      "root_markers": [".git", ".matlab-lsprc.json", "project.m"]
    }
  }
}
```

**Neovim (`init.lua`):**
```lua
require('lspconfig').matlab_lsp.setup({
  cmd = { "matlab-lsp", "--stdio" },
  filetypes = { "matlab", "m" },
  root_dir = require('lspconfig.util').root_pattern(
    ".git", ".matlab-lsprc.json", "project.m"
  ),
})
```

**VS Code (`.vscode/settings.json`):**
```json
{
  "languageserver": {
    "matlab": {
      "command": "matlab-lsp",
      "args": ["--stdio"],
      "filetypes": ["matlab", "m"],
      "rootPatterns": [".git", ".matlab-lsprc.json"]
    }
  }
}
```

**Emacs (`init.el`):**
```elisp
(use-package eglot
  :ensure t
  :config
  (add-to-list 'eglot-server-programs
               '(matlab-mode . ("matlab-lsp" "--stdio"))))
```

*See [INTEGRATION.md](INTEGRATION.md) for more editors and detailed configuration.*

---

## Verification

### Check Installation

```bash
# Check version
matlab-lsp --version

# Expected output: MATLAB LSP Server v0.2.1
```

### Test Server

```bash
# Run in TCP mode for testing
matlab-lsp --tcp --port 4389

# In another terminal, connect
telnet localhost 4389

# Send initialize request
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}
```

### Test with Editor

1. Open your editor
2. Open any `.m` file
3. Type `function test() end`
4. Place cursor on `function`
5. Press F12 (or your editor's go-to-definition shortcut)
6. Server should navigate to definition

### Check Diagnostics

1. Create test file `test.m`:
   ```matlab
   function x = test(a, b)
       unused = 10;
       x = a + b;
   end
   ```
2. Open file in editor with LSP
3. Should see warning about unused variable (if MATLAB is configured)

---

## Troubleshooting

### Common Issues

#### "Python not found"

**Solution:**
- Windows: Reinstall Python with "Add to PATH"
- Linux/macOS: `sudo apt install python3` or use pyenv

#### "pip not found"

**Solution:**
```bash
# Ensure Python is installed
python3 --version

# Install pip
python3 -m ensurepip

# Or use get-pip.py
curl https://bootstrap.pypa.io/get-pip.py | python
```

#### "mlint not found"

**Solution:**
1. Server will use standalone analyzer (basic features work)
2. The server auto-detects MATLAB in standard locations
3. Or manually configure via `.matlab-lsprc.json`:
   ```json
   {
     "matlabPath": "C:/Program Files/MATLAB/R2023b"
   }
   ```
4. Or set `MATLAB_PATH` environment variable

#### "No diagnostics shown"

**Solution:**
```bash
# Enable verbose logging
matlab-lsp --stdio --verbose

# Check MATLAB path configuration
# Verify mlint is found in logs
```

#### "Server not starting"

**Solution:**
1. Check Python version: `python --version` (must be 3.10+)
2. Check dependencies: `pip check`
3. Reinstall: `pip install --force-reinstall matlab-lsp-server`

#### "Slow performance"

**Solution:**
1. Enable caching (default: enabled)
2. Reduce `maxSuggestions` in config
3. Close unused documents
4. Use SSD for better performance

#### "Import errors"

**Solution:**
```bash
# Reinstall in clean environment
python -m venv fresh_env
fresh_env\Scripts\activate  # Windows
source fresh_env/bin/activate  # Linux/macOS
pip install matlab-lsp-server
```

### Getting Help

If you're still having issues:

1. Check [FAQ in README](README.md#troubleshooting)
2. Read [INTEGRATION.md](INTEGRATION.md) for detailed editor-specific guides
3. Search [existing issues](https://github.com/vmfu/matlab_lsp_server/issues)
4. [Create a new issue](https://github.com/vmfu/matlab_lsp_server/issues/new)
5. Include:
   - OS and version
   - Python version
   - Error messages
   - Configuration file content
   - Debug logs (with `--verbose`)

---

## Uninstallation

```bash
# Using pip
pip uninstall matlab-lsp-server

# Remove config (optional)
rm ~/.matlab-lsprc.json  # Linux/macOS
rm %USERPROFILE%\.matlab-lsprc.json  # Windows
```

---

## Next Steps

- [ ] Configure your [editor](#editor-configuration) or see [INTEGRATION.md](INTEGRATION.md)
- [ ] Read [README](README.md) for features
- [ ] Check [CHANGELOG](CHANGELOG.md) for updates
- [ ] Explore [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

---

**Need help?** See [README](README.md) or [create an issue](https://github.com/vmfu/matlab_lsp_server/issues)
