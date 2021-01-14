from abc import ABC, abstractmethod

from data.EventEntity import EventEntity


class ModelInterface(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def change_to_next_week(self):
        pass

    @abstractmethod
    def change_to_previous_week(self):
        pass

    @abstractmethod
    def add_event(self, event: EventEntity):
        pass
