# Migration Guide: Rename from lsp-matlab-for-windows to matlab-lsp-server

**Date:** February 7, 2026
**Old Name:** `lsp-matlab-for-windows`
**New Name:** `matlab-lsp-server`

---

## Why the Rename?

The original name `lsp-matlab-for-windows` no longer reflected the project's capabilities:

1. **Cross-Platform Support** - The server now works on Linux and macOS, not just Windows
2. **Simpler Name** - Shorter, easier to remember and type
3. **Clearer Purpose** - Name directly indicates it's an LSP server for MATLAB

---

## What Changed?

### Package Name

| Before | After |
|--------|-------|
| `lsp-matlab-for-windows` | `matlab-lsp-server` |

### Installation Command

```bash
# Old command (no longer works)
pip install lsp-matlab-for-windows

# New command
pip install matlab-lsp-server
```

### Repository URL

| Before | After |
|--------|-------|
| `https://github.com/yourusername/lsp_matlab_for_windows` | `https://github.com/yourusername/matlab_lsp_server` |

### PyPI URL

| Before | After |
|--------|-------|
| `https://pypi.org/project/lsp-matlab-for-windows/` | `https://pypi.org/project/matlab-lsp-server/` |

### Local Directory

| Before | After |
|--------|-------|
| `lsp_matlab_for_windows/` | `matlab_lsp_server/` |

---

## Migration Steps for Users

### Option 1: Upgrade to New Name (Recommended)

```bash
# Uninstall old version
pip uninstall lsp-matlab-for-windows

# Install new version
pip install matlab-lsp-server

# Update editor configuration with new command
# See below for editor-specific steps
```

### Option 2: Continue Using Old Name (Temporary)

The old package name will continue to work for a limited time, but **migration is recommended**:

```bash
# Old package still works (for now)
pip install lsp-matlab-for-windows

# But you should migrate soon!
```

---

## Editor Configuration Updates

### TUI Crush

**Old Configuration (.crush.json):**
```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab-lsp", "--stdio"],
      "filetypes": ["matlab", "m"]
    }
  }
}
```

**New Configuration (No Change Needed!):**
The command `matlab-lsp` (from pyproject.toml scripts section) works the same way:

```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab-lsp", "--stdio"],
      "filetypes": ["matlab", "m"]
    }
  }
}
```

Or use the direct command:

```json
{
  "lsp": {
    "matlab": {
      "command": "matlab-lsp-server",
      "args": ["--stdio"],
      "filetypes": ["matlab", "m"]
    }
  }
}
```

### VS Code

**Old Configuration (.vscode/settings.json):**
```json
{
  "matlab.lsp.serverPath": "python",
  "matlab.lsp.serverArgs": ["-m", "matlab-lsp", "--stdio"]
}
```

**New Configuration:**
```json
{
  "matlab.lsp.serverPath": "matlab-lsp-server",
  "matlab.lsp.serverArgs": ["--stdio"]
}
```

### Neovim (Lua)

**Old Configuration:**
```lua
require('lspconfig').matlab_lsp.setup {
  cmd = { 'python', '-m', 'matlab-lsp', '--stdio' },
  filetypes = { 'matlab', 'm' }
}
```

**New Configuration:**
```lua
require('lspconfig').matlab_lsp.setup {
  cmd = { 'matlab-lsp-server', '--stdio' },
  filetypes = { 'matlab', 'm' }
}
```

---

## For Developers

### Repository Clone

**Old URL:**
```bash
git clone https://github.com/yourusername/lsp_matlab_for_windows.git
cd lsp_matlab_for_windows
```

**New URL:**
```bash
git clone https://github.com/yourusername/matlab_lsp_server.git
cd matlab_lsp_server
```

### Local Development

If you have the old repository cloned:

```bash
# Update remote URL
cd lsp_matlab_for_windows
git remote set-url origin https://github.com/yourusername/matlab_lsp_server.git

# Optionally rename directory (outside of git)
cd ..
mv lsp_matlab_for_windows matlab_lsp_server
cd matlab_lsp_server
```

### Import Path Changes

**No changes needed!** The internal module structure (`src/`) remains the same:

```python
# This still works
from src.matlab_server import MatLSServer
from src.protocol.lifecycle import ...
```

---

## Breaking Changes

### None!

This rename is **backward compatible** for users:

1. ✅ Editor configurations using `python -m matlab-lsp --stdio` still work
2. ✅ All LSP features remain the same
3. ✅ Configuration file format unchanged
4. ✅ No API changes

The only change is the **PyPI package name** for installation.

---

## Timeline

- **v0.1.0** - Last release under old name (`lsp-matlab-for-windows`)
- **v0.1.1** - First release under new name (`matlab-lsp-server`)
- **v0.1.0** will be retired after 6 months from new release

---

## Questions?

- **Documentation:** See [README.md](README.md)
- **Issues:** [GitHub Issues](https://github.com/yourusername/matlab_lsp_server/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/matlab_lsp_server/discussions)

---

## Summary

| Item | Old | New |
|------|-----|-----|
| **Package Name** | `lsp-matlab-for-windows` | `matlab-lsp-server` |
| **Install Command** | `pip install lsp-matlab-for-windows` | `pip install matlab-lsp-server` |
| **Repository** | `lsp_matlab_for_windows` | `matlab_lsp_server` |
| **Command** | `matlab-lsp` (unchanged) | `matlab-lsp-server` (new) |

**Note:** The `matlab-lsp` command (from pyproject.toml scripts) continues to work!

---

**Thank you for using MATLAB LSP Server!**
