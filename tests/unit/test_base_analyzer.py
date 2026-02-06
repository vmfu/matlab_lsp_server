"""
Unit tests for Base Analyzer.
"""

import pytest
from src.analyzer.base_analyzer import BaseAnalyzer, DiagnosticResult


def test_diagnostic_result_creation():
    """Test DiagnosticResult can be created."""
    result = DiagnosticResult(
        file_uri="file:///test.m",
        diagnostics=[
            {
                "line": 1,
                "column": 1,
                "message": "Test error",
                "severity": "error",
                "code": "E001",
                "source": "test",
            }
        ]
    )

    assert result.file_uri == "file:///test.m"
    assert len(result.diagnostics) == 1
    assert result.diagnostics[0]["line"] == 1
    assert result.diagnostics[0]["message"] == "Test error"


def test_base_analyzer_is_abstract():
    """Test that BaseAnalyzer cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseAnalyzer()


def test_base_analyzer_has_abstract_methods():
    """Test that BaseAnalyzer defines abstract methods."""
    assert hasattr(BaseAnalyzer, "analyze")
    assert callable(getattr(BaseAnalyzer, "analyze"))
    assert hasattr(BaseAnalyzer, "is_available")
    assert callable(getattr(BaseAnalyzer, "is_available"))
    assert hasattr(BaseAnalyzer, "get_name")
    assert callable(getattr(BaseAnalyzer, "get_name"))


def test_base_analyzer_module_imports():
    """Test that BaseAnalyzer module can be imported."""
    from src.analyzer.base_analyzer import BaseAnalyzer, DiagnosticResult, get_logger

    assert BaseAnalyzer is not None
    assert DiagnosticResult is not None
    assert get_logger is not None
