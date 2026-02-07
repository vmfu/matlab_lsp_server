"""
Formatting Handler for MATLAB LSP Server.

This module implements textDocument/formatting to provide
code formatting functionality for MATLAB files.
"""

from typing import List

from lsprotocol.types import (
    DocumentFormattingOptions,
    TextEdit,
)
from pygls.server import LanguageServer

from ..utils.logging import get_logger

logger = get_logger(__name__)


class FormattingHandler:
    """Handler for code formatting in MATLAB LSP server."""

    def __init__(self):
        """Initialize formatting handler."""
        self._config = {
            "indent_size": 4,  # Default MATLAB indent
            "max_line_length": 80,  # Default line length
            "preserve_newlines": True,  # Preserve newlines
        }
        logger.debug("FormattingHandler initialized")

    def provide_formatting(
        self,
        server: LanguageServer,
        file_uri: str,
        content: str,
        options: DocumentFormattingOptions = None
    ) -> List[TextEdit]:
        """
        Provide code formatting edits for a file.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            content (str): File content to format
            options (DocumentFormattingOptions): Formatting options

        Returns:
            List[TextEdit]: List of text edits for formatting
        """
        logger.debug(
            f"Providing formatting for {file_uri}: "
            f"{len(content)} characters"
        )

        # Parse options
        tab_size = options.tab_size if options else self._config["indent_size"]
        insert_spaces = options.insert_spaces if options else True

        # Generate formatted content
        formatted_content = self._format_matlab_code(
            content,
            indent_size=tab_size,
            insert_spaces=insert_spaces,
        )

        # Calculate edits
        edits = []

        # If content is different, create edit
        if formatted_content != content:
            edit = TextEdit(
                range={
                    "start": {"line": 0, "character": 0},
                    "end": {
                        "line": len(content.split('\n')) - 1,
                        "character": len(content.split('\n')[-1]),
                    },
                },
                new_text=formatted_content,
            )
            edits.append(edit)

            logger.debug(f"Generated {len(edits)} formatting edits")
        else:
            logger.debug("Content already formatted, no edits needed")

        return edits

    def _format_matlab_code(
        self,
        content: str,
        indent_size: int = 4,
        insert_spaces: bool = True,
    ) -> str:
        """
        Format MATLAB code content.

        Args:
            content (str): Code content to format
            indent_size (int): Indentation size
            insert_spaces (bool): Whether to use spaces (True) or tabs (False)

        Returns:
            str: Formatted content
        """
        lines = content.split('\n')
        formatted_lines = []

        indent_level = 0
        indent_str = ' ' * indent_size if insert_spaces else '\t'

        for line in lines:
            # Check line type
            stripped_line = line.strip()

            # Skip empty lines
            if not stripped_line:
                formatted_lines.append(line)  # Preserve empty lines
                continue

            # Handle end statements (reduce indent)
            if stripped_line.startswith('end'):
                indent_level = max(0, indent_level - 1)

            # Handle classdef/function/for/while/if (increase indent)
            elif any(
                stripped_line.startswith(keyword)
                for keyword in ['classdef', 'function', 'for', 'while', 'if', 'else', 'elseif', 'try', 'catch']
            ):
                # Apply current indent
                formatted_line = indent_str * indent_level + stripped_line
                formatted_lines.append(formatted_line)
                indent_level += 1
                continue

            # Apply current indent
            formatted_line = indent_str * indent_level + stripped_line
            formatted_lines.append(formatted_line)

        # Join lines
        formatted_content = '\n'.join(formatted_lines)

        # Ensure trailing newline
        if not formatted_content.endswith('\n'):
            formatted_content += '\n'

        return formatted_content

    def set_config(self, config: dict):
        """
        Set formatting configuration.

        Args:
            config (dict): Configuration options
        """
        self._config.update(config)
        logger.debug(f"Formatting config updated: {config}")


# Global formatting handler instance
_formatting_handler = None


def get_formatting_handler() -> FormattingHandler:
    """Get or create global FormattingHandler instance."""
    global _formatting_handler
    if _formatting_handler is None:
        _formatting_handler = FormattingHandler()
        logger.debug("FormattingHandler instance created")
    return _formatting_handler
