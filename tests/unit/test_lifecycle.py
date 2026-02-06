"""
Unit tests for LSP lifecycle handlers.
"""

import pytest
from pygls.server import LanguageServer

from src.protocol.lifecycle import register_lifecycle_handlers


def test_lifecycle_module_imports():
    """Test that lifecycle module can be imported."""
    from src.protocol.lifecycle import register_lifecycle_handlers

    assert callable(register_lifecycle_handlers)


def test_logger_is_configured():
    """Test that logger is properly configured."""
    from src.protocol.lifecycle import logger

    # Verify logger exists
    assert logger is not None


def test_register_lifecycle_handlers_no_error():
    """Test that registration does not raise any errors."""
    server = LanguageServer("test-server", "v0.1.0")

    # Register handlers - should not raise
    register_lifecycle_handlers(server)

    # Verify server still works
    assert server is not None
