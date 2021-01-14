from abc import ABC, abstractmethod

from data.CalendarEntity import CalendarEntity
from data.EventEntity import EventEntity


class MainControllerInterface(ABC):

    @abstractmethod
    def previous_week_clicked(self):
        pass

    @abstractmethod
    def next_week_clicked(self):
        pass

    @abstractmethod
    def create_event_clicked(self):
        pass

    @abstractmethod
    def create_event(self, event: EventEntity):
        pass

    @abstractmethod
    def update_event(self, event: EventEntity):
        pass
