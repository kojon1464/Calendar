from abc import ABC, abstractmethod

from model.ObjectDetailsDTO import ObjectDetailsDTO


class ObjectDetailsObserverInterface(ABC):

    @abstractmethod
    def update_calendar(self, calendar: ObjectDetailsDTO):
        pass
