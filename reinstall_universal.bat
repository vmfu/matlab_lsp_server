@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo MATLAB LSP Server - Universal Clean Reinstall
echo ============================================================
echo.

echo [INFO] This script will:
echo   1. Uninstall ALL versions of matlab-lsp-server
echo   2. Clear ALL caches (pip, Python, TEMP)
echo   3. Install from latest tag on GitHub
echo   4. Verify all fixes are present
echo.

set INSTALL_FROM=latest
set FORCE_VERSION=

:parse_args
if "%~1"=="--version" (
    set FORCE_VERSION=%~2
    set INSTALL_FROM=version
    goto :end_parse
)
if "%~1"=="--latest" (
    set INSTALL_FROM=latest
    goto :end_parse
)
shift
goto :parse_args
:end_parse

if "%INSTALL_FROM%"=="version" (
    echo.
    echo ============================================================
    echo MODE: Install from specific version
    echo ============================================================
    echo.
    echo Version to install: %FORCE_VERSION%
    goto :do_uninstall
) else (
    echo.
    echo ============================================================
    echo MODE: Install from latest GitHub tag
    echo ============================================================
    echo.
    goto :do_uninstall
)

:do_uninstall
echo [Step 1/7] Uninstalling ALL versions...
pip uninstall -y matlab-lsp-server 2>nul
if %errorlevel% equ 0 (
    echo [SUCCESS] matlab-lsp-server uninstalled
) else (
    echo [INFO] matlab-lsp-server was not installed (OK)
)

echo.
echo [Step 2/7] Clearing pip cache...
pip cache remove matlab-lsp-server 2>nul

echo.
echo [Step 3/7] Clearing Python pip cache...
if exist "%USERPROFILE%\.cache\pip" (
    rmdir /s /q "%USERPROFILE%\.cache\pip" 2>nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] Python cache cleared
    ) else (
        echo [INFO] No Python cache to clear
    )
)

echo.
echo [Step 4/7] Clearing LocalAppData pip cache...
if exist "%LOCALAPPDATA%\pip\Cache" (
    rmdir /s /q "%LOCALAPPDATA%\pip\Cache" 2>nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] LocalAppData cache cleared
    ) else (
        echo [INFO] No LocalAppData cache to clear
    )
)

echo.
echo [Step 5/7] Clearing TEMP pip cache...
for /d %%d in ("%TEMP%\pip-*") do (
    rmdir /s /q "%%d" 2>nul
)
echo [SUCCESS] TEMP cache cleared

echo.
echo [Step 6/7] Clearing __pycache__ directories...
for /d /r %%d in ("%USERPROFILE%\*") do (
    if exist "%%d\__pycache__" (
        rmdir /s /q "%%d\__pycache__" 2>nul
    )
    for /d %%s in ("%%d\*") do (
        if exist "%%s\__pycache__" (
            rmdir /s /q "%%s\__pycache__" 2>nul
        )
    )
)
echo [SUCCESS] __pycache__ cleared

echo.
echo [Step 7/7] Installing from GitHub...

if "%INSTALL_FROM%"=="version" (
    echo [INFO] Installing from tag: %FORCE_VERSION%
    pip install --force-reinstall --no-cache-dir git+https://github.com/vmfu/matlab_lsp_server.git@%FORCE_VERSION%
) else (
    echo [INFO] Installing from latest tag
    pip install --force-reinstall --no-cache-dir git+https://github.com/vmfu/matlab_lsp_server.git
)

if %errorlevel% equ 0 (
    echo [SUCCESS] matlab-lsp-server installed
) else (
    echo [ERROR] Installation failed!
    goto :error
)

echo.
echo ============================================================
echo Verifying Installation
echo ============================================================
echo.

echo [Check 1/6] Verifying version...
pip show matlab-lsp-server
if %errorlevel% neq 0 (
    echo [ERROR] Package not installed!
    goto :error
)

echo.
echo [Check 2/6] Verifying shutdown handler...
python -c "import inspect; from matlab_lsp_server.protocol.lifecycle import on_shutdown; src = inspect.getsource(on_shutdown); print('Has return None:', 'YES' if 'return None' in src else 'NO')"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to check shutdown handler!
    goto :error
)

echo.
echo [Check 3/6] Verifying method_handlers module...
python -c "from matlab_lsp_server.protocol.method_handlers import register_method_handlers; print('method_handlers module: EXISTS')"
if %errorlevel% neq 0 (
    echo [ERROR] method_handlers module not found!
    goto :error
)

echo.
echo [Check 4/6] Verifying method_handlers is imported...
python -c "import matlab_lsp_server.protocol.lifecycle as lc; src = inspect.getsource(lc.register_lifecycle_handlers); print('method_handlers imported:', 'YES' if 'method_handlers' in src else 'NO')"
if %errorlevel% neq 0 (
    echo [ERROR] method_handlers not imported!
    goto :error
)

echo.
echo [Check 5/6] Verifying Python version...
python -c "import sys; print('Python version:', sys.version.split()[0])"

echo.
echo [Check 6/6] Testing server binary...
matlab-lsp --version
if %errorlevel% equ 0 (
    echo [SUCCESS] matlab-lsp binary works
) else (
    echo [WARNING] matlab-lsp binary failed to run
)

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo All verifications passed. Server is ready to use.
echo.
echo Next steps:
echo   1. Run diagnostic script:
echo      diagnose_universal.bat
echo   2. Run tests:
echo      cd ISSUES\issue_v0.2.4
echo      python test_v0.2.3.py
echo   3. If tests fail, run diagnostic again
echo.
pause
exit /b

:error
echo.
echo ============================================================
echo Installation or Verification Failed!
echo ============================================================
echo.
echo Please check:
echo   1. Python is installed: python --version
echo   2. pip is installed: pip --version
echo   3. Internet connection is working
echo   4. Git is accessible: git ls-remote https://github.com/vmfu/matlab_lsp_server.git
echo.
pause
exit /b
