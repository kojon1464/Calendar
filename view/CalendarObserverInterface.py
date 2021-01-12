from abc import ABC, abstractmethod

from data.CalendarEntity import CalendarEntity


class CalendarObserverInterface(ABC):
    @abstractmethod
    def update_calendar(self, calendar: CalendarEntity):
        pass