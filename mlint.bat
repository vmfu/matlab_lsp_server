@echo off
REM MATLAB Lint Script for Windows
REM Run mlint on all .m files in the current directory

set MATLAB_PATH=C:\Program Files\MATLAB\R2023b\bin\win64\mlint.exe

if not exist "%MATLAB_PATH%" (
    echo Error: mlint.exe not found at %MATLAB_PATH%
    exit /b 1
)

if "%~1"=="" (
    REM Run on all .m files
    for %%f in (*.m) do (
        echo === %%f ===
        "%MATLAB_PATH%" "%%f" -id -severity -fix 2>&1
        echo.
    )
) else (
    REM Run on specified files
    for %%f in (%*) do (
        if exist "%%f" (
            echo === %%f ===
            "%MATLAB_PATH%" "%%f" -id -severity -fix 2>&1
            echo.
        ) else (
            echo Error: File not found: %%f
        )
    )
)
