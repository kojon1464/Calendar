import calendar
from typing import List

from pandas import DataFrame

from data.enums.DayTime import DayTime
from data.EventEntity import EventEntity
from data.enums.Priority import Priority
from data.Statistics import Statistics


def get_weekday_distribution(events: List[EventEntity]) -> Statistics:
    count = [0] * 7

    for event in events:
        weekday = event.date_start.date().weekday()
        count[weekday] = count[weekday] + 1

    data = {'Weekday': list(calendar.day_name),
             'Number_of_events': count
             }
    df = DataFrame(data, columns=['Weekday', 'Number_of_events'])
    df = df[['Weekday', 'Number_of_events']].groupby('Weekday', sort=False).sum()

    return Statistics(df, "Weekdays")


def get_priority_distribution(events: List[EventEntity]) -> Statistics:
    priorities_dict = {priority.name: 0 for priority in list(Priority)}

    for event in events:
        priority_name = event.priority.name
        priorities_dict[priority_name] = priorities_dict[priority_name] + 1

    data = {'Priority': list(priorities_dict.keys()),
             'Number_of_events': list(priorities_dict.values())
             }
    df = DataFrame(data, columns=['Priority', 'Number_of_events'])
    df = df[['Priority', 'Number_of_events']].groupby('Priority', sort=False).sum()

    return Statistics(df, "Priorities")


def get_loose_windowed_distribution(events: List[EventEntity]) -> Statistics:
    dictionary = {item: 0 for item in ['Neither', 'Loose', 'Time Windowed']}

    for event in events:
        if event.loose:
            dictionary['Loose'] = dictionary['Loose'] + 1
        if event.time_window:
            dictionary['Time Windowed'] = dictionary['Time Windowed'] + 1
        if not event.loose and not event.time_window:
            dictionary['Neither'] = dictionary['Neither'] + 1

    data = {'State': list(dictionary.keys()),
             'Number_of_events': list(dictionary.values())
             }
    df = DataFrame(data, columns=['State', 'Number_of_events'])
    df = df[['State', 'Number_of_events']].groupby('State', sort=False).sum()

    return Statistics(df, "States of events")


def get_daytime_preferred_distribution(events: List[EventEntity]) -> Statistics:
    daytime_dict = {daytime.name: 0 for daytime in list(DayTime)}

    for event in events:
        daytime_name = event.day_time.name
        daytime_dict[daytime_name] = daytime_dict[daytime_name] + 1

    data = {'Day Time': list(daytime_dict.keys()),
             'Number_of_events': list(daytime_dict.values())
             }
    df = DataFrame(data, columns=['Day Time', 'Number_of_events'])
    df = df[['Day Time', 'Number_of_events']].groupby('Day Time', sort=False).sum()

    return Statistics(df, "Day Time")