"""
Unit tests for Diagnostics Handler.
"""

from lsprotocol.types import Diagnostic, DiagnosticSeverity
from pygls.server import LanguageServer

from src.analyzer.base_analyzer import DiagnosticResult
from src.handlers.diagnostics import mlint_result_to_lsp_diagnostics, publish_diagnostics


def test_mlint_result_to_lsp_diagnostics():
    """Test conversion of mlint results to LSP diagnostics."""
    # Create sample mlint result
    result = DiagnosticResult(
        file_uri="file:///test.m",
        diagnostics=[
            {
                "line": 10,
                "column": 1,
                "message": "Variable 'x' not used.",
                "severity": "error",
                "code": "E001",
                "source": "mlint",
            },
            {
                "line": 20,
                "column": 5,
                "message": "Missing semicolon.",
                "severity": "warning",
                "code": "C001",
                "source": "mlint",
            },
            {
                "line": 30,
                "column": 1,
                "message": "Use of 'eval' is discouraged.",
                "severity": "info",
                "code": "I001",
                "source": "mlint",
            },
        ]
    )

    # Convert to LSP diagnostics
    lsp_diagnostics = mlint_result_to_lsp_diagnostics(result)

    # Verify conversion
    assert len(lsp_diagnostics) == 3

    # Verify first diagnostic (error)
    assert isinstance(lsp_diagnostics[0], Diagnostic)
    assert lsp_diagnostics[0].range.start.line == 9  # 0-based
    assert lsp_diagnostics[0].range.start.character == 0  # 0-based
    assert lsp_diagnostics[0].message == "Variable 'x' not used."
    assert lsp_diagnostics[0].severity == DiagnosticSeverity.Error
    assert lsp_diagnostics[0].code == "E001"
    assert lsp_diagnostics[0].source == "mlint"

    # Verify second diagnostic (warning)
    assert isinstance(lsp_diagnostics[1], Diagnostic)
    assert lsp_diagnostics[1].range.start.line == 19
    assert lsp_diagnostics[1].severity == DiagnosticSeverity.Warning
    assert lsp_diagnostics[1].code == "C001"

    # Verify third diagnostic (info)
    assert isinstance(lsp_diagnostics[2], Diagnostic)
    assert lsp_diagnostics[2].range.start.line == 29
    assert lsp_diagnostics[2].severity == DiagnosticSeverity.Information
    assert lsp_diagnostics[2].code == "I001"


def test_publish_diagnostics():
    """Test publishing diagnostics to client."""
    # Create a mock server
    server = LanguageServer("test-server", "v0.1.0")

    # Create a mock analyzer that always returns same result
    class MockAnalyzer:
        def analyze(self, file_uri, file_path):
            return DiagnosticResult(
                file_uri=file_uri,
                diagnostics=[
                    {
                        "line": 1,
                        "column": 1,
                        "message": "Test diagnostic",
                        "severity": "error",
                        "code": "E001",
                        "source": "test",
                    }
                ]
            )

    mock_analyzer = MockAnalyzer()

    # Call publish_diagnostics (this will try to call
    # server.lsp.publish_diagnostics)
    # Note: Since we don't have a real LSP client connected, we can't test
    # the actual publish call. We'll just verify the function doesn't crash.
    try:
        from unittest.mock import patch
        with patch.object(server, 'lsp') as _:
            publish_diagnostics(
                server=server,
                file_uri="file:///test.m",
                analyzer=mock_analyzer,
                file_path="C:\\test.m",
            )
    except ImportError:
        # If unittest is not available, just test that function is callable
        assert callable(publish_diagnostics)


def test_severity_mapping_in_conversion():
    """Test that severity levels are correctly mapped."""
    result = DiagnosticResult(
        file_uri="file:///test.m",
        diagnostics=[
            {
                "line": 1,
                "column": 1,
                "message": "Test",
                "severity": "error",
                "code": "E",
                "source": "test",
            },
            {
                "line": 2,
                "column": 1,
                "message": "Test",
                "severity": "warning",
                "code": "W",
                "source": "test",
            },
            {
                "line": 3,
                "column": 1,
                "message": "Test",
                "severity": "info",
                "code": "I",
                "source": "test",
            },
            {
                "line": 4,
                "column": 1,
                "message": "Test",
                "severity": "warning",
                "code": "",
                "source": "test",
            },  # Unknown code
        ]
    )

    lsp_diagnostics = mlint_result_to_lsp_diagnostics(result)

    assert lsp_diagnostics[0].severity == DiagnosticSeverity.Error
    assert lsp_diagnostics[1].severity == DiagnosticSeverity.Warning
    assert lsp_diagnostics[2].severity == DiagnosticSeverity.Information
    (
        lsp_diagnostics[3].severity == DiagnosticSeverity.Warning
    )  # Unknown defaults to warning
    assert lsp_diagnostics[3].source == "test"


def test_diagnostics_handler_module_imports():
    """Test that DiagnosticsHandler module can be imported."""
    from src.handlers.diagnostics import (
        get_logger,
        mlint_result_to_lsp_diagnostics,
        publish_diagnostics,
    )

    assert publish_diagnostics is not None
    assert mlint_result_to_lsp_diagnostics is not None
    assert get_logger is not None
