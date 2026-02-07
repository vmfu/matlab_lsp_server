"""Logging configuration for MATLAB LSP Server."""

import logging
import sys
from typing import Optional

import colorlog

# Default log format with colors
LOG_FORMAT = (
    '%(log_color)s%(levelname)-8s%(reset)s '
    '%(blue)s%(name)s%(reset)s '
    '%(message)s%(reset)s'
)

# Default log level
DEFAULT_LOG_LEVEL = logging.INFO

# Log colors for different levels
LOG_COLORS = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}


def setup_logging(
    level: int = DEFAULT_LOG_LEVEL,
    log_format: Optional[str] = None,
    use_color: bool = True,
) -> None:
    """Set up logging configuration for the LSP server.

    Args:
        level: Logging level (default: INFO)
        log_format: Custom log format string (optional)
        use_color: Whether to use colored output (default: True)
    """
    root_logger = logging.getLogger()

    # Avoid adding multiple handlers
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stderr)

    if use_color:
        formatter = colorlog.ColoredFormatter(
            log_format or LOG_FORMAT,
            log_colors=LOG_COLORS,
            reset=True,
            style='%',
        )
    else:
        # Plain format for non-colored output
        plain_format = log_format or LOG_FORMAT
        # Remove color codes from format
        plain_format = plain_format.replace('%(log_color)s', '')
        plain_format = plain_format.replace('%(reset)s', '')
        plain_format = plain_format.replace('%(blue)s', '')
        plain_format = plain_format.replace('%(message_log_color)s', '')
        formatter = logging.Formatter(plain_format, style='%')

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_log_level(level: int) -> None:
    """Set the global logging level.

    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logging.getLogger().setLevel(level)


def get_log_level(level_str: str) -> int:
    """Convert a string log level to logging constant.

    Args:
        level_str: String representation of log level
                   (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR')

    Returns:
        Logging level constant

    Raises:
        ValueError: If level_str is not a valid log level
    """
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    level_str_upper = level_str.upper()
    if level_str_upper not in level_map:
        raise ValueError(
            f"Invalid log level: {level_str}. "
            f"Valid levels: {', '.join(level_map.keys())}"
        )

    return level_map[level_str_upper]
