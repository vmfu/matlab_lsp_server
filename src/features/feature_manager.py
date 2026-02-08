"""
Feature Manager for LSP capabilities.

This module provides a centralized way to manage and configure
LSP server capabilities.
"""

from lsprotocol.types import (
    CodeActionOptions,
    CompletionOptions,
    ServerCapabilities,
    SignatureHelpOptions,
    TextDocumentSyncKind,
    TextDocumentSyncOptions,
    WorkspaceSymbolOptions,
)

from ..utils.logging import get_logger

logger = get_logger(__name__)


class FeatureManager:
    """Manages LSP server capabilities and features."""

    def __init__(self):
        """Initialize FeatureManager with default capabilities."""
        self._capabilities: ServerCapabilities = ServerCapabilities()

        # Configure default features
        self._configure_text_document_sync()
        self._configure_completion()
        self._configure_hover()
        self._configure_document_symbols()
        self._configure_signature_help()
        self._configure_definition()
        self._configure_references()
        self._configure_code_actions()
        self._configure_document_formatting()
        self._configure_workspace_symbols()

    def _configure_text_document_sync(self):
        """Configure text document synchronization."""
        self._capabilities.text_document_sync = TextDocumentSyncOptions(
            open_close=True,
            change=TextDocumentSyncKind.Incremental,
            will_save=True,
            will_save_wait_until=True,
        )
        logger.debug("Text document sync configured: Incremental")

    def _configure_completion(self, enable: bool = True):
        """Configure completion feature."""
        if enable:
            self._capabilities.completion_provider = CompletionOptions(
                resolve_provider=False,
                trigger_characters=[".", "("],
            )
            logger.debug("Completion provider enabled")
        else:
            self._capabilities.completion_provider = None
            logger.debug("Completion provider disabled")

    def _configure_hover(self, enable: bool = True):
        """Configure hover feature."""
        if enable:
            self._capabilities.hover_provider = True
            logger.debug("Hover provider enabled")
        else:
            self._capabilities.hover_provider = False
            logger.debug("Hover provider disabled")

    def _configure_document_symbols(self, enable: bool = True):
        """Configure document symbols feature."""
        if enable:
            self._capabilities.document_symbol_provider = True
            logger.debug("Document symbol provider enabled")
        else:
            self._capabilities.document_symbol_provider = False
            logger.debug("Document symbol provider disabled")

    def _configure_signature_help(self, enable: bool = True):
        """Configure signature help feature."""
        if enable:
            self._capabilities.signature_help_provider = SignatureHelpOptions(
                trigger_characters=["(", ","],
                retrigger_characters=[")"],
            )
            logger.debug("Signature help provider enabled")
        else:
            self._capabilities.signature_help_provider = None
            logger.debug("Signature help provider disabled")

    def _configure_definition(self, enable: bool = True):
        """Configure go-to-definition feature."""
        if enable:
            self._capabilities.definition_provider = True
            logger.debug("Definition provider enabled")
        else:
            self._capabilities.definition_provider = False
            logger.debug("Definition provider disabled")

    def _configure_references(self, enable: bool = True):
        """Configure find-references feature."""
        if enable:
            self._capabilities.references_provider = True
            logger.debug("References provider enabled")
        else:
            self._capabilities.references_provider = False
            logger.debug("References provider disabled")

    def _configure_code_actions(self, enable: bool = True):
        """Configure code actions feature."""
        if enable:
            self._capabilities.code_action_provider = CodeActionOptions(
                code_action_kinds=["quickfix", "refactor", "source"]
            )
            logger.debug("Code action provider enabled")
        else:
            self._capabilities.code_action_provider = None
            logger.debug("Code action provider disabled")

    def _configure_document_formatting(self, enable: bool = True):
        """Configure document formatting feature."""
        if enable:
            self._capabilities.document_formatting_provider = True
            logger.debug("Document formatting provider enabled")
        else:
            self._capabilities.document_formatting_provider = False
            logger.debug("Document formatting provider disabled")

    def _configure_workspace_symbols(self, enable: bool = True):
        """Configure workspace symbols feature."""
        if enable:
            self._capabilities.workspace_symbol_provider = (
                WorkspaceSymbolOptions()
            )
            logger.debug("Workspace symbol provider enabled")
        else:
            self._capabilities.workspace_symbol_provider = None
            logger.debug("Workspace symbol provider disabled")

    def get_capabilities(self) -> ServerCapabilities:
        """
        Get the configured server capabilities.

        Returns:
            ServerCapabilities: The LSP server capabilities object
        """
        logger.debug("Returning server capabilities")
        return self._capabilities

    def enable_all_features(self):
        """Enable all LSP features."""
        self._configure_completion(enable=True)
        self._configure_hover(enable=True)
        self._configure_document_symbols(enable=True)
        self._configure_signature_help(enable=True)
        self._configure_definition(enable=True)
        self._configure_references(enable=True)
        self._configure_code_actions(enable=True)
        self._configure_document_formatting(enable=True)
        self._configure_workspace_symbols(enable=True)
        logger.info("All LSP features enabled")

    def disable_all_features(self):
        """Disable all LSP features (keep text sync)."""
        self._configure_completion(enable=False)
        self._configure_hover(enable=False)
        self._configure_document_symbols(enable=False)
        self._configure_signature_help(enable=False)
        self._configure_definition(enable=False)
        self._configure_references(enable=False)
        self._configure_code_actions(enable=False)
        self._configure_document_formatting(enable=False)
        self._configure_workspace_symbols(enable=False)
        logger.info("All LSP features disabled")
