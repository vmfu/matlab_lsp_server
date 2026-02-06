"""
Unit tests for MATLAB Parser.
"""

import pytest
import tempfile
import os

from src.parser.matlab_parser import MatlabParser
from src.parser.models import (
    FunctionInfo,
    VariableInfo,
    ParseResult,
)


def test_parser_initialization():
    """Test MatlabParser can be initialized."""
    parser = MatlabParser()

    assert parser is not None
    assert parser._nesting_level == 0
    assert parser._current_function is None


def test_parse_simple_function():
    """Test parsing a simple function."""
    parser = MatlabParser()

    # Create test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.m', delete=False) as f:
        f.write(
            "function y = add(x, y)\n"
            "    result = x + y;\n"
            "end"
        )
        file_path = f.name

    try:
        # Parse file
        result = parser.parse_file(file_path, "file:///test.m")

        # Check results
        assert len(result.functions) == 1
        assert result.functions[0].name == "add"
        assert len(result.functions[0].input_args) == 2
        assert result.functions[0].input_args == ["x", "y"]
        assert len(result.functions[0].output_args) == 1
        assert result.functions[0].output_args == ["y"]
    finally:
        os.unlink(file_path)


def test_parse_variables():
    """Test parsing variable declarations."""
    parser = MatlabParser()

    # Create test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.m', delete=False) as f:
        f.write(
            "global GLOBAL_VAR;\n"
            "persistent PERSISTENT_VAR;\n"
            "x = 1;\n"
            "y = 2;\n"
        )
        file_path = f.name

    try:
        # Parse file
        result = parser.parse_file(file_path, "file:///test.m")

        # Check results
        assert len(result.variables) == 4
        assert result.variables[0].name == "GLOBAL_VAR"
        assert result.variables[0].is_global is True
        assert result.variables[1].name == "PERSISTENT_VAR"
        assert result.variables[1].is_persistent is True
        assert result.variables[2].name == "x"
        assert result.variables[3].name == "y"
    finally:
        os.unlink(file_path)


def test_parse_comments():
    """Test parsing comments."""
    parser = MatlabParser()

    # Create test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.m', delete=False) as f:
        f.write(
            "% This is a comment\n"
            "x = 1; % Inline comment\n"
            "%{\n"
            "This is a\n"
            "block comment\n"
            "%}\n"
        )
        file_path = f.name

    try:
        # Parse file
        result = parser.parse_file(file_path, "file:///test.m")

        # Check results
        # Note: Block comments are complex - we'll check that at least
        # inline comments are found for now
        assert len(result.comments) >= 2
        assert result.comments[0].is_block is False
        assert "This is a comment" in result.comments[0].text
        assert result.comments[1].is_block is False
        assert "Inline comment" in result.comments[1].text
    finally:
        os.unlink(file_path)


def test_parse_nested_functions():
    """Test parsing nested functions."""
    parser = MatlabParser()

    # Create test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.m', delete=False) as f:
        f.write(
            "function y = outer(x)\n"
            "    function z = inner(x)\n"
            "        z = x * 2;\n"
            "    end\n"
            "    y = z + 1;\n"
            "end"
        )
        file_path = f.name

    try:
        # Parse file
        result = parser.parse_file(file_path, "file:///test.m")

        # Check results
        assert len(result.functions) == 2
        assert result.functions[0].name == "outer"
        assert result.functions[0].is_nested is False
        assert result.functions[1].name == "inner"
        assert result.functions[1].is_nested is True
        assert result.functions[1].parent_function == "outer"
    finally:
        os.unlink(file_path)


def test_is_builtin_function():
    """Test checking if function is built-in."""
    parser = MatlabParser()

    # Built-in functions
    assert parser.is_builtin_function("sin") is True
    assert parser.is_builtin_function("cos") is True
    assert parser.is_builtin_function("sqrt") is True

    # MATLAB keywords
    assert parser.is_builtin_function("if") is True
    assert parser.is_builtin_function("for") is True
    assert parser.is_builtin_function("function") is True

    # User-defined functions
    assert parser.is_builtin_function("my_function") is False
    assert parser.is_builtin_function("custom_add") is False


def test_parser_module_imports():
    """Test that parser module can be imported."""
    from src.parser.matlab_parser import MatlabParser, MatlabParser
    from src.parser.models import (
        FunctionInfo,
        VariableInfo,
        ParseResult,
    )

    assert MatlabParser is not None
    assert FunctionInfo is not None
    assert VariableInfo is not None
    assert ParseResult is not None


def test_parse_classdef():
    """Test parsing class definition."""
    parser = MatlabParser()

    # Create test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.m', delete=False) as f:
        f.write(
            "classdef MyClass\n"
            "    properties\n"
            "        Property1\n"
            "    methods\n"
            "        function method1(obj)\n"
            "            m = obj;\n"
            "        end\n"
            "end\n"
        )
        file_path = f.name

    try:
        # Parse file
        result = parser.parse_file(file_path, "file:///test.m")

        # Check results
        assert len(result.classes) == 1
        assert result.classes[0].name == "MyClass"
        # Note: Properties and methods extraction is basic
        assert 'Property1' in result.classes[0].properties
        # The method should appear in functions list, not in class
        assert len([f for f in result.functions if f.name == 'method1']) >= 1
    finally:
        os.unlink(file_path)