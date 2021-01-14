from abc import ABC, abstractmethod

from data.CalendarEntity import CalendarEntity


class WeekViewInterface(ABC):

    @abstractmethod
    def update_view(self, calendar: CalendarEntity):
        pass
