"""
Unit tests for Document Symbol Handler.
"""

from pygls.server import LanguageServer

from src.handlers.document_symbol import DocumentSymbolHandler, get_document_symbol_handler
from src.utils.symbol_table import SymbolTable


def test_document_symbol_handler_initialization():
    """Test DocumentSymbolHandler can be initialized."""
    table = SymbolTable()
    handler = DocumentSymbolHandler(symbol_table=table)

    assert handler is not None


def test_provide_document_symbols_with_classes():
    """Test providing document symbols with classes."""
    table = SymbolTable()
    handler = DocumentSymbolHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add class
    table.add_symbol(
        name="MyClass",
        kind="class",
        uri="file:///test.m",
        line=1,
        detail="class MyClass",
    )

    # Add method
    table.add_symbol(
        name="myMethod",
        kind="method",
        uri="file:///test.m",
        line=2,
        detail="function myMethod()",
        scope="MyClass",
    )

    # Provide document symbols
    symbols = handler.provide_document_symbols(
        server=server,
        file_uri="file:///test.m",
    )

    # Should have class with method
    assert len(symbols) >= 1
    class_symbols = [s for s in symbols if s.name == "MyClass"]
    assert len(class_symbols) >= 1


def test_provide_document_symbols_with_functions():
    """Test providing document symbols with functions."""
    table = SymbolTable()
    handler = DocumentSymbolHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add function
    table.add_symbol(
        name="main",
        kind="function",
        uri="file:///test.m",
        line=1,
        detail="function main()",
        scope="global",
    )

    # Provide document symbols
    symbols = handler.provide_document_symbols(
        server=server,
        file_uri="file:///test.m",
    )

    # Should have function
    assert len(symbols) >= 1
    function_symbols = [s for s in symbols if s.name == "main"]
    assert len(function_symbols) >= 1


def test_provide_document_symbols_with_variables():
    """Test providing document symbols with variables."""
    table = SymbolTable()
    handler = DocumentSymbolHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add variable
    table.add_symbol(
        name="globalVar",
        kind="variable",
        uri="file:///test.m",
        line=1,
        detail="variable",
        scope="global",
    )

    # Provide document symbols
    symbols = handler.provide_document_symbols(
        server=server,
        file_uri="file:///test.m",
    )

    # Should have variable
    assert len(symbols) >= 1
    var_symbols = [s for s in symbols if s.name == "globalVar"]
    assert len(var_symbols) >= 1


def test_map_symbol_kind():
    """Test mapping symbol kinds."""
    table = SymbolTable()
    handler = DocumentSymbolHandler(symbol_table=table)

    from lsprotocol.types import SymbolKind

    assert handler._map_symbol_kind_to_symbol_kind(
        "function"
    ) == SymbolKind.Function

    assert handler._map_symbol_kind_to_symbol_kind(
        "class"
    ) == SymbolKind.Class

    assert handler._map_symbol_kind_to_symbol_kind(
        "variable"
    ) == SymbolKind.Variable


def test_get_document_symbol_handler():
    """Test getting global document symbol handler instance."""
    handler1 = get_document_symbol_handler()
    handler2 = get_document_symbol_handler()

    assert handler1 is handler2  # Should return same instance


def test_document_symbol_handler_module_imports():
    """Test that document symbol handler module can be imported."""
    from src.handlers.document_symbol import DocumentSymbolHandler, get_document_symbol_handler

    assert DocumentSymbolHandler is not None
    assert get_document_symbol_handler is not None
