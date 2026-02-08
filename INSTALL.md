# Installation Guide

Complete installation instructions for LSP MATLAB Server on Windows, Linux, and macOS.

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
pip install lsp-matlab-for-windows
```

That's it! Now [configure your editor](#editor-configuration) and start coding.

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
pip install lsp-matlab-for-windows

# Verify installation
python -m matlab_lsp --version

# Run server
python -m matlab_lsp --stdio
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
pip install lsp-matlab-for-windows
```

---

### Method 2: Install from Source

**Best for:** Developers, testing latest features, contributing

```bash
# Clone repository
git clone https://github.com/yourusername/lsp_matlab_for_windows.git
cd lsp_matlab_for_windows

# Install in editable mode
pip install -e .

# Verify installation
python server.py --version

# Run server
python server.py --stdio
```

---

### Method 3: Download Release

**Best for:** Offline installation, specific version, no Git

1. Go to [Releases page](https://github.com/yourusername/lsp_matlab_for_windows/releases)
2. Download latest release (`.tar.gz` or `.zip`)
3. Extract the archive:
   ```bash
   # Linux/macOS
   tar -xzf lsp_matlab_server_v*.tar.gz

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
   python server.py --stdio
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
pip install lsp-matlab-for-windows

# Or from PowerShell
python -m pip install lsp-matlab-for-windows
```

#### MATLAB Path Configuration

If MATLAB is installed, configure the path:

**Option 1: Environment Variable**
```cmd
setx MATLAB_PATH "C:\Program Files\MATLAB\R2023b"
```

**Option 2: Config File**
Create `.matlab-lsprc.json`:
```json
{
  "matlabPath": "C:/Program Files/MATLAB/R2023b"
}
```

#### Troubleshooting
- If `pip` not found: Add Python to PATH and restart terminal
- If scripts not found: Reinstall Python with "Add to PATH" checked
- If mlint not found: Set `MATLAB_PATH` or install MATLAB

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
pip install lsp-matlab-for-windows
```

#### MATLAB Path Configuration

If MATLAB is installed, configure the path:

**Option 1: Environment Variable**
```bash
export MATLAB_PATH="/usr/local/MATLAB/R2023b"
echo 'export MATLAB_PATH="/usr/local/MATLAB/R2023b"' >> ~/.bashrc
```

**Option 2: Config File**
Create `.matlab-lsprc.json`:
```json
{
  "matlabPath": "/usr/local/MATLAB/R2023b"
}
```

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
pip install lsp-matlab-for-windows
```

#### MATLAB Path Configuration

If MATLAB is installed, configure the path:

**Option 1: Environment Variable**
```bash
export MATLAB_PATH="/Applications/MATLAB_R2023b.app"
echo 'export MATLAB_PATH="/Applications/MATLAB_R2023b.app"' >> ~/.zshrc
```

**Option 2: Config File**
Create `.matlab-lsprc.json`:
```json
{
  "matlabPath": "/Applications/MATLAB_R2023b.app"
}
```

---

## Configuration

### Configuration File

Create `.matlab-lsprc.json` in your project root:

```json
{
  "matlabPath": "C:/Program Files/MATLAB/R2023b",
  "workspace": ["C:/MyProjects"],
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

### Configuration Options

| Option | Type | Default | Description |
|---------|-------|----------|-------------|
| `matlabPath` | string | auto | Path to MATLAB installation |
| `workspace` | array | [] | Workspace folders to index |
| `maxDiagnostics` | integer | 100 | Max diagnostics per file |
| `diagnosticRules.all` | boolean | true | Enable all rules |
| `diagnosticRules.unusedVariable` | boolean | true | Check unused variables |
| `diagnosticRules.missingSemicolon` | boolean | false | Check missing semicolons |
| `formatting.indentSize` | integer | 4 | Indentation size |
| `formatting.insertSpaces` | boolean | true | Use spaces (vs tabs) |
| `completion.enableSnippets` | boolean | true | Enable code snippets |
| `completion.maxSuggestions` | integer | 50 | Max completion items |
| `cache.enabled` | boolean | true | Enable caching |
| `cache.maxSize` | integer | 1000 | Max cache entries |

### Environment Variables

```bash
# MATLAB path
export MATLAB_PATH="C:/Program Files/MATLAB/R2023b"

# Log level (DEBUG, INFO, WARNING, ERROR)
export LSP_LOG_LEVEL="INFO"

# Maximum diagnostics
export LSP_MAX_DIAGNOSTICS="100"

# Cache size
export LSP_CACHE_SIZE="1000"
```

---

## Editor Configuration

### TUI Crush

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

### VS Code

Install the official MATLAB extension, then configure:

**Option 1: Using settings.json**
```json
{
  "matlab.lsp.enabled": true,
  "matlab.lsp.path": "python",
  "matlab.lsp.args": ["-m", "matlab-lsp", "--stdio"]
}
```

**Option 2: Using languageserver.json**
Create `.vscode/languageserver.json`:
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

### Neovim (nvim-lspconfig)

Add to `init.lua`:

```lua
require('lspconfig').matlab_lsp.setup({
  cmd = {"python", "-m", "matlab-lsp", "--stdio"},
  filetypes = {"matlab", "m"},
  root_dir = require('lspconfig.util').root_pattern(
    ".git", ".matlab-lsprc.json"
  ),
  settings = {
    matlab = {
      diagnostics = { all = true },
      completion = { maxSuggestions = 50 }
    }
  }
})
```

### Emacs (eglot)

Add to `init.el`:

```elisp
(use-package eglot
  :ensure t
  :config
  (add-to-list 'eglot-server-programs
               '(matlab-mode . ("python" "-m" "matlab-lsp" "--stdio"))))
```

---

## Verification

### Check Installation

```bash
# Check version
python -m matlab_lsp --version

# Expected output: MATLAB LSP Server v0.1.0
```

### Test Server

```bash
# Run in TCP mode for testing
python -m matlab_lsp --tcp --port 4389

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
3. Should see warning about unused variable

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
1. Install MATLAB R2020b or later
2. Set `MATLAB_PATH` environment variable
3. Create `.matlab-lsprc.json` with `matlabPath`
4. Server will use standalone analyzer (limited features)

#### "No diagnostics shown"

**Solution:**
```bash
# Enable debug logging
export LSP_LOG_LEVEL="DEBUG"

# Check logs for errors
python -m matlab_lsp --stdio --verbose
```

#### "Server not starting"

**Solution:**
1. Check Python version: `python --version` (must be 3.10+)
2. Check dependencies: `pip check`
3. Reinstall: `pip install --force-reinstall lsp-matlab-for-windows`

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
pip install lsp-matlab-for-windows
```

### Getting Help

If you're still having issues:

1. Check [FAQ in README](README.md#troubleshooting)
2. Search [existing issues](https://github.com/yourusername/lsp_matlab_for_windows/issues)
3. [Create a new issue](https://github.com/yourusername/lsp_matlab_for_windows/issues/new)
4. Include:
   - OS and version
   - Python version
   - Error messages
   - Configuration file content
   - Debug logs (with `--verbose`)

---

## Uninstallation

```bash
# Using pip
pip uninstall lsp-matlab-for-windows

# Remove config (optional)
rm ~/.matlab-lsprc.json  # Linux/macOS
rm %USERPROFILE%\.matlab-lsprc.json  # Windows
```

---

## Next Steps

- [ ] Configure your [editor](#editor-configuration)
- [ ] Create a [configuration file](#configuration)
- [ ] Read [README](README.md) for features
- [ ] Check [CHANGELOG](CHANGELOG.md) for updates

---

**Need help?** See [README](README.md) or [create an issue](https://github.com/yourusername/lsp_matlab_for_windows/issues)
