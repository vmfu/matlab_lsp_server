"""
Unit tests for Hover Handler.
"""

import pytest
from lsprotocol.types import Position
from pygls.server import LanguageServer

from src.handlers.hover import HoverHandler, get_hover_handler
from src.utils.symbol_table import SymbolTable


def test_hover_handler_initialization():
    """Test HoverHandler can be initialized."""
    table = SymbolTable()
    handler = HoverHandler(symbol_table=table)

    assert handler is not None


def test_provide_hover_with_symbol():
    """Test providing hover with a matching symbol."""
    table = SymbolTable()
    handler = HoverHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add symbol
    table.add_symbol(
        name="testFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
        detail="function testFunction()",
        documentation="This is a test function",
    )

    # Provide hover
    result = handler.provide_hover(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        word="testFunction"
    )

    # Should return hover with documentation
    assert result is not None
    assert "testFunction" in result.contents
    assert "This is a test function" in result.contents


def test_provide_hover_without_symbol():
    """Test providing hover without matching symbol."""
    table = SymbolTable()
    handler = HoverHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Provide hover for non-existent symbol
    result = handler.provide_hover(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        word="nonExistentFunction"
    )

    # Should return None
    assert result is None


def test_provide_hover_empty_word():
    """Test providing hover with empty word."""
    table = SymbolTable()
    handler = HoverHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Provide hover with empty word
    result = handler.provide_hover(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        word=""
    )

    # Should return None
    assert result is None


def test_create_hover_content():
    """Test creating hover content from symbol."""
    table = SymbolTable()
    handler = HoverHandler(symbol_table=table)

    # Create test symbol
    from src.utils.symbol_table import Symbol
    symbol = Symbol(
        name="myFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
        detail="function myFunction(x, y)",
        documentation="Calculate sum of x and y",
    )

    # Create hover content
    content = handler._create_hover_content(symbol)

    # Should include kind, name, detail, documentation
    assert "function" in content
    assert "myFunction" in content
    assert "function myFunction(x, y)" in content
    assert "Calculate sum of x and y" in content


def test_find_symbol_at_position():
    """Test finding symbol at position."""
    table = SymbolTable()
    handler = HoverHandler(symbol_table=table)

    # Add symbol at line 1
    table.add_symbol(
        name="myFunc",
        kind="function",
        uri="file:///test.m",
        line=1,
    )

    # Search at line 1
    file_symbols = table.get_symbols_by_uri("file:///test.m")
    found = handler._find_symbol_at_position(
        file_symbols,
        Position(line=0, character=0),
        "myFunc"
    )

    assert found is not None
    assert found.name == "myFunc"


def test_get_hover_handler():
    """Test getting global hover handler instance."""
    handler1 = get_hover_handler()
    handler2 = get_hover_handler()

    assert handler1 is handler2  # Should return same instance


def test_hover_handler_module_imports():
    """Test that hover handler module can be imported."""
    from src.handlers.hover import (
        HoverHandler,
        get_hover_handler,
    )

    assert HoverHandler is not None
    assert get_hover_handler is not None
