# Mission 049 - Event Bus
# Fixed solution

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event, handler):
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(handler)

    def unsubscribe(self, event, handler):
        if event in self.subscribers:
            self.subscribers[event].remove(handler)

    def publish(self, event, data=None):
        handlers = self.subscribers.get(event, [])
        for handler in handlers:
            handler(data)
        return len(handlers)
