"""
LSP Lifecycle Handlers for MATLAB LSP Server.

This module contains the core lifecycle handlers that manage the
server's lifecycle: initialize, shutdown, and exit.
"""

from typing import Any, Optional
from lsprotocol.types import (
    InitializeParams,
    InitializeResult,
)
from pygls.server import LanguageServer

from src.utils.logging import get_logger
from src.features.feature_manager import FeatureManager

logger = get_logger(__name__)

# Global feature manager instance
_feature_manager = None


def get_feature_manager() -> FeatureManager:
    """Get or create the global FeatureManager instance."""
    global _feature_manager
    if _feature_manager is None:
        _feature_manager = FeatureManager()
        logger.debug("FeatureManager instance created")
    return _feature_manager


def register_lifecycle_handlers(server: LanguageServer) -> None:
    """Register all lifecycle handlers with the server.

    Args:
        server: The LSP server instance.
    """
    @server.feature("initialize")
    async def initialize(params: InitializeParams) -> InitializeResult:
        """Handle the initialize request.

        This is the first request sent by the client. The server responds
        with its capabilities and any initialization options.

        Args:
            params: Initialization parameters from the client.

        Returns:
            InitializeResult containing server capabilities.
        """
        logger.info(
            f"Initialize request from client: "
            f"{params.client_info.name if params.client_info else 'unknown'} "
            f"v{params.client_info.version if params.client_info else 'unknown'}"
        )

        # Get capabilities from FeatureManager
        feature_mgr = get_feature_manager()
        capabilities = feature_mgr.get_capabilities()

        logger.info("Server capabilities configured")
        return InitializeResult(
            capabilities=capabilities,
            server_info={
                "name": "matlab-lsp",
                "version": "0.1.0",
            }
        )

    @server.feature("shutdown")
    async def shutdown(params: Any) -> None:
        """Handle the shutdown request.

        The shutdown notification is sent from the client when the client
        wants to shut down the server but exit it gracefully.

        After shutdown is called, no further requests should be sent to
        the server except exit.

        Args:
            params: Shutdown parameters (empty).
        """
        logger.info("Shutdown request received")
        # Perform cleanup operations
        # TODO: Clear caches, close file handles, etc.
        logger.info("Server shutting down gracefully")

    @server.feature("exit")
    async def exit(params: Any) -> None:
        """Handle the exit notification.

        The exit notification is sent from the client when the client
        wants to completely shut down the server process.

        This should be called after shutdown to terminate the process.

        Args:
            params: Exit parameters (empty).
        """
        logger.info("Exit notification received")
        # Terminate the server process
        # pygls handles this automatically after this handler completes
        logger.info("Server process terminating")
