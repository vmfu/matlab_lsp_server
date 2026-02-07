"""
Document Symbol Handler for MATLAB LSP Server.

This module implements textDocument/documentSymbol to provide
hierarchical document structure (outline) for MATLAB files.
"""

from typing import Any, Dict, List

from lsprotocol.types import (
    DocumentSymbol,
    SymbolInformation,
    SymbolKind,
)
from pygls.server import LanguageServer

from ..parser.models import ClassInfo, FunctionInfo, ParseResult
from ..utils.logging import get_logger
from ..utils.symbol_table import Symbol, SymbolTable, get_symbol_table

logger = get_logger(__name__)


class DocumentSymbolHandler:
    """Handler for document symbols in MATLAB LSP server."""

    def __init__(self, symbol_table: SymbolTable = None):
        """Initialize document symbol handler.

        Args:
            symbol_table (SymbolTable): Symbol table instance
        """
        self._symbol_table = symbol_table if symbol_table else get_symbol_table()
        logger.debug("DocumentSymbolHandler initialized")

    def provide_document_symbols(
        self,
        server: LanguageServer,
        file_uri: str,
    ) -> List[DocumentSymbol]:
        """
        Provide hierarchical document symbols for a file.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI

        Returns:
            List[DocumentSymbol]: Hierarchical document symbols
        """
        logger.debug(f"Providing document symbols for {file_uri}")

        # Get symbols from table
        file_symbols = self._symbol_table.get_symbols_by_uri(file_uri)

        # Convert to DocumentSymbol format with hierarchy
        document_symbols = self._create_document_symbols(file_symbols)

        logger.debug(f"Returning {len(document_symbols)} document symbols")

        return document_symbols

    def _create_document_symbols(
        self,
        symbols: List[Symbol]
    ) -> List[DocumentSymbol]:
        """
        Create hierarchical document symbols from symbol list.

        Args:
            symbols (List[Symbol]): List of symbols

        Returns:
            List[DocumentSymbol]: Hierarchical document symbols
        """
        # Group symbols by kind
        classes = [s for s in symbols if s.kind == "class"]
        functions = [s for s in symbols if s.kind == "function"]
        methods = [s for s in symbols if s.kind == "method"]
        variables = [s for s in symbols if s.kind == "variable"]

        # Build hierarchy: classes contain methods
        document_symbols = []

        # Add classes with their methods
        for cls in classes:
            # Find methods belonging to this class
            class_methods = [m for m in methods if m.scope == cls.name]

            # Create class document symbol
            class_symbol = self._create_document_symbol(
                cls.name,
                "class",
                cls.detail or "class",
                cls.line,
                cls.column,
                cls.name,
                children=self._methods_to_document_symbols(class_methods),
            )
            document_symbols.append(class_symbol)

        # Add standalone functions (not nested, not in class)
        for func in functions:
            # Function is standalone if it's not in a class scope
            # and doesn't have a parent function in its scope
            is_nested = func.scope and func.scope != "global" and func.scope != ""
            is_in_class = any(c.name == func.scope for c in classes)

            if not is_in_class:
                # Create function document symbol
                func_symbol = self._create_document_symbol(
                    func.name,
                    "function",
                    func.detail,
                    func.line,
                    func.column,
                    func.name,
                    children=self._find_nested_functions(functions, func.name),
                )
                document_symbols.append(func_symbol)

        # Add top-level variables
        for var in variables:
            if var.scope == "global":
                var_symbol = self._create_document_symbol(
                    var.name,
                    "variable",
                    var.detail or "variable",
                    var.line,
                    var.column,
                    var.name,
                    children=[],
                )
                document_symbols.append(var_symbol)

        return document_symbols

    def _create_document_symbol(
        self,
        name: str,
        kind: str,
        detail: str,
        line: int,
        column: int,
        selection_text: str,
        children: List[DocumentSymbol] = None
    ) -> DocumentSymbol:
        """
        Create a DocumentSymbol with proper range.

        Args:
            name (str): Symbol name
            kind (str): Symbol kind
            detail (str): Symbol detail
            line (int): Line number
            column (int): Column number
            selection_text (str): Text for selection range
            children (List[DocumentSymbol]): Child symbols

        Returns:
            DocumentSymbol: Document symbol object
        """
        # Calculate range
        range_obj = {
            "start": {
                "line": line - 1,  # LSP is 0-based
                "character": column - 1,
            },
            "end": {
                "line": line,  # Approximate
                "character": column + len(name),
            },
        }

        # Calculate selection range (same as range for now)
        selection_range_obj = range_obj

        return DocumentSymbol(
            name=name,
            kind=self._map_symbol_kind_to_symbol_kind(kind),
            detail=detail,
            range=range_obj,
            selection_range=selection_range_obj,
            children=children or [],
        )

    def _methods_to_document_symbols(
        self,
        methods: List[Symbol]
    ) -> List[DocumentSymbol]:
        """
        Convert method symbols to DocumentSymbol list.

        Args:
            methods (List[Symbol]): List of method symbols

        Returns:
            List[DocumentSymbol]: Document symbols for methods
        """
        doc_symbols = []

        for method in methods:
            method_symbol = self._create_document_symbol(
                method.name,
                "method",
                method.detail,
                method.line,
                method.column,
                method.name,
                children=[],  # Methods don't have children (simplified)
            )
            doc_symbols.append(method_symbol)

        return doc_symbols

    def _find_nested_functions(
        self,
        functions: List[Symbol],
        parent_name: str
    ) -> List[DocumentSymbol]:
        """
        Find nested functions for a parent function.

        Args:
            functions (List[Symbol]): List of function symbols
            parent_name (str): Parent function name

        Returns:
            List[DocumentSymbol]: Nested function symbols
        """
        # Nested functions have parent function as scope
        nested = [f for f in functions if f.scope == parent_name]

        nested_symbols = []

        for func in nested:
            func_symbol = self._create_document_symbol(
                func.name,
                "function",
                func.detail,
                func.line,
                func.column,
                func.name,
                children=self._find_nested_functions(functions, func.name),
            )
            nested_symbols.append(func_symbol)

        return nested_symbols

    def _map_symbol_kind_to_symbol_kind(
        self,
        symbol_kind: str
    ) -> SymbolKind:
        """Map symbol kind to LSP SymbolKind."""
        kind_map = {
            "function": SymbolKind.Function,
            "method": SymbolKind.Method,
            "class": SymbolKind.Class,
            "variable": SymbolKind.Variable,
            "property": SymbolKind.Property,
        }
        return kind_map.get(symbol_kind, SymbolKind.Variable)


# Global document symbol handler instance
_document_symbol_handler = None


def get_document_symbol_handler() -> DocumentSymbolHandler:
    """Get or create global DocumentSymbolHandler instance."""
    global _document_symbol_handler
    if _document_symbol_handler is None:
        _document_symbol_handler = DocumentSymbolHandler()
        logger.debug("DocumentSymbolHandler instance created")
    return _document_symbol_handler
