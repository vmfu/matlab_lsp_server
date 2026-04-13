"""
MATLAB Language Server built on pygls.

All handler registration happens in __init__, before start_io().
pygls 2.0 has builtin handlers for core protocol methods
(initialize, initialized, shutdown, exit, didOpen, didChange, didClose).
Our handlers extend the server for MATLAB-specific features.

Builtin didOpen/didChange/didClose are generators that yield to
user-registered handlers after workspace management. So registering
our custom handlers via @server.feature() chains them correctly.
"""

from pygls.lsp.server import LanguageServer

from matlab_lsp_server.analyzer.mlint_analyzer import MlintAnalyzer
from matlab_lsp_server.parser.matlab_parser import MatlabParser
from matlab_lsp_server.utils.config import ConfigManager
from matlab_lsp_server.utils.document_store import DocumentStore
from matlab_lsp_server.utils.logging import get_logger
from matlab_lsp_server.utils.symbol_table import get_symbol_table

logger = get_logger(__name__)


class MatLSServer(LanguageServer):
    """MATLAB Language Server."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._document_store = DocumentStore()
        self._symbol_table = get_symbol_table()
        self._matlab_parser = MatlabParser()

        matlab_path = self._get_matlab_path()
        self._mlint_analyzer = MlintAnalyzer(matlab_path=matlab_path)

        if self._mlint_analyzer.is_available():
            logger.info(
                "MlintAnalyzer available at: "
                f"{self._mlint_analyzer.mlint_path}"
            )
        else:
            logger.warning(
                "MlintAnalyzer NOT available. "
                f"matlab_path={matlab_path}"
            )

        self._register_handlers()

    def _get_matlab_path(self) -> str:
        """Read MATLAB path from config file or env var."""
        try:
            config = ConfigManager()
            path = config.get_matlab_path()
            if path:
                logger.info(f"MATLAB path from config: {path}")
                return path
        except Exception as e:
            logger.debug(f"Config load error: {e}")
        return ""

    def _register_handlers(self):
        """Register all LSP method handlers before start_io().

        pygls 2.0 builtins handle: initialize, initialized, shutdown,
        exit, textDocument/didOpen, didChange, didClose.
        Builtin document sync handlers are generators that yield to
        user handlers after workspace management, so our custom
        didOpen/didChange/didClose handlers chain correctly.
        """
        from matlab_lsp_server.protocol.document_sync import (
            register_document_sync_handlers,
        )
        from matlab_lsp_server.protocol.method_handlers import (
            register_method_handlers,
        )

        register_document_sync_handlers(
            self,
            self._document_store,
            self._mlint_analyzer,
            self._symbol_table,
            self._matlab_parser,
        )
        register_method_handlers(self)
        logger.info("All handlers registered")
