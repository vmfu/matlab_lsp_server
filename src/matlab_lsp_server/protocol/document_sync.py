# Added for v0.2.6: MATLAB parsing

from matlab_lsp_server.parser.matlab_parser import MatlabParser

from matlab_lsp_server.parser.models import get_symbol_table
"""
Document Synchronization Handlers for MATLAB LSP Server.

This module implements LSP document synchronization methods:
- textDocument/didOpen
- textDocument/didClose
- textDocument/didChange
"""

from pathlib import Path
from urllib.parse import unquote, urlparse

from lsprotocol.types import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
)
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.analyzer.mlint_analyzer import MlintAnalyzer
from matlab_lsp_server.handlers.diagnostics import publish_diagnostics
from matlab_lsp_server.utils.document_store import DocumentStore
from matlab_lsp_server.utils.logging import get_logger

logger = get_logger(__name__)

# Global instances (will be initialized in server)
document_store = None
mlint_analyzer = None


def register_document_sync_handlers(
    document_store,
    mlint_analyzer,
    symbol_table: Optional[SymbolTable] = None,
    matlab_parser: Optional[MatlabParser] = None
    server: LanguageServer,
    doc_store: DocumentStore,
    analyzer: MlintAnalyzer,
) -> None:
    """
    Register document synchronization handlers with the server.

    Args:
        server (LanguageServer): LSP server instance
        doc_store (DocumentStore): Document store instance
        analyzer (MlintAnalyzer): Analyzer instance (e.g., MlintAnalyzer)
    """
    global document_store, mlint_analyzer

    document_store = doc_store
    mlint_analyzer = analyzer

    logger.debug("Registering document sync handlers")

    @server.feature("textDocument/didOpen")
    async def did_open(params: DidOpenTextDocumentParams) -> None:
        """Handle textDocument/didOpen notification.

        Args:
            params (DidOpenTextDocumentParams): Open parameters
                containing document URI and text content
        """
        text_doc = params.text_document
        uri = text_doc.uri
        file_path = _uri_to_path(uri)
        content = text_doc.text

        logger.debug(f"Document opened: {file_path}")

        # Add to document store
        document_store.add_document(uri, file_path, content)

        # Added for v0.2.6: Parse MATLAB code to extract symbols
        try:
            parse_result = matlab_parser.parse_file(file_path, uri, use_cache=True)
            symbol_table.update_from_parse_result(uri, content, parse_result)
            logger.info(f\"Updated symbol table for {file_path}\")
        except Exception as e:
            logger.error(f\"Error parsing file {file_path}: {e}\")

        # Trigger analysis (only if analyzer is available)
        if mlint_analyzer.is_available():
            publish_diagnostics(server, uri, mlint_analyzer, file_path)

    @server.feature("textDocument/didClose")
    async def did_close(params: DidCloseTextDocumentParams) -> None:
        """Handle textDocument/didClose notification.

        Args:
            params (DidCloseTextDocumentParams): Close parameters
                containing document URI
        """
        uri = params.text_document.uri
        file_path = _uri_to_path(uri)

        logger.debug(f"Document closed: {file_path}")

        # Remove from document store
        document_store.remove_document(uri)

        # Added for v0.2.6: Remove symbols from table
        symbol_table.remove_symbols_by_uri(uri)

    @server.feature("textDocument/didChange")
    async def did_change(params: DidChangeTextDocumentParams) -> None:
        """Handle textDocument/didChange notification.

        Args:
            params (DidChangeTextDocumentParams): Change parameters
                containing document URI and content changes
        """
        text_doc = params.text_document
        uri = text_doc.uri
        file_path = _uri_to_path(uri)

        logger.debug(f"Document changed: {file_path}")

        # Get current document
        current_doc = document_store.get_document(uri)

        if current_doc is None:
            logger.warning(f"Document changed but not in store: {file_path}")
            return

        # Apply changes to document content
        new_content = current_doc.content
        for change in params.content_changes:
            # Extract text range and new text
            if hasattr(change, "range") and change.range:
                # Partial change - replace range with new text
                # For simplicity, just append the new text
                # A proper implementation would handle range replacement
                new_content += change.text
            else:
                # Full document change
                new_content = change.text

        # Update document store
        document_store.update_document_content(uri, new_content)

        # Trigger analysis with debouncing
        _trigger_analysis_with_debounce(server, uri, file_path)

    def _uri_to_path(uri: str) -> str:
        """
        Convert file URI to local file path.

        Args:
            uri (str): File URI (e.g., "file:///C:/path/to/file.m")

        Returns:
            str: Local file path
        """
        # Parse URI
        parsed = urlparse(uri)

        # Handle file:/// URIs
        if parsed.scheme == "file":
            # Get the path and decode URL encoding
            path = unquote(parsed.path)

            # Remove leading slash on Windows (file:///C:/path -> C:/path)
            if path.startswith("/") and len(path) > 2 and path[2] == ":":
                path = path[1:]

            return str(Path(path))

        return uri


def _trigger_analysis_with_debounce(
    server: LanguageServer,
    uri: str,
    file_path: str,
    debounce_ms: int = 500,
) -> None:
    """
    Trigger analysis with debouncing to avoid
    excessive analysis on rapid changes.

    Args:
        server (LanguageServer): LSP server instance
        uri (str): Document URI
        file_path (str): Local file path
        debounce_ms (int): Debounce time in milliseconds
    """
    # Simple debounce implementation
    # In production, use a proper debounce library
    import asyncio

    async def analyze_task():
        logger.debug(f"Triggering analysis for: {file_path}")
        if mlint_analyzer.is_available():
            publish_diagnostics(server, uri, mlint_analyzer, file_path)

    # Cancel any existing task and schedule new one
    if hasattr(_trigger_analysis_with_debounce, "_task"):
        try:
            _trigger_analysis_with_debounce._task.cancel()
        except Exception:
            pass

    async def debounced_analyze():
        await asyncio.sleep(debounce_ms / 1000)
        await analyze_task()

    _trigger_analysis_with_debounce._task = asyncio.create_task(  # type: ignore[attr-defined]
        debounced_analyze()
    )


def update_analyzer(analyzer: MlintAnalyzer) -> None:
    """
    Update the analyzer used by document sync handlers.

    Args:
        analyzer (MlintAnalyzer): New analyzer instance
    """
    global mlint_analyzer
    mlint_analyzer = analyzer
    logger.info(f"Document sync analyzer updated to: {analyzer.get_name()}")
