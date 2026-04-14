# Mission 056 - Observer Pattern
# Fix the 2 bugs in this script.

class IncidentSubject:
    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers = observer  # BUG 1: should append, not replace

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, incident):
        observer = self._observers[-1]  # BUG 2: should notify all observers
        observer.update(incident)

    def report_incident(self, incident):
        self._state = incident
        self.notify(incident)

class SlackObserver:
    def __init__(self):
        self.received = []
    def update(self, incident):
        self.received.append(("slack", incident))

class PagerObserver:
    def __init__(self):
        self.received = []
    def update(self, incident):
        self.received.append(("pager", incident))
