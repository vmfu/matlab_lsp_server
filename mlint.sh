#!/usr/bin/env bash
# MATLAB Lint Script
# Run mlint on all .m files in the current directory

MATLAB_PATH="/c/Program Files/MATLAB/R2023b/bin/win64/mlint.exe"

if [ ! -f "$MATLAB_PATH" ]; then
    echo "Error: mlint.exe not found at $MATLAB_PATH"
    exit 1
fi

if [ $# -eq 0 ]; then
    # Run on all .m files
    for file in *.m; do
        if [ -f "$file" ]; then
            echo "=== $file ==="
            "$MATLAB_PATH" "$file" -id -severity -fix 2>&1
            echo ""
        fi
    done
else
    # Run on specific files
    for file in "$@"; do
        if [ -f "$file" ]; then
            echo "=== $file ==="
            "$MATLAB_PATH" "$file" -id -severity -fix 2>&1
            echo ""
        else
            echo "Error: File not found: $file"
        fi
    done
fi
