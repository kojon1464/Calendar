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
    def update_event_clicked(self, event_id):
        pass

    @abstractmethod
    def create_event(self, event: EventEntity):
        pass

    @abstractmethod
    def update_event(self, event: EventEntity):
        pass

    @abstractmethod
    def delete_event(self, event: EventEntity):
        pass

    @abstractmethod
    def check_notification(self):
        pass

    @abstractmethod
    def import_clicked(self):
        pass

    @abstractmethod
    def export_clicked(self):
        pass

    @abstractmethod
    def export_calendar(self, path):
        pass

    @abstractmethod
    def import_calendar(self, path):
        pass
