from enum import Enum


class Priority(Enum):
    UNDEFINED = 0,
    EMERGENCY = 1,
    URGENT = 2,
    HIGH = 3,
    MEDIUM = 4,
    STANDARD = 5,
    LOW = 8,
    LOWEST = 9
