import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Instance, PostgresInstance, RedisInstance, tag


def test_base_instance_label():
    assert Instance("x", "eu").label() == "x@eu"


def test_postgres_has_base_attributes():
    pg = PostgresInstance("pg-main", "eu-1", "15")
    assert pg.name == "pg-main", "call super().__init__ so the base sets its attributes"
    assert pg.region == "eu-1"


def test_postgres_has_its_own_attribute():
    assert PostgresInstance("pg", "eu", "15").version == "15"


def test_postgres_describe():
    assert PostgresInstance("pg-main", "eu-1", "15").describe() == "pg-main@eu-1 postgres 15"


def test_redis_has_base_attributes():
    r = RedisInstance("cache-1", "us-2", 512)
    assert (r.name, r.region) == ("cache-1", "us-2")
    assert r.tags == []


def test_redis_describe():
    assert RedisInstance("cache-1", "us-2", 512).describe() == "cache-1@us-2 redis 512MB"


def test_tag_works_on_subclasses():
    r = RedisInstance("c", "us", 64)
    assert tag(r, "prod") == ["prod"]
    pg = PostgresInstance("p", "us", "14")
    assert tag(pg, "db") == ["db"]
