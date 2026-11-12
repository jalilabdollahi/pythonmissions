import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

FULL = {"name": "web", "spec": {"resources": {"limits": {"memory": "512Mi"}, "requests": {"cpu": "250m"}}}}
NO_RESOURCES = {"name": "legacy", "spec": {}}
NO_SPEC = {"name": "bare"}
NO_LIMITS = {"name": "half", "spec": {"resources": {"requests": {"cpu": "1"}}}}


def test_memory_limit_when_present():
    assert broken.memory_limit(FULL) == "512Mi"


def test_missing_resources_section_returns_none():
    assert broken.memory_limit(NO_RESOURCES) is None, "an absent section should mean 'no limit', not a crash"


def test_missing_spec_returns_none():
    assert broken.memory_limit(NO_SPEC) is None


def test_missing_limits_returns_none():
    assert broken.memory_limit(NO_LIMITS) is None


def test_unlimited_lists_manifests_without_limits():
    assert broken.unlimited([FULL, NO_RESOURCES, NO_LIMITS]) == ["legacy", "half"]


def test_summarize_uses_placeholders():
    assert broken.summarize(NO_RESOURCES) == "legacy mem=unlimited cpu=unset"
    assert broken.summarize(FULL) == "web mem=512Mi cpu=250m"
