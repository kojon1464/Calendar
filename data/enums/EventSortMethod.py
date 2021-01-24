from datetime import datetime
from enum import Enum
from typing import List

from data.EventEntity import EventEntity


def sort_by_priority(events: List[EventEntity]):
    events.sort(key=lambda e: e.priority.value)


def sort_by_priority_reverse(events: List[EventEntity]):
    events.sort(key=lambda e: e.priority.value, reverse=True)


def sort_by_day_time(events: List[EventEntity]):
    events.sort(key=lambda e: e.day_time.value[0])


def sort_by_day_time_reverse(events: List[EventEntity]):
    events.sort(key=lambda e: e.day_time.value[0], reverse=True)


def sort_by_start_time(events: List[EventEntity]):
    events.sort(key=lambda e: get_date(e))


def sort_by_start_time_reverse(events: List[EventEntity]):
    events.sort(key=lambda e: get_date(e), reverse=True)


def get_date(event):
    if event.loose:
        return datetime.min
    else:
        return event.date_start


class EventSortMethod(Enum):
    PRIORITY = 1, sort_by_priority
    PRIORITY_REVERSED = 2, sort_by_priority_reverse
    DAY_TIME = 3, sort_by_day_time
    DAY_TIME_REVERSED = 4, sort_by_day_time_reverse
    START_TIME = 3, sort_by_start_time
    START_TIME_REVERSED = 4, sort_by_start_time_reverse

