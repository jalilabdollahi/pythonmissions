import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_plain_500_counts_as_error():
    assert broken.error_rate_percent([500, 200]) == 50.0, "500 itself is a server error"


def test_client_errors_are_not_server_errors():
    assert broken.error_rate_percent([404, 429, 200, 200]) == 0.0


def test_denominator_is_all_responses():
    statuses = [200, 200, 301, 404, 503]
    assert broken.error_rate_percent(statuses) == 20.0, "errors / ALL responses, not only the 2xx ones"


def test_one_in_twenty_is_five_percent():
    statuses = [200] * 19 + [502]
    assert broken.error_rate_percent(statuses) == 5.0


def test_fraction_is_kept_with_two_decimals():
    statuses = [200] * 199 + [500]
    assert broken.error_rate_percent(statuses) == 0.5, "0.5% must not be truncated to 0"
    assert broken.error_rate_percent([200, 200, 500]) == 33.33


def test_empty_list_is_zero():
    assert broken.error_rate_percent([]) == 0.0


def test_breaching_services_uses_strict_threshold():
    data = {
        "cart": [200] * 98 + [500, 500],
        "search": [200] * 99 + [500],
        "pay": [200] * 90 + [503] * 10,
    }
    assert broken.breaching_services(data, 1.0) == ["cart", "pay"]
