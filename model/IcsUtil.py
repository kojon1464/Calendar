from datetime import timedelta
from typing import List

from ics import Calendar, Event
from ics.parse import ContentLine

from data.DayTime import DayTime
from data.EventEntity import EventEntity
from data.Priority import Priority


def export_file(events: List[EventEntity], file_path: str):
    c = Calendar()
    for event in events:
        e = Event()
        e.name = event.name
        e.begin = event.date_start
        e.end = event.date_end
        e.uid = event.uid

        e.extra.append(ContentLine(name="LOOSE", value=event.loose))
        e.extra.append(ContentLine(name="PRIORITY", value=event.priority.name))
        e.extra.append(ContentLine(name="DAYTIME", value=event.day_time.name))
        e.extra.append(ContentLine(name="TIMEWINDOW", value=event.time_window))
        e.extra.append(ContentLine(name="TIMEBEFORE", value=event.time_after))
        e.extra.append(ContentLine(name="TIMEAFTER", value=event.time_before))

        c.events.add(e)

    with open(file_path, 'w') as f:
        f.write(str(c))


def import_file(file_path: str) -> List[EventEntity]:
    with open(file_path, 'r') as f:
        text = f.read()
        c = Calendar(text)
        my_events: List[EventEntity] = []
        for event in c.events:
            my_event = EventEntity(event.name, event.begin.datetime, event.end.datetime)
            my_event.uid = event.uid
            parse_extras(my_event, event)
            my_events.append(my_event)

        return my_events


def parse_extras(my_event: EventEntity, event:Event):
    for extra in event.extra:
        name = extra.name
        value = extra.value
        if name == "LOOSE":
            if value == 'True':
                my_event.loose = True
            else:
                my_event.loose = False
        elif name == "PRIORITY":
            my_event.priority = Priority[value]
        elif name == "DAYTIME":
            my_event.day_time = DayTime[value]
        elif name == "TIMEWINDOW":
            if value == 'True':
                my_event.time_window = True
            else:
                my_event.time_window = False
        elif name == "TIMEBEFORE":
            my_event.time_before = parse_timedelta(value)
        elif name == "TIMEAFTER":
            my_event.time_after = parse_timedelta(value)


def parse_timedelta(value: str) -> timedelta:
    segments = value.split(':')
    return timedelta(hours=int(segments[0]), minutes=int(segments[1]))
