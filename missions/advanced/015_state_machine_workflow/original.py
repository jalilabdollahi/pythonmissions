# Mission 015 (Advanced) - State Machine Workflow
# Fix the 2 bugs in this script.

class StateMachine:
    def __init__(self, initial_state, transitions):
        self.state = initial_state
        self._transitions = transitions
        # transitions: {(from, event): {"to": state, "guard": fn or None}}

    def trigger(self, event, context=None):
        key = (self.state, event)
        transition = self._transitions.get(key)
        if transition is None:
            return False  # correct: no such transition
        guard = transition.get("guard")
        if guard and not guard(context):
            return False
        self.state = transition["to"]
        return True

    def can_trigger(self, event, context=None):
        key = (self.state, event)
        transition = self._transitions.get(key)
        if not transition:
            return True  # BUG 1: should return False if no transition
        guard = transition.get("guard")
        return not guard or guard(context)  # BUG 2: this logic is correct — bug is line above
