from abc import ABC
from datetime import date, time
from typing import List

from data.EventEntity import EventEntity


class OrganizeStrategyInterface(ABC):

    def organize_events(self, events: List[EventEntity], period_start: date, period_end: date, time_start: time, time_end: time):
        pass