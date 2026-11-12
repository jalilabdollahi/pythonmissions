import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken
from broken import CacheConfig, DatabaseConfig, ServiceConfig, load


def test_flat_and_nested_values_are_loaded():
    cfg = load(ServiceConfig, {"name": "api", "database": {"host": "db1", "port": 6432}, "replicas": 3})
    assert cfg == ServiceConfig("api", DatabaseConfig("db1", 6432), None, 3)


def test_defaults_apply_when_keys_are_missing():
    cfg = load(ServiceConfig, {"name": "api", "database": {"host": "db1"}})
    assert cfg.database.port == 5432
    assert cfg.cache is None
    assert cfg.replicas == 1


def test_unknown_top_level_keys_are_ignored():
    cfg = load(ServiceConfig, {"name": "api", "database": {"host": "h"}, "owner": "team-x"})
    assert cfg.name == "api"


def test_unknown_keys_in_nested_sections_are_ignored():
    cfg = load(ServiceConfig, {"name": "api", "database": {"host": "h", "pool_size": 10}})
    assert isinstance(cfg.database, DatabaseConfig)
    assert cfg.database.host == "h"


def test_optional_nested_section_becomes_a_dataclass():
    cfg = load(ServiceConfig, {"name": "api", "database": {"host": "h"}, "cache": {"url": "redis://c", "ttl": 5}})
    assert isinstance(cfg.cache, CacheConfig), "Optional[CacheConfig] must be unwrapped to find the dataclass"
    assert cfg.cache.ttl == 5


def test_optional_section_ignores_unknown_keys_too():
    cfg = load(ServiceConfig, {"name": "a", "database": {"host": "h"}, "cache": {"url": "u", "evict": "lru"}})
    assert cfg.cache == CacheConfig("u", 60)


def test_unwrap_leaves_plain_types_alone():
    assert broken._unwrap(int) is int
