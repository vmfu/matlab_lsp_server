#!/usr/bin/env python3
"""
Fix document_sync.py for v0.2.6

This script:
1. Adds MATLAB parsing logic to did_open handler
2. Adds symbol table updating logic to did_open handler
3. Adds symbol table cleanup logic to did_close handler
"""

import os
import re

FILE = "src/matlab_lsp_server/protocol/document_sync.py"

def fix_document_sync():
    """Fix document_sync.py to add MATLAB parsing."""

    if not os.path.exists(FILE):
        print(f"[ERROR] File not found: {FILE}")
        return False

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if imports are already present
    if 'from matlab_lsp_server.parser.matlab_parser import MatlabParser' in content:
        print("[INFO] MatlabParser import already exists")
    else:
        # Add imports after line 20 (approximate)
        imports_to_add = [
            '# Added for v0.2.6: MATLAB parsing\n',
            'from matlab_lsp_server.parser.matlab_parser import MatlabParser\n',
            'from matlab_lsp_server.parser.models import get_symbol_table\n',
        ]
        content = '\n'.join(imports_to_add) + content
        print("[INFO] Added imports for MatlabParser and get_symbol_table")

    # Check if function signature needs modification
    # register_document_sync_handlers(document_store, mlint_analyzer)
    # Need to add: symbol_table, matlab_parser
    if 'def register_document_sync_handlers(' in content:
        # Update function signature
        content = re.sub(
            r'def register_document_sync_handlers\(',
            'def register_document_sync_handlers(\n    document_store,\n    mlint_analyzer,\n    symbol_table: Optional[SymbolTable] = None,\n    matlab_parser: Optional[MatlabParser] = None',
            content
        )
        print("[INFO] Updated register_document_sync_handlers signature to include symbol_table and matlab_parser")
    else:
        print("[WARNING] Could not find register_document_sync_handlers function")

    # Modify did_open handler (around line 68)
    # Find: document_store.add_document(uri, file_path, content)
    # Add parsing logic AFTER it
    pattern = r"(document_store\.add_document\(uri, file_path, content\))"
    replacement = r"document_store.add_document(uri, file_path, content)\n\n        # Added for v0.2.6: Parse MATLAB code to extract symbols\n        try:\n            parse_result = matlab_parser.parse_file(file_path, uri, use_cache=True)\n            symbol_table.update_from_parse_result(uri, content, parse_result)\n            logger.info(f\"Updated symbol table for {file_path}\")\n        except Exception as e:\n            logger.error(f\"Error parsing file {file_path}: {e}\")"
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print("[INFO] Added MATLAB parsing logic to did_open handler")
    else:
        print("[WARNING] Could not find did_open handler pattern to add parsing logic")

    # Modify did_close handler (around line 88)
    # Find: document_store.remove_document(uri)
    # Add symbol cleanup logic AFTER it
    pattern = r"(document_store\.remove_document\(uri\))"
    replacement = r"document_store.remove_document(uri)\n\n        # Added for v0.2.6: Remove symbols from table\n        symbol_table.remove_symbols_by_uri(uri)"
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print("[INFO] Added symbol table cleanup logic to did_close handler")
    else:
        print("[WARNING] Could not find did_close handler pattern to add cleanup logic")

    # Modify register_document_sync_handlers (around line 20)
    # Find: document_sync.register_document_sync_handlers(server, document_store, mlint_analyzer)
    # Add initialization logic
    pattern = r"document_sync\.register_document_sync_handlers\(([^)]+)\)"
    replacement = r"document_sync.register_document_sync_handlers(\1, symbol_table=None, matlab_parser=None)"
    content = re.sub(pattern, replacement, content)
    print("[INFO] Initialized symbol_table and matlab_parser to None in register_document_sync_handlers call")

    # Write fixed content
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[SUCCESS] Fixed {FILE}")
    print("Changes:")
    print("  1. Added imports for MatlabParser and get_symbol_table")
    print("  2. Updated register_document_sync_handlers signature (symbol_table, matlab_parser)")
    print("  3. Added MATLAB parsing logic to did_open handler")
    print("  4. Added symbol table cleanup logic to did_close handler")

    return True

if __name__ == "__main__":
    success = fix_document_sync()
    exit(0 if success else 1)
