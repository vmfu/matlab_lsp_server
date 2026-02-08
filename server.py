#!/usr/bin/env python3
"""
MATLAB LSP Server

Lightweight Language Server Protocol implementation for MATLAB language support.
"""

import argparse
import logging
import sys

from pathlib import Path

from src.matlab_server import MatLSServer
from src.utils.config import ensure_config_exists
from src.utils.logging import get_logger, setup_logging

__version__ = "0.1.0"
__all__ = ["main"]

# Global logger
logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="MATLAB Language Server Protocol Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run in stdio mode (for LSP clients)
  python server.py --stdio

  # Run in TCP mode (for debugging)
  python server.py --tcp --port 4389

  # Run with verbose logging
  python server.py --stdio --verbose

  # Show version
  python server.py --version
        """,
    )

    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run in stdio mode (communicate via stdin/stdout)",
    )

    parser.add_argument(
        "--tcp", action="store_true", help="Run in TCP mode (for debugging)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=4389,
        help="Port for TCP mode (default: 4389)",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host for TCP mode (default: 127.0.0.1)",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--no-init-config",
        action="store_true",
        help="Disable automatic config file creation",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"MATLAB LSP Server v{__version__}",
    )

    return parser


def main() -> int:
    """Main entry point for LSP server."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)
    logger.info(f"MATLAB LSP Server v{__version__} starting...")

    # Create default config if not exists
    if not args.no_init_config:
        config_path = Path.cwd() / ".matlab-lsprc.json"
        config_created = ensure_config_exists()
        if config_created:
            import json
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    matlab_path = config.get("matlabPath", "")
                    if matlab_path:
                        logger.info(
                            f"Auto-generated config with MATLAB path: {matlab_path}"
                        )
                    else:
                        logger.info(
                            "Auto-generated config. MATLAB not found. "
                            "Basic LSP features will work without MATLAB. "
                            "To enable full diagnostics, install MATLAB and set matlabPath."
                        )
            except Exception:
                logger.info("Auto-generated config created")
        else:
            logger.info("Using existing config file")

    # Validate arguments
    if not args.stdio and not args.tcp:
        parser.print_help()
        return 1

    if args.stdio and args.tcp:
        logger.error("Cannot specify both --stdio and --tcp")
        return 1

    # Create server instance
    # (uses custom MatLSServer with overridden lsp_initialize)
    server = MatLSServer("matlab-lsp", __version__)

    logger.info("Custom MatLSServer instance created")

    # Run server
    try:
        if args.stdio:
            logger.debug("Starting in stdio mode")
            server.start_io()
        elif args.tcp:
            logger.info(f"Starting TCP mode on " f"{args.host}:{args.port}")
            server.start_tcp(args.host, args.port)

        return 0

    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
