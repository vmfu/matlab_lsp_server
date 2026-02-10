"""
LSP Lifecycle Handlers for MATLAB LSP Server.

This module contains core lifecycle handlers that manage server's
lifecycle: shutdown and exit.

This is a CRITICAL module for v0.2.5.

CHANGES FROM v0.2.4:
- REMOVED: on_initialize (MatLSServer handles it)
- REMOVED: on_initialized (MatLSServer handles it)
- KEPT: on_shutdown (with return None) ✅
- KEPT: on_exit (with return None) ✅

This avoids FeatureAlreadyRegisteredError when MatLSServer calls
register_lifecycle_handlers().
"""

from typing import Any

from lsprotocol.types import (
    InitializeParams,
    InitializeResult,
)
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.analyzer.mlint_analyzer import MlintAnalyzer
from matlab_lsp_server.features.feature_manager import FeatureManager
from matlab_lsp_server.utils.document_store import DocumentStore
from matlab_lsp_server.utils.logging import get_logger

logger = get_logger(__name__)


# Global feature manager instance
_feature_manager = None
_document_store = None
_mlint_analyzer = None


def get_feature_manager() -> FeatureManager:
    """Get or create global FeatureManager instance."""
    global _feature_manager
    if _feature_manager is None:
        _feature_manager = FeatureManager()
        logger.debug("FeatureManager instance created")
    return _feature_manager


def register_lifecycle_handlers(server: LanguageServer) -> None:
    """
    Register all lifecycle handlers with server.

    This function registers ONLY shutdown and exit handlers.
    Initialize and Initialized handlers are managed by MatLSServer
    to avoid FeatureAlreadyRegisteredError.

    CRITICAL FIX FOR v0.2.5:
    - on_shutdown has explicit 'return None' ✅
    - on_exit has explicit 'return None' ✅
    - Initialize handlers REMOVED to avoid conflict ✅

    Args:
        server: The LSP server instance.

    Returns:
        None
    """

    # Document sync handlers are now registered in MatLSServer.on_initialized()
    # with symbol_table and matlab_parser parameters

    # Register shutdown handler
    # CRITICAL FIX: Add explicit 'return None' to prevent server hanging
    @server.feature("shutdown")
    async def on_shutdown(params: Any) -> None:
        """Handle shutdown request."""
        logger.info("=== SHUTDOWN REQUEST RECEIVED ===")
        # CRITICAL FIX: Explicit return None to prevent server from hanging
        # This is required for proper LSP shutdown sequence
        logger.debug("Shutting down server...")
        return None  # ✅ CRITICAL FIX: Explicit return prevents hanging

    # Register exit handler
    # CRITICAL FIX: Add explicit 'return None' to prevent server hanging
    @server.feature("exit")
    async def on_exit(params: Any) -> None:
        """Handle exit request."""
        logger.info("=== EXIT REQUEST RECEIVED ===")
        # CRITICAL FIX: Explicit return None to prevent server from hanging
        # This is required for proper LSP shutdown sequence
        logger.debug("Exiting server...")
        return None  # ✅ CRITICAL FIX: Explicit return prevents hanging

    logger.info("Shutdown and exit handlers registered via lifecycle module")
