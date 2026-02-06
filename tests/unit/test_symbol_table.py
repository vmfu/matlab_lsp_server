"""
Unit tests for Symbol Table.
"""

import pytest
from src.utils.symbol_table import (
    SymbolTable,
    Symbol,
    get_symbol_table,
)


def test_symbol_table_initialization():
    """Test SymbolTable can be initialized."""
    table = SymbolTable()

    assert table is not None
    assert len(table._symbols) == 0


def test_add_and_get_symbols():
    """Test adding and getting symbols."""
    table = SymbolTable()

    # Add symbols
    table.add_symbol(
        name="test_func",
        kind="function",
        uri="file:///test.m",
        line=1,
    )

    table.add_symbol(
        name="test_var",
        kind="variable",
        uri="file:///test.m",
        line=2,
    )

    # Get symbols
    symbols = table.get_symbols_by_uri("file:///test.m")

    assert len(symbols) == 2
    assert symbols[0].name == "test_func"
    assert symbols[1].name == "test_var"


def test_search_symbols():
    """Test searching for symbols."""
    table = SymbolTable()

    # Add symbols
    table.add_symbol(
        name="myFunction",
        kind="function",
        uri="file:///test.m",
        line=1,
    )

    table.add_symbol(
        name="yourFunction",
        kind="function",
        uri="file:///test.m",
        line=2,
    )

    # Search for function
    results = table.search_symbols("function")
    assert len(results) == 2

    # Search for specific name
    results = table.search_symbols("my")
    assert len(results) >= 1
    assert results[0].name == "myFunction"


def test_remove_symbols_by_uri():
    """Test removing symbols by URI."""
    table = SymbolTable()

    # Add symbols
    table.add_symbol(
        name="test_func",
        kind="function",
        uri="file:///test.m",
        line=1,
    )

    # Remove symbols
    count = table.remove_symbols_by_uri("file:///test.m")

    assert count == 1
    assert len(table.get_symbols_by_uri("file:///test.m")) == 0


def test_clear_symbol_table():
    """Test clearing symbol table."""
    table = SymbolTable()

    # Add symbols
    table.add_symbol(
        name="test_func",
        kind="function",
        uri="file:///test.m",
        line=1,
    )

    # Clear table
    table.clear()

    assert len(table.get_all_symbols()) == 0


def test_update_from_parse_result():
    """Test updating symbol table from parse result."""
    table = SymbolTable()

    # Create mock parse result
    from src.parser.models import ParseResult, FunctionInfo, ClassInfo

    parse_result = ParseResult(
        file_uri="file:///test.m",
        file_path="C:\\test.m",
        functions=[
            FunctionInfo(
                name="main",
                line=1,
                input_args=["x"],
                output_args=["y"],
            )
        ],
        classes=[
            ClassInfo(
                name="MyClass",
                line=5,
                properties=["prop1"],
                methods=[
                    FunctionInfo(
                        name="method1",
                        line=6,
                        input_args=[],
                        output_args=[],
                    )
                ],
            )
        ],
        raw_content="",
    )

    # Update symbol table
    table.update_from_parse_result(
        uri="file:///test.m",
        content="function main(x); end",
        parse_result=parse_result,
    )

    # Check symbols
    symbols = table.get_symbols_by_uri("file:///test.m")

    # Should have: function "main", class "MyClass", method "method1", property "prop1"
    assert len(symbols) >= 3  # At least function and class
    function_names = [s.name for s in symbols if s.kind == "function"]
    assert "main" in function_names


def test_get_symbol_table():
    """Test getting global symbol table instance."""
    table1 = get_symbol_table()
    table2 = get_symbol_table()

    assert table1 is table2  # Should return same instance


def test_symbol_stats():
    """Test getting symbol table statistics."""
    table = SymbolTable()

    # Add symbols
    table.add_symbol(
        name="func1",
        kind="function",
        uri="file:///test.m",
        line=1,
    )
    table.add_symbol(
        name="var1",
        kind="variable",
        uri="file:///test.m",
        line=2,
    )

    # Get stats
    stats = table.get_stats()

    assert stats["total"] == 2
    assert stats["by_kind"]["function"] == 1
    assert stats["by_kind"]["variable"] == 1


def test_symbol_module_imports():
    """Test that symbol table module can be imported."""
    from src.utils.symbol_table import (
        SymbolTable,
        Symbol,
        get_symbol_table,
    )

    assert SymbolTable is not None
    assert Symbol is not None
    assert get_symbol_table is not None
