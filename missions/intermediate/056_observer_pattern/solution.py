# Mission 056 - Observer Pattern
# Fixed solution

class IncidentSubject:
    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, incident):
        for observer in self._observers:
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
