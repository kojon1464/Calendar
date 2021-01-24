import datetime
from typing import Set, List

from data.EventEntity import EventEntity


class CalendarEntity:

    date: datetime.date
    week: List[datetime.datetime]
    events: Set[EventEntity]
    events_for_list: List[EventEntity]

    def __init__(self):
        pass

    def get_events_within_day(self, date: datetime.date) -> List[EventEntity]:
        return [event for event in self.events if event.date_start.date() == date or event.date_end.date() == date]