from abc import ABC, abstractmethod

from data.CalendarEntity import CalendarEntity


class EventsViewInterface(ABC):

    @abstractmethod
    def update_view(self, calendar: CalendarEntity):
        pass
