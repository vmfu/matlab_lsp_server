# MATLAB LSP Server - Universal Diagnostic & Reinstall Scripts

## Quick Start

### For Clean Installation

```bash
# 1. Run universal reinstall (installs latest v0.2.4)
reinstall_universal.bat

# 2. Run diagnostics to verify installation
diagnose_universal.bat

# 3. Run tests
cd ISSUES\issue_v0.2.4
python test_v0.2.3.py
```

### For Specific Version

```bash
# Install specific version (e.g., v0.2.4)
reinstall_universal.bat --version v0.2.4

# Verify installation
diagnose_universal.bat
```

---

## Scripts Overview

### 1. `diagnose_universal.bat` - Universal Diagnostic Script

**Purpose:** Automatically diagnose installation and verify all bug fixes are present.

**What it checks:**
- ✅ Which version is installed
- ✅ Python location and version
- ✅ Whether in virtual environment
- ✅ Module file location
- ✅ If `return None` is present in shutdown handler
- ✅ If `method_handlers` module exists
- ✅ If `method_handlers` is imported in lifecycle
- ✅ Latest tag version
- ✅ Server binary startup

**Output:**
- Clear PASS/FAIL for each check
- Installed version detected automatically
- Latest tag version detected automatically
- Guidance on next steps

**Usage:**
```bash
diagnose_universal.bat
```

---

### 2. `reinstall_universal.bat` - Universal Clean Reinstall Script

**Purpose:** Clean install MATLAB LSP Server from GitHub, removing all traces of old installations.

**What it does:**
- ✅ Uninstalls ALL versions of matlab-lsp-server
- ✅ Clears pip cache
- ✅ Clears Python cache (~/.cache/pip)
- ✅ Clears LocalAppData cache
- ✅ Clears TEMP cache
- ✅ Removes old site-packages
- ✅ Clears ALL __pycache__ directories
- ✅ Installs from GitHub (latest or specific version)
- ✅ Verifies installation (version, return None, method_handlers)
- ✅ Tests server binary

**Modes:**

#### Mode 1: Install Latest Tag (Default)
```bash
reinstall_universal.bat

# OR explicitly:
reinstall_universal.bat --latest
```

Installs from latest GitHub tag.

#### Mode 2: Install Specific Version
```bash
# Install specific version
reinstall_universal.bat --version v0.2.4
```

Installs from specific tag.

**Usage Examples:**
```bash
# Install latest version
reinstall_universal.bat

# Install specific version
reinstall_universal.bat --version v0.2.4

# Install development version (from master)
reinstall_universal.bat --version master
```

---

## Troubleshooting

### Problem: Diagnostics Show Fixes Present, But Tests Still Fail

**Cause:** Python or pip cache contains old code.

**Solution:**
```bash
# Reinstall with universal script
reinstall_universal.bat

# Then run diagnostics again
diagnose_universal.bat
```

---

### Problem: "ModuleNotFoundError" or "ImportError"

**Cause:** Old installation remnants or corrupted cache.

**Solution:**
```bash
# Use universal reinstall (clears ALL caches)
reinstall_universal.bat --version v0.2.4
```

---

### Problem: "File already exists" on PyPI

**Cause:** Trying to publish version that's already on PyPI.

**Solution:**
- Use `reinstall_universal.bat --version v0.2.4` to test
- Publish newer version (e.g., v0.2.5) to PyPI
- DO NOT republish v0.2.3 to PyPI

---

### Problem: Version Mismatch

**Symptom:**
- `pip show` shows v0.2.3
- Code still shows v0.2.2

**Cause:** Python cache not cleared properly.

**Solution:**
```bash
# Use universal reinstall (clears ALL caches)
reinstall_universal.bat --version v0.2.4

# Verify with diagnostics
diagnose_universal.bat
```

---

## Verification Checklist

After running `reinstall_universal.bat`, verify with `diagnose_universal.bat`:

- [ ] Installed version is correct (e.g., 0.2.4)
- [ ] Python version meets requirements (3.10+)
- [ ] Module location is correct
- [ ] Shutdown handler has `return None`
- [ ] `method_handlers` module exists
- [ ] `method_handlers` is imported in lifecycle
- [ ] Server binary runs (`matlab-lsp --version`)
- [ ] All 6 tests pass

---

## Scripts Comparison

### Old Scripts (DEPRECATED)

| Script | Issues |
|---------|---------|
| `clean_reinstall_v0.2.3.bat` | Only for v0.2.3, no auto-detection |
| `diagnose_v0.2.3.bat` | Only for v0.2.3, hardcoded version |

### New Universal Scripts (RECOMMENDED)

| Script | Advantages |
|---------|------------|
| `diagnose_universal.bat` | Auto-detects version, comprehensive checks, flexible |
| `reinstall_universal.bat` | Works with any version, clears ALL caches, multiple modes |

---

## Advanced Usage

### Install from Specific Branch/Commit

```bash
# Install from specific branch
reinstall_universal.bat --version main

# Install from specific commit
reinstall_universal.bat --version a01ce27
```

### Debug Installation Issues

1. Run diagnostics:
```bash
diagnose_universal.bat
```

2. Check output for:
- Version mismatch
- Missing fixes
- Cache issues

3. If issues found, run clean reinstall:
```bash
reinstall_universal.bat --version v0.2.4
```

---

## Notes

### Why Universal Scripts?

**Old Scripts:**
- ❌ Hardcoded version numbers
- ❌ Only work for specific version
- ❌ Limited diagnostics
- ❌ No auto-detection

**Universal Scripts:**
- ✅ Auto-detect installed version
- ✅ Work with any version
- ✅ Comprehensive diagnostics
- ✅ Multiple installation modes
- ✅ Clear caching instructions

### Cache Management

Universal scripts clear:
- ✅ pip cache
- ✅ Python cache (~/.cache/pip)
- ✅ LocalAppData cache
- ✅ TEMP cache
- ✅ All __pycache__ directories
- ✅ Old site-packages

This ensures clean installation every time.

---

## Version Information

- **Current Release:** v0.2.4
- **Latest Tag:** Automatically detected
- **PyPI Status:** v0.2.3 published, v0.2.4 pending
- **GitHub:** https://github.com/vmfu/matlab_lsp_server

---

## Support

If issues persist after using universal scripts:

1. Check Python installation:
   ```bash
   python --version
   # Should be 3.10+
   ```

2. Check pip installation:
   ```bash
   pip --version
   ```

3. Check internet connection:
   ```bash
   git ls-remote https://github.com/vmfu/matlab_lsp_server.git
   ```

4. Create GitHub issue with:
   - Diagnostic output from `diagnose_universal.bat`
   - Test results from `ISSUES/issue_v0.2.4/test_v0.2.3.py`
   - Python and pip versions
   - Operating system

---

**For the latest version and updates, visit:**
https://github.com/vmfu/matlab_lsp_server/releases
