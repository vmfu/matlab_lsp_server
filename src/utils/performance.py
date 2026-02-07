"""
Performance Optimization Module for LSP Server.

This module provides performance optimization utilities including
LRU caching and debouncing for LSP operations.
"""

import time
from functools import wraps
from typing import Any, Callable, Dict, Optional

from .logging import get_logger

logger = get_logger(__name__)


class LRUCache:
    """Simple LRU (Least Recently Used) cache implementation."""

    def __init__(self, capacity: int = 128):
        """Initialize LRU cache.

        Args:
            capacity (int): Maximum number of items to cache
        """
        self.capacity = capacity
        self._cache: Dict[str, Any] = {}
        self._order: List[str] = []

        logger.debug(f"LRUCache initialized with capacity {capacity}")

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key (str): Cache key

        Returns:
            Optional[Any]: Cached value or None
        """
        if key not in self._cache:
            return None

        # Move to end of order list (most recently used)
        if key in self._order:
            self._order.remove(key)
        self._order.append(key)

        return self._cache[key]

    def put(self, key: str, value: Any) -> None:
        """
        Put value into cache.

        Args:
            key (str): Cache key
            value (Any): Value to cache
        """
        # If key already exists, update and move to end
        if key in self._cache:
            self._order.remove(key)
            self._order.append(key)
            self._cache[key] = value
            return

        # If at capacity, remove least recently used
        if len(self._cache) >= self.capacity:
            lru_key = self._order.pop(0)
            del self._cache[lru_key]

        # Add new key
        self._cache[key] = value
        self._order.append(key)

        logger.debug(
            f"LRUCache put: {key} (size: {len(self._cache)})"
        )

    def clear(self) -> None:
        """Clear all items from cache."""
        self._cache.clear()
        self._order.clear()
        logger.debug("LRUCache cleared")

    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)

    def __len__(self) -> int:
        """Get cache size."""
        return len(self._cache)


class Debouncer:
    """Debouncer for delaying function calls."""

    def __init__(self, delay: float = 0.5):
        """Initialize debouncer.

        Args:
            delay (float): Delay in seconds
        """
        self.delay = delay
        self._timer = None
        self._last_args = None
        self._last_kwargs = None
        self._function = None

        logger.debug(f"Debouncer initialized with delay {delay}s")

    def debounce(self, function: Callable) -> Callable:
        """
        Wrap a function with debouncing.

        Args:
            function (Callable): Function to debounce

        Returns:
            Callable: Wrapped function
        """
        self._function = function

        @wraps(function)
        def wrapper(*args, **kwargs):
            # Cancel previous timer
            if self._timer is not None:
                self._timer.cancel()

            # Store args/kwargs for delayed call
            self._last_args = args
            self._last_kwargs = kwargs

            # Create new timer
            self._timer = time.time() + self.delay
            # In actual implementation, would use threading.Timer
            # For now, just log
            logger.debug(f"Debounced call delayed by {self.delay}s")

        return wrapper

    def flush(self) -> None:
        """Flush pending debounced call."""
        if self._timer is not None and self._function is not None:
            # Cancel timer
            self._timer = None

            # Execute function immediately
            if self._last_args is not None or self._last_kwargs is not None:
                args = self._last_args or ()
                kwargs = self._last_kwargs or {}
                result = self._function(*args, **kwargs)
                logger.debug("Debounced call flushed")

                # Clear stored args
                self._last_args = None
                self._last_kwargs = None

                return result

        return None


def measure_time(function: Callable) -> Callable:
    """
    Decorator to measure function execution time.

    Args:
        function (Callable): Function to measure

    Returns:
        Callable: Wrapped function with timing
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()

        elapsed_time = (end_time - start_time) * 1000  # ms

        logger.debug(
            f"{function.__name__} executed in {elapsed_time:.2f}ms"
        )

        return result

    return wrapper


def create_lru_symbol_table_cache(capacity: int = 128) -> LRUCache:
    """
    Create LRU cache for symbol table.

    Args:
        capacity (int): Cache capacity

    Returns:
        LRUCache: LRU cache instance
    """
    cache = LRUCache(capacity=capacity)

    logger.info(f"Created LRU cache for symbol table with capacity {capacity}")

    return cache
