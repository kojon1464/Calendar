import tkinter as tk
import calendar
from datetime import datetime
from enum import Enum
from typing import List

from controller.MainControllerInterface import MainControllerInterface
from data.CalendarEntity import CalendarEntity
from data.EventEntity import EventEntity
from view.EventView import EventView
from view.EventsViewInterface import EventsViewInterface

DAY_FILED_HEIGHT = 80

EVENT_TAG = 'event'
COLUMN_MARGIN = 7

MIN_EVENT_HEIGHT = 65


class Positions(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    MIDDLE = 'middle'

class WeekViewFrame(tk.Frame, EventsViewInterface):
    controller: MainControllerInterface
    calendar: CalendarEntity

    def __init__(self, parent, controller: MainControllerInterface):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent, borderwidth=2, relief="groove")

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def draw_window(self):
        self.draw_weekdays_columns()
        self.draw_events()

    def draw_weekdays_columns(self):
        self.canvas.create_line(0, DAY_FILED_HEIGHT, self.winfo_width(), DAY_FILED_HEIGHT)

        self.create_columns_lines()
        self.create_weekdays_labels()

    def create_columns_lines(self):
        for i in range(1, 7):
            x_position = self.winfo_width() / 7 * i
            self.canvas.create_line(x_position, 0, x_position, self.winfo_height())

    def create_weekdays_labels(self):
        weekdays_names = list(calendar.day_name)

        for i in range(0, 7):
            x_position = self.winfo_width() / 14 * (2 * i + 1)
            self.canvas.create_text(x_position, DAY_FILED_HEIGHT / 3, text=weekdays_names[i], font="Times 20 bold")
            self.canvas.create_text(x_position, 2 * DAY_FILED_HEIGHT / 3, text=self.calendar.week[i])

    def update_view(self, calendar: CalendarEntity):
        self.calendar = calendar
        self.canvas.delete('all')
        self.draw_window()

    def create_event(self, event: EventEntity, x0, y0, x1, y1, color: str, tag:str):
        width = x1 - x0
        height = max(y1 - y0, MIN_EVENT_HEIGHT)
        event_view = EventView(self.parent, event, color)
        event_view.bind_with_children('<Button-1>', lambda e: self.controller.update_event_clicked(event.id))
        self.canvas.create_window(x0, y0, width=width, height=height, window=event_view, anchor=tk.NW, tags=(tag, EVENT_TAG))

    def draw_events(self):
        for i in range(0, 7):
            day = self.calendar.week[i]
            self.draw_events_for_day(self.calendar.get_events_within_day(day), i)
            self.fix_overlapping_events_for_day(i)

    def draw_events_for_day(self, events: List[EventEntity], day_number: int):
        x0 = (self.winfo_width() / 7) * day_number + COLUMN_MARGIN
        x1 = (self.winfo_width() / 7) * (day_number + 1) - COLUMN_MARGIN

        for event in events:
            size_of_minute = (self.winfo_height() - DAY_FILED_HEIGHT) / (24 * 60)
            y0 = size_of_minute * self.tome_to_minutes(event.date_start.time()) + DAY_FILED_HEIGHT
            y1 = size_of_minute * self.tome_to_minutes(event.date_end.time()) + DAY_FILED_HEIGHT

            self.create_event(event, x0, y0, x1, y1, 'red', EVENT_TAG + day_number.__str__())

    def fix_overlapping_events_for_day(self, day_number: int):
        x0 = (self.winfo_width() / 7) * day_number + COLUMN_MARGIN
        x1 = (self.winfo_width() / 7) * (day_number + 1) - COLUMN_MARGIN
        number_of_segments = 24*4
        segment_height = (self.winfo_height() - DAY_FILED_HEIGHT) / number_of_segments

        for i in range(0, number_of_segments):
            overlapping = self.get_overlapping_events(x0, segment_height * i + DAY_FILED_HEIGHT, x1, segment_height * (i + 1) + DAY_FILED_HEIGHT)

            for event in overlapping:
                self.ensure_tag(event, len(overlapping).__str__())

        for event in self.canvas.find_withtag(EVENT_TAG + day_number.__str__()):
            self.change_width_by_tag_number(event)

        for i in range(0, number_of_segments):
            overlapping = self.get_overlapping_events(x0, segment_height * i, x1, segment_height * (i + 1))
            (without, taken) = self.get_without_position_and_taken_positions(overlapping)
            for event in without:
                if Positions.LEFT not in taken:
                    self.ensure_tag(event, Positions.LEFT.value)
                    taken.append(Positions.LEFT)
                elif Positions.RIGHT not in taken:
                    self.ensure_tag(event, Positions.RIGHT.value)
                    taken.append(Positions.RIGHT)
                elif Positions.MIDDLE not in taken:
                    self.ensure_tag(event, Positions.MIDDLE.value)
                    taken.append(Positions.MIDDLE)

        for event in self.canvas.find_withtag(EVENT_TAG + day_number.__str__()):
            self.move_event_to_correct_position(event)

    def move_event_to_correct_position(self, event: int):
        position = self.get_event_position(event)
        event_width = self.get_event_width(event)

        if Positions.LEFT == position:
            return
        elif Positions.RIGHT == position:
            if self.get_width_divider(event) == 2:
                self.canvas.move(event, event_width, 0)
            else:
                self.canvas.move(event, 2 * event_width, 0)
        elif Positions.MIDDLE == position:
            self.canvas.move(event, event_width, 0)

    def get_event_position(self, event: int) -> Positions:
        tags = self.canvas.gettags(event)
        for position in Positions:
            if position.value in tags:
                return position

        return None

    def get_without_position_and_taken_positions(self, events: List[int]):
        taken = []
        without = []
        for event in events:
            position = self.get_event_position(event)

            if position is None:
                without.append(event)
            else:
                taken.append(position)

        return (without, taken)

    def change_width_by_tag_number(self, id: int):
        divider = self.get_width_divider(id)
        self.change_event_width(id, self.get_event_width(id) / divider)

    def get_width_divider(self, event: int) -> int:
        tags = self.canvas.gettags(event)
        for i in reversed(range(1, 4)):
            if i.__str__() in tags:
                return i

        return 4

    def ensure_tag(self, id: int, tag: str):
        if tag not in self.canvas.gettags(id):
            self.canvas.addtag_withtag(tag, id)

    def get_overlapping_events(self, x0, y0, x1, y1) -> List[int]:
        overlapps = list(self.canvas.find_overlapping(x0 + 3, y0 + 3, x1 - 3, y1 - 3))
        return [item for item in overlapps if EVENT_TAG in self.canvas.gettags(item)]

    def change_event_width(self, event_id: int, width: int):
        self.canvas.itemconfigure(event_id, width=width)

    def get_event_width(self, event_id: int) -> int:
        configuration = self.canvas.itemconfigure(event_id)
        return int(configuration['width'][4])

    def get_event_height(self, event_id: int) -> int:
        configuration = self.canvas.itemconfigure(event_id)
        return int(configuration['height'][4])

    def tome_to_minutes(self, time: datetime.time) -> int:
        return time.hour * 60 + time.minute
