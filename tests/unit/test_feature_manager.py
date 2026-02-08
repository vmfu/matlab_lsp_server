"""
Unit tests for FeatureManager.
"""

from lsprotocol.types import (
    CodeActionOptions,
    CompletionOptions,
    ServerCapabilities,
    SignatureHelpOptions,
    TextDocumentSyncOptions,
    WorkspaceSymbolOptions,
)

from src.features.feature_manager import FeatureManager


def test_feature_manager_initialization():
    """Test that FeatureManager initializes with default capabilities."""
    manager = FeatureManager()

    # Verify capabilities is not None
    assert manager._capabilities is not None
    assert isinstance(manager._capabilities, ServerCapabilities)


def test_text_document_sync_configured():
    """Test that text document sync is configured correctly."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify text document sync is configured
    assert capabilities.text_document_sync is not None
    assert isinstance(capabilities.text_document_sync, TextDocumentSyncOptions)
    assert capabilities.text_document_sync.open_close is True
    assert capabilities.text_document_sync.change.value == 2  # Incremental


def test_completion_provider_configured():
    """Test that completion provider is configured correctly."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify completion provider is configured
    assert capabilities.completion_provider is not None
    assert isinstance(capabilities.completion_provider, CompletionOptions)
    assert capabilities.completion_provider.resolve_provider is False
    assert capabilities.completion_provider.trigger_characters == [".", "("]


def test_hover_provider_enabled():
    """Test that hover provider is enabled by default."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify hover provider is enabled
    assert capabilities.hover_provider is True


def test_document_symbol_provider_enabled():
    """Test that document symbol provider is enabled by default."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify document symbol provider is enabled
    assert capabilities.document_symbol_provider is True


def test_signature_help_provider_configured():
    """Test that signature help provider is configured correctly."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify signature help provider is configured
    assert capabilities.signature_help_provider is not None
    assert isinstance(
        capabilities.signature_help_provider, SignatureHelpOptions
    )
    assert (
        capabilities.signature_help_provider.trigger_characters == ["(", ","]
    )
    assert capabilities.signature_help_provider.retrigger_characters == [")"]


def test_definition_provider_enabled():
    """Test that definition provider is enabled by default."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify definition provider is enabled
    assert capabilities.definition_provider is True


def test_references_provider_enabled():
    """Test that references provider is enabled by default."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify references provider is enabled
    assert capabilities.references_provider is True


def test_code_action_provider_configured():
    """Test that code action provider is configured correctly."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify code action provider is configured
    assert capabilities.code_action_provider is not None
    assert isinstance(capabilities.code_action_provider, CodeActionOptions)
    expected_kinds = ["quickfix", "refactor", "source"]
    assert (
        capabilities.code_action_provider.code_action_kinds == expected_kinds
    )


def test_document_formatting_provider_enabled():
    """Test that document formatting provider is enabled by default."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify document formatting provider is enabled
    assert capabilities.document_formatting_provider is True


def test_workspace_symbol_provider_configured():
    """Test that workspace symbol provider is configured correctly."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify workspace symbol provider is configured
    assert capabilities.workspace_symbol_provider is not None
    assert (
        isinstance(
            capabilities.workspace_symbol_provider, WorkspaceSymbolOptions
        )
    )


def test_get_capabilities_returns_server_capabilities():
    """Test that get_capabilities returns ServerCapabilities instance."""
    manager = FeatureManager()
    capabilities = manager.get_capabilities()

    # Verify return type
    assert isinstance(capabilities, ServerCapabilities)


def test_feature_manager_module_imports():
    """Test that FeatureManager module can be imported."""
    from src.features.feature_manager import FeatureManager, get_logger

    assert FeatureManager is not None
    assert get_logger is not None
