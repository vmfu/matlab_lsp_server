#!/usr/bin/env python3
"""
Modify matlab_server.py for v0.2.5

This script:
1. Adds imports for lifecycle and method_handlers
2. Adds calls to register_lifecycle_handlers() and register_method_handlers() in _register_handlers()
"""

import os
import sys

FILE = "src/matlab_lsp_server/matlab_server.py"

def modify_matlab_server():
    """Modify matlab_server.py for v0.2.5."""

    if not os.path.exists(FILE):
        print(f"[ERROR] File not found: {FILE}")
        sys.exit(1)

    with open(FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    new_lines = []

    # INSERT 1: Add imports after last import
    last_import_line = None
    for i, line in enumerate(lines):
        if line.strip().startswith('from '):
            last_import_line = i
        new_lines.append(line)

    if last_import_line is not None:
        # Insert imports after last import line
        imports_to_add = [
            "# CRITICAL FIX v0.2.5: Import lifecycle handlers\n",
            "from matlab_lsp_server.protocol.lifecycle import register_lifecycle_handlers\n",
            "# CRITICAL FIX v0.2.5: Import method handlers\n",
            "from matlab_lsp_server.protocol.method_handlers import register_method_handlers\n",
        ]
        for j, import_line in enumerate(imports_to_add):
            new_lines.insert(last_import_line + 1 + j, import_line)

        print(f"[INFO] Added imports after line {last_import_line + 1}")
        modified = True
    else:
        print("[WARNING] Could not find import section to insert after")

    # INSERT 2: Add registration calls at end of _register_handlers()
    # Find line with "=== SERVER FULLY CONFIGURED ===" which is end of _register_handlers
    for i, line in enumerate(new_lines):
        if "=== SERVER FULLY CONFIGURED ===" in line:
            # Insert registration calls BEFORE this line
            calls_to_add = [
                "\n",
                "            # CRITICAL FIX v0.2.5: Register shutdown/exit handlers (FIXES HANGING!)\n",
                "            from matlab_lsp_server.protocol.lifecycle import register_lifecycle_handlers\n",
                "            register_lifecycle_handlers(self)\n",
                "            logger.info(\"Lifecycle handlers registered (shutdown/exit with return None)\")\n",
                "\n",
                "            # CRITICAL FIX v0.2.5: Register all LSP method handlers (FIXES DOCUMENT SYMBOLS!)\n",
                "            from matlab_lsp_server.protocol.method_handlers import register_method_handlers\n",
                "            register_method_handlers(self)\n",
                "            logger.info(\"Method handlers registered (completion, hover, documentSymbol, etc.)\")\n",
                "            logger.info(\"[INFO] All handlers now registered correctly!\")\n",
                "\n",
            ]
            for k, call_line in enumerate(calls_to_add):
                new_lines.insert(i + k, call_line)

            print(f"[INFO] Added registration calls before line {i}")
            modified = True
            break

    if not modified:
        print("[WARNING] No modifications made to file")
        return False

    # Write modified file
    with open(FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"[SUCCESS] Modified {FILE} for v0.2.5")
    print("Changes:")
    print("  1. Added imports for lifecycle and method_handlers")
    print("  2. Added calls to register_lifecycle_handlers() in _register_handlers()")
    print("  3. Added calls to register_method_handlers() in _register_handlers()")
    return True

if __name__ == "__main__":
    success = modify_matlab_server()
    sys.exit(0 if success else 1)
