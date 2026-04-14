# Mission 052 - Abstract Base Class
# Fix the 2 bugs in this script.
from abc import ABC, abstractmethod

class BasePlugin:  # BUG 1: should inherit from ABC
    def execute(self, data):  # BUG 2: missing @abstractmethod decorator
        pass

    @abstractmethod
    def name(self):
        pass

class ConcretePlugin(BasePlugin):
    def name(self):
        return "concrete"

    def execute(self, data):
        return data.upper()
