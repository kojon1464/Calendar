from abc import ABC, abstractmethod
from typing import List

from data.Statistics import Statistics


class StatisticsViewInterface(ABC):

    @abstractmethod
    def set_statistics(self, statistics: List[Statistics]):
        pass
