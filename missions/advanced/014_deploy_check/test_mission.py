import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


def test_version_newer_basic():
    from broken import is_newer_version
    assert is_newer_version("2.0.0", "1.0.0") is True


def test_version_older():
    from broken import is_newer_version
    assert is_newer_version("1.0.0", "2.0.0") is False


def test_version_same():
    from broken import is_newer_version
    assert is_newer_version("1.5.0", "1.5.0") is False


def test_version_minor_bump():
    from broken import is_newer_version
    assert is_newer_version("1.10.0", "1.9.0") is True


def test_version_patch_bump():
    from broken import is_newer_version
    assert is_newer_version("1.2.10", "1.2.9") is True


def test_health_all_healthy():
    from broken import is_healthy_enough
    replicas = [{"id": f"pod-{i}", "healthy": True} for i in range(5)]
    assert is_healthy_enough(replicas) is True


def test_health_below_threshold():
    from broken import is_healthy_enough
    replicas = [
        {"id": "pod-1", "healthy": True},
        {"id": "pod-2", "healthy": False},
        {"id": "pod-3", "healthy": False},
        {"id": "pod-4", "healthy": False},
    ]
    assert is_healthy_enough(replicas, min_healthy=0.8) is False


def test_health_at_threshold():
    from broken import is_healthy_enough
    replicas = [
        {"id": "pod-1", "healthy": True},
        {"id": "pod-2", "healthy": True},
        {"id": "pod-3", "healthy": True},
        {"id": "pod-4", "healthy": False},
    ]
    assert is_healthy_enough(replicas, min_healthy=0.75) is True


def test_can_deploy_happy_path():
    from broken import can_deploy
    replicas = [{"id": f"pod-{i}", "healthy": True} for i in range(5)]
    allowed, reason = can_deploy("1.10.0", "1.9.0", replicas)
    assert allowed is True


def test_can_deploy_blocked_by_version():
    from broken import can_deploy
    replicas = [{"id": f"pod-{i}", "healthy": True} for i in range(5)]
    allowed, reason = can_deploy("1.0.0", "2.0.0", replicas)
    assert allowed is False
    assert "not newer" in reason.lower() or "1.0.0" in reason


def test_can_deploy_blocked_by_health():
    from broken import can_deploy
    replicas = [
        {"id": "pod-1", "healthy": True},
        {"id": "pod-2", "healthy": False},
        {"id": "pod-3", "healthy": False},
    ]
    allowed, reason = can_deploy("2.0.0", "1.0.0", replicas)
    assert allowed is False
