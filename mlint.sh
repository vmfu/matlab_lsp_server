#!/usr/bin/env bash
# MATLAB Lint Script
# Run mlint on all .m files in current directory

# Search for mlint in common locations
if [ "$(uname)" = "Darwin" ]; then
    # macOS
    MATLAB_PATH=$(find /Applications -name "mlint" 2>/dev/null | head -n 1)
elif [ "$(uname)" = "Linux" ]; then
    # Linux
    MATLAB_PATH=$(which mlint)
    if [ -z "$MATLAB_PATH" ]; then
        MATLAB_PATH=$(find /usr/local /opt ~/MATLAB -name "mlint" 2>/dev/null | head -n 1)
    fi
else
    # Windows (Git Bash, WSL)
    MATLAB_PATH=$(which mlint.exe 2>/dev/null)
fi

if [ ! -f "$MATLAB_PATH" ]; then
    echo "Error: mlint not found"
    echo "Please install MATLAB or configure MATLAB_PATH environment variable"
    exit 1
fi

echo "Using mlint from: $MATLAB_PATH"
echo ""

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
