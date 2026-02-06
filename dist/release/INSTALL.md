# LSP MATLAB Server - Installation Guide

Guide for installing and running LSP MATLAB Server.

## Installation

### Option 1: Install from Source

```bash
git clone https://github.com/yourusername/lsp_matlab_for_windows.git
cd lsp_matlab_for_windows
pip install -r requirements.txt
```

### Option 2: Install from Release

```bash
# Download release
cd dist/release

# Install dependencies
pip install -r requirements.txt

# Verify installation
python run_server.py --version
```

## Running the Server

### From Source Directory

```bash
# Install in development mode
pip install -e .

# Run server
python -m src.server --stdio
```

### From Release Directory

```bash
cd dist/release

# Run server
python run_server.py --stdio
```

## Configuration

### VS Code Integration

Create `.vscode/settings.json`:

```json
{
  "matlab.lsp.path": "python",
  "matlab.lsp.args": ["run_server.py", "--stdio"]
}
```

### JetBrains Integration

Configure in Settings > Languages & Frameworks > MATLAB:

- **Language Server**: Custom
- **Server path**: `python`
- **Arguments**: `run_server.py --stdio`

### Command Line Options

```bash
# Standard I/O mode (recommended for IDEs)
python run_server.py --stdio

# TCP mode (for testing)
python run_server.py --tcp 5050

# Help
python run_server.py --help
```

## Troubleshooting

### Import Errors

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```

### Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Check versions
pip list
```

## System Requirements

- Python 3.10+
- 4GB RAM recommended
- Network connection (for remote LSP)

## Directory Structure (Release)

```
dist/release/
├── src/                    # Source code
├── run_server.py           # Server launcher
├── requirements.txt          # Dependencies
├── README.md              # Project overview
├── CHANGELOG.md           # Version history
├── ARCHITECTURE.md        # Design docs
├── DEVELOPMENT.md         # Development guide
├── TODO.md                # Development tasks
├── .pre-commit-config.yaml # Pre-commit hooks
└── pyproject.toml         # Project config
```

## Verification

### Check Installation

```bash
python -c "import src.server; print('Installation successful')"
```

### Run Tests

```bash
cd dist/release
python -m pytest --version
```

### Start Server

```bash
cd dist/release
python run_server.py --stdio
```

## License

MIT License - See LICENSE file for details.
