import datetime
import uuid

from sqlalchemy import Column, Integer, String, DateTime

from base import Base


class EventEntity(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    uid = Column(String)
    name = Column(String)
    date_start = Column(DateTime)
    date_end = Column(DateTime)

    def __init__(self, name, date_start, date_end, uid=None):
        self.name = name
        self.date_start = date_start
        self.date_end = date_end

        if uid is None:
            self.uid = uuid.uuid1().__str__()
        else:
            self.uid = uid

    def get_time_label(self) -> str:
        return self.date_start.time().strftime('%H:%M') + '-' + self.date_end.time().strftime('%H:%M')

    def copy_from(self, event):
        self.name = event.name
        self.date_start = event.date_start
        self.date_end = event.date_end
