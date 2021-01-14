from abc import ABC, abstractmethod

from view.ObjectDetailsObserverInterface import ObjectDetailsObserverInterface


class ObjectDetailsProviderInterface(ABC):
    @abstractmethod
    def subscribe_details(self, observer: ObjectDetailsObserverInterface):
        pass

    @abstractmethod
    def unsubscribe_details(self, observer: ObjectDetailsObserverInterface):
        pass

    @abstractmethod
    def notify(self):
        pass