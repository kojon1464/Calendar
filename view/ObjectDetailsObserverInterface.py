from abc import ABC, abstractmethod

from model.ObjectDetailsDTO import ObjectDetailsDTO


class ObjectDetailsObserverInterface(ABC):

    @abstractmethod
    def update_details(self, calendar: ObjectDetailsDTO):
        pass
