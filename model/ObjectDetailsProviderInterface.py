from abc import ABC, abstractmethod

from view.eventDetails.ObjectDetailsObserverInterface import ObjectDetailsObserverInterface


class ObjectDetailsProviderInterface(ABC):
    @abstractmethod
    def subscribe_details(self, observer: ObjectDetailsObserverInterface):
        pass

    @abstractmethod
    def unsubscribe_details(self, observer: ObjectDetailsObserverInterface):
        pass

    @abstractmethod
    def notify_details(self):
        pass