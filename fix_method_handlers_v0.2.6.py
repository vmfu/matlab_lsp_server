#!/usr/bin/env python3
"""
Fix method_handlers.py for v0.2.6

This script:
1. Fixes incorrect method calls (.handle() -> .provide_xxx())
2. Fixes incorrect arguments (server, uri, position, etc.)
"""

import os
import re

FILE = "src/matlab_lsp_server/protocol/method_handlers.py"

def fix_method_handlers():
    """Fix method_handlers.py to call correct methods."""

    if not os.path.exists(FILE):
        print(f"[ERROR] File not found: {FILE}")
        return False

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix 1: Completion Handler (line 90)
    # Old: return await completion_handler.handle(params)
    # New: return completion_handler.provide_completion(server, uri, position, "")
    content = re.sub(
        r'return await completion_handler\.handle\(params\)',
        'return completion_handler.provide_completion(\\n            server,\\n            params.text_document.uri,\\n            params.position,\\n            ""  # prefix\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed Completion Handler")

    # Fix 2: Hover Handler (line 96)
    # Old: return await hover_handler.handle(params)
    # New: return hover_handler.provide_hover(server, uri, position, None)
    content = re.sub(
        r'return await hover_handler\.handle\(params\)',
        'return hover_handler.provide_hover(\\n            server,\\n            params.text_document.uri,\\n            params.position,\\n            None  # word\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed Hover Handler")

    # Fix 3: Definition Handler (line 102)
    # Old: return await definition_handler.handle(params)
    # New: return definition_handler.provide_definition(server, uri, position, None)
    content = re.sub(
        r'return await definition_handler\.handle\(params\)',
        'return definition_handler.provide_definition(\\n            server,\\n            params.text_document.uri,\\n            params.position,\\n            None  # word\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed Definition Handler")

    # Fix 4: References Handler (line 108)
    # Old: return await references_handler.handle(params)
    # New: return references_handler.provide_references(server, uri, position, True)
    content = re.sub(
        r'return await references_handler\.handle\(params\)',
        'return references_handler.provide_references(\\n            server,\\n            params.text_document.uri,\\n            params.position,\\n            True  # include_declaration\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed References Handler")

    # Fix 5: Document Symbol Handler (line 114)
    # Old: return document_symbol_handler.provide_document_symbols(server, uri)
    # New: return document_symbol_handler.provide_document_symbols(server, uri, None)
    content = re.sub(
        r'return document_symbol_handler\.provide_document_symbols\(\\s*server,\\s*params\.text_document\.uri\\s*\)',
        'return document_symbol_handler.provide_document_symbols(\\n            server,\\n            params.text_document.uri,\\n            None  # word\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed Document Symbol Handler")

    # Fix 6: Workspace Symbol Handler (line 161)
    # Old: return await workspace_symbol_handler.handle(params)
    # New: return workspace_symbol_handler.provide_workspace_symbols(server, None)
    content = re.sub(
        r'return await workspace_symbol_handler\.handle\(params\)',
        'return workspace_symbol_handler.provide_workspace_symbols(\\n            server,\\n            None  # query\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed Workspace Symbol Handler")

    # Fix 7: Code Action Handler (line 128)
    # Old: return await code_action_handler.handle(params)
    # New: return code_action_handler.provide_code_actions(server, uri, [])
    content = re.sub(
        r'return await code_action_handler\.handle\(params\)',
        'return code_action_handler.provide_code_actions(\\n            server,\\n            params.text_document.uri,\\n            []  # diagnostics\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed Code Action Handler")

    # Fix 8: Formatting Handler (line 168)
    # Old: return await formatting_handler.handle(params)
    # New: return formatting_handler.provide_formatting(server, uri, content, None)
    # Need to match the return line first
    content = re.sub(
        r'return await formatting_handler\.handle\(params\)',
        'return formatting_handler.provide_formatting(\\n            server,\\n            params.text_document.uri,\\n            params.text_document.text,\\n            None  # options\\n        )',
        content,
        count=1
    )
    print("[INFO] Fixed Formatting Handler")

    # Write fixed content
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[SUCCESS] Fixed {FILE}")
    print("Changes:")
    print("  1. Fixed Completion Handler (.handle() -> .provide_completion())")
    print("  2. Fixed Hover Handler (.handle() -> .provide_hover())")
    print("  3. Fixed Definition Handler (.handle() -> .provide_definition())")
    print("  4. Fixed References Handler (.handle() -> .provide_references())")
    print("  5. Fixed Document Symbol Handler (arguments)")
    print("  6. Fixed Workspace Symbol Handler (.handle() -> .provide_workspace_symbols())")
    print("  7. Fixed Code Action Handler (.handle() -> .provide_code_actions())")
    print("  8. Fixed Formatting Handler (.handle() -> .provide_formatting())")

    return True

if __name__ == "__main__":
    success = fix_method_handlers()
    exit(0 if success else 1)
