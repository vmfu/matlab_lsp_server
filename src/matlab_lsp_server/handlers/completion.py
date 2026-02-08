"""
Completion Handler for MATLAB LSP Server.

This module implements textDocument/completion to provide
code completion suggestions for MATLAB code.
"""

from typing import Any, Dict, List, Optional

from lsprotocol.types import CompletionItem, CompletionItemKind, CompletionList
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.utils.logging import get_logger
from matlab_lsp_server.utils.symbol_table import Symbol, SymbolTable, get_symbol_table

logger = get_logger(__name__)


class CompletionHandler:
    """Handler for code completion in MATLAB LSP server."""

    # Built-in MATLAB functions and keywords
    BUILTIN_COMPLETIONS: Dict[str, Dict[str, Any]] = {
        # Math functions
        "sin": {"kind": CompletionItemKind.Function, "detail": "math.sin"},
        "cos": {"kind": CompletionItemKind.Function, "detail": "math.cos"},
        "tan": {"kind": CompletionItemKind.Function, "detail": "math.tan"},
        "sqrt": {"kind": CompletionItemKind.Function, "detail": "math.sqrt"},
        "abs": {"kind": CompletionItemKind.Function, "detail": "math.abs"},
        # Array operations
        "zeros": {
            "kind": CompletionItemKind.Function,
            "detail": "creates zero array",
        },
        "ones": {
            "kind": CompletionItemKind.Function,
            "detail": "creates ones array",
        },
        "eye": {
            "kind": CompletionItemKind.Function,
            "detail": "creates identity matrix",
        },
        "size": {
            "kind": CompletionItemKind.Function,
            "detail": "array dimensions",
        },
        "length": {
            "kind": CompletionItemKind.Function,
            "detail": "array length",
        },
        # Control flow
        "if": {"kind": CompletionItemKind.Keyword, "detail": "conditional"},
        "else": {"kind": CompletionItemKind.Keyword, "detail": "alternative"},
        "elseif": {
            "kind": CompletionItemKind.Keyword,
            "detail": "conditional",
        },
        "for": {"kind": CompletionItemKind.Keyword, "detail": "loop"},
        "while": {"kind": CompletionItemKind.Keyword, "detail": "loop"},
        "end": {
            "kind": CompletionItemKind.Keyword,
            "detail": "block terminator",
        },
        "function": {
            "kind": CompletionItemKind.Keyword,
            "detail": "function definition",
        },
        "return": {
            "kind": CompletionItemKind.Keyword,
            "detail": "return value",
        },
        "break": {"kind": CompletionItemKind.Keyword, "detail": "exit loop"},
        "continue": {
            "kind": CompletionItemKind.Keyword,
            "detail": "next iteration",
        },
        # Built-in functions
        "disp": {"kind": CompletionItemKind.Function, "detail": "display"},
        "fprintf": {
            "kind": CompletionItemKind.Function,
            "detail": "print to file",
        },
        "input": {"kind": CompletionItemKind.Function, "detail": "user input"},
        "keyboard": {
            "kind": CompletionItemKind.Function,
            "detail": "debug mode",
        },
        "error": {
            "kind": CompletionItemKind.Function,
            "detail": "throw error",
        },
        "warning": {
            "kind": CompletionItemKind.Function,
            "detail": "issue warning",
        },
    }

    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        """Initialize completion handler.

        Args:
            symbol_table (SymbolTable): Symbol table instance
        """
        self._symbol_table = (
            symbol_table if symbol_table else get_symbol_table()
        )
        logger.debug("CompletionHandler initialized")

    def provide_completion(
        self, server: LanguageServer, file_uri: str, position: Any, prefix: str
    ) -> CompletionList:
        """
        Provide completion suggestions for a position in file.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            position (Any): Cursor position (Position or dict)
            prefix (str): Word prefix before cursor

        Returns:
            CompletionList: List of completion items
        """
        # Handle position as either Position object or dict
        line = (
            position.line
            if hasattr(position, "line")
            else position.get("line", 0)
        )
        character = (
            position.character
            if hasattr(position, "character")
            else position.get("character", 0)
        )

        logger.debug(
            f"Providing completion for {file_uri}:"
            f"({line}:{character}) "
            f"prefix: '{prefix}'"
        )

        # Collect completion candidates
        candidates = []

        # 1. Add symbols from current file
        file_symbols = self._symbol_table.get_symbols_by_uri(file_uri)
        candidates.extend(
            self._create_completion_items_from_symbols(file_symbols, prefix)
        )

        # 2. Add built-in MATLAB functions and keywords
        candidates.extend(self._create_completion_items_from_builtins(prefix))

        # 3. Rank candidates by relevance
        ranked_candidates = self._rank_candidates(candidates, prefix)

        # Limit to top 20 results
        limited_candidates = ranked_candidates[:20]

        logger.debug(
            f"Returning {len(limited_candidates)} completion candidates"
        )

        return CompletionList(
            is_incomplete=False,
            items=limited_candidates,
        )

    def _create_completion_items_from_symbols(
        self, symbols: List[Symbol], prefix: str
    ) -> List[CompletionItem]:
        """
        Create completion items from symbol list.

        Args:
            symbols (List[Symbol]): List of symbols
            prefix (str): Word prefix

        Returns:
            List[CompletionItem]: List of completion items
        """
        items = []

        for symbol in symbols:
            # Filter by prefix (case-insensitive)
            if prefix and prefix.lower() not in symbol.name.lower():
                continue

            # Determine kind based on symbol type
            kind = self._map_symbol_kind_to_completion_kind(symbol.kind)

            # Create completion item
            item = CompletionItem(
                label=symbol.name,
                kind=kind,
                detail=symbol.detail or symbol.kind,
                documentation=symbol.documentation,
            )

            # Add filter text (for LSP filtering)
            item.filter_text = symbol.name

            # Add sort text (for ranking)
            item.sort_text = symbol.name

            items.append(item)

        return items

    def _create_completion_items_from_builtins(
        self, prefix: str
    ) -> List[CompletionItem]:
        """
        Create completion items from built-in functions.

        Args:
            prefix (str): Word prefix

        Returns:
            List[CompletionItem]: List of completion items
        """
        items = []

        for name, info in self.BUILTIN_COMPLETIONS.items():
            # Filter by prefix (case-insensitive)
            if prefix and prefix.lower() not in name.lower():
                continue

            # Create completion item
            item = CompletionItem(
                label=name,
                kind=info["kind"],
                detail=info["detail"],
            )

            # Add filter text
            item.filter_text = name

            # Add sort text
            item.sort_text = name

            items.append(item)

        return items

    def _rank_candidates(
        self, candidates: List[CompletionItem], prefix: str
    ) -> List[CompletionItem]:
        """
        Rank completion candidates by relevance.

        Ranking criteria:
        1. Exact match with prefix
        2. Prefix match at start
        3. Partial match anywhere

        Args:
            candidates (List[CompletionItem]): Completion candidates
            prefix (str): Word prefix

        Returns:
            List[CompletionItem]: Ranked completion items
        """
        if not prefix:
            return candidates

        # Ensure sort_text is not None for sorting
        for candidate in candidates:
            label_lower = candidate.label.lower()
            prefix_lower = prefix.lower()

            # Exact match (highest score)
            if label_lower == prefix_lower:
                candidate.sort_text = f"0:{candidate.label}"
            # Prefix match at start
            elif label_lower.startswith(prefix_lower):
                candidate.sort_text = f"1:{candidate.label}"
            # Partial match anywhere (lower score)
            else:
                candidate.sort_text = f"2:{candidate.label}"

        # Sort by relevance (sort_text)
        # Use str() to handle Optional[str]
        ranked = sorted(candidates, key=lambda x: str(x.sort_text))

        return ranked

    def _map_symbol_kind_to_completion_kind(
        self, symbol_kind: str
    ) -> CompletionItemKind:
        """Map symbol kind to LSP CompletionItemKind."""
        kind_map = {
            "function": CompletionItemKind.Function,
            "method": CompletionItemKind.Method,
            "class": CompletionItemKind.Class,
            "variable": CompletionItemKind.Variable,
            "property": CompletionItemKind.Property,
        }
        return kind_map.get(symbol_kind, CompletionItemKind.Variable)


# Global completion handler instance
_completion_handler = None


def get_completion_handler() -> CompletionHandler:
    """Get or create global CompletionHandler instance."""
    global _completion_handler
    if _completion_handler is None:
        _completion_handler = CompletionHandler()
        logger.debug("CompletionHandler instance created")
    return _completion_handler
