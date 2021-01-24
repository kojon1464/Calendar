from datetime import datetime, time
from typing import List

from sqlalchemy import and_

from data.EventEntity import EventEntity
from repository.AbstractRepository import AbstractRepository


class EventRepository(AbstractRepository):

    def get_type(self):
        return EventEntity

    def get_not_loose_between_dates(self, start: datetime.date, end: datetime.date):
        end_datetime = datetime.combine(end, time(23, 59, 59))
        return self.session.query(self.get_type()).filter(and_(EventEntity.loose == False, and_(EventEntity.date_start >= start, EventEntity.date_end <= end_datetime)))

    def get_not_loose_start_date_between(self, start: datetime, end: datetime):
        return self.session.query(self.get_type()).filter(and_(EventEntity.loose == False, and_(EventEntity.date_start >= start, EventEntity.date_start <= end)))

    def get_by_uids(self, uids: List[str]):
        return self.session.query(self.get_type()).filter(EventEntity.uid.in_(uids)).all()

    def commit_changes(self):
        self.session.commit()

    def get_loose(self):
        return self.session.query(self.get_type()).filter(EventEntity.loose == True).all()

    def get_not_loose(self):
        return self.session.query(self.get_type()).filter(EventEntity.loose == False).all()

    def update(self, new_event: EventEntity):
        event = self.get(new_event.id)
        event.copy_from(new_event)
        self.session.commit()
