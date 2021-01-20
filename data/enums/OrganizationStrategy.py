from enum import Enum

from model.organize.DayTimeStrategy import DayTimeStrategy
from model.organize.DistributedStrategy import DistributedStrategy
from model.organize.GreedyStrategy import GreedyStrategy


class OrganizationStrategy(Enum):
    GREEDY = (GreedyStrategy, 'Takes events by priority and puts them in first available space')
    DISTRIBUTED = (DistributedStrategy, 'Takes events by priority and uses ties to put even number of events to each day')
    DAY_TIME = (DayTimeStrategy, 'Takes events by priority and puts them in first available space during day time hours')
