#!/usr/bin/env bash3
"""
Modify matlab_server.py for v0.2.5

This script:
1. Updates version to 0.2.5
2. Adds imports for lifecycle and method_handlers
3. Adds calls to register_lifecycle_handlers() and register_method_handlers()
"""

set -e

FILE="src/matlab_lsp_server/matlab_server.py"
TMP_FILE="${FILE}.tmp"

echo "Modifying ${FILE} for v0.2.5..."

# Read file line by line
line_num=0
while IFS= read -r line; do
    line_num=$((line_num + 1))

    # REPLACE 1: Update version to 0.2.5
    if [[ "$line" == *'"version": "0.2.4"'* ]]; then
        echo "$line" | sed 's/0\.2\.4/0.2.5/g' >> "${TMP_FILE}"
        echo "[INFO] Updated version to 0.2.5"
        continue
    fi

    # INSERT 1: Add import for register_lifecycle_handlers
    if [[ $line_num -eq 36 ]]; then
        echo "" >> "${TMP_FILE}"
        echo "# CRITICAL FIX v0.2.5: Import lifecycle handlers" >> "${TMP_FILE}"
        echo "from matlab_lsp_server.protocol.lifecycle import register_lifecycle_handlers" >> "${TMP_FILE}"
        echo "[INFO] Added import for register_lifecycle_handlers"
        continue
    fi

    # INSERT 2: Add import for register_method_handlers
    if [[ $line_num -eq 37 ]]; then
        echo "# CRITICAL FIX v0.2.5: Import method handlers" >> "${TMP_FILE}"
        echo "from matlab_lsp_server.protocol.method_handlers import register_method_handlers" >> "${TMP_FILE}"
        echo "[INFO] Added import for register_method_handlers"
        continue
    fi

    # INSERT 3: Add registration calls (after on_initialized logic)
    if [[ $line_num -eq 135 ]]; then
        echo "" >> "${TMP_FILE}"
        echo "            # CRITICAL FIX v0.2.5: Register shutdown/exit handlers (FIXES HANGING!)" >> "${TMP_FILE}"
        echo "            from matlab_lsp_server.protocol.lifecycle import register_lifecycle_handlers" >> "${TMP_FILE}"
        echo "            register_lifecycle_handlers(self)" >> "${TMP_FILE}"
        echo "            logger.info(\"Lifecycle handlers registered (shutdown/exit with return None)\")" >> "${TMP_FILE}"
        echo "" >> "${TMP_FILE}"
        echo "            # CRITICAL FIX v0.2.5: Register all LSP method handlers (FIXES DOCUMENT SYMBOLS!)" >> "${TMP_FILE}"
        echo "            from matlab_lsp_server.protocol.method_handlers import register_method_handlers" >> "${TMP_FILE}"
        echo "            register_method_handlers(self)" >> "${TMP_FILE}"
        echo "            logger.info(\"Method handlers registered (completion, hover, documentSymbol, etc.)\")" >> "${TMP_FILE}"
        echo "" >> "${TMP_FILE}"
        echo "            # CRITICAL FIX v0.2.5: All handlers now registered correctly!" >> "${TMP_FILE}"
        echo "[INFO] Added calls to register_lifecycle_handlers and register_method_handlers"
        continue
    fi

    # Echo line as is
    echo "$line" >> "${TMP_FILE}"

done < "${FILE}"

# Replace original file with modified
mv "${TMP_FILE}" "${FILE}"

echo "[SUCCESS] Modified ${FILE} for v0.2.5"
echo "Changes:"
echo "  1. Version updated to 0.2.5"
echo "  2. Added imports for lifecycle and method_handlers"
echo "  3. Added calls to register_lifecycle_handlers()"
echo "  4. Added calls to register_method_handlers()"
