from abc import ABC, abstractmethod

from view.CalendarObserverInterface import CalendarObserverInterface


class CalendarProviderInterface(ABC):
    @abstractmethod
    def subscribe_calendar(self, observer: CalendarObserverInterface):
        pass

    @abstractmethod
    def unsubscribe_calendar(self, observer: CalendarObserverInterface):
        pass

    @abstractmethod
    def notify_calendar(self):
        pass