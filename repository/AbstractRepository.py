from abc import ABC, abstractmethod
from typing import List

from base import Session


class AbstractRepository(ABC):

    def __init__(self):
        self.session: Session = Session()

    @abstractmethod
    def get_type(self):
        pass

    def get_all(self):
        return self.session.query(self.get_type()).all()

    def get(self, id: int):
        return self.session.query(self.get_type()).get(id)

    def get_multiple(self, ids: List[int]):
        return self.session.query(self.get_type()).filter(self.get_type().id.in_(ids)).all()

    def save(self, object_data):
        self.session.add(object_data)
        self.session.commit()

    def delete(self, id: int):
        object = self.session.query(self.get_type()).get(id)
        self.session.delete(object)
        self.session.commit()
