# Mission 119 - API Mock Server
# Fix the 2 bugs in this script.
import json

class MockServer:
    def __init__(self):
        self._routes = {}

    def register(self, method, path, response_data, status=200):
        key = path  # BUG 1: should include method: key = (method, path)
        self._routes[key] = {"data": response_data, "status": status}

    def handle(self, method, path):
        key = (method.upper(), path)
        route = self._routes.get(key)
        if route is None:
            return 404, json.dumps({"error": "Not found"})
        body = json.dumps(json.dumps(route["data"]))  # BUG 2: double-serialized
        return route["status"], body
