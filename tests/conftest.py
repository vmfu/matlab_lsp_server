"""
Pytest configuration and fixtures for MATLAB LSP Server.

This module provides common fixtures for testing LSP server components.
"""

import pytest
import tempfile
import asyncio
from pathlib import Path

from pygls.server import LanguageServer
from src.protocol.lifecycle import register_lifecycle_handlers
from src.protocol.document_sync import register_document_sync_handlers
from src.utils.document_store import DocumentStore
from src.analyzer.mlint_analyzer import MlintAnalyzer
from src.handlers.diagnostics import publish_diagnostics


@pytest.fixture
def server():
    """
    Create a LanguageServer instance for testing.

    Returns:
        LanguageServer: Test LSP server instance
    """
    svr = LanguageServer("matlab-lsp-test", "v0.1.0")

    # Register lifecycle handlers
    register_lifecycle_handlers(svr)

    # Create document store and mlint analyzer
    doc_store = DocumentStore()
    analyzer = MlintAnalyzer()

    # Register document sync handlers
    register_document_sync_handlers(svr, doc_store, analyzer)

    # Note: We don't register diagnostics here to avoid
    # actual LSP client calls in tests

    return svr


@pytest.fixture
def event_loop():
    """
    Create an event loop for async tests.

    Returns:
        asyncio.AbstractEventLoop: Event loop instance
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_m_file():
    """
    Create a temporary .m file for testing.

    Returns:
        Path: Path to temporary .m file
    """
    fd, path = tempfile.mkstemp(suffix=".m", text=True, delete=False)
    with open(fd, 'w') as f:
        f.write("function test_function()\nend")
    return Path(path)


@pytest.fixture
def temp_matlab_file():
    """
    Create a temporary .m file with MATLAB code for testing.

    Returns:
        Path: Path to temporary .m file with MATLAB code
    """
    fd, path = tempfile.mkstemp(suffix=".m", text=True, delete=False)
    with open(fd, 'w') as f:
        f.write(
            "function [x, y] = add(x, y)\n"
            "    result = x + y;\n"
            "end"
        )
    return Path(path)


@pytest.fixture
async def server_with_docs(server, temp_m_file, temp_matlab_file):
    """
    Create server with open documents for testing.

    Args:
        server: LanguageServer fixture
        temp_m_file: Temporary .m file fixture
        temp_matlab_file: Temporary MATLAB code file fixture

    Returns:
        Tuple[LanguageServer, str, str]: (server, simple_uri, matlab_uri)
    """
    # Open simple file
    simple_content = "x = 1;\n"
    server.lsp.did_open(
        text_document={
            "uri": "file:///simple.m",
            "version": 0,
            "languageId": "matlab",
            "text": simple_content,
        }
    )

    # Open MATLAB file
    server.lsp.did_open(
        text_document={
            "uri": "file:///code.m",
            "version": 0,
            "languageId": "matlab",
            "text": temp_matlab_file.read_text(),
        }
    )

    return (
        server,
        "file:///simple.m",
        "file:///code.m",
    )
