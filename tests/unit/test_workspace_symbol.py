"""
Unit tests for Workspace Symbol Handler.
"""

import pytest
from pygls.server import LanguageServer

from src.handlers.workspace_symbol import WorkspaceSymbolHandler, get_workspace_symbol_handler
from src.utils.symbol_table import SymbolTable


def test_workspace_symbol_handler_initialization():
    """Test WorkspaceSymbolHandler can be initialized."""
    table = SymbolTable()
    handler = WorkspaceSymbolHandler(symbol_table=table)

    assert handler is not None


def test_provide_workspace_symbols_with_query():
    """Test providing workspace symbols with query."""
    table = SymbolTable()
    handler = WorkspaceSymbolHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add symbols
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
    )
    table.add_symbol(
        name="otherFunction",
        kind="function",
        uri="file:///test.m",
        line=2,
    )

    # Provide workspace symbols with query
    results = handler.provide_workspace_symbols(
        server=server,
        query="my"
    )

    # Should return matching symbols
    assert len(results) >= 1
    assert any("my" in s.name.lower() for s in results)


def test_provide_workspace_symbols_without_query():
    """Test providing workspace symbols without query."""
    table = SymbolTable()
    handler = WorkspaceSymbolHandler(symbol_table=table)
    server = LanguageServer("test", "v0.1.0")

    # Add symbol
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
    )

    # Provide workspace symbols without query
    results = handler.provide_workspace_symbols(
        server=server,
        query=None
    )

    # Should return all symbols
    assert len(results) >= 1


def test_filter_symbols_by_query():
    """Test filtering symbols by query."""
    table = SymbolTable()
    handler = WorkspaceSymbolHandler(symbol_table=table)

    # Add symbols
    table.add_symbol(
        name="function1",
        kind="function",
        uri="file:///test.m",
        line=1,
    )
    table.add_symbol(
        name="function2",
        kind="function",
        uri="file:///test.m",
        line=2,
    )

    # Get all symbols
    all_symbols = table.get_all_symbols()

    # Filter by query
    filtered = handler._filter_symbols_by_query(
        all_symbols, "function"
    )

    # Should return both matching symbols
    assert len(filtered) >= 1
    assert all("function" in s.name.lower() for s in filtered)


def test_filter_by_kind():
    """Test filtering symbols by kind."""
    table = SymbolTable()
    handler = WorkspaceSymbolHandler(symbol_table=table)

    # Add symbols
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
    )
    table.add_symbol(
        name="myVar",
        kind="variable",
        uri="file:///test.m",
        line=2,
    )

    # Get all symbols
    all_symbols = table.get_all_symbols()

    # Filter by kind
    filtered = handler.filter_by_kind(all_symbols, ["function"])

    # Should return only functions
    assert len(filtered) >= 1
    assert all(s.kind == "function" for s in filtered)


def test_get_workspace_symbol_handler():
    """Test getting global workspace symbol handler instance."""
    handler1 = get_workspace_symbol_handler()
    handler2 = get_workspace_symbol_handler()

    assert handler1 is handler2  # Should return same instance


def test_workspace_symbol_handler_module_imports():
    """Test that workspace symbol handler module can be imported."""
    from src.handlers.workspace_symbol import (
        WorkspaceSymbolHandler,
        get_workspace_symbol_handler,
    )

    assert WorkspaceSymbolHandler is not None
    assert get_workspace_symbol_handler is not None
