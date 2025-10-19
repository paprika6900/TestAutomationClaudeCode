"""
Logging configuration for the test automation framework.

This module provides centralized logging configuration that can be used across
all framework components, page objects, and tests.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = None,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Configure and return a logger with standardized formatting.

    Args:
        name: Logger name. If None, returns root logger
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path. If provided, logs to file
        console_output: Whether to output logs to console (default: True)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger(__name__, level=logging.DEBUG)
        >>> logger.info("Test started")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler (if log file specified)
    if log_file:
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to avoid duplicate logs
    logger.propagate = False

    return logger


def get_test_logger(test_name: str, log_dir: str = "logs") -> logging.Logger:
    """
    Get a logger configured specifically for test execution.

    Args:
        test_name: Name of the test (typically __name__ from test module)
        log_dir: Directory to store log files (default: "logs")

    Returns:
        Configured logger instance with both console and file output

    Example:
        >>> logger = get_test_logger(__name__)
        >>> logger.info("Test execution started")
    """
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"{test_name}_{timestamp}.log"

    return setup_logger(
        name=test_name,
        level=logging.DEBUG,  # Tests get DEBUG level by default
        log_file=str(log_file),
        console_output=True
    )


def log_test_step(logger: logging.Logger, step: str):
    """
    Log a test step with visual separation for better readability.

    Args:
        logger: Logger instance
        step: Description of the test step

    Example:
        >>> log_test_step(logger, "Navigate to login page")
    """
    logger.info(f"{'='*60}")
    logger.info(f"STEP: {step}")
    logger.info(f"{'='*60}")


def log_assertion(logger: logging.Logger, condition: str, actual: any, expected: any, passed: bool):
    """
    Log an assertion result with clear formatting.

    Args:
        logger: Logger instance
        condition: Description of what is being asserted
        actual: Actual value
        expected: Expected value
        passed: Whether the assertion passed

    Example:
        >>> log_assertion(logger, "Page title", actual_title, "Login", actual_title == "Login")
    """
    status = "PASS" if passed else "FAIL"
    level = logging.INFO if passed else logging.ERROR

    logger.log(level, f"ASSERT [{status}]: {condition}")
    logger.log(level, f"  Expected: {expected}")
    logger.log(level, f"  Actual: {actual}")


# Default framework logger
framework_logger = setup_logger('framework', level=logging.INFO)
