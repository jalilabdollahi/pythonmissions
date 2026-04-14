# Mission 112 - Request Middleware Chain
# Fix the 2 bugs in this script.

class MiddlewareChain:
    def __init__(self):
        self._middlewares = []

    def use(self, middleware):
        self._middlewares.append(middleware)

    def handle(self, request):
        def build_chain(middlewares, final_handler):
            if not middlewares:
                return final_handler
            current = middlewares[0]
            rest = build_chain(middlewares[1:], final_handler)
            return lambda req: current(req, rest)

        def final(req):
            return {"status": 200, "request": req}

        chain = build_chain(list(reversed(self._middlewares)), final)  # BUG 1: don't reverse
        return chain(request)

def auth_middleware(request, next_handler):
    if not request.get("token"):
        return {"status": 401, "error": "Unauthorized"}
    request["authenticated"] = True
    return next_handler(request)  # BUG 2: this is correct — bug is in build_chain reversal

def logging_middleware(request, next_handler):
    result = next_handler(request)
    return result
