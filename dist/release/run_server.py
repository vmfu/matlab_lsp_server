#!/usr/bin/env python3
"""
LSP MATLAB Server - Launcher Script

This script starts LSP MATLAB Server with proper configuration.
"""

import sys
import os

# Add src to path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

# Import server
from server import __version__

def main():
    """Main entry point for LSP MATLAB Server launcher."""
    print(f"LSP MATLAB Server v{__version__}")

    # Check command line arguments
    if len(sys.argv) > 1:
        if '--version' in sys.argv or '-v' in sys.argv:
            print(f"Version: {__version__}")
            print(f"Python: {sys.version}")
            sys.exit(0)

    print("Starting Language Server...")
    print("Use --stdio for stdio mode (recommended)")
    print("Use --tcp <port> for TCP mode")

    # Import and run server
    from server import start_server
    start_server()

if __name__ == "__main__":
    main()
