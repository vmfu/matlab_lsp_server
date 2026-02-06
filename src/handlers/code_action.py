"""
Code Action Handler for MATLAB LSP Server.

This module implements textDocument/codeAction to provide
quick fixes for MATLAB code issues.
"""

from typing import Optional, List
from lsprotocol.types import (
    CodeAction,
    CodeActionKind,
    Diagnostic,
)
from pygls.server import LanguageServer

from ..analyzer.base_analyzer import DiagnosticResult
from ..utils.logging import get_logger

logger = get_logger(__name__)


class CodeActionHandler:
    """Handler for code actions (quick fixes) in MATLAB LSP server."""

    def __init__(self):
        """Initialize code action handler."""
        logger.debug("CodeActionHandler initialized")

    def provide_code_actions(
        self,
        server: LanguageServer,
        file_uri: str,
        diagnostics: List[Diagnostic],
    ) -> List[CodeAction]:
        """
        Provide code actions (quick fixes) for diagnostics.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            diagnostics (List[Diagnostic]): List of diagnostics

        Returns:
            List[CodeAction]: List of code actions
        """
        logger.debug(
            f"Providing code actions for {file_uri}: "
            f"{len(diagnostics)} diagnostics"
        )

        code_actions = []

        # Create quick fixes for each diagnostic
        for diagnostic in diagnostics:
            # Skip if diagnostic doesn't have suggestions
            if not hasattr(diagnostic, 'data') or not diagnostic.data:
                continue

            quick_fixes = diagnostic.data.get('quickFixes', [])

            for fix in quick_fixes:
                # Create code action
                action = self._create_code_action(
                    diagnostic=diagnostic,
                    fix=fix,
                )
                code_actions.append(action)

        logger.debug(f"Returning {len(code_actions)} code actions")

        return code_actions

    def _create_code_action(
        self,
        diagnostic: Diagnostic,
        fix: dict
    ) -> CodeAction:
        """
        Create a CodeAction from diagnostic and fix suggestion.

        Args:
            diagnostic (Diagnostic): Diagnostic to fix
            fix (dict): Fix suggestion

        Returns:
            CodeAction: Code action object
        """
        # Create title
        title = fix.get('title', f'Fix: {diagnostic.message}')

        # Create code action
        action = CodeAction(
            title=title,
            kind=CodeActionKind.QuickFix,
            diagnostics=[diagnostic],
            is_preferred=True,
        )

        # Add edit if available
        if 'edit' in fix:
            action.edit = fix['edit']

        return action

    def generate_quick_fixes_from_diagnostic(
        self,
        diagnostic: Diagnostic
    ) -> List[dict]:
        """
        Generate quick fix suggestions from a diagnostic.

        Args:
            diagnostic (Diagnostic): Diagnostic

        Returns:
            List[dict]: List of fix suggestions
        """
        # Check diagnostic message for common patterns
        message = diagnostic.message.lower()
        fixes = []

        # Pattern 1: "Undefined function 'xxx'"
        if 'undefined function' in message:
            fixes.append({
                'title': 'Create function stub',
                'edit': None,  # Would need to generate code
            })

        # Pattern 2: "Missing semicolon"
        if 'semicolon' in message:
            fixes.append({
                'title': 'Add semicolon',
                'edit': None,  # Would need to add semicolon
            })

        # Pattern 3: "Variable 'xxx' may be unused"
        if 'unused' in message:
            fixes.append({
                'title': 'Remove variable',
                'edit': None,  # Would need to remove line
            })

        # Pattern 4: "End of input"
        if 'end of input' in message:
            fixes.append({
                'title': 'Add end statement',
                'edit': None,  # Would need to add end
            })

        return fixes

    def apply_code_action(
        self,
        server: LanguageServer,
        file_uri: str,
        action: CodeAction
    ) -> None:
        """
        Apply a code action to the file.

        Args:
            server (LanguageServer): LSP server instance
            file_uri (str): File URI
            action (CodeAction): Code action to apply
        """
        logger.debug(
            f"Applying code action for {file_uri}: "
            f"{action.title}"
        )

        # Apply the edit
        if action.edit:
            # Would need to implement WorkspaceEdit application
            # For now, just log
            logger.info(
                f"Applying edit to {file_uri}: "
                f"{len(action.edit.get('documentChanges', []))} changes"
            )


# Global code action handler instance
_code_action_handler = None


def get_code_action_handler() -> CodeActionHandler:
    """Get or create global CodeActionHandler instance."""
    global _code_action_handler
    if _code_action_handler is None:
        _code_action_handler = CodeActionHandler()
        logger.debug("CodeActionHandler instance created")
    return _code_action_handler
