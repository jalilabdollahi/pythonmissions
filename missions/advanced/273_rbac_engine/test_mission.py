import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Policy, Statement, allowed_actions, matches


def build():
    p = Policy()
    p.add_role("reader", [Statement("read-logs", "allow", ["s3:Get*", "s3:List*"], ["arn:logs/*"])])
    p.add_role("writer", [Statement("write-logs", "allow", ["s3:PutObject"], ["arn:logs/*"])], inherits=["reader"])
    p.add_role("admin", [Statement("all", "allow", ["*"], ["*"])], inherits=["writer"])
    p.add_role("no-prod", [Statement("block-prod", "deny", ["*"], ["arn:logs/prod/*"])])
    p.assign("rita", "reader")
    p.assign("wes", "writer")
    p.assign("ada", "admin", "no-prod")
    return p


def test_wildcard_matching_is_anchored_at_both_ends():
    assert matches("s3:Get*", "s3:GetObject")
    assert not matches("s3:Get", "s3:GetObject"), "no star means exact match"
    assert not matches("s3:GetObject", "s3:Get")
    assert matches("*", "anything:at/all")
    assert matches("arn:*:prod", "arn:db:prod")


def test_only_star_is_special_everything_else_is_literal():
    assert matches("logs.prod/*", "logs.prod/app")
    assert not matches("logs.prod/*", "logsXprod/app"), "a dot in a pattern is just a dot"
    assert not matches("a+b", "aab")
    assert matches("a+b", "a+b")
    assert matches("file(1)?", "file(1)?")


def test_implicit_deny_without_matching_statement():
    p = build()
    assert not p.can("rita", "s3:DeleteObject", "arn:logs/app.log")
    assert not p.can("nobody", "s3:GetObject", "arn:logs/app.log")
    assert p.explain("rita", "s3:DeleteObject", "arn:logs/app.log") == ("deny", None)


def test_allow_reports_which_statement_granted_it():
    assert build().explain("rita", "s3:GetObject", "arn:logs/app.log") == ("allow", "read-logs")


def test_roles_inherit_transitively():
    p = build()
    assert p.can("wes", "s3:PutObject", "arn:logs/app.log")
    assert p.can("wes", "s3:GetObject", "arn:logs/app.log"), "writer inherits reader"
    assert p.can("ada", "s3:ListBucket", "arn:logs/x"), "admin inherits writer inherits reader"
    assert p.effective_roles("ada") == {"admin", "writer", "reader", "no-prod"}


def test_inheritance_cycles_do_not_hang():
    p = Policy()
    p.add_role("a", inherits=["b"])
    p.add_role("b", [Statement("s", "allow", ["x"], ["*"])], inherits=["a"])
    p.assign("u", "a")
    assert p.effective_roles("u") == {"a", "b"}
    assert p.can("u", "x", "r")


def test_explicit_deny_overrides_allow_regardless_of_role_order():
    p = build()
    assert not p.can("ada", "s3:GetObject", "arn:logs/prod/db.log")
    assert p.explain("ada", "s3:GetObject", "arn:logs/prod/db.log") == ("deny", "block-prod")
    # "admin" sorts before "no-prod": the allow is seen first and must not win
    assert p.can("ada", "s3:GetObject", "arn:logs/staging/db.log")


def test_allowed_actions_filters_candidates():
    p = build()
    cands = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    assert allowed_actions(p, "rita", cands, "arn:logs/a") == ["s3:GetObject"]
    assert allowed_actions(p, "wes", cands, "arn:logs/a") == ["s3:GetObject", "s3:PutObject"]
    with pytest.raises(ValueError):
        Statement("bad", "maybe", ["*"], ["*"])
