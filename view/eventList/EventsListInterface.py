from abc import ABC, abstractmethod
from typing import List


class EventsListInterface(ABC):

    @abstractmethod
    def disable_double_click(self):
        pass

    @abstractmethod
    def get_selected_ids(self) -> List[int]:
        pass
