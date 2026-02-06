#!/usr/bin/env python3
"""
MATLAB LSP Server for Windows

Language Server Protocol implementation for MATLAB language support.
"""

import argparse
import sys
from typing import Optional

from pygls.protocol import LanguageServerProtocol
from pygls.server import LanguageServer

__version__ = "0.1.0"
__all__ = ["MatLSServer", "main"]


class MatLSServer(LanguageServer):
    """MATLAB Language Server.

    Extends pygls LanguageServer to provide MATLAB-specific language features.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def initialize_process(self):
        """Initialize the server and register LSP capabilities."""
        # TODO: Register handlers and capabilities
        pass


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
        """
    )

    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run in stdio mode (communicate via stdin/stdout)"
    )

    parser.add_argument(
        "--tcp",
        action="store_true",
        help="Run in TCP mode (for debugging)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=4389,
        help="Port for TCP mode (default: 4389)"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host for TCP mode (default: 127.0.0.1)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"MATLAB LSP Server v{__version__}"
    )

    return parser


def main() -> int:
    """Main entry point for the LSP server."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate arguments
    if not args.stdio and not args.tcp:
        parser.print_help()
        return 1

    if args.stdio and args.tcp:
        print("Error: Cannot specify both --stdio and --tcp", file=sys.stderr)
        return 1

    # Create server instance
    server = MatLSServer(
        "matlab-lsp",
        __version__
    )

    # Run server
    try:
        if args.stdio:
            print(f"MATLAB LSP Server v{__version__} starting in stdio mode...",
                  file=sys.stderr)
            server.start_io()
        elif args.tcp:
            print(f"MATLAB LSP Server v{__version__} starting on {args.host}:{args.port}...",
                  file=sys.stderr)
            server.start_tcp(args.host, args.port)

        return 0

    except KeyboardInterrupt:
        print("\nShutting down server...", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
