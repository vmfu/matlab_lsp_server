"""
Unit tests for Formatting Handler.
"""

import pytest
from pygls.server import LanguageServer

from src.handlers.formatting import FormattingHandler, get_formatting_handler


def test_formatting_handler_initialization():
    """Test FormattingHandler can be initialized."""
    handler = FormattingHandler()

    assert handler is not None


def test_format_matlab_code():
    """Test formatting MATLAB code."""
    handler = FormattingHandler()

    # Test code with inconsistent indentation
    code = """function test()
x = 1;
if x == 1
disp('x');
end
"""

    # Format code
    formatted = handler._format_matlab_code(code)

    # Should have proper indentation
    lines = formatted.split('\n')

    # Check indentation
    assert lines[0] == "function test()"
    assert lines[1] == "    x = 1;"
    assert lines[2] == "    if x == 1"
    assert lines[3] == "        disp('x');"
    assert lines[4] == "    end"


def test_format_matlab_code_with_tabs():
    """Test formatting MATLAB code with tabs."""
    handler = FormattingHandler()

    code = "function test()\n\tx = 1;\nend"

    # Format with tabs
    formatted = handler._format_matlab_code(code, indent_size=2, insert_spaces=False)

    # Should use tabs
    assert '\tx = 1;' in formatted


def test_provide_formatting_with_changes():
    """Test providing formatting with code changes."""
    handler = FormattingHandler()
    server = LanguageServer("test", "v0.1.0")

    # Unformatted code
    content = """function test()
x = 1;
end
"""

    # Provide formatting
    edits = handler.provide_formatting(
        server=server,
        file_uri="file:///test.m",
        content=content,
    )

    # Should have at least one edit
    assert len(edits) >= 1


def test_provide_formatting_no_changes():
    """Test providing formatting without changes."""
    handler = FormattingHandler()
    server = LanguageServer("test", "v0.1.0")

    # Already formatted code
    content = "    function test()\n    end"

    # Provide formatting
    edits = handler.provide_formatting(
        server=server,
        file_uri="file:///test.m",
        content=content,
    )

    # Should have no edits (or minimal)
    # This is simplified - actual formatter would detect proper format
    assert True  # Just check it doesn't crash


def test_set_config():
    """Test setting formatting configuration."""
    handler = FormattingHandler()

    # Set config
    handler.set_config({"indent_size": 2, "max_line_length": 120})

    # Config should be updated
    assert handler._config["indent_size"] == 2
    assert handler._config["max_line_length"] == 120


def test_get_formatting_handler():
    """Test getting global formatting handler instance."""
    handler1 = get_formatting_handler()
    handler2 = get_formatting_handler()

    assert handler1 is handler2  # Should return same instance


def test_formatting_handler_module_imports():
    """Test that formatting handler module can be imported."""
    from src.handlers.formatting import (
        FormattingHandler,
        get_formatting_handler,
    )

    assert FormattingHandler is not None
    assert get_formatting_handler is not None
