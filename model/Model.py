from calendar import Calendar
from datetime import datetime, time
from typing import List

from data.CalendarEntity import CalendarEntity
from data.EventEntity import EventEntity
from model.CalendarProviderInterface import CalendarProviderInterface
from view.CalendarObserverInterface import CalendarObserverInterface


class Model(CalendarProviderInterface):
    calendar: CalendarEntity
    observers: List[CalendarObserverInterface] = []

    def __init__(self):
        pass

    def initialize(self):
        self.calendar = CalendarEntity()
        self.calendar.date = datetime.now().date()
        self.calendar.week = self.get_week(self.calendar.date)

        event = EventEntity()
        event.name = 'test'
        event.date_start = datetime.combine(datetime.now().date(), time(15))
        event.date_end = datetime.now()

        event1 = EventEntity()
        event1.name = 'test2'
        event1.date_start = datetime.combine(datetime.now().date(), time(16, 30))
        event1.date_end = datetime.combine(datetime.now().date(), time(18))

        event2 = EventEntity()
        event2.name = 'test3'
        event2.date_start = datetime.combine(datetime.now().date(), time(16, 30))
        event2.date_end = datetime.combine(datetime.now().date(), time(18))

        event3 = EventEntity()
        event3.name = 'test3'
        event3.date_start = datetime.combine(datetime.now().date(), time(18, 30))
        event3.date_end = datetime.combine(datetime.now().date(), time(23))

        self.calendar.events = {event, event1, event2, event3}

        self.notify()

    def subscribe(self, observer: CalendarObserverInterface):
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer: CalendarObserverInterface):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update_calendar(self.calendar)

    def get_week(self, date: datetime.date) -> List[datetime.date]:
        return self.get_week_helper(date.year, self.get_week_number(date))

    def get_week_helper(self, year: int, week_number: int) -> List[datetime.date]:
        months = Calendar().yeardatescalendar(year, 12)[0]
        weeks = [week for month in months for week in month]
        return weeks[week_number]

    def get_week_number(self, date: datetime.date):
        return date.isocalendar()[1]
