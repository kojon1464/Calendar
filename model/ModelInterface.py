from abc import ABC, abstractmethod
from datetime import date, time
from typing import List

from data.EventEntity import EventEntity
from data.Statistics import Statistics
from model.organize.OrganizeStrategyInterface import OrganizeStrategyInterface


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
    def change_week_by_date(self, date: date):
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

    @abstractmethod
    def get_statistics(self) -> List[Statistics]:
        pass

    @abstractmethod
    def organize_events(self,
                        event_ids: List[int],
                        date_start: date,
                        date_end: date,
                        time_start: time,
                        time_end: time):
        pass

    @abstractmethod
    def set_organize_strategy(self, strategy_instance: OrganizeStrategyInterface):
        pass
