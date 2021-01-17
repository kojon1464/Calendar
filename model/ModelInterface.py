from abc import ABC, abstractmethod
from typing import List

from data.EventEntity import EventEntity


class ModelInterface(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def change_to_next_week(self):
        pass

    @abstractmethod
    def change_to_previous_week(self):
        pass

    @abstractmethod
    def add_event(self, event: EventEntity):
        pass

    @abstractmethod
    def update_event(self, event: EventEntity):
        pass

    @abstractmethod
    def delete_event(self, event: EventEntity):
        pass

    @abstractmethod
    def send_event_details(self, event_id):
        pass

    @abstractmethod
    def get_events_to_notify(self) -> List[EventEntity]:
        pass

    @abstractmethod
    def export_calendar(self, path: str):
        pass

    @abstractmethod
    def import_calendar(self, path: str):
        pass
