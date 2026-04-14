# Mission 119 - API Mock Server
# Fixed solution
import json

class MockServer:
    def __init__(self):
        self._routes = {}

    def register(self, method, path, response_data, status=200):
        key = (method.upper(), path)
        self._routes[key] = {"data": response_data, "status": status}

    def handle(self, method, path):
        key = (method.upper(), path)
        route = self._routes.get(key)
        if route is None:
            return 404, json.dumps({"error": "Not found"})
        body = json.dumps(route["data"])
        return route["status"], body
