"""
Unit tests for Performance Module.
"""

import pytest
import time

from src.utils.performance import (
    LRUCache,
    Debouncer,
    measure_time,
    create_lru_symbol_table_cache,
)


def test_lru_cache_initialization():
    """Test LRUCache can be initialized."""
    cache = LRUCache(capacity=10)

    assert cache is not None
    assert cache.capacity == 10


def test_lru_cache_put_and_get():
    """Test LRUCache put and get operations."""
    cache = LRUCache(capacity=3)

    # Put items
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")

    # Get items
    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_lru_cache_eviction():
    """Test LRUCache eviction when capacity exceeded."""
    cache = LRUCache(capacity=2)

    # Put 3 items (should evict first)
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")

    # First item should be evicted
    assert cache.get("key1") is None

    # Other items should be present
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_lru_cache_size():
    """Test LRUCache size tracking."""
    cache = LRUCache(capacity=10)

    assert cache.size() == 0

    cache.put("key1", "value1")

    assert cache.size() == 1


def test_lru_cache_clear():
    """Test LRUCache clear."""
    cache = LRUCache(capacity=10)

    cache.put("key1", "value1")
    cache.put("key2", "value2")

    cache.clear()

    assert cache.size() == 0
    assert cache.get("key1") is None


def test_debouncer_initialization():
    """Test Debouncer can be initialized."""
    debouncer = Debouncer(delay=0.1)

    assert debouncer is not None
    assert debouncer.delay == 0.1


def test_measure_time_decorator():
    """Test measure_time decorator."""
    @measure_time
    def test_function():
        time.sleep(0.01)
        return "result"

    # Execute function
    result = test_function()

    assert result == "result"


def test_create_lru_symbol_table_cache():
    """Test creating LRU cache for symbol table."""
    cache = create_lru_symbol_table_cache(capacity=50)

    assert cache is not None
    assert cache.capacity == 50


def test_performance_module_imports():
    """Test that performance module can be imported."""
    from src.utils.performance import (
        LRUCache,
        Debouncer,
        measure_time,
        create_lru_symbol_table_cache,
    )

    assert LRUCache is not None
    assert Debouncer is not None
    assert measure_time is not None
    assert create_lru_symbol_table_cache is not None
