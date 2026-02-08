# Release Instructions for v0.1.0

This document provides step-by-step instructions for completing the release of LSP MATLAB Server v0.1.0.

---

## Status

- [x] Git tag created: `v0.1.0`
- [x] All tests passing: 128/128
- [x] Code quality verified: black, isort, flake8, mypy
- [x] Documentation complete: README.md, INSTALL.md, CHANGELOG.md
- [ ] Pushed to remote repository
- [ ] GitHub Release created
- [ ] Published to PyPI (optional)

---

## Step 1: Configure and Push to Remote

### 1.1 Add Remote Repository (if not already configured)

```bash
# Replace with your GitHub repository URL
git remote add origin https://github.com/YOUR_USERNAME/matlab_lsp_server.git

# Or if using SSH
git remote add origin git@github.com:YOUR_USERNAME/matlab_lsp_server.git
```

### 1.2 Push to GitHub

```bash
# Push the master branch
git push origin master

# Push the release tag
git push origin v0.1.0
```

**Note:** If you get a "remote already exists" error:
```bash
# Update existing remote
git remote set-url origin https://github.com/YOUR_USERNAME/matlab_lsp_server.git
```

---

## Step 2: Create GitHub Release

### 2.1 Using GitHub Web Interface

1. Go to your repository on GitHub
2. Click **"Releases"** in the right sidebar
3. Click **"Create a new release"**
4. Select tag: `v0.1.0`
5. Release title: `v0.1.0 - Initial LSP MATLAB Server for Windows`
6. Description:

```markdown
## LSP MATLAB Server v0.1.0

### What's New

This is the initial stable release of LSP MATLAB Server for Windows - a lightweight, fast, and cross-platform Language Server Protocol implementation for MATLAB files.

### Features

- **Complete LSP Support**: All major LSP features implemented
  - Code completion
  - Hover information
  - Go-to-definition
  - Find all references
  - Document symbols
  - Diagnostics (via mlint integration)
  - Code actions
  - Code formatting
  - Workspace symbols

- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Lightweight**: Fast startup with minimal resource usage (~50MB RAM)
- **Customizable**: Configurable via `.matlab-lsprc.json`
- **Quality Assured**: 128 tests passing, 73% coverage, all code quality checks pass

### Installation

**Quick Install:**
```bash
pip install matlab-lsp-server
```

For detailed installation instructions, see [INSTALL.md](https://github.com/YOUR_USERNAME/matlab_lsp_server/blob/master/INSTALL.md)

### Why This Over Official MathWorks LSP?

- ✅ **Lightweight**: No Java dependency, ~50MB RAM vs 500MB+
- ✅ **Fast Startup**: ~1 second startup vs 10+ seconds
- ✅ **Cross-Platform**: Native support for Windows, Linux, macOS
- ✅ **Simple Configuration**: Single JSON file vs complex XML configs
- ✅ **MIT Licensed**: Open source and free to use

### Quick Start

After installation, configure your LSP client (e.g., TUI Crush, VS Code, Neovim):

**TUI Crush (`.crush.json`):**
```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["-m", "matlab_lsp", "--stdio"],
      "filetypes": ["matlab", "m"]
    }
  }
}
```

**VS Code (`.vscode/settings.json`):**
```json
{
  "matlab.lsp.serverPath": "matlab-lsp"
}
```

### Documentation

- [README](https://github.com/YOUR_USERNAME/matlab_lsp_server/blob/master/README.md) - Main documentation
- [INSTALL.md](https://github.com/YOUR_USERNAME/matlab_lsp_server/blob/master/INSTALL.md) - Installation guide
- [CHANGELOG.md](https://github.com/YOUR_USERNAME/matlab_lsp_server/blob/master/CHANGELOG.md) - Version history
- [CONTRIBUTING.md](https://github.com/YOUR_USERNAME/matlab_lsp_server/blob/master/CONTRIBUTING.md) - Contributing guidelines

### Known Limitations

- MATLAB R2020b or later required for full mlint diagnostics support
- Standalone analyzer has limited features without MATLAB

### Support

- Report bugs: [GitHub Issues](https://github.com/YOUR_USERNAME/matlab_lsp_server/issues)
- Feature requests: [GitHub Discussions](https://github.com/YOUR_USERNAME/matlab_lsp_server/discussions)
- Documentation: [Project Wiki](https://github.com/YOUR_USERNAME/matlab_lsp_server/wiki)

### License

MIT License - see [LICENSE](https://github.com/YOUR_USERNAME/matlab_lsp_server/blob/master/LICENSE) file

---

**Thank you for using LSP MATLAB Server!**
```

7. Set as a pre-release: ❌ (this is a stable release)
8. Click **"Publish release"**

### 2.2 Using GitHub CLI (Alternative)

```bash
# Install GitHub CLI first: https://cli.github.com/
gh release create v0.1.0 \
  --title "v0.1.0 - Initial LSP MATLAB Server for Windows" \
  --notes-file RELEASE_NOTES.md
```

---

## Step 3: Build and Publish to PyPI (Optional)

### 3.1 Build Source Distribution

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Output will be in dist/ directory:
# dist/matlab_lsp_server-0.1.0.tar.gz
# dist/matlab_lsp_server-0.1.0-py3-none-any.whl
```

### 3.2 Test on TestPyPI First

```bash
# Register on TestPyPI: https://test.pypi.org/account/register/
twine check dist/*
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple matlab-lsp-server
```

### 3.3 Publish to PyPI

```bash
# Register on PyPI: https://pypi.org/account/register/
twine upload dist/*

# Verify installation
pip install matlab-lsp-server
```

### 3.4 Post-Publish Verification

1. Go to https://pypi.org/project/matlab-lsp-server/
2. Verify package information is correct
3. Check that installation works: `pip install matlab-lsp-server`

---

## Verification Checklist

After completing all steps, verify:

- [ ] Tag `v0.1.0` is visible on GitHub: `https://github.com/YOUR_USERNAME/matlab_lsp_server/tags`
- [ ] Release is visible on GitHub: `https://github.com/YOUR_USERNAME/matlab_lsp_server/releases`
- [ ] Package can be installed: `pip install matlab-lsp-server`
- [ ] Server runs correctly: `matlab-lsp --version`
- [ ] Documentation links in release notes work correctly

---

## Common Issues and Solutions

### Issue: "remote already exists"

```bash
# View existing remote
git remote -v

# Update remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/matlab_lsp_server.git
```

### Issue: "failed to push some refs"

```bash
# Pull remote changes first
git pull origin master --rebase
git push origin master
```

### Issue: "403 Forbidden" when pushing to PyPI

- Verify PyPI username/password
- Use API token instead of password (recommended)
- Enable 2FA on PyPI account

### Issue: "Package name already exists on PyPI"

- Choose a different package name in `pyproject.toml`
- Update all documentation to use the new name

---

## Post-Release Tasks

1. **Announce the Release:**
   - Twitter/X
   - Reddit (r/matlab, r/programming)
   - MATLAB Central
   - Relevant forums and communities

2. **Monitor for Issues:**
   - Respond to GitHub Issues quickly
   - Fix critical bugs promptly

3. **Plan Next Release:**
   - Gather user feedback
   - Update CHANGELOG.md for next version
   - Start working on v0.2.0 features

---

## Notes

- This is the **v0.1.0 initial release**
- Package name on PyPI: `matlab-lsp-server`
- Version: `0.1.0`
- License: MIT

---

**Congratulations on releasing v0.1.0! 🎉**
