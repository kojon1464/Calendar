from datetime import date, time, timedelta, datetime
from typing import List

from data.EventEntity import EventEntity
from model.organize.DayOrganizeHelper import DayOrganizeHelper
from model.organize.OrganizeStrategyInterface import OrganizeStrategyInterface
from repository.EventRepository import EventRepository


class DayTimeStrategy(OrganizeStrategyInterface):

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
                day_time_value = event.day_time.value[0]
                print(day_time_value)
                period = self.common_window(time_start, time_end, day_time_value[1], day_time_value[2])
                duration = timedelta(minutes=event.duration)
                slots = helper.get_slots(period[0], period[1], duration)
                if len(slots) < 1:
                    continue
                helper.add_event(event, slots[0][0], slots[0][0] + duration)
                self.updated.append(event)
                break

        for event in self.updated:
            self.repository.update(event)

    def common_window(self, time_start: time, time_end: time, time_day_start: time, time_day_end: time):
        date = datetime.now().date()
        start = datetime.combine(date, time_start)
        end = datetime.combine(date, time_end)
        day_start = datetime.combine(date, time_day_start)
        day_end = datetime.combine(date, time_day_end)

        result_start = None
        if start < day_start:
            result_start = day_start.time()
        else:
            result_start = start.time()

        result_end = None
        if end < day_end:
            result_end = end.time()
        else:
            result_end = day_end.time()

        return (result_start, result_end)



    def set_event_repository(self, repository: EventRepository):
        self.repository = repository