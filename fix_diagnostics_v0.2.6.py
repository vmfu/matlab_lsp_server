#!/usr/bin/env python3
"""
Fix diagnostics.py for v0.2.6

This script:
1. Fixes PyPI API usage for publishing diagnostics
2. Changes .publish_diagnostics() to .text_document_publish_diagnostics()
"""

import os
import re

FILE = "src/matlab_lsp_server/handlers/diagnostics.py"

def fix_diagnostics():
    """Fix diagnostics.py to use correct PyPI API."""

    if not os.path.exists(FILE):
        print(f"[ERROR] File not found: {FILE}")
        return False

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix: Replace incorrect API call with correct API
    # Line 96 (approx): server.publish_diagnostics(...) -> server.text_document_publish_diagnostics(...)

    # Pattern 1: server.publish_diagnostics(file_uri, lsp_diagnostics)
    pattern1 = r'server\.publish_diagnostics\([^)]+\)'
    replacement1 = r'params = PublishDiagnosticsParams(uri=file_uri, diagnostics=lsp_diagnostics)\n            server.text_document_publish_diagnostics(params)'

    # Need to import PublishDiagnosticsParams if not already present
    # Check for import
    if 'from lsprotocol.types import PublishDiagnosticsParams' not in content:
        # Add import before def publish_diagnostics(...)
        import_pattern = r'(from lsprotocol\.types import \([^)]+\))'
        if re.search(import_pattern, content):
            replacement_import = r'\1\nfrom lsprotocol.types import PublishDiagnosticsParams'
            content = re.sub(import_pattern, replacement_import, content, count=1)
            print("[INFO] Added import for PublishDiagnosticsParams")
        else:
            print("[WARNING] Could not find import section to add PublishDiagnosticsParams")

    # Apply fix
    new_content = re.sub(pattern1, replacement1, content)

    # Write fixed content
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[SUCCESS] Fixed {FILE}")
    print("Changes:")
    print("  1. Fixed PyPI API usage (publish_diagnostics -> text_document_publish_diagnostics)")
    print("  2. Added PublishDiagnosticsParams import")

    return True

if __name__ == "__main__":
    success = fix_diagnostics()
    exit(0 if success else 1)
