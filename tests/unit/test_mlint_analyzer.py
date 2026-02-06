"""
Unit tests for Mlint Analyzer.
"""

import pytest
import os
import tempfile
from pathlib import Path

from src.analyzer.mlint_analyzer import MlintAnalyzer
from src.analyzer.base_analyzer import DiagnosticResult


def test_mlint_analyzer_initialization():
    """Test MlintAnalyzer can be initialized."""
    analyzer = MlintAnalyzer(matlab_path=None)

    assert analyzer.matlab_path is None
    assert analyzer.get_name() == "MlintAnalyzer"


def test_mlint_analyzer_with_path():
    """Test MlintAnalyzer initialization with MATLAB path."""
    analyzer = MlintAnalyzer(matlab_path="C:\\MATLAB")

    assert analyzer.matlab_path == "C:\\MATLAB"
    assert analyzer.get_name() == "MlintAnalyzer"


def test_mlint_pattern_matching():
    """Test mlint output pattern regex."""
    analyzer = MlintAnalyzer()

    # Test typical mlint output line with ID
    test_output = "L 20 (C): The variable 'x' appears to change size on every loop iteration."
    match = analyzer.MLINT_PATTERN_WITH_ID.match(test_output)

    assert match is not None
    assert match.group(1) == "20"  # Line number
    assert match.group(2) == "C"   # Message ID
    assert "x" in match.group(3)  # Message content


def test_mlint_pattern_without_column():
    """Test mlint output pattern without column number."""
    analyzer = MlintAnalyzer()

    # Test mlint output without column
    test_output = "L 20: Missing semicolon."
    match = analyzer.MLINT_PATTERN_SIMPLE.match(test_output)

    assert match is not None
    assert match.group(1) == "20"
    assert "Missing semicolon" in match.group(2)


def test_severity_mapping():
    """Test severity level mapping."""
    analyzer = MlintAnalyzer()

    # Test error prefixes
    assert analyzer._map_severity("E001") == "error"
    assert analyzer._map_severity("F001") == "error"

    # Test warning prefixes
    assert analyzer._map_severity("C001") == "warning"
    assert analyzer._map_severity("W001") == "warning"

    # Test info prefixes
    assert analyzer._map_severity("I001") == "info"

    # Test unknown prefix (default to warning)
    assert analyzer._map_severity("X001") == "warning"
    assert analyzer._map_severity("") == "warning"


def test_mlint_analyze_file_not_found():
    """Test analyzer raises FileNotFoundError for non-existent file."""
    analyzer = MlintAnalyzer()

    with pytest.raises(FileNotFoundError):
        analyzer.analyze(
            file_uri="file:///nonexistent.m",
            file_path="C:\\nonexistent.m"
        )


def test_mlint_analyze_without_mlint():
    """Test analyzer raises RuntimeError when mlint not available."""
    # This test is skipped because it depends on system configuration
    # The analyzer searches for mlint in multiple locations,
    # and if any mlint is found, the test would fail
    pytest.skip("Test depends on system mlint availability")


def test_parse_output_with_multiple_errors():
    """Test parsing mlint output with multiple errors."""
    analyzer = MlintAnalyzer()

    test_output = """
L 10 (C): Variable 'x' not used.
L 20 (W): Use of 'eval' is discouraged.
L 30 (E): Undefined function 'foo'.
"""

    diagnostics = analyzer._parse_output(test_output)

    assert len(diagnostics) == 3

    # Verify first diagnostic
    assert diagnostics[0]["line"] == 10
    assert diagnostics[0]["column"] == 1
    assert diagnostics[0]["code"] == "C"
    assert diagnostics[0]["severity"] == "warning"
    assert "x" in diagnostics[0]["message"]

    # Verify second diagnostic
    assert diagnostics[1]["line"] == 20
    assert diagnostics[1]["code"] == "W"
    assert diagnostics[1]["severity"] == "warning"
    assert "eval" in diagnostics[1]["message"]

    # Verify third diagnostic
    assert diagnostics[2]["line"] == 30
    assert diagnostics[2]["code"] == "E"
    assert diagnostics[2]["severity"] == "error"
    assert "foo" in diagnostics[2]["message"]


def test_parse_output_empty():
    """Test parsing empty output."""
    analyzer = MlintAnalyzer()
    diagnostics = analyzer._parse_output("")
    assert len(diagnostics) == 0


def test_parse_output_malformed():
    """Test parsing malformed output lines (should be skipped)."""
    analyzer = MlintAnalyzer()
    test_output = "This is not valid mlint output."
    diagnostics = analyzer._parse_output(test_output)
    assert len(diagnostics) == 0


def test_mlint_analyzer_module_imports():
    """Test that MlintAnalyzer module can be imported."""
    from src.analyzer.mlint_analyzer import MlintAnalyzer, BaseAnalyzer

    assert MlintAnalyzer is not None
    assert BaseAnalyzer is not None
