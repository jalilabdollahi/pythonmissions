# Mission 007 (Advanced) - Raft Leader Election
# Fixed solution

class RaftNode:
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

    def __init__(self, node_id, cluster_size):
        self.node_id = node_id
        self.cluster_size = cluster_size
        self.current_term = 0
        self.voted_for = None
        self.state = self.FOLLOWER
        self.votes_received = set()

    def request_vote(self, candidate_id, candidate_term):
        if candidate_term < self.current_term:
            return False, self.current_term
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.voted_for = None
            self.state = self.FOLLOWER
        if self.voted_for is None or self.voted_for == candidate_id:
            self.voted_for = candidate_id
            return True, self.current_term
        return False, self.current_term

    def receive_vote(self, voter_id, vote_granted):
        if vote_granted:
            self.votes_received.add(voter_id)
        majority = (self.cluster_size // 2) + 1
        if len(self.votes_received) >= majority:
            self.state = self.LEADER

    def start_election(self):
        self.current_term += 1
        self.state = self.CANDIDATE
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}

    def handle_heartbeat(self, leader_term):
        if leader_term > self.current_term:
            self.current_term = leader_term
            self.state = self.FOLLOWER
