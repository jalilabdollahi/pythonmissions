import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def layers():
    company = {"checkout": {"timeout": 30, "retries": {"max": 3, "backoff": 2}}, "currency": "EUR"}
    region = {"checkout": {"retries": {"max": 5}}, "tax": {"vat": 19}}
    store = {"checkout": {"timeout": 45}, "currency": "CHF"}
    return company, region, store


def test_later_layers_win():
    policy = broken.build_store_policy(*layers())
    assert policy["currency"] == "CHF"
    assert policy["checkout"]["timeout"] == 45


def test_nested_dicts_are_merged_not_replaced():
    policy = broken.build_store_policy(*layers())
    assert policy["checkout"]["retries"] == {"max": 5, "backoff": 2}, "only max is overridden, backoff must survive"
    assert policy["tax"] == {"vat": 19}


def test_no_layers_gives_empty_policy():
    assert broken.merge_layers() == {}


def test_single_layer_is_returned_as_an_equal_copy():
    (company, _, _) = layers()
    result = broken.merge_layers(company)
    assert result == company
    assert result is not company


def test_inputs_are_not_modified_by_merging():
    company, region, store = layers()
    snapshot = copy.deepcopy((company, region, store))
    broken.build_store_policy(company, region, store)
    assert (company, region, store) == snapshot, "reduce needs an initial {} so the first layer is not the accumulator"


def test_result_does_not_share_nested_dicts_with_inputs():
    company, region, store = layers()
    policy = broken.build_store_policy(company, region, store)
    policy["checkout"]["retries"]["max"] = 99
    assert company["checkout"]["retries"]["max"] == 3
    assert region["checkout"]["retries"]["max"] == 5


def test_flatten_lists_dotted_paths():
    policy = broken.build_store_policy(*layers())
    assert broken.flatten(policy)[:3] == ["checkout.retries.backoff=2", "checkout.retries.max=5", "checkout.timeout=45"]


def test_effective_limit_walks_a_path():
    policy = broken.build_store_policy(*layers())
    assert broken.effective_limit(policy, "checkout", "retries", "max") == 5
    assert broken.effective_limit(policy, "checkout", "nope", default=7) == 7
