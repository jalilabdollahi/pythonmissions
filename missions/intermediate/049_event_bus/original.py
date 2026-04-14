# Mission 049 - Event Bus
# Fix the 2 bugs in this script.

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event, handler):
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(handler)

    def unsubscribe(self, event, handler):
        if event in self.subscribers:
            self.subscribers[event].clear()  # BUG 1: should only remove specific handler

    def publish(self, event, data=None):
        handlers = self.subscribers.get("*", [])  # BUG 2: should use event name, not "*"
        for handler in handlers:
            handler(data)
        return len(handlers)
