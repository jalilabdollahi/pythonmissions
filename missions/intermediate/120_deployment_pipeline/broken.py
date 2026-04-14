# Mission 120 - Deployment Pipeline Stages
# Fix the 2 bugs in this script.

class StageResult:
    def __init__(self, name, success, output=""):
        self.name = name
        self.success = success
        self.output = output

class DeploymentPipeline:
    def __init__(self):
        self._stages = []

    def add_stage(self, name, fn):
        self._stages.append((name, fn))

    def run(self, context):
        results = []
        for name, fn in self._stages:
            try:
                output = fn(context)
                result = StageResult(name, True, output)
            except Exception as e:
                result = StageResult(name, False, str(e))
                # BUG 1: should break/return early on failure
            # BUG 2: result should be appended to results
        return {"success": all(r.success for r in results), "stages": results}
