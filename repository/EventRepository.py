from datetime import datetime, time

from sqlalchemy import and_

from data.EventEntity import EventEntity
from repository.AbstractRepository import AbstractRepository


class EventRepository(AbstractRepository):

    def get_type(self):
        return EventEntity

    def get_events_between_dates(self, start: datetime.date, end: datetime.date):
        end_datetime = datetime.combine(end, time(23, 59, 59))
        return self.session.query(self.get_type()).filter(and_(EventEntity.date_start >= start, EventEntity.date_end <= end_datetime))