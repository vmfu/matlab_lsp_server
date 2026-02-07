"""
Definition Handler for MATLAB LSP Server.

This module implements textDocument/definition to provide
go-to-definition functionality for MATLAB symbols.
"""

from typing import List, Optional

from lsprotocol.types import (
    Location,
    Position,
    Range,
)
from pygls.server import LanguageServer

from ..utils.logging import get_logger
from ..utils.symbol_table import Symbol, SymbolTable, get_symbol_table

logger = get_logger(__name__)


class DefinitionHandler:
    """Handler for go-to-definition in MATLAB LSP server."""

    def __init__(self, symbol_table: SymbolTable = None):
        """Initialize definition handler.

        Args:
            symbol_table (SymbolTable): Symbol table instance
        """
        self._symbol_table = symbol_table if symbol_table else get_symbol_table()
        logger.debug("DefinitionHandler initialized")

    def provide_definition(
        self,
        server: LanguageServer,
        file_uri: str,
        position: Position,
        word: str = None
    ) -> Optional[Location]:
        """
        Provide definition location for a symbol at cursor.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            position (Position): Cursor position (line, character)
            word (str): Word at cursor position

        Returns:
            Optional[Location]: Definition location if found
        """
        logger.debug(
            f"Providing definition for {file_uri}:"
            f"({position.line}:{position.character}) "
            f"word: '{word}'"
        )

        if not word or len(word) == 0:
            return None

        # Search for symbol in current file
        file_symbols = self._symbol_table.get_symbols_by_uri(file_uri)
        symbol = self._find_symbol_at_position(
            file_symbols, position, word
        )

        if not symbol:
            # Also search in all files
            all_symbols = self._symbol_table.get_all_symbols()
            symbol = self._find_symbol_by_name(all_symbols, word)

        if not symbol:
            logger.debug(f"No definition found for '{word}'")
            return None

        # Create location
        location = self._create_location(symbol)

        logger.debug(
            f"Definition for '{word}': "
            f"{symbol.uri}:{symbol.line}:{symbol.column}"
        )

        return location

    def _find_symbol_at_position(
        self,
        symbols: list,
        position: Position,
        word: str
    ) -> Optional[Symbol]:
        """
        Find symbol at specific position.

        Args:
            symbols (list): List of symbols in file
            position (Position): Cursor position
            word (str): Word at cursor

        Returns:
            Optional[Symbol]: Symbol at position
        """
        # Find symbol matching word at position
        cursor_line = position.line + 1  # Convert from 0-based to 1-based

        for symbol in symbols:
            # Check if symbol name matches word
            if symbol.name.lower() != word.lower():
                continue

            # Check if symbol is close to cursor position
            # Allow some tolerance for multi-line functions
            if abs(symbol.line - cursor_line) <= 5:
                return symbol

        return None

    def _find_symbol_by_name(
        self,
        symbols: list,
        name: str
    ) -> Optional[Symbol]:
        """
        Find symbol by name (case-insensitive).

        Args:
            symbols (list): List of symbols
            name (str): Symbol name

        Returns:
            Optional[Symbol]: First matching symbol
        """
        for symbol in symbols:
            if symbol.name.lower() == name.lower():
                return symbol
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

    def provide_definitions(
        self,
        server: LanguageServer,
        file_uri: str,
        position: Position,
        word: str = None
    ) -> List[Location]:
        """
        Provide all definition locations for a symbol.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            position (Position): Cursor position (line, character)
            word (str): Word at cursor position

        Returns:
            List[Location]: List of definition locations
        """
        logger.debug(f"Providing definitions for '{word}'")

        if not word or len(word) == 0:
            return []

        # Search for all matching symbols
        all_symbols = self._symbol_table.get_all_symbols()

        # Find all symbols matching name (case-insensitive)
        matching_symbols = [
            s for s in all_symbols
            if s.name.lower() == word.lower()
        ]

        # Create locations for all matches
        locations = [self._create_location(s) for s in matching_symbols]

        logger.debug(
            f"Found {len(locations)} definitions for '{word}'"
        )

        return locations


# Global definition handler instance
_definition_handler = None


def get_definition_handler() -> DefinitionHandler:
    """Get or create global DefinitionHandler instance."""
    global _definition_handler
    if _definition_handler is None:
        _definition_handler = DefinitionHandler()
        logger.debug("DefinitionHandler instance created")
    return _definition_handler
