# MATLAB LSP Server Integration Guide

Documentation on integrating MATLAB LSP Server with various LSP-compatible editors and clients.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration Methods](#configuration-methods)
  - [OpenCode CLI](#opencode-cli)
  - [Claude Code LSP / cclsp](#claude-code-lsp--cclsp)
  - [TUI Crush](#tui-crush)
  - [VS Code](#vs-code)
  - [Neovim](#neovim)
  - [Vim](#vim)
  - [Emacs](#emacs)
- [Testing Integration](#testing-integration)
- [Common Troubleshooting](#common-troubleshooting)
- [Advanced Configuration](#advanced-configuration)
- [Additional Resources](#additional-resources)

---

## Overview

**MATLAB LSP Server** is a lightweight Language Server Protocol implementation for MATLAB that provides intelligent code editing features. It can be integrated with any LSP-compatible editor or client to deliver:

- 🔍 Error and warning diagnostics
- 💡 Code autocompletion
- 📖 Hover tooltips
- 🔗 Go to definition
- 📑 File structure navigation
- 🛠️ Code actions and quick fixes
- 📝 Code formatting

---

## Requirements

1. **Python**: 3.10 or newer
2. **MATLAB**: R2020b or newer (for mlint-based diagnostics)
3. **MATLAB LSP Server**: Installed and configured
4. **LSP-Compatible Editor**: Any editor that supports Language Server Protocol

---

## Installation

### 1. Installing the Server

```bash
# Install from PyPI
pip install matlab-lsp-server

# Or install from source
git clone https://github.com/vmfuntikov/matlab-lsp-server.git
cd matlab-lsp-server
pip install -e .
```

### 2. Setting Up MATLAB Path

**Option 1: Configuration file**

Copy the configuration example to your project root:

```bash
cp .matlab-lsprc.json.example .matlab-lsprc.json
```

Then edit `.matlab-lsprc.json`:

```json
{
  "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
  "maxDiagnostics": 100,
  "diagnosticRules": {
    "all": true
  }
}
```

**Option 2: Environment variable**

```bash
# Windows
setx MATLAB_PATH "C:\Program Files\MATLAB\R2023b\bin\win64"

# Linux/Mac
export MATLAB_PATH="/usr/local/MATLAB/R2023b/bin"
```

**Option 3: Auto-discovery (NEW in v0.2.0)**

The server will automatically detect MATLAB installation in standard locations. No configuration needed for most setups.

### 3. Verifying Server Operation

```bash
# Run in TCP mode for testing
python -m matlab_lsp --tcp --port 4389

# In another terminal, check connection
telnet localhost 4389
# Or test with curl
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | nc localhost 4389
```

---

## Configuration Methods

### Configuration Priority

MATLAB LSP Server supports multiple configuration methods with the following priority order:

1. ✅ **initializationOptions** (highest priority) - Passed by LSP client during initialization
2. ✅ **.matlab-lsprc.json** - Project-level configuration file
3. ✅ **Environment Variables** - `MATLAB_PATH`, `MATLAB_LSP_*`
4. ✅ **Default Values** - Built-in defaults

**Note:** Settings from higher priority sources override those from lower priority sources.

### Supported initializationOptions

The server supports both nested and flat configuration structures:

**Option 1: Nested structure (recommended)**
```json
{
  "matlab": {
    "matlabPath": "C:\\Program Files\\MATLAB\\R2023b",
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
  "matlabPath": "C:\\Program Files\\MATLAB\\R2023b",
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

**Note:** The nested structure (`{matlab: {...}}`) is recommended for better organization and compatibility with LSP clients that namespace settings. Both formats work identically.

---

## OpenCode CLI

**OpenCode CLI** is a modern command-line editor with built-in LSP support.

### Basic Configuration

Create a `.opencode.json` file in your project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": {
    "matlab": {
      "command": ["python", "-m", "matlab_lsp", "--stdio"],
      "extensions": [".m"],
      "initialization": {
        "matlabPath": "C:\\Program Files\\MATLAB\\R2023b",
        "maxDiagnostics": 100
      }
    }
  }
}
```

### Full Configuration

```json
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": {
    "matlab": {
      "command": ["python", "-m", "matlab_lsp", "--stdio", "--verbose"],
      "extensions": [".m"],
      "initialization": {
        "matlabPath": "C:\\Program Files\\MATLAB\\R2023b",
        "maxDiagnostics": 100,
        "diagnosticRules": {
          "all": true,
          "unusedVariable": true,
          "missingSemicolon": false
        },
        "completion": {
          "enableSnippets": true,
          "maxSuggestions": 50
        },
        "formatting": {
          "indentSize": 4,
          "insertSpaces": true
        }
      }
    }
  }
}
```

### Global Configuration

OpenCode supports global configuration in `~/.opencode.json`:

```bash
# Automatic setup
npx opencode@latest setup --user

# Or manually edit ~/.opencode.json
```

### Environment Variables

```bash
export MATLAB_PATH="C:\\Program Files\\MATLAB\\R2023b"
export MATLAB_LSP_MAX_DIAGNOSTICS=100
```

### Verification

```bash
# Start OpenCode
opencode

# Open a MATLAB file
opencode test.m

# Check LSP status (if supported)
:LspInfo
```

---

## Claude Code LSP / cclsp

**Claude Code LSP (cclsp)** integrates LSP servers with Claude's MCP (Model Context Protocol) for AI-assisted coding.

### Basic Configuration

Create a `cclsp.json` file in your project root:

```json
{
  "servers": [
    {
      "extensions": ["m"],
      "command": ["python", "-m", "matlab_lsp", "--stdio"],
      "rootDir": ".",
      "initializationOptions": {
        "matlabPath": "C:\\Program Files\\MATLAB\\R2023b",
        "maxDiagnostics": 100
      }
    }
  ]
}
```

### Integration with Claude MCP

Add to your MCP client configuration (e.g., `~/.claude/config.json`):

```json
{
  "mcpServers": {
    "cclsp": {
      "command": "cclsp",
      "env": {
        "CCLSP_CONFIG_PATH": "/path/to/your/cclsp.json"
      }
    }
  }
}
```

### Installation

```bash
# Automatic setup
npx cclsp@latest setup --user

# Manual installation
npm install -g cclsp
```

### Environment Variables

```bash
export CCLSP_CONFIG_PATH="/path/to/your/cclsp.json"
export MATLAB_PATH="C:\\Program Files\\MATLAB\\R2023b"
```

### Verification

```bash
# Test cclsp configuration
cclsp test

# Start Claude MCP
claude-mcp start

# Open a .m file and verify LSP features
```

---

## TUI Crush

**TUI Crush** is a terminal UI AI assistant with excellent LSP support.

### Basic Configuration

Create or edit `.crush.json`:

```json
{
  "$schema": "https://charm.land/crush.json",
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab_lsp", "--stdio"],
      "filetypes": ["matlab", "m"],
      "root_markers": [".git", ".matlab-lsprc.json", "project.m"],
      "env": {
        "MATLAB_PATH": "C:/Program Files/MATLAB/R2023b"
      },
      "init_options": {
        "matlab": {
          "matlabPath": "C:/Program Files/MATLAB/R2023b",
          "maxDiagnostics": 100
        }
      }
    }
  }
}
```

### Full Configuration

```json
{
  "$schema": "https://charm.land/crush.json",
  "options": {
    "debug_lsp": true,
    "auto_lsp": true
  },
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab_lsp", "--stdio", "--verbose"],
      "filetypes": ["matlab", "m"],
      "root_markers": [".git", ".matlab-lsprc.json", "project.m"],
      "env": {
        "MATLAB_PATH": "C:/Program Files/MATLAB/R2023b"
      },
      "init_options": {
        "matlab": {
          "matlabPath": "C:/Program Files/MATLAB/R2023b",
          "maxDiagnostics": 100,
          "diagnosticRules": {
            "all": true,
            "unusedVariable": true,
            "missingSemicolon": false
          },
          "completion": {
            "enableSnippets": true,
            "maxSuggestions": 50
          },
          "formatting": {
            "indentSize": 4,
            "insertSpaces": true
          }
        }
      }
    }
  }
}
```

### Keyboard Shortcuts

| Command | Keybinding | Description |
|---------|-------------|-------------|
| Autocomplete | `Ctrl+Space` | Show completions |
| Hover | `K` | Show symbol information |
| Go to Definition | `gd` | Navigate to definition |
| Go Back | `Ctrl+o` | Navigate back |
| Diagnostics | `]d` / `[d` | Next/previous diagnostic |
| File Symbols | `Ctrl+Shift+o` | Document structure |
| Workspace Symbols | `Ctrl+t` | Search workspace symbols |

### Commands

```
:LspInfo         - Server information
:LspRestart      - Restart LSP server
:Diagnostics     - Show all diagnostics
:WorkspaceSymbol - Search workspace symbols
:DocumentSymbol  - Current file structure
:CodeAction      - Available fixes
```

### Verification

```bash
# Start TUI Crush
crush

# Open a MATLAB file
:e /path/to/test.m

# Check LSP status in the status bar
```

---

## VS Code

VS Code requires creating a custom extension to use external LSP servers.

### Project Structure

```
matlab-lsp-vscode/
├── package.json
├── src/
│   └── extension.ts
└── .vscodeignore
```

### package.json

```json
{
  "name": "matlab-lsp",
  "displayName": "MATLAB LSP Server",
  "description": "MATLAB Language Server Protocol implementation",
  "version": "0.2.0",
  "engines": {
    "vscode": "^1.80.0"
  },
  "activationEvents": [
    "onLanguage:matlab",
    "onLanguage:m"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "languages": [
      {
        "id": "matlab",
        "extensions": [".m"],
        "aliases": ["MATLAB", "matlab"],
        "configuration": "./language-configuration.json"
      }
    ],
    "configuration": {
      "title": "MATLAB LSP",
      "properties": {
        "matlabLsp.matlabPath": {
          "type": "string",
          "default": "",
          "description": "Path to MATLAB installation"
        },
        "matlabLsp.maxDiagnostics": {
          "type": "number",
          "default": 100,
          "description": "Maximum diagnostics to report"
        },
        "matlabLsp.trace.server": {
          "type": "string",
          "enum": ["off", "messages", "verbose"],
          "default": "off",
          "description": "LSP trace level"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./"
  },
  "devDependencies": {
    "@types/node": "^18.0.0",
    "@types/vscode": "^1.80.0",
    "typescript": "^5.0.0"
  },
  "dependencies": {
    "vscode-languageclient": "^8.1.0"
  }
}
```

### src/extension.ts

```typescript
import * as vscode from 'vscode';
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
  const serverOptions: ServerOptions = {
    run: {
      command: 'python',
      args: ['-m', 'matlab_lsp', '--stdio']
    },
    debug: {
      command: 'python',
      args: ['-m', 'matlab_lsp', '--stdio', '--verbose']
    }
  };

  const config = vscode.workspace.getConfiguration('matlabLsp');
  const clientOptions: LanguageClientOptions = {
    documentSelector: [
      { scheme: 'file', language: 'matlab' },
      { scheme: 'file', language: 'm' }
    ],
    initializationOptions: {
      matlabPath: config.get<string>('matlabPath', ''),
      maxDiagnostics: config.get<number>('maxDiagnostics', 100)
    }
  };

  client = new LanguageClient(
    'matlabLsp',
    'MATLAB LSP Server',
    serverOptions,
    clientOptions
  );

  client.start();
}

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}
```

### User Settings (.vscode/settings.json)

```json
{
  "matlabLsp.matlabPath": "C:\\Program Files\\MATLAB\\R2023b",
  "matlabLsp.maxDiagnostics": 100,
  "matlabLsp.trace.server": "verbose",
  "files.associations": {
    "*.m": "matlab"
  }
}
```

### Installation

```bash
cd matlab-lsp-vscode
npm install
npm run compile
vsce package
code --install-extension matlab-lsp-0.2.0.vsix
```

---

## Neovim

### Neovim 0.11+ (Recommended)

```lua
-- init.lua
vim.lsp.config('matlab_lsp', {
  cmd = { 'python', '-m', 'matlab_lsp', '--stdio' },
  filetypes = { 'matlab', 'm' },
  root_markers = { '.git', '.matlab-lsprc.json', 'project.m' },
  init_options = {
    matlabPath = "C:/Program Files/MATLAB/R2023b",
    maxDiagnostics = 100
  },
  settings = {
    matlab = {
      matlabPath = "C:/Program Files/MATLAB/R2023b",
      maxDiagnostics = 100
    }
  }
})

vim.lsp.enable('matlab_lsp')
```

### Legacy Neovim (lspconfig)

```lua
-- init.lua
local lspconfig = require('lspconfig')

lspconfig.matlab_lsp.setup {
  cmd = { 'python', '-m', 'matlab_lsp', '--stdio' },
  filetypes = { 'matlab', 'm' },
  root_dir = lspconfig.util.root_pattern('.git', '.matlab-lsprc.json'),
  init_options = {
    matlabPath = "C:/Program Files/MATLAB/R2023b",
    maxDiagnostics = 100
  }
}
```

### Verification

```bash
# Open a .m file
nvim test.m

# Check LSP status
:checkhealth lsp

# View server info
:LspInfo
```

---

## Vim

```vim
" .vimrc
autocmd BufRead,BufNewFile *.m set filetype=matlab

if executable('python')
  au User lsp_setup call lsp#register_server({
    \ 'name': 'matlab-lsp',
    \ 'cmd': {server_info->['python', '-m', 'matlab_lsp', '--stdio']},
    \ 'whitelist': ['matlab', 'm'],
    \ 'workspace_config': {
    \   'matlab': {
    \     'matlabPath': 'C:\\Program Files\\MATLAB\\R2023b',
    \     'maxDiagnostics': 100
    \   }
    \ }
    \ })
endif
```

---

## Emacs

### Basic Configuration

```elisp
;; init.el
(use-package lsp-mode
  :config
  (lsp-register-client
    (make-lsp-client
      :new-connection (lsp-stdio-connection '("python" "-m" "matlab_lsp" "--stdio"))
      :major-modes '(matlab-mode)
      :server-id 'matlab-lsp
      :initialization-options
      '((matlabPath . "C:/Program Files/MATLAB/R2023b")
        (maxDiagnostics . 100)))))

(use-package matlab-mode
  :after lsp-mode
  :config
  (add-hook 'matlab-mode-hook #'lsp))
```

### Extended Configuration

```elisp
;; init.el
(use-package lsp-mode
  :config
  (defcustom matlab-lsp-matlab-path ""
    "Path to MATLAB installation directory."
    :type 'string
    :group 'matlab-lsp)

  (defcustom matlab-lsp-max-diagnostics 100
    "Maximum number of diagnostics to report."
    :type 'integer
    :group 'matlab-lsp)

  (lsp-register-custom-settings
   '(("matlab.matlabPath" matlab-lsp-matlab-path)
     ("matlab.maxDiagnostics" matlab-lsp-max-diagnostics)))

  (lsp-register-client
    (make-lsp-client
      :new-connection (lsp-stdio-connection '("python" "-m" "matlab_lsp" "--stdio"))
      :major-modes '(matlab-mode)
      :server-id 'matlab-lsp
      :environment-fn (lambda ()
                        '(("MATLAB_PATH" . matlab-lsp-matlab-path)))
      :initialization-options (lambda ()
                           `((matlabPath . ,matlab-lsp-matlab-path)
                             (maxDiagnostics . ,matlab-lsp-max-diagnostics)))
      :initialized-fn (lambda (workspace)
                        (with-lsp-workspace workspace
                          (lsp--set-configuration
                           (lsp-configuration-section "matlab")))))))

(use-package matlab-mode
  :after lsp-mode
  :config
  (add-hook 'matlab-mode-hook #'lsp))
```

---

## Testing Integration

### Basic Test File

Create a test file `test_lsp.m`:

```matlab
function test_lsp()
    x = 10
    y = x + z  % Error: z undefined
    result = undefined_func(x)  % Error: function doesn't exist
end
```

### Expected Behavior

- **Diagnostics**: Errors should be underlined in red
- **Hover**: Positioning cursor over symbols should show information
- **Completion**: Typing should trigger suggestions (Ctrl+Space, Tab)
- **Definition**: `gd` (or equivalent) should navigate to definitions

### Testing in Different Editors

**OpenCode CLI:**
```bash
opencode test_lsp.m
```

**TUI Crush:**
```bash
crush
:e test_lsp.m
```

**Neovim:**
```bash
nvim test_lsp.m
```

**VS Code:**
```bash
code test_lsp.m
```

---

## Common Troubleshooting

### Server Won't Start

**Symptoms:**
- LSP client cannot connect to server
- Connection timeout errors

**Solutions:**

1. **Check Python path:**
   - Ensure Python is in PATH
   - Try full path: `C:/Python310/python.exe`

2. **Verify server installation:**
   ```bash
   pip install --upgrade matlab-lsp-server
   ```

3. **Test manually:**
   ```bash
   python -m matlab_lsp --tcp --port 4389 --verbose
   ```

4. **Check dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### MATLAB Not Found

**Symptoms:**
- Server warns about missing mlint
- Limited diagnostics available

**Solutions:**

1. **Configure MATLAB path:**
   - Via `init_options` in editor config
   - Via `.matlab-lsprc.json`
   - Via `MATLAB_PATH` environment variable

2. **Auto-discovery (v0.2.0+):**
   - Server automatically detects MATLAB in standard locations
   - No configuration needed for most setups

3. **Verify mlint exists:**
   ```bash
   # Windows
   dir "C:\Program Files\MATLAB\R2023b\bin\win64\mlint.exe"

   # Linux/Mac
   ls /usr/local/MATLAB/R2023b/bin/mlint
   ```

### Diagnostics Not Appearing

**Symptoms:**
- No error highlighting
- Completion not working

**Solutions:**

1. **Check file extension:**
   - Ensure files have `.m` extension
   - Verify filetype is recognized: `:set filetype?` (Vim/Neovim)

2. **Restart LSP:**
   - TUI Crush: `:LspRestart`
   - Neovim: `:LspRestart`
   - VS Code: Command Palette > Restart Language Server

3. **Enable debugging:**
   - Add `--verbose` flag to server arguments
   - Check editor's LSP logs

4. **Verify diagnostic rules:**
   ```json
   {
     "diagnosticRules": {
       "all": true
     }
   }
   ```

### Slow Performance

**Symptoms:**
- Delays when typing
- Lags when opening files

**Solutions:**

1. **Reduce diagnostics:**
   ```json
   {
     "maxDiagnostics": 50
   }
   ```

2. **Disable unnecessary rules:**
   ```json
   {
     "diagnosticRules": {
       "all": false,
       "unusedVariable": true,
       "undefinedFunction": true
     }
   }
   ```

3. **Increase cache:**
   ```json
   {
     "cache": {
       "maxSize": 2000
     }
   }
   ```

---

## Advanced Configuration

### Complete Configuration Options

The server supports the following configuration options. Settings can be provided via:
- LSP client `initializationOptions`
- `.matlab-lsprc.json` file
- Environment variables (prefix: `MATLAB_LSP_`)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| **matlabPath** | string | `""` | Path to MATLAB installation directory. Can be empty - server will auto-detect MATLAB. |
| **maxDiagnostics** | integer | `100` | Maximum number of diagnostics to report per file (range: 0-1000). |
| **diagnosticRules.all** | boolean | `true` | Enable all diagnostic rules. |
| **diagnosticRules.unusedVariable** | boolean | `true` | Check for unused variables. |
| **diagnosticRules.missingSemicolon** | boolean | `false` | Check for missing semicolons at end of statements. |
| **formatting.indentSize** | integer | `4` | Number of spaces to use for indentation. |
| **formatting.insertSpaces** | boolean | `true` | Use spaces for indentation (false = use tabs). |
| **completion.enableSnippets** | boolean | `true` | Enable code snippets in completion suggestions. |
| **completion.maxSuggestions** | integer | `50` | Maximum number of completion suggestions to provide. |
| **cache.enabled** | boolean | `true` | Enable in-memory caching for better performance. |
| **cache.maxSize** | integer | `1000` | Maximum number of entries in the cache. |

### Configuration Examples

**Minimal Configuration (auto-discovery):**
```json
{
  "matlabPath": ""
}
```
The server will automatically search for MATLAB in standard locations.

**Full Configuration:**
```json
{
  "matlabPath": "C:\\Program Files\\MATLAB\\R2023b",
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

### Detailed Option Descriptions

#### **matlabPath** (string)

Path to MATLAB installation directory. This is used to locate `mlint.exe` for static analysis.

**Behavior when empty:**
- Server starts normally without errors
- Basic LSP features work (completion, hover, go-to-definition, etc.)
- Diagnostics from MATLAB's mlint analyzer will be unavailable
- Server attempts to auto-discover MATLAB in standard locations

**Auto-discovery searches:**
1. System PATH (recursive search, including `bin/win64/`)
2. Windows: `C:/Program Files/MATLAB`, `D:/Program Files/MATLAB`, etc.
3. macOS: `/Applications/MATLAB_R*.app`
4. Linux: `/usr/local/MATLAB`, `/opt/MATLAB`, `~/MATLAB`

**Example values:**
- Windows: `"C:\\Program Files\\MATLAB\\R2023b"`
- macOS: `"/Applications/MATLAB_R2023b.app"`
- Linux: `"/usr/local/MATLAB/R2023b"`

#### **maxDiagnostics** (integer, 0-1000)

Maximum number of diagnostic messages to report for a single file.

**Use cases:**
- Set to `0` to disable diagnostics
- Lower values (10-50) for cleaner output
- Higher values (100-1000) for comprehensive analysis

#### **diagnosticRules** (object)

Fine-grained control over which diagnostic rules are enabled.

- **all** (boolean): Master switch for all diagnostic rules
- **unusedVariable** (boolean): Flag variables that are defined but never used
- **missingSemicolon** (boolean): Flag statements ending without semicolon

**Example:**
```json
{
  "diagnosticRules": {
    "all": false,
    "unusedVariable": true
  }
}
```
This enables only the unusedVariable check, disabling all other rules.

#### **formatting** (object)

Code formatting preferences.

- **indentSize** (integer): Number of characters per indentation level
- **insertSpaces** (boolean): `true` for spaces, `false` for tabs

**Example:**
```json
{
  "formatting": {
    "indentSize": 2,
    "insertSpaces": true
  }
}
```

#### **completion** (object)

Code completion behavior.

- **enableSnippets** (boolean): Include code snippets in completion suggestions
- **maxSuggestions** (integer): Maximum number of suggestions to show

**Example:**
```json
{
  "completion": {
    "enableSnippets": false,
    "maxSuggestions": 30
  }
}
```

#### **cache** (object)

Performance tuning via caching.

- **enabled** (boolean): Enable/disable in-memory caching
- **maxSize** (integer): Maximum number of cache entries (LRU eviction)

Caching improves performance for:
- Repeated symbol lookups
- File analysis
- Mlint results

### Environment Variables

You can configure the server using environment variables. All variables use the `MATLAB_LSP_` prefix.

| Environment Variable | Config Option | Example |
|-------------------|--------------|---------|
| `MATLAB_LSP_MATLAB_PATH` | `matlabPath` | `export MATLAB_LSP_MATLAB_PATH="/usr/local/MATLAB/R2023b"` |
| `MATLAB_LSP_MAX_DIAGNOSTICS` | `maxDiagnostics` | `export MATLAB_LSP_MAX_DIAGNOSTICS="50"` |
| `MATLAB_LSP_DIAGNOSTIC_RULES_ALL` | `diagnosticRules.all` | `export MATLAB_LSP_DIAGNOSTIC_RULES_ALL="true"` |

**Note:** Environment variables are case-insensitive and can use either underscores or hyphens.

### Monitoring and Debugging

**Enable verbose logging:**

```bash
# Command line
python -m matlab_lsp --stdio --verbose

# Environment variable (not yet implemented)
# export LSP_LOG_LEVEL="DEBUG"
```

**TCP mode for debugging:**

```bash
# Start server in TCP mode
python -m matlab_lsp --tcp --port 4389 --verbose

# Test with netcat (Windows: use telnet)
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | nc localhost 4389
```

---

## Additional Resources

### Documentation

- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [ARCHITECTURE.md](ARCHITECTURE.md) - Server architecture
- [DOCUMENTATION.md](DOCUMENTATION.md) - API documentation

### Editor Documentation

- [TUI Crush](https://charm.sh/crush/)
- [VS Code LSP](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide)
- [Neovim LSP](https://neovim.io/doc/user/lsp.html)
- [Emacs lsp-mode](https://emacs-lsp.github.io/lsp-mode/)

### Support

- **Issues**: [GitHub Issues](https://github.com/vmfuntikov/matlab-lsp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vmfuntikov/matlab-lsp-server/discussions)

---

## Tips for AI-Assisted Development

If you encounter integration issues, use MCP tools for assistance:

- **context7 MCP** - Up-to-date documentation for LSP clients
- **DuckDuckGo MCP** - Search for similar configurations
- **Filesystem MCP** - Verify project structure and paths

Example:
```
agent: "Generate optimal LSP configuration for MATLAB LSP Server in [editor name]"
```

---

**Happy coding with MATLAB LSP Server! 🎉**
