"""
Symbol Table for MATLAB LSP Server.

This module provides code indexing for LSP features like
completion, go-to-definition, etc.
"""

import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class Symbol:
    """Represents a code symbol (function, variable, class, etc.).

    Attributes:
        name (str): Symbol name
        kind (str): Symbol kind ("function", "variable", "class", "property", etc.)
        uri (str): File URI where symbol is defined
        line (int): Line number where symbol is defined
        column (int): Column number where symbol is defined
        detail (str): Additional details (e.g., function signature)
        documentation (Optional[str]): Symbol documentation (from comments)
        is_global (bool): Whether symbol is globally accessible
        scope (str): Scope name (e.g., parent function name)
    """
    name: str
    kind: str  # "function", "variable", "class", "property"
    uri: str
    line: int = 1
    column: int = 1
    detail: str = ""
    documentation: Optional[str] = None
    is_global: bool = False
    scope: str = ""


class SymbolTable:
    """Index of code symbols for LSP operations.

    Provides methods to add, remove, and search symbols.
    """

    # Symbol kinds
    KIND_FUNCTION = "function"
    KIND_VARIABLE = "variable"
    KIND_CLASS = "class"
    KIND_PROPERTY = "property"
    KIND_METHOD = "method"

    def __init__(self):
        """Initialize symbol table."""
        self._symbols: Dict[str, List[Symbol]] = {}
        # Key: (uri + ":" + name), Value: List of symbols
        # Use list to allow same name in different scopes
        self._file_hashes: Dict[str, str] = {}
        self._uri_to_symbols: Dict[str, List[Symbol]] = {}
        logger.debug("SymbolTable initialized")

    def add_symbol(
        self,
        name: str,
        kind: str,
        uri: str,
        line: int,
        column: int = 1,
        detail: str = "",
        documentation: Optional[str] = None,
        is_global: bool = False,
        scope: str = ""
    ) -> None:
        """
        Add a symbol to the table.

        Args:
            name (str): Symbol name
            kind (str): Symbol kind
            uri (str): File URI
            line (int): Line number
            column (int): Column number
            detail (str): Additional details
            documentation (str): Symbol documentation
            is_global (bool): Global flag
            scope (str): Symbol scope
        """
        symbol = Symbol(
            name=name,
            kind=kind,
            uri=uri,
            line=line,
            column=column,
            detail=detail,
            documentation=documentation,
            is_global=is_global,
            scope=scope,
        )

        # Add to index by name
        key = self._get_symbol_key(name, uri, scope)
        if key not in self._symbols:
            self._symbols[key] = []
        self._symbols[key].append(symbol)

        # Add to index by URI
        if uri not in self._uri_to_symbols:
            self._uri_to_symbols[uri] = []
        self._uri_to_symbols[uri].append(symbol)

        logger.debug(f"Added symbol: {name} ({kind}) at {uri}:{line}")

    def remove_symbols_by_uri(self, uri: str) -> int:
        """
        Remove all symbols from a specific file.

        Args:
            uri (str): File URI

        Returns:
            int: Number of symbols removed
        """
        if uri not in self._uri_to_symbols:
            return 0

        count = len(self._uri_to_symbols[uri])

        # Remove from URI index
        del self._uri_to_symbols[uri]

        # Remove from name index (find and delete all matching)
        keys_to_remove = [
            key for key in self._symbols.keys()
            if key.startswith(uri + ":")
        ]
        for key in keys_to_remove:
            del self._symbols[key]

        # Remove file hash
        if uri in self._file_hashes:
            del self._file_hashes[uri]

        logger.info(f"Removed {count} symbols from {uri}")
        return count

    def get_symbols_by_uri(self, uri: str) -> List[Symbol]:
        """
        Get all symbols from a specific file.

        Args:
            uri (str): File URI

        Returns:
            List[Symbol]: List of symbols in file
        """
        return self._uri_to_symbols.get(uri, []).copy()

    def search_symbols(
        self,
        query: str,
        uri: str = None,
        kind: str = None
    ) -> List[Symbol]:
        """
        Search for symbols by name.

        Args:
            query (str): Search query (symbol name)
            uri (str): Optional file URI to restrict search
            kind (str): Optional kind filter

        Returns:
            List[Symbol]: Matching symbols
        """
        results = []

        # Search in name index (fuzzy match)
        for key, symbols in self._symbols.items():
            for symbol in symbols:
                # Filter by URI if provided
                if uri and symbol.uri != uri:
                    continue

                # Filter by kind if provided
                if kind and symbol.kind != kind:
                    continue

                # Check if name matches (case-insensitive)
                if query.lower() in symbol.name.lower():
                    results.append(symbol)

        logger.debug(f"Search for '{query}': found {len(results)} symbols")
        return results

    def get_all_symbols(self) -> List[Symbol]:
        """
        Get all symbols in the table.

        Returns:
            List[Symbol]: All symbols
        """
        all_symbols = []
        for symbols in self._symbols.values():
            all_symbols.extend(symbols)
        return all_symbols

    def update_from_parse_result(
        self,
        uri: str,
        content: str,
        parse_result: Any,
    ) -> None:
        """
        Update symbol table from MATLAB parser result.

        Args:
            uri (str): File URI
            content (str): File content for hash
            parse_result (ParseResult): Parser result
        """
        # Check if content changed (using hash)
        new_hash = self._hash_content(content)
        old_hash = self._file_hashes.get(uri)

        # Skip if content hasn't changed
        if old_hash == new_hash:
            logger.debug(f"Content unchanged for {uri}, skipping update")
            return

        # Remove old symbols
        self.remove_symbols_by_uri(uri)

        # Store new hash
        self._file_hashes[uri] = new_hash

        # Add functions
        for func in parse_result.functions:
            detail = f"function {func.name}"
            if func.input_args:
                detail += f"({', '.join(func.input_args)})"
            if func.output_args:
                if len(func.output_args) > 1:
                    detail = f"[{', '.join(func.output_args)}] = {detail}"

            self.add_symbol(
                name=func.name,
                kind=self.KIND_FUNCTION,
                uri=uri,
                line=func.line,
                column=func.column,
                detail=detail,
                documentation=func.docstring,
                is_global=not func.is_nested,
                scope=func.parent_function if func.parent_function else "global",
            )

        # Add classes
        for cls in parse_result.classes:
            self.add_symbol(
                name=cls.name,
                kind=self.KIND_CLASS,
                uri=uri,
                line=cls.line,
                column=cls.column,
                detail=f"class {cls.name}",
                documentation=cls.docstring,
                is_global=True,
                scope="global",
            )

            # Add class methods
            for method in cls.methods:
                detail = f"function {method.name}"
                if method.input_args:
                    detail += f"({', '.join(method.input_args)})"
                if method.output_args:
                    detail = f"[{', '.join(method.output_args)}] = {detail}"

                self.add_symbol(
                    name=method.name,
                    kind=self.KIND_METHOD,
                    uri=uri,
                    line=method.line,
                    column=method.column,
                    detail=detail,
                    documentation=method.docstring,
                    is_global=False,
                    scope=cls.name,
                )

        # Add properties
        for prop in cls.properties:
            self.add_symbol(
                name=prop,
                kind=self.KIND_PROPERTY,
                uri=uri,
                line=cls.line + 1,  # Approximate (property section starts after classdef)
                column=1,
                detail=f"property {prop}",
                documentation=None,
                is_global=False,
                scope=cls.name,
            )

        logger.info(f"Updated symbol table for {uri}: "
                    f"{len(parse_result.functions)} functions, "
                    f"{len(parse_result.classes)} classes")

    def clear(self) -> None:
        """Clear all symbols."""
        count = len(self._uri_to_symbols)
        self._symbols.clear()
        self._uri_to_symbols.clear()
        self._file_hashes.clear()
        logger.info(f"Symbol table cleared: {count} symbols removed")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get symbol table statistics.

        Returns:
            Dict[str, Any]: Statistics (total symbols, symbols by kind, etc.)
        """
        all_symbols = self.get_all_symbols()
        stats = {
            "total": len(all_symbols),
            "by_kind": {},
            "by_uri": {uri: len(symbols) for uri, symbols in self._uri_to_symbols.items()},
        }

        # Count by kind
        for symbol in all_symbols:
            kind = symbol.kind
            if kind not in stats["by_kind"]:
                stats["by_kind"][kind] = 0
            stats["by_kind"][kind] += 1

        return stats

    def _get_symbol_key(self, name: str, uri: str, scope: str) -> str:
        """Generate key for symbol index."""
        return f"{uri}:{scope}:{name}"

    def _hash_content(self, content: str) -> str:
        """Generate hash of file content."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()


# Global symbol table instance
_symbol_table = None


def get_symbol_table() -> SymbolTable:
    """Get or create global SymbolTable instance."""
    global _symbol_table
    if _symbol_table is None:
        _symbol_table = SymbolTable()
        logger.debug("SymbolTable instance created")
    return _symbol_table
