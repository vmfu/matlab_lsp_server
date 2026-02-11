"""
Mlint Analyzer for MATLAB code.

This module provides integration with MATLAB's Code Analyzer (mlint.exe).
"""

import os
import platform
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from matlab_lsp_server.utils.logging import get_logger
from .base_analyzer import BaseAnalyzer, DiagnosticResult

logger = get_logger(__name__)


class MlintAnalyzer(BaseAnalyzer):
    """Analyzer for MATLAB code using mlint.exe.

    This analyzer calls MATLAB's mlint.exe tool to analyze
    .m files and parse -> output into structured diagnostics.
    """

    # Regex patterns to parse mlint output
    # Pattern 1: "L line (ID): message" (with -id flag)
    # Pattern 2: "L line: message" (simple format)
    # Note: The ID part can be like "C 5-10" or "FNDEF"
    MLINT_PATTERN_WITH_ID = re.compile(
        r"^L\s+(\d+)\s+\(([^)]+)\)\s*:\s*(.+)$", re.MULTILINE
    )
    MLINT_PATTERN_SIMPLE = re.compile(r"^L\s+(\d+)\s*:\s*(.+)$", re.MULTILINE)

    def __init__(self, matlab_path: Optional[str] = None):
        """Initialize MlintAnalyzer.

        Args:
            matlab_path (str): Path to MATLAB installation directory
                              (e.g., "C:/Program Files/MATLAB/R2023b")
        """
        super().__init__(matlab_path=matlab_path)
        self.mlint_path = self._find_mlint_path()

    def _find_mlint_path(self) -> Optional[str]:
        """
        Find mlint.exe executable.

        Searches in multiple locations:
        1. Configured MATLAB path (if provided and valid)
        2. System PATH (recursive search)
        3. Common MATLAB installation paths

        Returns:
            Optional[str]: Path to mlint.exe or None if not found
        """
        if self.matlab_path:
            # Use configured MATLAB path if it exists
            matlab_dir = Path(self.matlab_path)
            if matlab_dir.exists():
                possible_paths = [
                    matlab_dir / "bin" / "win64" / "mlint.exe",
                    matlab_dir / "bin" / "mlint.exe",
                ]
                for path in possible_paths:
                    if path.exists():
                        logger.debug(f"Found mlint at configured path: {path}")
                        return str(path)
            else:
                logger.warning(
                    f"Configured MATLAB path does not exist: {self.matlab_path}. "
                    "Searching for alternative..."
                )

        # Search in PATH (recursive)
        mlint_in_path = self._find_mlint_in_path_recursive()
        if mlint_in_path:
            logger.info(f"Found mlint in PATH: {mlint_in_path}")
            return mlint_in_path

        # Search in common installation paths (platform-specific)
        if platform.system() == "Windows":
            common_paths = [
                Path("C:/Program Files/MATLAB"),
                Path("C:/Program Files (x86)/MATLAB"),
                Path("D:/Program Files/MATLAB"),
                Path("E:/Program Files/MATLAB"),
                Path("F:/Program Files/MATLAB"),
                Path("G:/Program Files/MATLAB"),
                Path("H:/Program Files/MATLAB"),
                Path("I:/Program Files/MATLAB"),
                Path("J:/Program Files/MATLAB"),
            ]
        elif platform.system() == "Darwin":  # macOS
            common_paths = [
                Path("/Applications/MATLAB_R*.app"),
                Path("/Applications/MATLAB.app"),
                Path("/usr/local/MATLAB"),
            ]
        else:  # Linux and others
            common_paths = [
                Path("/usr/local/MATLAB"),
                Path("/opt/MATLAB"),
                Path("/opt/matlab"),
                Path("/usr/local/matlab"),
                Path.home() / "MATLAB",
                Path.home() / "matlab",
                Path("/usr/share/matlab"),
            ]

        for base in common_paths:
            # Handle glob patterns for macOS versions
            if "*" in str(base):
                import glob as glob_module

                matches = glob_module.glob(str(base))
                for match in sorted(matches, reverse=True):
                    # Try newest version first
                    mlint_path = self._find_mlint_in_dir(Path(match))
                    if mlint_path:
                        logger.info(f"Found mlint at: {mlint_path}")
                        return mlint_path
            elif base.exists():
                mlint_path = self._find_mlint_in_dir(base)
                if mlint_path:
                    logger.info(f"Found mlint at: {mlint_path}")
                    return mlint_path

        logger.warning("mlint not found in any location")
        return None

    def _find_mlint_in_path_recursive(self) -> Optional[str]:
        """Recursively search for mlint.exe in PATH directories.

        Returns:
            Path to mlint.exe or None
        """
        mlint_names = ["mlint.exe"]

        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            base_dir = Path(path_dir)
            if not base_dir.exists():
                continue

            # Search recursively up to 3 levels deep
            for root, dirs, files in os.walk(base_dir):
                # Limit depth to avoid searching entire filesystem
                depth = root.replace(str(base_dir), "").count(os.sep)
                if depth > 3:
                    dirs[:] = []  # Don't go deeper
                    continue

                for mlint_name in mlint_names:
                    if mlint_name in files:
                        full_path = Path(root) / mlint_name
                        if full_path.exists():
                            return str(full_path)

        return None

    def _find_mlint_in_dir(self, base_dir: Path) -> Optional[str]:
        """Find mlint in a directory tree.

        Args:
            base_dir: Base directory to search (e.g., "C:/Program Files/MATLAB")

        Returns:
            Path to mlint executable or None
        """
        # mlint binary name
        mlint_names = ["mlint.exe"] if platform.system() == "Windows" else ["mlint"]

        # Only search in bin directories (mlint is always in bin/)
        for root, dirs, files in os.walk(base_dir):
            if "bin" in root:
                for mlint_name in mlint_names:
                    if mlint_name in files:
                        return str(Path(root) / mlint_name)

        return None

    def is_available(self) -> bool:
        """Check if mlint analyzer is available."""
        if self.mlint_path is None:
            return False
        return os.path.exists(self.mlint_path)

    def get_name(self) -> str:
        """Get analyzer name."""
        return "MlintAnalyzer"

    def analyze(self, file_uri: str, file_path: str) -> DiagnosticResult:
        """
        Analyze file using mlint.exe.

        Args:
            file_uri (str): URI of file (e.g., "file:///path/to/file.m")
            file_path (str): Local path to the file

        Returns:
            DiagnosticResult: Analysis result with diagnostics

        Raises:
            FileNotFoundError: If file does not exist
            RuntimeError: If mlint is not available or analysis fails
        """
        # Check file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check mlint is available
        if not self.is_available():
            raise RuntimeError("mlint.exe is not available")

        # Assert mlint_path is not None (mypy doesn't narrow type from is_available)
        assert (
            self.mlint_path is not None
        ), "mlint_path should be set if is_available() is True"

        logger.debug(f"Analyzing file: {file_path}")

        # Run mlint
        # mlint returns non-zero if issues are found - this is expected
        # Don't use check=True to avoid CalledProcessError
        result = subprocess.run(
            [self.mlint_path, file_path, "-id"],
            capture_output=True,
            text=True,
        )
        # Mlint outputs diagnostics to stderr
        output = result.stderr if result.stderr else result.stdout

        # Parse output
        diagnostics = self._parse_output(output)

        logger.debug(f"Found {len(diagnostics)} diagnostics")
        return DiagnosticResult(file_uri=file_uri, diagnostics=diagnostics)

    def _parse_output(self, output: str) -> List[Dict[str, Any]]:
        """
        Parse mlint output into structured diagnostics.

        Args:
            output (str): Raw output from mlint.exe

        Returns:
            List[Dict]: List of diagnostic dictionaries
        """
        diagnostics = []

        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Skip mlint header lines
            # (e.g., "========== path/to/file.m ==========")
            if line.startswith("=========="):
                continue

            # Try to match patterns
            match = None
            msg_id = ""
            message = ""

            # Try pattern with ID first: "L line (ID): message"
            match = self.MLINT_PATTERN_WITH_ID.match(line)
            if match:
                line_num = int(match.group(1))
                msg_id_from_match = match.group(2) if match.group(2) else ""
                message = match.group(3)
                msg_id = msg_id_from_match
            else:
                # Try simple pattern: "L line: message"
                match = self.MLINT_PATTERN_SIMPLE.match(line)
                if match:
                    line_num = int(match.group(1))
                    message = match.group(2)

            if match:
                # Map message ID to severity
                severity = self._map_severity(msg_id)

                diagnostic = {
                    "line": line_num,
                    "column": 1,  # Default to column 1
                    "message": message,
                    "severity": severity,
                    "code": msg_id,
                    "source": "mlint",
                }
                diagnostics.append(diagnostic)

        return diagnostics

    def _map_severity(self, msg_id: str) -> str:
        """
        Map mlint message ID to LSP severity level.

        Args:
            msg_id (str): mlint message ID (e.g., "C", "W")

        Returns:
            str: LSP severity ("error", "warning", "info")
        """
        # Common mlint message prefixes
        error_prefixes = ["E", "F"]  # Error, Fatal
        warning_prefixes = ["C", "W"]  # Code Analyzer, Warning
        info_prefixes = ["I"]  # Info

        if not msg_id:
            # Default to warning for unknown IDs
            return "warning"

        msg_id_upper = msg_id.upper()

        if any(msg_id_upper.startswith(prefix) for prefix in error_prefixes):
            return "error"
        elif any(
            msg_id_upper.startswith(prefix) for prefix in warning_prefixes
        ):
            return "warning"
        elif any(msg_id_upper.startswith(prefix) for prefix in info_prefixes):
            return "info"
        else:
            return "warning"
