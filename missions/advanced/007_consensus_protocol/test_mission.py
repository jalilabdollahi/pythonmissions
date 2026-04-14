import pytest, sys
sys.path.insert(0, ".")
from broken import RaftNode

def test_majority_needed():
    node = RaftNode("n1", cluster_size=5)
    node.start_election()
    node.receive_vote("n2", True)
    assert node.state == node.CANDIDATE  # 2/5 not majority
    node.receive_vote("n3", True)
    assert node.state == node.LEADER  # 3/5 is majority

def test_no_vote_same_term():
    n1 = RaftNode("n1", 3)
    n2 = RaftNode("n2", 3)
    n1.current_term = 5; n1.voted_for = "n3"
    granted, _ = n1.request_vote("n2", 5)
    assert granted is False

def test_heartbeat_resets_only_newer():
    node = RaftNode("n1", 3)
    node.current_term = 5
    node.state = node.LEADER
    node.handle_heartbeat(5)  # same term — should NOT step down
    assert node.state == node.LEADER
    node.handle_heartbeat(6)
    assert node.state == node.FOLLOWER
