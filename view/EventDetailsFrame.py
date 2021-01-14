import tkinter as tk
from datetime import datetime, time
from tkinter import ttk

from tkcalendar import DateEntry

from controller.MainControllerInterface import MainControllerInterface
from data.EventEntity import EventEntity
from model.ObjectDetailsDTO import ObjectDetailsDTO
from view.AbstractEventDetailsFrame import AbstractEventDetailsFrame

HOURS = [item for item in range(0, 24)]
MINUTES = [item for item in range(0, 60, 5)]


class EventDetailsFrame(AbstractEventDetailsFrame):

    def __init__(self, parent, controller: MainControllerInterface):
        super().__init__(parent, controller)

        self.name = tk.StringVar()
        tk.Entry(self, text=self.name).pack()

        self.date = DateEntry(self, state="readonly")
        self.date.set_date(datetime.now().date())
        self.date.pack()

        self.hour_start = tk.IntVar()
        ttk.Combobox(self, values=HOURS, textvariable=self.hour_start, state="readonly").pack()

        self.minute_start = tk.IntVar()
        ttk.Combobox(self, values=MINUTES, textvariable=self.minute_start, state="readonly").pack()

        self.hour_end = tk.IntVar()
        ttk.Combobox(self, values=HOURS, textvariable=self.hour_end, state="readonly").pack()

        self.minute_end = tk.IntVar()
        ttk.Combobox(self, values=MINUTES, textvariable=self.minute_end, state="readonly").pack()

        self.set_start_time(datetime.now().time())
        self.set_end_time(datetime.now().time())

    def set_start_time(self, time: datetime.time):
        self.hour_start.set(time.hour)
        self.minute_start.set(time.minute)

    def set_end_time(self, time: datetime.time):
        self.hour_end.set(time.hour)
        self.minute_end.set(time.minute)

    def get_start_datetime(self) -> datetime:
        t = time(self.hour_start.get(), self.minute_start.get())
        return datetime.combine(self.date.get_date(), t)

    def get_end_datetime(self) -> datetime:
        t = time(self.hour_end.get(), self.minute_end.get())
        return datetime.combine(self.date.get_date(), t)

    def update_calendar(self, details_dto: ObjectDetailsDTO):
        event = details_dto.event
        if event is None:
            return

        self.name.set(event.name)
        self.date.set_date(event.date_start.date())
        self.set_start_time(event.date_start.time())
        self.set_end_time(event.date_end.time())

    def get_event(self) -> EventEntity:
        return EventEntity(self.name.get()
                           , self.get_start_datetime()
                           , self.get_end_datetime())
