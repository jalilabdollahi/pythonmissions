# Mission 015 (Advanced) - State Machine Workflow
# Fixed solution

class StateMachine:
    def __init__(self, initial_state, transitions):
        self.state = initial_state
        self._transitions = transitions

    def trigger(self, event, context=None):
        key = (self.state, event)
        transition = self._transitions.get(key)
        if transition is None:
            return False
        guard = transition.get("guard")
        if guard and not guard(context):
            return False
        self.state = transition["to"]
        return True

    def can_trigger(self, event, context=None):
        key = (self.state, event)
        transition = self._transitions.get(key)
        if not transition:
            return False
        guard = transition.get("guard")
        return not guard or guard(context)
