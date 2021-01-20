from datetime import time, datetime, timedelta

from data.EventEntity import EventEntity


class DayOrganizeHelper:

    def __init__(self, events: [EventEntity], date):
        self.date = date
        self.events = []

        for event in events:
            copy = EventEntity()
            copy.copy_from(event)
            self.events.append(copy)

    def can_be_placed(self, time_start: time, time_end: time):
        return len(self.get_colliding_events(time_start, time_end)) < 1

    def get_colliding_events(self, time_start: time, time_end: time):
        colliding = []
        for e in self.events:
            if e.date_start.time() < time_end and e.date_end.time() > time_start:
                colliding.append(e)

        return colliding

    def can_free_space(self, time_start: time, time_end: time, event: EventEntity):
        if not event.loose:
            return False

        delta_before_cal = event.date_end - datetime.combine(self.date, time_start)
        if 0 < delta_before_cal < event.time_before:
            col = self.get_colliding_events((event.date_start - delta_before_cal).time(), (event.date_end - delta_before_cal).time())
            if len(col) == 1 and col[0] == event:
                return True

        delta_after_cal = datetime.combine(self.date, time_end) - event.date_start
        if 0 < delta_after_cal < event.time_after:
            col = self.get_colliding_events((event.date_start + delta_after_cal).time(), (event.date_end + delta_after_cal).time())
            if len(col) == 1 and col[0] == event:
                return True

        return False

    def add_event(self, event: EventEntity, start: datetime, end: datetime):
        event.date_start = start
        event.date_end = end
        event.loose = False
        event.time_window = False
        self.events.append(event)

    def get_slots(self, time_start: time, time_end: time, duration: timedelta):
        hours = (datetime.combine(self.date, time_start), datetime.combine(self.date, time_end))
        appointments = [(event.date_start, event.date_end) for event in self.events]

        return self.__get_slots(hours, appointments, duration)

    def __get_slots(self, hours, appointments, duration):
        found = []
        slots = [(hours[0], hours[0])] + sorted(appointments) + [(hours[1], hours[1])]
        for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
            if start + duration <= end:
                found.append((start, end))
        return found

    #==================================================================================================================

    def place_event_in_array(self, event: EventEntity):
        start_index = self.time_to_minutes(event.date_start.time())
        end_index = self.time_to_minutes(event.date_end.time())

        for i in range(start_index, end_index + 1):
            self.minutes[i].append(event)

    def time_to_minutes(self, time):
        return time.hour * 60 + time.minute
