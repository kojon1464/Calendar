import tkinter as tk
import calendar
from datetime import datetime
from typing import List

from controller.MainController import MainController
from data.CalendarEntity import CalendarEntity
from data.EventEntity import EventEntity
from view.EventView import EventView

DAY_FILED_HEIGHT = 80

EVENT_TAG = 'event'
EVENT_MARGIN = 5


class WeekViewFrame(tk.Frame):
    controller: MainController
    calendar: CalendarEntity

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

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
        self.draw_window()

    def create_event(self, event: EventEntity, x0, y0, x1, y1, color: str):
        width = x1 - x0
        height = y1 - y0
        event_view = EventView(self.parent, event, color)
        self.canvas.create_window(x0, y0, width=width, height=height, window=event_view, anchor=tk.NW, tags=EVENT_TAG)

    def draw_events(self):
        for i in range(0, 7):
            day = self.calendar.week[i]
            self.draw_events_for_day(self.calendar.get_events_within_day(day), i)

        self.fix_overlapping_events()

    def draw_events_for_day(self, events: List[EventEntity], day_number: int):
        x0 = (self.winfo_width() / 7) * day_number + 7
        x1 = (self.winfo_width() / 7) * (day_number + 1) - 7

        for event in events:
            size_of_minute = (self.winfo_height() - DAY_FILED_HEIGHT) / (24 * 60)
            y0 = size_of_minute * self.tome_to_minutes(event.date_start.time())
            y1 = size_of_minute * self.tome_to_minutes(event.date_end.time())

            self.create_event(event, x0, y0, x1, y1, 'red')

    def fix_overlapping_events(self):
        for event_id in self.canvas.find_withtag(EVENT_TAG):
            overlapping = self.get_overlapping_for_event(event_id)

            if len(overlapping) <= 1:
                continue

            desired_width = (self.winfo_width() / 7 - 14) / len(overlapping)

            for overlapping_id in overlapping:
                if self.get_event_width(overlapping_id) > desired_width:
                    self.change_event_width(overlapping_id, desired_width)

            for overlapping_id in overlapping:
                self.move_to_free_space(overlapping_id, len(overlapping))

    def move_to_free_space(self, event_id: int, number_od_moves: int):
        for i in range(0, number_od_moves):
            if len(self.get_overlapping_for_event(event_id)) > 1:
                self.canvas.move(event_id, self.get_event_width(event_id), 0)
            else:
                return

    def get_overlapping_for_event(self, event_id: int) -> List[int]:
        (x, y) = self.canvas.coords(event_id)
        overlapps = list(self.canvas.find_overlapping(x + 3, y + 3, x + self.get_event_width(event_id) - 3, y + self.get_event_height(event_id) - 3))
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
