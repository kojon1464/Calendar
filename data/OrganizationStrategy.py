from enum import Enum

from model.DayTimeStrategy import DayTimeStrategy
from model.DistributedStrategy import DistributedStrategy
from model.GreedyStrategy import GreedyStrategy


class OrganizationStrategy(Enum):
    GREEDY = (GreedyStrategy, 'test information: greedy organization')
    DISTRIBUTED = (DistributedStrategy, 'test information: dsiributed organization')
    DAY_TIME = (DayTimeStrategy, 'test information: day_time organization')
