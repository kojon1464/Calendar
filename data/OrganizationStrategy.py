from enum import Enum

from model.DistributedStrategy import DistributedStrategy
from model.GreedyStrategy import GreedyStrategy


class OrganizationStrategy(Enum):
    GREEDY = (GreedyStrategy, 'test information: greedy organization')
    DISTRIBUTED = (DistributedStrategy, 'test information: dsiributed organization')
