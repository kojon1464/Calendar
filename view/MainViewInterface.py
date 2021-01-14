from abc import ABC, abstractmethod

from controller.MainControllerInterface import MainControllerInterface
from data.CalendarEntity import CalendarEntity


class MainViewInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_top_level(self, title):
        pass

    @abstractmethod
    def get_root(self):
        pass