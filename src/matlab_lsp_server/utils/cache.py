"""
Cache Manager for LSP Server.

This module provides caching for:
- MATLAB file parsing results
- Mlint analysis results
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from matlab_lsp_server.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class CacheEntry:
    """Represents a cache entry.

    Attributes:
        value (Any): Cached value
        timestamp (float): Entry creation time
        ttl (float): Time to live in seconds
        size (int): Approximate memory size in bytes
    """

    value: Any
    timestamp: float = field(default_factory=time.time)
    ttl: float = 300.0  # 5 minutes default
    size: int = 0


class CacheManager:
    """Manager for caching LSP server data.

    Provides in-memory caching with TTL support
    and automatic invalidation.
    """

    # Default TTL values (in seconds)
    PARSE_CACHE_TTL = 300.0  # 5 minutes
    MLINT_CACHE_TTL = 300.0  # 5 minutes

    def __init__(self):
        """Initialize cache manager."""
        self._cache: Dict[str, CacheEntry] = {}
        self._stats: Dict[str, int] = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
        }
        logger.debug("CacheManager initialized")

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key (str): Cache key

        Returns:
            Optional[Any]: Cached value if exists and valid, None otherwise
        """
        entry = self._cache.get(key)
        if entry is None:
            self._stats["misses"] += 1
            logger.debug(f"Cache miss: {key}")
            return None

        # Check if entry is expired
        if self._is_expired(entry):
            self.invalidate(key)
            self._stats["misses"] += 1
            logger.debug(f"Cache expired: {key}")
            return None

        # Return cached value
        self._stats["hits"] += 1
        logger.debug(f"Cache hit: {key}")
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        Set value in cache.

        Args:
            key (str): Cache key
            value (Any): Value to cache
            ttl (float): Time to live in seconds (None for default)
        """
        if ttl is None:
            ttl = self.PARSE_CACHE_TTL

        # Estimate size (rough approximation)
        size = len(str(value)) if value is not None else 0

        entry = CacheEntry(
            value=value,
            timestamp=time.time(),
            ttl=ttl,
            size=size,
        )

        self._cache[key] = entry
        logger.debug(f"Cache set: {key} " f"(TTL: {ttl}s, Size: {size} bytes)")

    def invalidate(self, key: str) -> bool:
        """
        Invalidate cache entry.

        Args:
            key (str): Cache key

        Returns:
            bool: True if entry existed, False otherwise
        """
        if key in self._cache:
            del self._cache[key]
            self._stats["evictions"] += 1
            logger.debug(f"Cache invalidated: {key}")
            return True
        return False

    def invalidate_prefix(self, prefix: str) -> int:
        """
        Invalidate all cache entries matching prefix.

        Args:
            prefix (str): Cache key prefix (e.g., "parse:", "mlint:")

        Returns:
            int: Number of entries invalidated
        """
        count = 0
        for key in list(self._cache.keys()):
            if key.startswith(prefix):
                del self._cache[key]
                self._stats["evictions"] += 1
                count += 1

        logger.debug(f"Cache invalidated prefix '{prefix}': {count} entries")
        return count

    def clear(self) -> None:
        """Clear all cache entries."""
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"Cache cleared: {count} entries")

    def _is_expired(self, entry: CacheEntry) -> bool:
        """
        Check if cache entry is expired.

        Args:
            entry (CacheEntry): Cache entry

        Returns:
            bool: True if expired, False otherwise
        """
        age = time.time() - entry.timestamp
        return age > entry.ttl

    def get_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Dict[str, int]: Cache statistics (hits, misses, evictions)
        """
        return self._stats.copy()

    def print_stats(self) -> None:
        """Print cache statistics to logger."""
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate: float = 0.0
        if total_requests > 0:
            hit_rate = self._stats["hits"] / total_requests

        logger.info(
            f"Cache stats: hits={self._stats['hits']}, "
            f"misses={self._stats['misses']}, "
            f"evictions={self._stats['evictions']}, "
            f"hit_rate={hit_rate:.2%}"
        )


# Global cache manager instance
_cache_manager = None


def get_cache_manager() -> CacheManager:
    """Get or create global CacheManager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
        logger.debug("CacheManager instance created")
    return _cache_manager


def generate_parse_key(
    file_uri: str, content_hash: Optional[str] = None
) -> str:
    """
    Generate cache key for parse result.

    Args:
        file_uri (str): File URI
        content_hash (str): Optional hash of file content

    Returns:
        str: Cache key
    """
    if content_hash:
        return f"parse:{file_uri}:{content_hash}"
    return f"parse:{file_uri}"


def generate_mlint_key(
    file_uri: str, content_hash: Optional[str] = None
) -> str:
    """
    Generate cache key for mlint result.

    Args:
        file_uri (str): File URI
        content_hash (str): Optional hash of file content

    Returns:
        str: Cache key
    """
    if content_hash:
        return f"mlint:{file_uri}:{content_hash}"
    return f"mlint:{file_uri}"


def hash_content(content: str) -> str:
    """
    Generate hash of file content for cache invalidation.

    Args:
        content (str): File content

    Returns:
        str: MD5 hash of content
    """
    return hashlib.md5(content.encode("utf-8")).hexdigest()
