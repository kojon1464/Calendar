from enum import Enum


class Priority(Enum):
    UNDEFINED = 9,
    EMERGENCY = 0,
    URGENT = 1,
    HIGH = 2,
    MEDIUM = 3,
    STANDARD = 4,
    LOW = 5,
    LOWEST = 6
