"""
Unit tests for Code Action Handler.
"""

import pytest
from lsprotocol.types import Position, Range
from pygls.server import LanguageServer

from src.handlers.code_action import CodeActionHandler, get_code_action_handler


def test_code_action_handler_initialization():
    """Test CodeActionHandler can be initialized."""
    handler = CodeActionHandler()

    assert handler is not None


def test_generate_quick_fixes_from_diagnostic():
    """Test generating quick fixes from diagnostic."""
    handler = CodeActionHandler()

    # Create diagnostic with undefined function
    from lsprotocol.types import Diagnostic
    diagnostic = Diagnostic(
        range=Range(
            start=Position(line=0, character=0),
            end=Position(line=0, character=10),
        ),
        message="Undefined function 'myFunc'",
    )

    # Generate quick fixes
    fixes = handler.generate_quick_fixes_from_diagnostic(diagnostic)

    # Should have at least one fix
    assert len(fixes) >= 1


def test_generate_quick_fixes_missing_semicolon():
    """Test generating quick fixes for missing semicolon."""
    handler = CodeActionHandler()

    # Create diagnostic for missing semicolon
    from lsprotocol.types import Diagnostic
    diagnostic = Diagnostic(
        range=Range(
            start=Position(line=0, character=0),
            end=Position(line=0, character=10),
        ),
        message="Missing semicolon",
    )

    # Generate quick fixes
    fixes = handler.generate_quick_fixes_from_diagnostic(diagnostic)

    # Should have fix for semicolon
    semicolon_fixes = [f for f in fixes if 'semicolon' in f.get('title', '').lower()]
    assert len(semicolon_fixes) >= 1


def test_provide_code_actions_empty():
    """Test providing code actions with empty diagnostics."""
    handler = CodeActionHandler()
    server = LanguageServer("test", "v0.1.0")

    # Provide code actions with empty diagnostics
    actions = handler.provide_code_actions(
        server=server,
        file_uri="file:///test.m",
        diagnostics=[],
    )

    # Should return empty list
    assert len(actions) == 0


def test_get_code_action_handler():
    """Test getting global code action handler instance."""
    handler1 = get_code_action_handler()
    handler2 = get_code_action_handler()

    assert handler1 is handler2  # Should return same instance


def test_code_action_handler_module_imports():
    """Test that code action handler module can be imported."""
    from src.handlers.code_action import (
        CodeActionHandler,
        get_code_action_handler,
    )

    assert CodeActionHandler is not None
    assert get_code_action_handler is not None
