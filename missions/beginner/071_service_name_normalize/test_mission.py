import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_spaces_become_hyphens():
    assert broken.normalize("payment gateway") == "payment-gateway"


def test_everything_is_lower_case():
    assert broken.normalize("  Payment Gateway ") == "payment-gateway", "capitalize() keeps only the first letter upper-case"


def test_underscores_become_hyphens():
    assert broken.normalize("auth_service") == "auth-service"


def test_mixed_case_and_underscore():
    assert broken.normalize("Auth_Service") == "auth-service"


def test_conflicts_are_found_after_normalising():
    names = ["Billing API", "billing_api", "search"]
    assert broken.conflicts(names) == ["billing-api"]


def test_registry_key():
    assert broken.registry_key("Core Team", "Edge_Proxy") == "core-team/edge-proxy"


def test_is_normalized():
    assert broken.is_normalized("already-ok") is True
    assert broken.is_normalized("Not Ok") is False
