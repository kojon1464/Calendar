from abc import ABC, abstractmethod

from base import Session


class AbstractRepository(ABC):

    def __init__(self):
        self.session: Session = Session()

    @abstractmethod
    def get_type(self):
        pass

    def get_all(self):
        return self.session.query(self.get_type()).all()

    def save(self, object_data):
        self.session.add(object_data)
        self.session.commit()
