# Mission 052 - Abstract Base Class
# Fixed solution
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def execute(self, data):
        pass

    @abstractmethod
    def name(self):
        pass

class ConcretePlugin(BasePlugin):
    def name(self):
        return "concrete"

    def execute(self, data):
        return data.upper()
