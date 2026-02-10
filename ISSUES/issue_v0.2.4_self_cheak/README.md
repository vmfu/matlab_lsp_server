# MATLAB LSP Server v0.2.4 Testing Instructions

## Quick Test

### 1. Clean Reinstall

Run the diagnostic script first:
```bash
diagnose_v0.2.3.bat
```

This will check:
- Which version is installed
- If Python is in virtual environment
- Which module location is being used
- If `return None` is present in shutdown handler
- If `method_handlers` module exists and is imported

### 2. Force Reinstall (if needed)

If diagnostics show issues, run clean reinstall:
```bash
clean_reinstall_v0.2.3.bat
```

This will:
- Uninstall old versions
- Clear pip cache
- Clear Python cache
- Reinstall from GitHub master
- Verify installation

### 3. Run Tests

After clean reinstall, run:
```bash
cd ISSUES/issue_v0.2.4
python test_v0.2.3.py
```

Expected results:
- ✅ Initialize - PASS
- ✅ Open Document - PASS
- ✅ Document Symbols - PASS (should work now)
- ✅ Completion - PASS
- ✅ Hover - PASS
- ✅ Shutdown - PASS (should work now)

## Verification

### Check Code Matches Tag

Verify that installed code matches tag v0.2.4:
```bash
# Check version
pip show matlab-lsp-server

# Check if fixes are present
python -c "from matlab_lsp_server.protocol.lifecycle import on_shutdown; import inspect; src = inspect.getsource(on_shutdown); print('Has return None:', 'YES' if 'return None' in src else 'NO')"

# Check if method_handlers exists
python -c "from matlab_lsp_server.protocol import method_handlers; print('method_handlers exists:', 'YES' if method_handlers else 'NO')"

# Check if method_handlers is imported
python -c "from matlab_lsp_server.protocol import lifecycle; import inspect; src = inspect.getsource(lifecycle.register_lifecycle_handlers); print('method_handlers imported:', 'YES' if 'method_handlers' in src else 'NO')"
```

## Known Issues

If tests still fail after clean reinstall:

### Issue 1: Python Cache
**Symptom:** Diagnostics show correct code, but tests fail
**Solution:**
```bash
# Clear all caches
rmdir /s /q "%USERPROFILE%\.cache\pip"
rmdir /s /q "%LOCALAPPDATA%\pip\Cache"
rmdir /s /q "%TEMP%\pip-*"
```

### Issue 2: Multiple Installations
**Symptom:** `pip show` shows multiple versions
**Solution:**
```bash
# Uninstall all
pip uninstall -y matlab-lsp-server

# Check remaining files
dir "%USERPROFILE%\.local\lib\python*\site-packages\matlab*"

# Delete manually if any remain
rmdir /s /q "%USERPROFILE%\.local\lib\python*\site-packages\matlab*"
```

### Issue 3: Virtual Environment Issues
**Symptom:** Global Python used instead of venv
**Solution:**
```bash
# Deactivate current venv
deactivate

# Recreate venv
python -m venv venv
venv\Scripts\activate

# Reinstall
pip install git+https://github.com/vmfu/matlab_lsp_server.git
```

## Expected Results

### v0.2.4 vs v0.2.3

| Test | v0.2.3 | v0.2.4 |
|-------|---------|---------|
| Initialize | ✅ PASS | ✅ PASS |
| Open Document | ✅ PASS | ✅ PASS |
| Document Symbols | ❌ FAIL | ✅ PASS |
| Completion | ✅ PASS | ✅ PASS |
| Hover | ✅ PASS | ✅ PASS |
| Shutdown | ❌ FAIL | ✅ PASS |

**Expected:** All 6 tests PASS (100%)

## What Changed in v0.2.4

### Code
- ✅ `src/matlab_lsp_server/protocol/lifecycle.py` - Added `return None`
- ✅ `src/matlab_lsp_server/protocol/method_handlers.py` - Registers all LSP handlers

### Documentation
- ✅ All configurations updated to use `matlab-lsp` command
- ✅ Version numbers updated to v0.2.4

## Next Steps

1. Run `diagnose_v0.2.3.bat`
2. Run `clean_reinstall_v0.2.3.bat` if needed
3. Run tests with `python ISSUES/issue_v0.2.4/test_v0.2.3.py`
4. Report results

## Testing Checklist

- [ ] Diagnostics run
- [ ] Clean reinstall performed (if needed)
- [ ] Version verified as 0.2.4
- [ ] `return None` confirmed in shutdown handler
- [ ] `method_handlers` confirmed as registered
- [ ] All 6 tests pass
- [ ] Document symbols work
- [ ] Shutdown works cleanly
- [ ] No timeouts

---

**Note:** v0.2.4 includes ALL bug fixes and documentation updates. If issues persist, they may be deeper than expected or require additional investigation.
