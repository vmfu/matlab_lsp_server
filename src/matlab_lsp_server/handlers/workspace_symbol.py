"""
Workspace Symbol Handler for MATLAB LSP Server.

This module implements workspace/symbol to provide
project-wide symbol search functionality.
"""

from typing import List, Optional

from lsprotocol.types import (
    Location,
    Position,
    Range,
    SymbolInformation,
    SymbolKind,
)
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.utils.logging import get_logger
from matlab_lsp_server.utils.symbol_table import Symbol, SymbolTable, get_symbol_table

logger = get_logger(__name__)


class WorkspaceSymbolHandler:
    """Handler for workspace symbols in MATLAB LSP server."""

    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        """Initialize workspace symbol handler.

        Args:
            symbol_table (SymbolTable): Symbol table instance
        """
        self._symbol_table = (
            symbol_table if symbol_table else get_symbol_table()
        )
        logger.debug("WorkspaceSymbolHandler initialized")

    def provide_workspace_symbols(
        self, server: LanguageServer, query: Optional[str] = None
    ) -> List[SymbolInformation]:
        """
        Provide workspace-wide symbols matching query.

        Args:
            server (LanguageServer): LSP server instance
            query (str): Search query (fuzzy matching)

        Returns:
            List[SymbolInformation]: List of matching symbols
        """
        logger.debug(f"Providing workspace symbols: " f"query='{query}'")

        # Get all symbols
        all_symbols = self._symbol_table.get_all_symbols()

        # Filter by query
        if query and len(query) > 0:
            matching_symbols = self._filter_symbols_by_query(
                all_symbols, query
            )
        else:
            matching_symbols = all_symbols

        # Convert to SymbolInformation format
        symbol_infos = [
            self._create_symbol_information(s) for s in matching_symbols
        ]

        logger.debug(f"Returning {len(symbol_infos)} workspace symbols")

        return symbol_infos

    def _filter_symbols_by_query(
        self, symbols: List[Symbol], query: str
    ) -> List[Symbol]:
        """
        Filter symbols by query (fuzzy matching).

        Args:
            symbols (List[Symbol]): List of symbols
            query (str): Search query

        Returns:
            List[Symbol]: Matching symbols
        """
        query_lower = query.lower()

        # Fuzzy matching: check if query is in symbol name
        matching = [s for s in symbols if query_lower in s.name.lower()]

        return matching

    def _create_symbol_information(self, symbol: Symbol) -> SymbolInformation:
        """
        Create SymbolInformation from symbol.

        Args:
            symbol (Symbol): Symbol to convert

        Returns:
            SymbolInformation: LSP SymbolInformation object
        """
        # Map symbol kind
        kind = self._map_symbol_kind_to_symbol_kind(symbol.kind)

        # Create range
        range_obj = Range(
            start=Position(
                line=symbol.line - 1,  # LSP is 0-based
                character=symbol.column - 1,
            ),
            end=Position(
                line=symbol.line - 1,
                character=symbol.column - 1 + len(symbol.name),
            ),
        )

        # Create location
        location = Location(
            uri=symbol.uri,
            range=range_obj,
        )

        # Create symbol information
        symbol_info = SymbolInformation(
            name=symbol.name,
            kind=kind,
            location=location,
            # Add container name (class name, etc.)
            container_name=symbol.scope if symbol.scope != "global" else None,
        )

        return symbol_info

    def _map_symbol_kind_to_symbol_kind(self, symbol_kind: str) -> SymbolKind:
        """Map symbol kind to LSP SymbolKind."""
        kind_map = {
            "function": SymbolKind.Function,
            "method": SymbolKind.Method,
            "class": SymbolKind.Class,
            "variable": SymbolKind.Variable,
            "property": SymbolKind.Property,
        }
        return kind_map.get(symbol_kind, SymbolKind.Variable)

    def filter_by_kind(
        self, symbols: List[Symbol], kinds: List[str]
    ) -> List[Symbol]:
        """
        Filter symbols by kind.

        Args:
            symbols (List[Symbol]): List of symbols
            kinds (List[str]): List of kinds to keep

        Returns:
            List[Symbol]: Filtered symbols
        """
        kind_set = set(kinds)
        return [s for s in symbols if s.kind in kind_set]


# Global workspace symbol handler instance
_workspace_symbol_handler = None


def get_workspace_symbol_handler() -> WorkspaceSymbolHandler:
    """Get or create global WorkspaceSymbolHandler instance."""
    global _workspace_symbol_handler
    if _workspace_symbol_handler is None:
        _workspace_symbol_handler = WorkspaceSymbolHandler()
        logger.debug("WorkspaceSymbolHandler instance created")
    return _workspace_symbol_handler
