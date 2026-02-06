#!/usr/bin/env python3
"""
LSP MATLAB Server - Launcher Script

This script starts the LSP MATLAB Server with proper configuration.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.server import __version__

def main():
    """Main entry point for LSP MATLAB Server."""
    print(f"LSP MATLAB Server v{__version__}")
    print("Starting Language Server...")
    print("Use --stdio for stdio mode (recommended)")
    print("Use --tcp <port> for TCP mode")

    # Import server
    from src.server import start_server

    # Start server
    start_server()

if __name__ == "__main__":
    main()
