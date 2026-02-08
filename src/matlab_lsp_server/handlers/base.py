"""Base handler class for LSP methods."""

from abc import ABC, abstractmethod
from typing import Any

from pygls.lsp.server import LanguageServer


class BaseHandler(ABC):
    """Abstract base class for all LSP method handlers.

    Provides a common interface for implementing LSP features
    and ensures consistent handler structure across the project.
    """

    def __init__(self, server: LanguageServer):
        """Initialize handler with server instance.

        Args:
            server: The LanguageServer instance
        """
        self.server = server

    @property
    @abstractmethod
    def method_name(self) -> str:
        """Get the LSP method name this handler implements.

        Returns:
            The LSP method name (e.g., 'textDocument/completion')
        """
        pass

    @abstractmethod
    async def handle(self, *args: Any, **kwargs: Any) -> Any:
        """Handle the LSP method call.

        Args:
            *args: Positional arguments from LSP request
            **kwargs: Keyword arguments from LSP request

        Returns:
            The LSP response object
        """
        pass

    def __repr__(self) -> str:
        """Get string representation of handler.

        Returns:
            String representation with handler name
        """
        return f"{self.__class__.__name__}(method='{self.method_name}')"
