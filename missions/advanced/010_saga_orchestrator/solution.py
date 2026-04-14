# Mission 010 (Advanced) - Saga Orchestrator
# Fixed solution
import logging

logger = logging.getLogger(__name__)

class SagaOrchestrator:
    def __init__(self):
        self._steps = []
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
        for name, compensation in reversed(self._completed):
            try:
                compensation(context)
            except Exception as e:
                logger.error(f"Compensation failed for {name}: {e}")
