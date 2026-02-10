@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Clean Reinstall MATLAB LSP Server v0.2.4
echo ============================================================
echo.

echo Step 1: Uninstall ALL versions...
pip uninstall -y matlab-lsp-server
if %errorlevel% equ 0 (
    echo [SUCCESS] matlab-lsp-server uninstalled
) else (
    echo [WARNING] matlab-lsp-server was not installed (OK)
)

echo.
echo Step 2: Clear pip cache...
pip cache remove matlab-lsp-server

echo.
echo Step 3: Clear Python pip cache...
if exist "%USERPROFILE%\.cache\pip" (
    rmdir /s /q "%USERPROFILE%\.cache\pip\matlab-lsp-server*" 2>nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] Python cache cleared
    ) else (
        echo [INFO] No matlab-lsp-server cache to clear
    )
)

echo.
echo Step 4: Clear LocalAppData pip cache...
if exist "%LOCALAPPDATA%\pip\Cache" (
    rmdir /s /q "%LOCALAPPDATA%\pip\Cache\*matlab-lsp-server*" 2>nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] LocalAppData cache cleared
    ) else (
        echo [INFO] No LocalAppData cache to clear
    )
)

echo.
echo Step 5: Clear TEMP pip cache...
for /d %%d in ("%TEMP%\pip-*") do (
    rmdir /s /q "%%d\matlab-lsp-server*" 2>nul
)

echo.
echo Step 6: Remove site-packages...
if exist "%USERPROFILE%\.local\lib\python*\site-packages\matlab_lsp_server*" (
    rmdir /s /q "%USERPROFILE%\.local\lib\python*\site-packages\matlab_lsp_server*" 2>nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] Old site-packages removed
    ) else (
        echo [WARNING] Could not remove site-packages
    )
)

echo.
echo Step 7: Install from GitHub tag v0.2.4...
pip install --force-reinstall --no-cache-dir git+https://github.com/vmfu/matlab_lsp_server.git@v0.2.4

if %errorlevel% equ 0 (
    echo [SUCCESS] matlab-lsp-server v0.2.4 installed
) else (
    echo [ERROR] Installation failed!
    goto :error
)

echo.
echo Step 8: Verify installation...
pip show matlab-lsp-server

echo.
echo Step 9: Check version...
python -c "import matlab_lsp_server; print('Module version:', matlab_lsp_server.__version__)"

echo.
echo Step 10: Check if shutdown handler has return None...
python -c "import inspect; from matlab_lsp_server.protocol.lifecycle import on_shutdown; src = inspect.getsource(on_shutdown); print('Has return None:', 'YES' if 'return None' in src else 'NO')"

echo.
echo Step 11: Check if method_handlers exists...
python -c "from matlab_lsp_server.protocol import method_handlers; print('method_handlers module:', 'EXISTS' if method_handlers else 'NOT FOUND')"

echo.
echo Step 12: Check if method_handlers is imported...
python -c "from matlab_lsp_server.protocol import lifecycle; import inspect; src = inspect.getsource(lifecycle.register_lifecycle_handlers); print('method_handlers imported:', 'YES' if 'method_handlers' in src else 'NO')"

echo.
echo Step 13: Test server startup...
matlab-lsp --version

echo.
echo ============================================================
echo Installation complete!
echo ============================================================
echo.
echo Next steps:
echo 1. cd ISSUES/issue_v0.2.4
echo 2. python test_v0.2.3.py
echo 3. Check if document symbols and shutdown work
echo 4. If tests pass, report back!
echo.
pause
exit /b

:error
echo.
echo ============================================================
echo Installation failed!
echo ============================================================
echo.
echo Please check:
echo 1. Python is installed: python --version
echo 2. pip is installed: pip --version
echo 3. Internet connection to GitHub
echo 4. Git is installed: git --version
echo.
pause
exit /b
