from datetime import time
from enum import Enum


class DayTime(Enum):
    UNDEFINED = (0, time(0), time(23, 59)),
    EARLY_MORNING = (1, time(7), time(4)),
    MORNING = (2, time(6), time(12)),
    LATE_MORNING = (3, time(10), time(12)),
    EARLY_AFTERNOON = (4, time(12), time(15)),
    AFTERNOON = (5, time(12), time(18)),
    LATE_AFTERNOON = (6, time(16), time(18)),
