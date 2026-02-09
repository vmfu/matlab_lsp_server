@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo MATLAB LSP Server v0.2.3 - Diagnostic Script
echo ============================================================
echo.

echo Step 1: Check current installation...
pip show matlab-lsp-server
if %errorlevel% neq 0 (
    echo [ERROR] matlab-lsp-server not installed!
    goto :error
)

echo.
echo Step 2: Check Python location...
where python

echo.
echo Step 3: Check if using virtual environment...
python -c "import sys; print('Virtual env:', sys.prefix != sys.base_prefix)"

echo.
echo Step 4: Check which module is imported...
python -c "import matlab_lsp_server.protocol.lifecycle as lc; print('Module location:', lc.__file__)"

echo.
echo Step 5: Check if shutdown handler has return None...
python -c "import inspect; from matlab_lsp_server.protocol.lifecycle import on_shutdown; src = inspect.getsource(on_shutdown); print('Has return None:', 'YES' if 'return None' in src else 'NO')"

echo.
echo Step 6: Check if method_handlers exists...
python -c "import matlab_lsp_server.protocol.method_handlers as mh; print('method_handlers exists:', 'YES' if mh else 'NO')"

echo.
echo Step 7: Check if method_handlers is imported in lifecycle.py...
python -c "import matlab_lsp_server.protocol.lifecycle as lc; src = inspect.getsource(lc); print('method_handlers imported:', 'YES' if 'from . import method_handlers' in src else 'NO')"

echo.
echo Step 8: Check version numbers...
python -c "import matlab_lsp_server; print('Module version:', matlab_lsp_server.__version__)"
python -c "import sys; print('Python version:', sys.version.split()[0])"

echo.
echo Step 9: Check if server binary matches...
matlab-lsp --version

echo.
echo ============================================================
echo Diagnostic complete!
echo ============================================================
echo.
echo If return None is YES and method_handlers is YES:
echo   but tests still fail, it may be a caching issue.
echo.
echo Try:
echo   1. Delete: %USERPROFILE%\.cache\pip\*matlab-lsp-server*
echo   2. Delete: %LOCALAPPDATA%\pip\Cache\*matlab-lsp-server*
echo   3. Delete: %USERPROFILE%\.local\pip\cache\*matlab-lsp-server*
echo.
pause
exit /b

:error
echo.
echo ============================================================
echo Installation check failed!
echo ============================================================
echo.
echo Please install the server first:
echo   pip install git+https://github.com/vmfu/matlab_lsp_server.git
echo.
pause
exit /b
