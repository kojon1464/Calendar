from abc import ABC, abstractmethod
from datetime import date, time
from typing import List

from data.EventEntity import EventEntity
from repository.EventRepository import EventRepository


class OrganizeStrategyInterface(ABC):

    @abstractmethod
    def organize_events(self, events: List[EventEntity], period_start: date, period_end: date, time_start: time, time_end: time):
        pass

    @abstractmethod
    def set_event_repository(self, repository: EventRepository):
        pass