"""
Custom Language Server for MATLAB with configuration via
initialized notification.
"""

from lsprotocol.types import (
    InitializedParams,
    InitializeParams,
    InitializeResult,
)
from pygls.lsp.server import LanguageServer

from matlab_lsp_server.analyzer.mlint_analyzer import MlintAnalyzer
from matlab_lsp_server.features.feature_manager import FeatureManager
from matlab_lsp_server.protocol import document_sync
from matlab_lsp_server.utils.document_store import DocumentStore
from matlab_lsp_server.utils.logging import get_logger

logger = get_logger(__name__)


class MatLSServer(LanguageServer):
    """MATLAB Language Server."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._document_store = None
        self._mlint_analyzer = None
        self._feature_manager = None

        # Store initialization params for later use
        self._init_params = None

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register all custom handlers."""

        # Intercept the initialize request to store params
        @self.feature("initialize")
        async def on_initialize(params: InitializeParams) -> InitializeResult:
            """Store initialization parameters for later use."""
            logger.info("=== STORING INITIALIZATION PARAMS ===")
            client_name = (
                params.client_info.name if params.client_info else "unknown"
            )
            client_version = (
                params.client_info.version if params.client_info else "unknown"
            )
            logger.info(
                "Initialize request from client: "
                f"{client_name} v{client_version}"
            )
            self._init_params = params

            # Return default result (will be overwritten later if needed)
            from matlab_lsp_server.features.feature_manager import FeatureManager

            fm = FeatureManager()
            return InitializeResult(
                capabilities=fm.get_capabilities(),
                server_info={
                    "name": "matlab-lsp",
                    "version": "0.2.0"
                },
            )

        # Handle initialized notification - this is called AFTER initialize
        @self.feature("initialized")
        async def on_initialized(params: InitializedParams):
            """Configure the server using stored initialization parameters."""
            logger.info("=== INITIALIZED NOTIFICATION RECEIVED ===")

            if self._init_params is None:
                logger.warning("No initialization params stored!")
                return

            # Initialize document store
            self._document_store = DocumentStore()
            logger.info("DocumentStore initialized")

            # Extract MATLAB path from initialization options
            matlab_path = None
            init_opts = self._init_params.initialization_options
            if init_opts:
                logger.debug(f"Initialization options: {init_opts}")
                if isinstance(init_opts, dict):
                    if "matlab" in init_opts and isinstance(
                        init_opts["matlab"], dict
                    ):
                        matlab_path = init_opts["matlab"].get("matlabPath")
                        logger.info(
                            "Found matlab path from nested config: "
                            f"{matlab_path}"
                        )
                    elif "matlabPath" in init_opts:
                        matlab_path = init_opts.get("matlabPath")
                        logger.info(
                            "Found matlab path from flat config: "
                            f"{matlab_path}"
                        )
                    elif "matlab_path" in init_opts:
                        matlab_path = init_opts.get("matlab_path")
                        logger.info(
                            "Found matlab path from matlab_path key: "
                            f"{matlab_path}"
                        )

            logger.info(f"Extracted matlab_path: {matlab_path}")

            # Initialize analyzer
            self._mlint_analyzer = MlintAnalyzer(matlab_path=matlab_path)
            logger.info(f"MlintAnalyzer created with path: {matlab_path}")

            if self._mlint_analyzer.is_available():
                logger.info(
                    "MlintAnalyzer is available at: "
                    f"{self._mlint_analyzer.mlint_path}"
                )
            else:
                logger.error(
                    "MlintAnalyzer is NOT available! "
                    f"matlab_path={matlab_path}, "
                    f"mlint_path={self._mlint_analyzer.mlint_path}"
                )

            # Initialize feature manager
            self._feature_manager = FeatureManager()

            # Register document sync handlers
            document_sync.register_document_sync_handlers(
                self, self._document_store, self._mlint_analyzer
            )
            logger.info("Document sync handlers registered")
            logger.info("=== SERVER FULLY CONFIGURED ===")
