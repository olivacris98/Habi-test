from abc import ABC, abstractmethod


class Abstract(ABC):
    """
    Abstract responsible exclusive method in class
    """
    def __init__(self):
        pass

    @abstractmethod
    def get(self):
        pass
