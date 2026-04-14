# Mission 010 (Advanced) - Saga Orchestrator
# Fix the 2 bugs in this script.

class SagaOrchestrator:
    def __init__(self):
        self._steps = []  # (name, action, compensation)
        self._completed = []

    def step(self, name, action, compensation):
        self._steps.append((name, action, compensation))

    def execute(self, context):
        self._completed = []
        for name, action, compensation in self._steps:
            try:
                result = action(context)
                context[name] = result
                self._completed.append((name, compensation))
            except Exception as e:
                self._compensate(context)
                raise RuntimeError(f"Saga failed at {name}: {e}") from e
        return context

    def _compensate(self, context):
        """Run compensating transactions for completed steps."""
        for name, compensation in self._completed:  # BUG 1: should reverse the order
            try:
                compensation(context)
            except Exception:
                pass  # BUG 2: compensation failures should be logged but not re-raised (this is fine)
