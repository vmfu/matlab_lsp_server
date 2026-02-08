"""
Unit tests for Definition Handler.
"""

from lsprotocol.types import Position
from pygls.server import LanguageServer

from src.handlers.definition import DefinitionHandler, get_definition_handler
from src.utils.symbol_table import SymbolTable


def test_definition_handler_initialization():
    """Test DefinitionHandler can be initialized."""
    table = SymbolTable()
    handler = DefinitionHandler(symbol_table=table)

    assert handler is not None


def test_provide_definition_with_symbol():
    """Test providing definition with a matching symbol."""
    table = SymbolTable()
    handler = DefinitionHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add symbol
    table.add_symbol(
        name="testFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
        detail="function testFunction()",
    )

    # Provide definition
    result = handler.provide_definition(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        word="testFunction"
    )

    # Should return location
    assert result is not None
    assert result.uri == "file:///test.m"
    assert result.range.start.line == 0  # 0-based


def test_provide_definition_without_symbol():
    """Test providing definition without matching symbol."""
    table = SymbolTable()
    handler = DefinitionHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Provide definition for non-existent symbol
    result = handler.provide_definition(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        word="nonExistentFunction"
    )

    # Should return None
    assert result is None


def test_provide_definition_empty_word():
    """Test providing definition with empty word."""
    table = SymbolTable()
    handler = DefinitionHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Provide definition with empty word
    result = handler.provide_definition(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        word=""
    )

    # Should return None
    assert result is None


def test_provide_definitions_multiple():
    """Test providing all definitions for a symbol."""
    table = SymbolTable()
    handler = DefinitionHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add same symbol in multiple files
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test1.m",
        line=1,
    )
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test2.m",
        line=2,
    )

    # Provide definitions
    results = handler.provide_definitions(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        word="myFunction"
    )

    # Should return both locations
    assert len(results) == 2
    assert results[0].uri == "file:///test1.m"
    assert results[1].uri == "file:///test2.m"


def test_get_definition_handler():
    """Test getting global definition handler instance."""
    handler1 = get_definition_handler()
    handler2 = get_definition_handler()

    assert handler1 is handler2  # Should return same instance


def test_definition_handler_module_imports():
    """Test that definition handler module can be imported."""
    from src.handlers.definition import DefinitionHandler, get_definition_handler

    assert DefinitionHandler is not None
    assert get_definition_handler is not None
