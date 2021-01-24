import re
import uuid
from datetime import datetime, timedelta, time

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Interval

from base import Base
from data.enums.DayTime import DayTime
from data.enums.Priority import Priority


class EventEntity(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    uid = Column(String)
    name = Column(String)
    description = Column(String)
    loose = Column(Boolean)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    duration = Column(Integer)
    priority = Column(Enum(Priority))
    day_time = Column(Enum(DayTime))
    time_window = Column(Boolean)
    time_before = Column(Interval)
    time_after = Column(Interval)

    def __init__(self
                 , name=''
                 , date_start=datetime.now()
                 , date_end=datetime.now()
                 , description=''
                 , duration=0
                 , loose=False
                 , priority=Priority.UNDEFINED
                 , day_time=DayTime.UNDEFINED
                 , time_window=False
                 , time_before=timedelta()
                 , time_after=timedelta()
                 , uid=None):
        self.name = name
        self.date_start = date_start
        self.date_end = date_end
        self.duration = duration
        self.description = description
        self.loose = loose
        self.priority = priority
        self.day_time = day_time
        self.time_window = time_window
        self.time_before = time_before
        self.time_after = time_after

        if uid is None:
            self.uid = uuid.uuid1().__str__()
        else:
            self.uid = uid

    def get_time_label(self) -> str:
        return self.date_start.time().strftime('%H:%M') + '-' + self.date_end.time().strftime('%H:%M')

    def get_delta_label(self) -> str:
        date = datetime.now().date()

        if self.time_window:
            return (datetime.combine(date, time()) + self.time_before).strftime('-%H:%M') + \
               '|' + \
               (datetime.combine(date, time()) + self.time_after).strftime('+%H:%M')
        else:
            return ''

    def get_single_line_description(self) -> str:
        return re.sub(r'\s+', ' ', self.description)

    def get_duration_str(self) -> str:
        if self.loose:
            return self.duration.__str__()
        else:
            return ''

    def get_start_str(self) -> str:
        if not self.loose:
            return self.date_start.__str__()
        else:
            return ''

    def get_end_str(self) -> str:
        if not self.loose:
            return self.date_end.__str__()
        else:
            return ''


    def copy_from(self, event):
        if event.id is not None:
            self.id = event.id
        self.uid = event.uid
        self.name = event.name
        self.date_start = event.date_start
        self.date_end = event.date_end
        self.duration = event.duration
        self.description = event.description
        self.loose = event.loose
        self.priority = event.priority
        self.day_time = event.day_time
        self.time_window = event.time_window
        self.time_before = event.time_before
        self.time_after = event.time_after

    def validate(self):
        if self.date_start > self.date_end:
            return 'Start time cannot be after end time'
        if self.name == '':
            return 'Name cannot be empty'
        if self.date_start - self.time_before < datetime.combine(self.date_start.date(), time()):
            return 'Time window cannot stretch to other day'
        if self.date_end + self.time_after > datetime.combine(self.date_start.date(), time(23, 59)):
            return 'Time window cannot stretch to other day'
        if self.duration < 0:
            return 'Duration cannot be negative'
        return None
