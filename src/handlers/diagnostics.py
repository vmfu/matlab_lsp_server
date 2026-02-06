"""
Diagnostics Handler for MATLAB LSP Server.

This module handles textDocument/publishDiagnostics notifications
to publish analysis results to the LSP client.
"""

from typing import List, Dict, Any
from lsprotocol.types import Diagnostic, DiagnosticSeverity
from pygls.server import LanguageServer

from ..analyzer.base_analyzer import BaseAnalyzer, DiagnosticResult
from ..utils.logging import get_logger

logger = get_logger(__name__)


def mlint_result_to_lsp_diagnostics(
    result: DiagnosticResult
) -> List[Diagnostic]:
    """
    Convert MlintAnalyzer result to LSP Diagnostic objects.

    Args:
        result (DiagnosticResult): Analysis result from MlintAnalyzer

    Returns:
        List[Diagnostic]: List of LSP Diagnostic objects
    """
    diagnostics = []

    for diag_dict in result.diagnostics:
        # Map severity string to LSP DiagnosticSeverity
        severity_map = {
            "error": DiagnosticSeverity.Error,
            "warning": DiagnosticSeverity.Warning,
            "info": DiagnosticSeverity.Information,
        }
        severity = severity_map.get(diag_dict["severity"], DiagnosticSeverity.Warning)

        # Create LSP Diagnostic
        diagnostic = Diagnostic(
            range={
                "start": {
                    "line": diag_dict["line"] - 1,  # LSP is 0-based
                    "character": diag_dict["column"] - 1,
                },
                "end": {
                    "line": diag_dict["line"] - 1,
                    "character": diag_dict["column"],  # End after message
                },
            },
            message=diag_dict["message"],
            severity=severity,
            code=diag_dict["code"],
            source=diag_dict["source"],
        )
        diagnostics.append(diagnostic)

    logger.debug(f"Converted {len(result.diagnostics)} diagnostics to LSP format")
    return diagnostics


def publish_diagnostics(
    server: LanguageServer,
    file_uri: str,
    analyzer: BaseAnalyzer,
    file_path: str,
) -> None:
    """
    Analyze file and publish diagnostics to client.

    Args:
        server (LanguageServer): LSP server instance
        file_uri (str): URI of file to analyze
        analyzer (BaseAnalyzer): Analyzer instance (e.g., MlintAnalyzer)
        file_path (str): Local path to file
    """
    logger.debug(f"Publishing diagnostics for: {file_path}")

    try:
        # Run analyzer
        result = analyzer.analyze(file_uri=file_uri, file_path=file_path)

        # Convert to LSP diagnostics
        lsp_diagnostics = mlint_result_to_lsp_diagnostics(result)

        # Publish to client
        server.lsp.publish_diagnostics(
            params={
                "uri": file_uri,
                "diagnostics": lsp_diagnostics,
            }
        )

        logger.info(f"Published {len(lsp_diagnostics)} diagnostics for {file_path}")

    except FileNotFoundError:
        logger.warning(f"File not found, skipping diagnostics: {file_path}")
    except Exception as e:
        logger.error(f"Error analyzing file {file_path}: {e}")
