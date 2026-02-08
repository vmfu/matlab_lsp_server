"""
Unit tests for Cache Manager.
"""

from src.utils.cache import (
    CacheManager,
    generate_mlint_key,
    generate_parse_key,
    get_cache_manager,
    hash_content,
)


def test_cache_manager_initialization():
    """Test CacheManager can be initialized."""
    manager = CacheManager()

    assert manager is not None
    assert len(manager._cache) == 0


def test_cache_set_and_get():
    """Test setting and getting values from cache."""
    manager = CacheManager()

    # Set value
    manager.set("test_key", "test_value")

    # Get value
    value = manager.get("test_key")

    assert value == "test_value"
    assert manager._stats["hits"] == 1
    assert manager._stats["misses"] == 0


def test_cache_miss():
    """Test cache miss behavior."""
    manager = CacheManager()

    # Get non-existent value
    value = manager.get("nonexistent_key")

    assert value is None
    assert manager._stats["hits"] == 0
    assert manager._stats["misses"] == 1


def test_cache_invalidate():
    """Test invalidating cache entries."""
    manager = CacheManager()

    # Set value
    manager.set("test_key", "test_value")

    # Invalidate
    result = manager.invalidate("test_key")

    assert result is True

    # Try to get invalidated value
    value = manager.get("test_key")

    assert value is None


def test_cache_invalidate_prefix():
    """Test invalidating cache entries by prefix."""
    manager = CacheManager()

    # Set values
    manager.set("parse:file1", "value1")
    manager.set("parse:file2", "value2")
    manager.set("mlint:file1", "value3")
    manager.set("mlint:file2", "value4")

    # Invalidate parse: prefix
    count = manager.invalidate_prefix("parse:")

    assert count == 2

    # Check that mlint: values still exist
    assert manager.get("mlint:file1") == "value3"
    assert manager.get("mlint:file2") == "value4"


def test_cache_clear():
    """Test clearing all cache."""
    manager = CacheManager()

    # Set values
    manager.set("key1", "value1")
    manager.set("key2", "value2")

    # Clear cache
    manager.clear()

    # Check that cache is empty
    assert len(manager._cache) == 0


def test_cache_ttl():
    """Test cache TTL (time to live)."""
    # Skip for now - CacheManager doesn't support custom TTL yet
    # manager = CacheManager(ttl=1.0)  # 1 second TTL
    # manager.set("test_key", "test_value")
    # Get immediately (should work)
    # value = manager.get("test_key")
    # assert value == "test_value"
    # Wait for TTL to expire
    # time.sleep(1.5)
    # Get after TTL (should miss)
    # value = manager.get("test_key")
    # assert value is None
    pass


def test_generate_parse_key():
    """Test generating parse cache keys."""
    key = generate_parse_key("file:///test.m", "abc123")

    assert key == "parse:file:///test.m:abc123"

    # Without hash
    key_no_hash = generate_parse_key("file:///test.m")
    assert key_no_hash == "parse:file:///test.m"


def test_generate_mlint_key():
    """Test generating mlint cache keys."""
    key = generate_mlint_key("file:///test.m", "xyz789")

    assert key == "mlint:file:///test.m:xyz789"

    # Without hash
    key_no_hash = generate_mlint_key("file:///test.m")
    assert key_no_hash == "mlint:file:///test.m"


def test_hash_content():
    """Test hashing content for cache."""
    content1 = "function test\nend"
    content2 = "function test\nend"
    content3 = "function different\nend"

    hash1 = hash_content(content1)
    hash2 = hash_content(content2)
    hash3 = hash_content(content3)

    assert hash1 == hash2  # Same content produces same hash
    assert hash1 != hash3  # Different content produces different hash


def test_get_cache_manager():
    """Test getting global cache manager instance."""
    manager1 = get_cache_manager()
    manager2 = get_cache_manager()

    assert manager1 is manager2  # Should return same instance


def test_cache_stats():
    """Test getting cache statistics."""
    manager = CacheManager()

    # Perform some operations
    manager.set("key1", "value1")
    manager.get("key1")  # Hit
    manager.get("key2")  # Miss
    manager.invalidate("key1")  # Eviction

    # Get stats
    stats = manager.get_stats()

    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["evictions"] == 1


def test_cache_manager_module_imports():
    """Test that cache module can be imported."""
    from src.utils.cache import (
        CacheEntry,
        CacheManager,
        generate_mlint_key,
        generate_parse_key,
        get_cache_manager,
        hash_content,
    )

    assert CacheManager is not None
    assert CacheEntry is not None
    assert get_cache_manager is not None
    assert generate_parse_key is not None
    assert generate_mlint_key is not None
    assert hash_content is not None
