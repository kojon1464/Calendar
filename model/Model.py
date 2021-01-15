from calendar import Calendar
from datetime import datetime, time, date, timedelta
from typing import List

from data.CalendarEntity import CalendarEntity
from data.EventEntity import EventEntity
from model.CalendarProviderInterface import CalendarProviderInterface
from model.ModelInterface import ModelInterface
from model.ObjectDetailsDTO import ObjectDetailsDTO
from model.ObjectDetailsProviderInterface import ObjectDetailsProviderInterface
from repository.EventRepository import EventRepository
from view.CalendarObserverInterface import CalendarObserverInterface
from view.ObjectDetailsObserverInterface import ObjectDetailsObserverInterface


MINUTES_NOTIFICATION_BEFORE = 5

class Model(CalendarProviderInterface, ObjectDetailsProviderInterface, ModelInterface):

    notified: List[int]
    calendar: CalendarEntity
    object_details: ObjectDetailsDTO
    calendar_observers: List[CalendarObserverInterface] = []
    object_details_observers: List[ObjectDetailsObserverInterface] = []
    event_repository: EventRepository

    def __init__(self):
        self.notified = []
        self.event_repository = EventRepository()

        event = EventEntity('test', datetime.combine(datetime.now().date(), time(8)), datetime.combine(datetime.now().date(), time(18)))
        event1 = EventEntity('test1', datetime.combine(datetime.now().date(), time(10)), datetime.combine(datetime.now().date(), time(12)))
        event2 = EventEntity('test2', datetime.combine(datetime.now().date(), time(11)), datetime.combine(datetime.now().date(), time(18)))
        event3 = EventEntity('test3', datetime.combine(datetime.now().date(), time(15)),
                             datetime.combine(datetime.now().date(), time(20)))

        self.event_repository.save(event)
        self.event_repository.save(event1)
        self.event_repository.save(event2)
        self.event_repository.save(event3)

    def initialize(self):
        self.calendar = CalendarEntity()
        self.set_calendar_for_date(datetime.now().date())

    def set_calendar_for_date(self, date: datetime.date):
        self.calendar.date = date
        self.update_calendar()

    def update_calendar(self):
        week = self.get_week(self.calendar.date)
        self.calendar.week = week
        self.calendar.events = set(self.event_repository.get_events_between_dates(week[0], week[6]))

        self.notify_calendar()

    def get_week(self, date: datetime.date) -> List[datetime.date]:
        return self.get_week_helper(date.year, self.get_week_number(date))

    def get_week_helper(self, year: int, week_number: int) -> List[datetime.date]:
        months = Calendar().yeardatescalendar(year, 12)[0]
        weeks = [week for month in months for week in month]
        return weeks[week_number]

    def get_week_number(self, date: datetime.date):
        return date.isocalendar()[1]

    def change_to_next_week(self):
        week_delta = timedelta(7)
        self.set_calendar_for_date(self.calendar.date + week_delta)

    def change_to_previous_week(self):
        week_delta = timedelta(7)
        self.set_calendar_for_date(self.calendar.date - week_delta)

    def add_event(self, event: EventEntity):
        self.event_repository.save(event)
        self.update_calendar()

    def update_event(self, event: EventEntity):
        self.event_repository.update(event)
        self.update_calendar()

    def delete_event(self, event: EventEntity):
        self.event_repository.delete(event.id)
        self.update_calendar()

    def send_event_details(self, event_id):
        event = self.event_repository.get(event_id)
        self.object_details = ObjectDetailsDTO(event=event)
        self.notify_details()

    def get_events_to_notify(self) -> List[EventEntity]:
        now = datetime.now()
        in_5_min = now + timedelta(minutes=MINUTES_NOTIFICATION_BEFORE)
        events = self.event_repository.get_start_date_between(now, in_5_min)
        to_notify = []

        for event in events:
            if not event.id in self.notified:
                to_notify.append(event)
                self.notified.append(event.id)

        return to_notify


    # region CalendarProviderInterface
    def subscribe_calendar(self, observer: CalendarObserverInterface):
        if observer not in self.calendar_observers:
            self.calendar_observers.append(observer)

    def unsubscribe_calendar(self, observer: CalendarObserverInterface):
        self.calendar_observers.remove(observer)

    def notify_calendar(self):
        for observer in self.calendar_observers:
            observer.update_calendar(self.calendar)
    # endregion

    # region ObjectDetailsProviderInterface
    def subscribe_details(self, observer: ObjectDetailsObserverInterface):
        if observer not in self.object_details_observers:
            self.object_details_observers.append(observer)

    def unsubscribe_details(self, observer: ObjectDetailsObserverInterface):
        self.object_details_observers.remove(observer)

    def notify_details(self):
        for observer in self.object_details_observers:
            observer.update_calendar(self.object_details)
    # endregion
