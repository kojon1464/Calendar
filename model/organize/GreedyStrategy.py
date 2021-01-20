from datetime import date, time, timedelta
from typing import List

from data.EventEntity import EventEntity
from model.organize.DayOrganizeHelper import DayOrganizeHelper
from model.organize.OrganizeStrategyInterface import OrganizeStrategyInterface
from repository.EventRepository import EventRepository


class GreedyStrategy(OrganizeStrategyInterface):

    def organize_events(self, events: List[EventEntity], period_start: date, period_end: date, time_start: time,
                        time_end: time):
        self.helpers = []
        self.updated = []

        date_delta = period_end - period_start
        for i in range(0, date_delta.days + 1):
            date = period_start + timedelta(days=i)
            events_for_day = self.repository.get_not_loose_between_dates(date, date)
            self.helpers.append(DayOrganizeHelper(events_for_day, date))

        for event in events:
            for helper in self.helpers:
                duration = timedelta(minutes=event.duration)
                slots = helper.get_slots(time_start, time_end, duration)
                if len(slots) < 1:
                    continue
                helper.add_event(event, slots[0][0], slots[0][0] + duration)
                self.updated.append(event)
                break

        for event in self.updated:
            self.repository.update(event)

    def set_event_repository(self, repository: EventRepository):
        self.repository = repository