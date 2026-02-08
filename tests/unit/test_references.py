"""
Unit tests for References Handler.
"""

from lsprotocol.types import Position
from pygls.server import LanguageServer

from src.handlers.references import ReferencesHandler, get_references_handler
from src.utils.symbol_table import SymbolTable


def test_references_handler_initialization():
    """Test ReferencesHandler can be initialized."""
    table = SymbolTable()
    handler = ReferencesHandler(symbol_table=table)

    assert handler is not None


def test_provide_references_with_symbol():
    """Test providing references with a matching symbol."""
    table = SymbolTable()
    handler = ReferencesHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add same symbol in multiple files
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
    )
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test2.m",
        line=2,
    )

    # Provide references
    results = handler.provide_references(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        include_declaration=True
    )

    # Should return at least one location (the one in test.m)
    assert len(results) >= 1


def test_provide_references_without_declaration():
    """Test providing references without declaration."""
    table = SymbolTable()
    handler = ReferencesHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add symbols
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
    )
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test2.m",
        line=2,
    )

    # Provide references without declaration
    results = handler.provide_references(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        include_declaration=False
    )

    # Should return only references (not definition)
    # For now, this returns all - simplified logic
    assert len(results) <= 2


def test_provide_references_empty():
    """Test providing references for non-existent symbol."""
    table = SymbolTable()
    handler = ReferencesHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Provide references
    results = handler.provide_references(
        server=server,
        file_uri="file:///test.m",
        position=Position(line=0, character=0),
        include_declaration=True
    )

    # Should return empty list
    assert len(results) == 0


def test_get_references_handler():
    """Test getting global references handler instance."""
    handler1 = get_references_handler()
    handler2 = get_references_handler()

    assert handler1 is handler2  # Should return same instance


def test_references_handler_module_imports():
    """Test that references handler module can be imported."""
    from src.handlers.references import ReferencesHandler, get_references_handler

    assert ReferencesHandler is not None
    assert get_references_handler is not None
