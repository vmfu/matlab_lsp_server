@echo off
echo.
echo ============================================================
echo Clean Reinstall MATLAB LSP Server v0.2.3
echo ============================================================
echo.

echo Step 1: Uninstall old versions...
pip uninstall -y matlab-lsp-server

echo.
echo Step 2: Clear pip cache...
pip cache remove matlab-lsp-server

echo.
echo Step 3: Clear Python cache...
if exist "%LOCALAPPDATA%\pip\Cache" (
    del /Q "%LOCALAPPDATA%\pip\Cache\*matlab-lsp-server*" 2>nul
)

echo.
echo Step 4: Install from GitHub master...
pip install --force-reinstall git+https://github.com/vmfu/matlab_lsp_server.git

echo.
echo Step 5: Verify installation...
pip show matlab-lsp-server

echo.
echo Step 6: Check if fixes are present...
python -c "from matlab_lsp_server.protocol import lifecycle; import inspect; print(inspect.getsource(lifecycle.register_lifecycle_handlers))" | findstr /C:"return None" >nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Return None found in shutdown handler!
) else (
    echo [WARNING] Return None NOT found - bug may not be fixed
)

python -c "from matlab_lsp_server.protocol import method_handlers; print('method_handlers module:', 'EXISTS' if method_handlers else 'NOT FOUND')"

echo.
echo ============================================================
echo Installation complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Run: python ISSUES/issue_v0.2.3/test_v0.2.3.py
echo 2. Check if document symbols and shutdown work
echo 3. If still failing, check if code matches tag v0.2.3
echo.
pause
