from abc import ABC, abstractmethod

from view.CalendarObserverInterface import CalendarObserverInterface


class CalendarProviderInterface(ABC):
    @abstractmethod
    def subscribe(self, observer: CalendarObserverInterface):
        pass

    @abstractmethod
    def unsubscribe(self, observer: CalendarObserverInterface):
        pass

    @abstractmethod
    def notify(self):
        pass