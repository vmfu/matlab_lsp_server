"""
References Handler for MATLAB LSP Server.

This module implements textDocument/references to provide
find-all-references functionality for MATLAB symbols.
"""

from typing import List, Optional

from lsprotocol.types import Location, Position, Range
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.utils.logging import get_logger
from matlab_lsp_server.utils.symbol_table import Symbol, SymbolTable, get_symbol_table

logger = get_logger(__name__)


class ReferencesHandler:
    """Handler for find-all-references in MATLAB LSP server."""

    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        """Initialize references handler.

        Args:
            symbol_table (SymbolTable): Symbol table instance
        """
        self._symbol_table = (
            symbol_table if symbol_table else get_symbol_table()
        )
        logger.debug("ReferencesHandler initialized")

    def provide_references(
        self,
        server: LanguageServer,
        file_uri: str,
        position: Position,
        include_declaration: bool = True,
    ) -> List[Location]:
        """
        Provide all reference locations for a symbol.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            position (Position): Cursor position (line, character)
            include_declaration (bool): Whether to include declaration

        Returns:
            List[Location]: List of reference locations
        """
        logger.debug(
            f"Providing references for {file_uri}:"
            f"({position.line}:{position.character}) "
            f"include_declaration: {include_declaration}"
        )

        # Get word at position (simplified - assume we already have it)
        # In practice, need to extract word from document
        # For now, we'll search all symbols

        # Search for symbols in current file
        file_symbols = self._symbol_table.get_symbols_by_uri(file_uri)

        # Search for symbol at position
        # For references, we need to know which symbol to find
        # This is simplified - in practice, parse word from document
        word = self._extract_word_at_position(file_symbols, position)

        if not word:
            logger.debug("No word found at position")
            return []

        # Search for all symbols with matching name
        all_symbols = self._symbol_table.get_all_symbols()
        matching_symbols = [
            s for s in all_symbols if s.name.lower() == word.lower()
        ]

        logger.debug(
            f"Found {len(matching_symbols)} symbols matching '{word}'"
        )

        # Create locations for all matches
        locations = [self._create_location(s) for s in matching_symbols]

        # Filter out declaration if needed
        if not include_declaration:
            # Keep only symbols that are not in the same file/position
            # This is simplified - should actually check if symbol
            # is definition. For now, we keep all except the first
            # (which is likely definition)
            if len(locations) > 0:
                locations = locations[1:]

        logger.debug(f"Returning {len(locations)} reference locations")

        return locations

    def _extract_word_at_position(
        self, symbols: List[Symbol], position: Position
    ) -> Optional[str]:
        """
        Extract word at cursor position.

        Args:
            symbols (list): List of symbols in file
            position (Position): Cursor position

        Returns:
            Optional[str]: Word at position
        """
        # Find symbol close to cursor position
        cursor_line = position.line + 1  # Convert from 0-based to 1-based

        for symbol in symbols:
            # Check if symbol is close to cursor position
            if abs(symbol.line - cursor_line) <= 5:
                return symbol.name

        return None

    def _create_location(self, symbol: Symbol) -> Location:
        """
        Create LSP Location from symbol.

        Args:
            symbol (Symbol): Symbol to create location for

        Returns:
            Location: LSP Location object
        """
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

        return location


# Global references handler instance
_references_handler = None


def get_references_handler() -> ReferencesHandler:
    """Get or create global ReferencesHandler instance."""
    global _references_handler
    if _references_handler is None:
        _references_handler = ReferencesHandler()
        logger.debug("ReferencesHandler instance created")
    return _references_handler
