# Mission 117 - API Version Router
# Fix the 2 bugs in this script.
import re

class APIVersionRouter:
    def __init__(self):
        self._handlers = {}
        self._default = None

    def register(self, version, handler):
        self._handlers[version] = handler

    def set_default(self, handler):
        self._default = handler

    def _extract_version(self, accept_header):
        match = re.search(r'version=(\d+)', accept_header or "")
        return int(match.group(1)) if match else None

    def route(self, accept_header, request):
        version = self._extract_version(accept_header)
        handler = self._handlers.get(str(version))  # BUG 1: key is int in register, don't convert to str
        if handler is None:
            handler = self._handlers.get(version)  # BUG 2: redundant, should use default
        if handler is None:
            handler = self._default
        if handler is None:
            return {"error": "No handler"}, 406
        return handler(request)
