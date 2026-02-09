"""
LSP Method Handlers for MATLAB LSP Server.

This module registers all LSP method handlers (completion, hover,
definition, etc.) with the server.
"""

from typing import Any

from lsprotocol.types import (
    CodeAction,
    CodeActionContext,
    CodeActionParams,
    CompletionContext,
    CompletionItem,
    CompletionList,
    CompletionParams,
    DefinitionParams,
    DocumentSymbol,
    DocumentSymbolParams,
    Hover,
    HoverParams,
    Location,
    LocationLink,
    ReferenceContext,
    ReferenceParams,
    SymbolInformation,
    TextDocumentPositionParams,
    WorkspaceSymbolParams,
)
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.handlers.code_action import (
    CodeActionHandler,
    get_code_action_handler,
)
from matlab_lsp_server.handlers.completion import (
    CompletionHandler,
    get_completion_handler,
)
from matlab_lsp_server.handlers.definition import (
    DefinitionHandler,
    get_definition_handler,
)
from matlab_lsp_server.handlers.document_symbol import (
    DocumentSymbolHandler,
    get_document_symbol_handler,
)
from matlab_lsp_server.handlers.formatting import (
    FormattingHandler,
    get_formatting_handler,
)
from matlab_lsp_server.handlers.hover import HoverHandler, get_hover_handler
from matlab_lsp_server.handlers.references import (
    ReferencesHandler,
    get_references_handler,
)
from matlab_lsp_server.handlers.workspace_symbol import (
    WorkspaceSymbolHandler,
    get_workspace_symbol_handler,
)
from matlab_lsp_server.utils.logging import get_logger
from matlab_lsp_server.utils.symbol_table import SymbolTable, get_symbol_table

logger = get_logger(__name__)


def register_method_handlers(server: LanguageServer) -> None:
    """Register all LSP method handlers with the server.

    Args:
        server (LanguageServer): The LSP server instance
    """
    logger.info("Registering LSP method handlers...")

    # Get handler instances
    completion_handler = get_completion_handler()
    hover_handler = get_hover_handler()
    definition_handler = get_definition_handler()
    references_handler = get_references_handler()
    document_symbol_handler = get_document_symbol_handler()
    workspace_symbol_handler = get_workspace_symbol_handler()
    code_action_handler = get_code_action_handler()
    formatting_handler = get_formatting_handler()

    # Register completion handler
    @server.feature("textDocument/completion")
    async def on_completion(params: CompletionParams) -> CompletionList:
        """Handle completion requests."""
        return await completion_handler.handle(params)

    # Register hover handler
    @server.feature("textDocument/hover")
    async def on_hover(params: HoverParams) -> Hover | None:
        """Handle hover requests."""
        return await hover_handler.handle(params)

    # Register definition handler
    @server.feature("textDocument/definition")
    async def on_definition(params: DefinitionParams) -> list[Location] | list[LocationLink] | None:
        """Handle go-to-definition requests."""
        return await definition_handler.handle(params)

    # Register references handler
    @server.feature("textDocument/references")
    async def on_references(params: ReferenceParams) -> list[Location] | None:
        """Handle find-references requests."""
        return await references_handler.handle(params)

    # Register document symbol handler
    @server.feature("textDocument/documentSymbol")
    async def on_document_symbols(params: DocumentSymbolParams) -> list[DocumentSymbol]:
        """Handle document outline requests."""
        return document_symbol_handler.provide_document_symbols(
            server, params.text_document.uri
        )

    # Register workspace symbol handler
    @server.feature("workspace/symbol")
    async def on_workspace_symbols(params: WorkspaceSymbolParams) -> list[SymbolInformation]:
        """Handle workspace search requests."""
        return await workspace_symbol_handler.handle(params)

    # Register code action handler
    @server.feature("textDocument/codeAction")
    async def on_code_actions(params: CodeActionParams) -> list[CodeAction] | None:
        """Handle code action requests."""
        return code_action_handler.handle(params)

    # Register document formatting handler
    @server.feature("textDocument/formatting")
    async def on_formatting(params: Any) -> list[Any] | None:
        """Handle document formatting requests."""
        return await formatting_handler.handle(params)

    logger.info("All LSP method handlers registered successfully")
