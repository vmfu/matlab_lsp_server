"""
Hover Handler for MATLAB LSP Server.

This module implements textDocument/hover to provide
documentation and information about symbols at cursor position.
"""

from typing import List, Optional

from lsprotocol.types import Hover, Position, Range
from pygls.server import LanguageServer

from ..utils.logging import get_logger
from ..utils.symbol_table import Symbol, SymbolTable, get_symbol_table

logger = get_logger(__name__)


class HoverHandler:
    """Handler for hover information in MATLAB LSP server."""

    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        """Initialize hover handler.

        Args:
            symbol_table (SymbolTable): Symbol table instance
        """
        self._symbol_table = (
            symbol_table if symbol_table else get_symbol_table()
        )
        logger.debug("HoverHandler initialized")

    def provide_hover(
        self,
        server: LanguageServer,
        file_uri: str,
        position: Position,
        word: Optional[str] = None,
    ) -> Optional[Hover]:
        """
        Provide hover information for a position in file.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            position (Position): Cursor position (line, character)
            word (str): Word at cursor position

        Returns:
            Optional[Hover]: Hover information if symbol found
        """
        logger.debug(
            f"Providing hover for {file_uri}:"
            f"({position.line}:{position.character}) "
            f"word: '{word}'"
        )

        if not word or len(word) == 0:
            return None

        # Search for symbol in current file
        file_symbols = self._symbol_table.get_symbols_by_uri(file_uri)
        symbol = self._find_symbol_at_position(file_symbols, position, word)

        if not symbol:
            # Also search in all files for built-in functions
            all_symbols = self._symbol_table.get_all_symbols()
            symbol = self._find_symbol_by_name(all_symbols, word)

        if not symbol:
            logger.debug(f"No symbol found for '{word}'")
            return None

        # Create hover content
        hover_content = self._create_hover_content(symbol)

        logger.debug(f"Hover information for '{word}': {symbol.kind}")

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

        return Hover(
            contents=hover_content,
            range=range_obj,
        )

    def _find_symbol_at_position(
        self, symbols: List[Symbol], position: Position, word: str
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
        # Find symbol matching the word at the position
        # Simple heuristic: symbol on the same line or close to cursor
        cursor_line = position.line + 1  # Convert from 0-based to 1-based

        for symbol in symbols:
            # Check if symbol name matches the word
            if symbol.name.lower() != word.lower():
                continue

            # Check if symbol is close to cursor position
            # Allow some tolerance for multi-line functions
            if abs(symbol.line - cursor_line) <= 5:
                return symbol

        return None

    def _find_symbol_by_name(
        self, symbols: List[Symbol], name: str
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

    def _create_hover_content(self, symbol: Symbol) -> str:
        """
        Create hover content for symbol.

        Args:
            symbol (Symbol): Symbol to create hover for

        Returns:
            str: Hover content in Markdown format
        """
        # Build markdown content
        lines = []

        # Symbol kind and name
        kind_emoji = self._get_kind_emoji(symbol.kind)
        lines.append(f"**{kind_emoji} {symbol.kind}: {symbol.name}**")

        # Additional details
        if symbol.detail and symbol.detail != symbol.kind:
            lines.append(f"\n{symbol.detail}")

        # Documentation
        if symbol.documentation:
            lines.append(f"\n---\n\n{symbol.documentation}")

        # Join lines with newlines
        content = "\n".join(lines)

        return content

    def _get_kind_emoji(self, kind: str) -> str:
        """Get emoji for symbol kind."""
        emoji_map = {
            "function": "🔹",
            "method": "🔹",
            "class": "🏛",
            "property": "📋",
            "variable": "📝",
        }
        return emoji_map.get(kind, "📌")


# Global hover handler instance
_hover_handler = None


def get_hover_handler() -> HoverHandler:
    """Get or create global HoverHandler instance."""
    global _hover_handler
    if _hover_handler is None:
        _hover_handler = HoverHandler()
        logger.debug("HoverHandler instance created")
    return _hover_handler
