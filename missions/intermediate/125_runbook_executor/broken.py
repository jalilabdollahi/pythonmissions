# Mission 125 - Runbook Step Executor
# Fix the 2 bugs in this script.

class RunbookExecutor:
    def __init__(self):
        self._steps = []

    def add_step(self, name, fn, continue_on_error=False):
        self._steps.append({"name": name, "fn": fn, "continue_on_error": continue_on_error})

    def execute(self, context):
        report = {"steps": [], "success": True}
        for step in self._steps:
            try:
                output = step["fn"](context)
                report["steps"].append({"name": step["name"], "status": "ok", "output": output})
            except Exception as e:
                report["steps"].append({"name": step["name"], "status": "failed", "error": str(e)})
                # BUG 1: logic inverted — stop if NOT continue_on_error
                if step["continue_on_error"]:
                    report["success"] = False
                    break
        # BUG 2: report success should be based on steps that failed without continue_on_error
        report["success"] = all(s["status"] == "ok" for s in report["steps"])
        return report
