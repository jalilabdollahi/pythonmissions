# Mission 012 - OOP Server Monitor
# Fixed solution

class ServerMonitor:
    def __init__(self, server_name):
        self.server_name = server_name
        self.metrics = []

    def record(self, cpu, memory):
        self.metrics.append({"cpu": cpu, "memory": memory})

    def average_cpu(self):
        if not self.metrics:
            return 0.0
        return sum(m["cpu"] for m in self.metrics) / len(self.metrics)

    def average_memory(self):
        if not self.metrics:
            return 0.0
        return sum(m["memory"] for m in self.metrics) / len(self.metrics)

    def report(self):
        return f"{self.server_name}: CPU={self.average_cpu():.1f}% MEM={self.average_memory():.1f}%"
