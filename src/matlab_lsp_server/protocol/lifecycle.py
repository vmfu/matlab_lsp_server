"""
LSP Lifecycle Handlers for MATLAB LSP Server.

This module contains the core lifecycle handlers that manage the
server's lifecycle: initialize, shutdown, and exit.
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

# Import document sync handlers
from . import document_sync

logger = get_logger(__name__)

# Global feature manager instance
_feature_manager = None
_document_store = None
_mlint_analyzer = None


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
    global _document_store, _mlint_analyzer

    # Initialize document store and analyzer
    # (analyzer will be recreated in initialize)
    _document_store = DocumentStore()
    _mlint_analyzer = MlintAnalyzer()

    logger.info("DocumentStore initialized")
    logger.warning(
        "MlintAnalyzer will be reconfigured after initialization request"
    )

    # Register document synchronization handlers
    document_sync.register_document_sync_handlers(
        server, _document_store, _mlint_analyzer
    )
    logger.info("Document sync handlers registered")

    # Define and register initialize handler
    @server.feature("initialize")
    async def on_initialize(params: InitializeParams) -> InitializeResult:
        """Handle the initialize request."""
        client_name = (
            params.client_info.name if params.client_info else "unknown"
        )
        client_version = (
            params.client_info.version if params.client_info else "unknown"
        )
        logger.info(
            "Initialize request from client: "
            f"{client_name} v{client_version}"
        )

        # Extract configuration from initialization options
        # Priority: initializationOptions > config file > env > default
        matlab_path = None
        max_diagnostics = None

        if params.initialization_options:
            init_opts = params.initialization_options
            logger.debug(f"Initialization options: {init_opts}")

            # Support both flat and nested structures
            if isinstance(init_opts, dict):
                # Try nested structure: {matlab: {matlabPath: "..."}}
                if "matlab" in init_opts and isinstance(
                    init_opts["matlab"], dict
                ):
                    matlab_opts = init_opts["matlab"]
                    matlab_path = matlab_opts.get("matlabPath")
                    max_diagnostics = matlab_opts.get("maxDiagnostics")
                    logger.info(
                        f"Matlab options from init: "
                        f"path={matlab_path}, "
                        f"maxDiag={max_diagnostics}"
                    )
                # Try flat structure: {matlabPath: "..."}
                elif "matlabPath" in init_opts:
                    matlab_path = init_opts.get("matlabPath")
                    max_diagnostics = init_opts.get("maxDiagnostics")
                    logger.info(
                        f"Matlab options from flat init: "
                        f"path={matlab_path}, "
                        f"maxDiag={max_diagnostics}"
                    )
                # Try other common keys
                elif "matlab_path" in init_opts:
                    matlab_path = init_opts.get("matlab_path")
                    logger.info(
                        "Found matlab path from matlab_path key: "
                        f"{matlab_path}"
                    )

        # Recreate MlintAnalyzer with configured path
        global _mlint_analyzer
        _mlint_analyzer = MlintAnalyzer(matlab_path=matlab_path)

        # Check if mlint is available and log status
        if _mlint_analyzer.is_available():
            logger.info(
                f"MlintAnalyzer is available at: {_mlint_analyzer.mlint_path}"
            )
        else:
            logger.error(
                "MlintAnalyzer is NOT available! "
                f"matlab_path={matlab_path}, "
                f"mlint_path={_mlint_analyzer.mlint_path}"
            )

        # Update document_sync handlers with new analyzer
        document_sync.update_analyzer(_mlint_analyzer)
        logger.info("Document sync analyzer updated")

        # Get capabilities from FeatureManager
        feature_mgr = get_feature_manager()
        capabilities = feature_mgr.get_capabilities()

        logger.info("Server capabilities configured")
        result = InitializeResult(
            capabilities=capabilities,
            server_info={
                "name": "matlab-lsp",
                "version": "0.2.0"
            },
        )
        logger.info(f"Returning initialize result: {result}")
        return result

    # Define and register shutdown handler
    @server.feature("shutdown")
    async def on_shutdown(params: Any) -> None:
        """Handle the shutdown request."""
        logger.info("Shutdown request received")
        # Perform cleanup operations
        # TODO: Clear caches, close file handles, etc.
        logger.info("Server shutting down gracefully")

    # Define and register exit handler
    @server.feature("exit")
    async def on_exit(params: Any) -> None:
        """Handle the exit notification."""
        logger.info("Exit notification received")
        # Terminate the server process
        # pygls handles this automatically after this handler completes
        logger.info("Server process terminating")

    logger.info("Lifecycle handlers registered")
