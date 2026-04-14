# Mission 075 - Context Variables
# Fix the 2 bugs in this script.
import contextvars
import asyncio

request_id_var = contextvars.ContextVar("request_id", default="none")

async def handle_request(request_id):
    token = request_id_var.set(request_id)
    try:
        result = await process()
        return result
    finally:
        request_id_var.reset(token)

async def process():
    rid = request_id_var.get()
    return f"processed request {rid}"

async def log_request():
    rid = request_id_var.get("unknown")  # BUG 1: .get() takes no args; default set in ContextVar()
    return f"[{rid}] logging"

async def run_concurrent():
    results = await asyncio.gather(
        handle_request("req-001"),
        handle_request("req-002"),
    )
    return results
