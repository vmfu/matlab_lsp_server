@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo MATLAB LSP Server - Universal Diagnostic Script
echo ============================================================
echo.

echo [Step 1/10] Checking installation...
pip show matlab-lsp-server
if %errorlevel% neq 0 (
    echo [ERROR] matlab-lsp-server not installed!
    echo.
    echo Please install first:
    echo   pip install git+https://github.com/vmfu/matlab_lsp_server.git
    echo.
    goto :error
)

echo.
echo [Step 2/10] Getting installed version...
for /f "tokens=2 delims= " %%v in ('pip show matlab-lsp-server ^| findstr /C:"Version:"') do (
    set INSTALLED_VERSION=%%v
)
echo Installed version: %INSTALLED_VERSION%

echo.
echo [Step 3/10] Checking Python environment...
python -c "import sys; print('Python location:', sys.executable)"
python -c "import sys; print('Virtual env:', 'YES' if sys.prefix != sys.base_prefix else 'NO')"

echo.
echo [Step 4/10] Checking module location...
python -c "import matlab_lsp_server.protocol.lifecycle as lc; print('Module file:', lc.__file__)"

echo.
echo [Step 5/10] Checking if shutdown handler has return None...
python -c "import inspect; from matlab_lsp_server.protocol.lifecycle import on_shutdown; src = inspect.getsource(on_shutdown); print('Has return None:', 'YES' if 'return None' in src else 'NO')" > result.txt
set /p RETURN_NONE=<result.txt
echo [Result] Shutdown handler has return None: %RETURN_NONE%

echo.
echo [Step 6/10] Checking if method_handlers module exists...
python -c "import matlab_lsp_server.protocol.method_handlers as mh; print('method_handlers module:', 'EXISTS' if mh else 'NOT FOUND')" > result.txt
set /p METHOD_HANDLER=<result.txt
echo [Result] Method handlers module: %METHOD_HANDLER%

echo.
echo [Step 7/10] Checking if method_handlers is imported...
python -c "import matlab_lsp_server.protocol.lifecycle as lc; src = inspect.getsource(lc); print('method_handlers imported:', 'YES' if 'from . import method_handlers' in src else 'NO')" > result.txt
set /p METHOD_HANDLER_IMPORTED=<result.txt
echo [Result] Method handlers imported: %METHOD_HANDLER_IMPORTED%

echo.
echo [Step 8/10] Checking latest tag version...
for /f "tokens=*" %%t in ('git tag -l "v*" ^| sort -V ^| tail -1') do (
    set LATEST_TAG=%%t
)
echo Latest tag: %LATEST_TAG%

echo.
echo [Step 9/10] Checking version numbers...
python -c "import matlab_lsp_server; print('Module version:', matlab_lsp_server.__version__)"
python -c "import sys; print('Python version:', sys.version.split()[0])"

echo.
echo [Step 10/10] Testing server binary...
matlab-lsp --version
if %errorlevel% equ 0 (
    echo [OK] matlab-lsp binary works
) else (
    echo [WARNING] matlab-lsp binary failed to run
)

echo.
del result.txt
echo ============================================================
echo Diagnostic Summary
echo ============================================================
echo.
echo Installed Version: %INSTALLED_VERSION%
echo Latest Tag:      %LATEST_TAG%
echo Shutdown Fixed:   %RETURN_NONE%
echo Handlers Exists:  %METHOD_HANDLER%
echo Handlers Imported: %METHOD_HANDLER_IMPORTED%
echo.

if "%RETURN_NONE%"=="YES" (
    if "%METHOD_HANDLER_IMPORTED%"=="YES" (
        echo [STATUS] All fixes are present in installed code!
        echo.
        echo If tests are still failing:
        echo   1. This may be a caching issue
        echo   2. Clear Python and pip caches
        echo   3. Reinstall with --force-reinstall
        echo.
        goto :cache_notice
    ) else (
        echo [WARNING] method_handlers exists but not imported!
        echo.
        echo This means fixes are incomplete.
        echo.
        goto :fix_needed
    )
) else (
    echo [WARNING] Shutdown handler does NOT have return None!
    echo.
    echo This means fixes are NOT present.
    echo.
    goto :fix_needed
)

:fix_needed
echo [ACTION] Fixes are NOT present in installed code.
echo.
echo Recommended actions:
echo   1. Update to latest version:
echo      pip install --upgrade git+https://github.com/vmfu/matlab_lsp_server.git
echo   2. Or clean reinstall from specific tag:
echo      pip install --force-reinstall --no-cache-dir git+https://github.com/vmfu/matlab_lsp_server.git@v0.2.4
echo.
echo.
echo After reinstalling, run this diagnostic script again to verify.
pause
exit /b

:cache_notice
echo [STATUS] All fixes present but tests may still fail.
echo.
echo This is likely a caching issue.
echo.
echo Try these steps in order:
echo   1. Clear pip cache:
echo      pip cache remove matlab-lsp-server
echo   2. Clear Python __pycache__:
echo      for /d /r %%d in (%%USERPROFILE%%\*) do @if exist "%%d\__pycache__" rmdir /s /q "%%d\__pycache__"
echo   3. Clear local pip cache:
echo      if exist "%%LOCALAPPDATA%%\pip\Cache" rmdir /s /q "%%LOCALAPPDATA%%\pip\Cache"
echo   4. Reinstall with --force-reinstall:
echo      pip install --force-reinstall --no-cache-dir git+https://github.com/vmfu/matlab_lsp_server.git
echo.
pause
exit /b

:error
echo.
echo ============================================================
echo Installation check failed!
echo ============================================================
echo.
pause
exit /b
