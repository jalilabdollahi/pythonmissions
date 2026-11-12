import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import RaftNode


def test_stale_term_is_rejected_and_reports_current_term():
    n = RaftNode("n1", 5)
    n.current_term = 4
    assert n.handle_request_vote(3, "n2", 0, 0) == (4, False)


def test_only_one_vote_per_term():
    n = RaftNode("n1", 5)
    assert n.handle_request_vote(1, "n2", 0, 0) == (1, True)
    term, granted = n.handle_request_vote(1, "n3", 0, 0)
    assert not granted, "a node must not vote for two candidates in the same term"


def test_same_candidate_may_retry_and_gets_the_same_vote():
    n = RaftNode("n1", 5)
    n.handle_request_vote(1, "n2", 0, 0)
    assert n.handle_request_vote(1, "n2", 0, 0) == (1, True), "RPC retries must be idempotent"


def test_higher_term_clears_previous_vote():
    n = RaftNode("n1", 5)
    n.handle_request_vote(1, "n2", 0, 0)
    term, granted = n.handle_request_vote(2, "n3", 0, 0)
    assert (term, granted) == (2, True), "a new term starts with no vote cast"


def test_log_with_newer_last_term_wins_even_if_shorter():
    n = RaftNode("n1", 5, log_terms=[1, 1, 3])
    _, granted = n.handle_request_vote(5, "n2", 7, 2)
    assert not granted, "long log with an older last term is behind"
    n2 = RaftNode("n1", 5, log_terms=[1, 1, 3])
    _, granted = n2.handle_request_vote(5, "n3", 1, 4)
    assert granted, "short log with a newer last term is ahead"


def test_equal_last_term_falls_back_to_log_length():
    n = RaftNode("n1", 5, log_terms=[2, 2, 2])
    assert not n.handle_request_vote(3, "n2", 2, 2)[1]
    assert n.handle_request_vote(3, "n3", 3, 2)[1]


def test_majority_needs_more_than_half_of_cluster():
    four = RaftNode("n1", 4)
    assert not four.has_majority(2), "2 of 4 is a tie, not a quorum"
    assert four.has_majority(3)
    five = RaftNode("n1", 5)
    assert not five.has_majority(2) and five.has_majority(3)


def test_election_wins_with_quorum_and_loses_without():
    cand = RaftNode("n1", 5, log_terms=[1])
    peers = [RaftNode(f"p{i}", 5, log_terms=[1]) for i in range(4)]
    assert cand.run_election(peers)
    assert cand.role == "leader" and cand.current_term == 1
    lagging = RaftNode("n9", 5, log_terms=[])
    ahead = [RaftNode(f"q{i}", 5, log_terms=[1, 2]) for i in range(4)]
    assert not lagging.run_election(ahead)
    assert lagging.role == "follower"
