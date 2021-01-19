from datetime import date, time, timedelta, datetime
from typing import List

from data.EventEntity import EventEntity
from model.DayOrganizeHelper import DayOrganizeHelper
from model.OrganizeStrategyInterface import OrganizeStrategyInterface
from repository.EventRepository import EventRepository


class DistributedStrategy(OrganizeStrategyInterface):

    def organize_events(self, events: List[EventEntity], period_start: date, period_end: date, time_start: time,
                        time_end: time):
        self.helpers = []
        self.updated = []

        date_delta = period_end - period_start
        for i in range(0, date_delta.days + 1):
            date = period_start + timedelta(days=i)
            events_for_day = self.repository.get_not_loose_between_dates(date, date)
            self.helpers.append(DayOrganizeHelper(events_for_day, date))

        offset = 0
        for event in events:
            helpers_count = len(self.helpers)
            for i in range(0, helpers_count):
                helper = self.helpers[(i + offset)% helpers_count]
                duration = timedelta(minutes=event.duration)
                slots = helper.get_slots(time_start, time_end, duration)
                if slots is None:
                    continue
                helper.add_event(event, slots[0][0], slots[0][0] + duration)
                self.updated.append(event)
                offset = offset + 1
                break

        for event in self.updated:
            self.repository.update(event)

    def set_event_repository(self, repository: EventRepository):
        self.repository = repository
