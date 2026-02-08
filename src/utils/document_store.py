"""
Document Store for LSP server.

This module provides a document store to manage
open documents and their contents.
"""

from dataclasses import dataclass
from typing import Dict, Optional

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class Document:
    """Represents an open document in the editor.

    Attributes:
        uri (str): Document URI
        path (str): Local file path
        content (str): Document text content
        version (int): Document version (for change tracking)
    """

    uri: str
    path: str
    content: str
    version: int = 0


class DocumentStore:
    """Store for managing open documents.

    Provides methods to add, remove, and retrieve documents.
    """

    def __init__(self):
        """Initialize empty document store."""
        self._documents: Dict[str, Document] = {}
        logger.debug("DocumentStore initialized")

    def add_document(self, uri: str, path: str, content: str) -> Document:
        """
        Add a document to the store.

        Args:
            uri (str): Document URI
            path (str): Local file path
            content (str): Document text content

        Returns:
            Document: Created or updated document
        """
        document = Document(
            uri=uri,
            path=path,
            content=content,
            version=0,
        )
        self._documents[uri] = document
        logger.debug(f"Document added to store: {path}")
        return document

    def get_document(self, uri: str) -> Optional[Document]:
        """
        Get a document by URI.

        Args:
            uri (str): Document URI

        Returns:
            Optional[Document]: Document if found, None otherwise
        """
        return self._documents.get(uri)

    def remove_document(self, uri: str) -> bool:
        """
        Remove a document from the store.

        Args:
            uri (str): Document URI

        Returns:
            bool: True if document was removed, False if not found
        """
        if uri in self._documents:
            document = self._documents.pop(uri)
            logger.debug(f"Document removed from store: {document.path}")
            return True
        return False

    def update_document_content(
        self, uri: str, new_content: str
    ) -> Optional[Document]:
        """
        Update document content and increment version.

        Args:
            uri (str): Document URI
            new_content (str): New document content

        Returns:
            Optional[Document]: Updated document if found, None otherwise
        """
        if uri in self._documents:
            document = self._documents[uri]
            document.content = new_content
            document.version += 1
            logger.debug(
                "Document content updated: "
                f"{document.path} (v{document.version})"
            )
            return document
        return None

    def get_all_documents(self) -> Dict[str, Document]:
        """
        Get all documents in the store.

        Returns:
            Dict[str, Document]: All documents indexed by URI
        """
        return self._documents.copy()

    def clear(self) -> None:
        """
        Clear all documents from the store.
        """
        count = len(self._documents)
        self._documents.clear()
        logger.info(f"DocumentStore cleared: {count} documents removed")
