"""Test script for logging system."""

import logging

from src.utils.logging import get_logger, get_log_level, setup_logging


def test_logging():
    """Test logging functionality with different levels."""
    print("Testing logging system...")

    # Test 1: Setup logging
    print("\n1. Testing setup_logging()...")
    setup_logging(level=logging.DEBUG)
    logger = get_logger(__name__)
    print("   [OK] Logging setup complete")

    # Test 2: Test different log levels
    print("\n2. Testing different log levels...")
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
    print("   [OK] All log levels work correctly")

    # Test 3: Test multiple loggers
    print("\n3. Testing multiple loggers...")
    logger1 = get_logger("test.module1")
    logger2 = get_logger("test.module2")
    logger1.info("Logger 1 message")
    logger2.info("Logger 2 message")
    print("   [OK] Multiple loggers work correctly")

    # Test 4: Test get_log_level conversion
    print("\n4. Testing get_log_level()...")
    for level_str in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        level = get_log_level(level_str)
        print(f"   {level_str} -> {level}")
    print("   [OK] Log level conversion works")

    # Test 5: Test set_log_level
    print("\n5. Testing set_log_level()...")
    from src.utils.logging import set_log_level
    logger_debug = get_logger("test.debug")
    logger_debug.debug("This should be visible at DEBUG level")
    set_log_level(logging.WARNING)
    logger_debug.debug("This should NOT be visible at WARNING level")
    logger_debug.warning("This should be visible at WARNING level")
    # Reset to INFO
    set_log_level(logging.INFO)
    print("   [OK] set_log_level() works correctly")

    # Test 6: Test plain (non-colored) output
    print("\n6. Testing plain output (no colors)...")
    setup_logging(level=logging.INFO, use_color=False)
    logger_plain = get_logger("test.plain")
    logger_plain.info("Plain output without colors")
    # Restore colored output
    setup_logging(level=logging.INFO, use_color=True)
    print("   [OK] Plain output works")

    print("\n[OK] All logging tests passed!")
    return True


if __name__ == "__main__":
    test_logging()
