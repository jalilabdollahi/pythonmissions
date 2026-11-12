import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_ten_network_is_internal():
    assert broken.is_internal("10.1.2.3") is True


def test_192_168_is_internal():
    assert broken.is_internal("192.168.4.20") is True, "every prefix in the list must be checked"


def test_172_16_is_internal():
    assert broken.is_internal("172.16.0.9") is True


def test_public_address_is_not_internal():
    assert broken.is_internal("8.8.8.8") is False


def test_external_only_keeps_order():
    ips = ["1.1.1.1", "10.0.0.1", "9.9.9.9", "192.168.0.1"]
    assert broken.external_only(ips) == ["1.1.1.1", "9.9.9.9"]


def test_summary_counts():
    assert broken.summary(["10.0.0.1", "192.168.1.1", "172.16.5.5", "8.8.4.4"]) == "3 internal, 1 external"


def test_audit_lines_labels():
    assert broken.audit_lines(["172.16.1.1", "4.4.4.4"]) == ["172.16.1.1 internal", "4.4.4.4 EXTERNAL"]
