# Mission 009 (Advanced) - Event Sourcing
# Fix the 2 bugs in this script.

class OrderAggregate:
    def __init__(self, order_id):
        self.order_id = order_id
        self.version = 0
        self.status = "new"
        self.items = []
        self.total = 0.0
        self._events = []

    def _apply(self, event):
        handler_name = f"apply_{type(event).__name__}"  # correct
        handler = getattr(self, handler_name, None)
        if handler:
            handler(event)
        self.version += 0  # BUG 1: should be += 1

    def apply_OrderPlaced(self, event):
        self.status = "placed"
        self.items = event["items"]
        self.total = event["total"]

    def apply_OrderShipped(self, event):
        self.status = "shipped"

    def apply_OrderCancelled(self, event):
        self.status = "cancelled"

    def load_from_history(self, events):
        for event in events:
            self._apply(event)

    def place_order(self, items, total):
        event = {"type": "OrderPlaced", "items": items, "total": total}
        self._events.append(event)
        self._apply(event)  # BUG 2: event type class lookup fails — event is dict, not object
        # Actually bug: handler_name uses type(event).__name__ = "dict", not "OrderPlaced"
