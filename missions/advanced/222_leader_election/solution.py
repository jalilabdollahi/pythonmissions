# Mission 222 - Ballot Box Election (solution)
# Voter-side logic for a Raft-style leader election.


class RaftNode:
    def __init__(self, node_id, cluster_size, log_terms=None):
        self.node_id = node_id
        self.cluster_size = cluster_size
        self.log_terms = list(log_terms or [])
        self.current_term = 0
        self.voted_for = None
        self.role = "follower"

    def last_log_term(self):
        return self.log_terms[-1] if self.log_terms else 0

    def last_log_index(self):
        return len(self.log_terms)

    def _log_is_up_to_date(self, last_index, last_term):
        if last_term != self.last_log_term():
            return last_term > self.last_log_term()
        return last_index >= self.last_log_index()

    def _observe_term(self, term):
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.role = "follower"

    def handle_request_vote(self, term, candidate_id, last_index, last_term):
        if term < self.current_term:
            return self.current_term, False
        self._observe_term(term)
        if self.voted_for not in (None, candidate_id):
            return self.current_term, False
        if not self._log_is_up_to_date(last_index, last_term):
            return self.current_term, False
        self.voted_for = candidate_id
        return self.current_term, True

    def start_election(self):
        self.current_term += 1
        self.voted_for = self.node_id
        self.role = "candidate"
        return self.current_term

    def has_majority(self, votes):
        return votes > self.cluster_size // 2

    def run_election(self, peers):
        term = self.start_election()
        votes = 1
        for peer in peers:
            peer_term, granted = peer.handle_request_vote(
                term, self.node_id, self.last_log_index(), self.last_log_term()
            )
            if peer_term > self.current_term:
                self._observe_term(peer_term)
                return False
            if granted:
                votes += 1
        if self.has_majority(votes):
            self.role = "leader"
            return True
        self.role = "follower"
        return False

    def status(self):
        return {
            "id": self.node_id,
            "term": self.current_term,
            "role": self.role,
            "voted_for": self.voted_for,
            "log_len": self.last_log_index(),
        }


def current_leaders(nodes):
    return sorted(n.node_id for n in nodes if n.role == "leader")
