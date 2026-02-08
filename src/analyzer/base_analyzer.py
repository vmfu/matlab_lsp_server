"""
Base Analyzer for MATLAB code analysis.

This module provides abstract base class for all code analyzers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class DiagnosticResult:
    """Result of code analysis containing diagnostics.

    Attributes:
        file_uri (str): URI of the analyzed file
        diagnostics (List[Dict]): List of diagnostic messages
            Each diagnostic is a dict with keys:
            - line (int): Line number (1-based)
            - column (int): Column number (1-based)
            - message (str): Diagnostic message
            - severity (str): "error" or "warning" or "info"
            - code (str): Error code (if available)
            - source (str): Source of the diagnostic (e.g., "mlint")
    """

    file_uri: str
    diagnostics: List[Dict[str, Any]]


class BaseAnalyzer(ABC):
    """Abstract base class for MATLAB code analyzers.

    All analyzers should inherit from this class and implement
    the analyze() method.
    """

    def __init__(self, matlab_path: Optional[str] = None):
        """Initialize analyzer.

        Args:
            matlab_path (str): Path to MATLAB installation
                              (if needed by analyzer)
        """
        self.matlab_path = matlab_path
        logger.debug(f"{self.__class__.__name__} initialized")

    @abstractmethod
    def analyze(self, file_uri: str, file_path: str) -> DiagnosticResult:
        """
        Analyze a file and return diagnostics.

        This method must be implemented by all analyzers.

        Args:
            file_uri (str): URI of the file to analyze
            file_path (str): Local path to the file to analyze

        Returns:
            DiagnosticResult: Analysis result with diagnostics

        Raises:
            FileNotFoundError: If file does not exist
            Exception: If analysis fails
        """
        pass

    def is_available(self) -> bool:
        """
        Check if analyzer is available and ready to use.

        Returns:
            bool: True if analyzer is available, False otherwise
        """
        return True

    def get_name(self) -> str:
        """
        Get the name of this analyzer.

        Returns:
            str: Analyzer name
        """
        return self.__class__.__name__
