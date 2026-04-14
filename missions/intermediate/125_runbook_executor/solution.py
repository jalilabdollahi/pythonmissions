# Mission 125 - Runbook Step Executor
# Fixed solution

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
                if not step["continue_on_error"]:
                    report["success"] = False
                    break
        report["success"] = report["success"] and all(
            s["status"] == "ok" or s.get("continue_on_error", False)
            for s in report["steps"]
        )
        return report
