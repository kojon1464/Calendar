import tkinter as tk
from datetime import datetime, time, timedelta
from tkinter import ttk

from tkcalendar import DateEntry

from controller.MainControllerInterface import MainControllerInterface
from data.DayTime import DayTime
from data.EventEntity import EventEntity
from data.Priority import Priority
from model.ObjectDetailsDTO import ObjectDetailsDTO
from view.AbstractEventDetailsFrame import AbstractEventDetailsFrame

HOURS = [item for item in range(0, 24)]
MINUTES = [item for item in range(0, 60, 5)]


class EventDetailsFrame(AbstractEventDetailsFrame):

    def __init__(self, parent, controller: MainControllerInterface):
        super().__init__(parent, controller)

        self.id = None
        self.uid = None

        self.name = tk.StringVar()
        tk.Entry(self, text=self.name).pack()

        self.loose = tk.BooleanVar()
        tk.Checkbutton(self, text="Lose event (time frame not set)", variable=self.loose, command=self.looseness_changed).pack()

        self.date = DateEntry(self, state="readonly")
        self.date.set_date(datetime.now().date())
        self.date.pack()

        self.hour_start = tk.IntVar()
        self.hour_start_combo = ttk.Combobox(self, values=HOURS, textvariable=self.hour_start, state="readonly")
        self.hour_start_combo.pack()

        self.minute_start = tk.IntVar()
        self.minute_start_combo = ttk.Combobox(self, values=MINUTES, textvariable=self.minute_start, state="readonly")
        self.minute_start_combo.pack()

        self.hour_end = tk.IntVar()
        self.hour_end_combo = ttk.Combobox(self, values=HOURS, textvariable=self.hour_end, state="readonly")
        self.hour_end_combo.pack()

        self.minute_end = tk.IntVar()
        self.minute_end_combo = ttk.Combobox(self, values=MINUTES, textvariable=self.minute_end, state="readonly")
        self.minute_end_combo.pack()

        self.time_window = tk.BooleanVar()
        tk.Checkbutton(self, text="Time window (for organising loose events)", variable=self.time_window, command=self.time_window_changed).pack()

        self.hour_before = tk.IntVar()
        self.hour_before_combo = ttk.Combobox(self, values=HOURS, textvariable=self.hour_before, state="readonly")

        self.minute_before = tk.IntVar()
        self.minute_before_combo = ttk.Combobox(self, values=MINUTES, textvariable=self.minute_before, state="readonly")

        self.hour_after = tk.IntVar()
        self.hour_after_combo = ttk.Combobox(self, values=HOURS, textvariable=self.hour_after, state="readonly")

        self.minute_after = tk.IntVar()
        self.minute_after_combo = ttk.Combobox(self, values=MINUTES, textvariable=self.minute_after, state="readonly")

        self.priority = tk.StringVar()
        self.priority.set(Priority.UNDEFINED.name)
        ttk.Combobox(self, values=[i.name for i in list(Priority)], textvariable=self.priority, state="readonly").pack()

        self.day_time = tk.StringVar()
        self.day_time.set(DayTime.UNDEFINED.name)
        ttk.Combobox(self, values=[i.name.replace('_', ' ') for i in list(DayTime)], textvariable=self.day_time, state="readonly").pack()

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.winfo_toplevel().destroy())
        self.cancel_btn.pack()

        self.set_start_time(datetime.now().time())
        self.set_end_time(datetime.now().time())

    # region time helpers
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
    # endregion

    # region delta helpers
    def set_before_time(self, delta: timedelta):
        self.hour_before.set(self.calculate_hours(delta))
        self.minute_before.set(self.calculate_minutes(delta))

    def set_after_time(self, delta: timedelta):
        self.hour_after.set(self.calculate_hours(delta))
        self.minute_after.set(self.calculate_minutes(delta))

    def get_before_timedelta(self) -> timedelta:
        return timedelta(hours=self.hour_before.get(), minutes=self.minute_before.get())

    def get_after_timedelta(self) -> timedelta:
        return timedelta(hours=self.hour_after.get(), minutes=self.minute_after.get())

    def calculate_hours(self, delta: timedelta):
        return delta.seconds//3600

    def calculate_minutes(self, delta: timedelta):
        return (delta.seconds//60)%60
    # endregion

    def update_calendar(self, details_dto: ObjectDetailsDTO):
        event = details_dto.event
        if event is None:
            return

        self.id = event.id
        self.uid = event.uid

        self.name.set(event.name)
        self.date.set_date(event.date_start.date())
        self.set_start_time(event.date_start.time())
        self.set_end_time(event.date_end.time())
        self.loose.set(event.loose)
        self.priority.set(event.priority.name)
        self.day_time.set(event.day_time.name.replace('_', ' '))
        self.time_window.set(event.time_window)
        self.set_before_time(event.time_before)
        self.set_after_time(event.time_after)

        self.looseness_changed()
        self.time_window_changed()

    def get_event(self) -> EventEntity:
        event = EventEntity(self.name.get()
                            , self.get_start_datetime()
                            , self.get_end_datetime()
                            , self.loose.get()
                            , Priority[self.priority.get()]
                            , DayTime[self.day_time.get().replace(' ', '_')]
                            , self.time_window.get()
                            , self.get_before_timedelta()
                            , self.get_after_timedelta())
        event.id = self.id
        event.uid = self.uid
        return event

    def time_window_changed(self):
        if self.time_window.get() == True:
            self.show_delta_picker()
        else:
            self.hide_delta_picker()

    def hide_delta_picker(self):
        self.hour_before_combo.pack_forget()
        self.minute_before_combo.pack_forget()
        self.hour_after_combo.pack_forget()
        self.minute_after_combo.pack_forget()

    def show_delta_picker(self):
        self.hour_before_combo.pack()
        self.minute_before_combo.pack()
        self.hour_after_combo.pack()
        self.minute_after_combo.pack()

    def looseness_changed(self):
        if self.loose.get() == False:
            self.show_time_picker()
        else:
            self.hide_time_picker()

    def hide_time_picker(self):
        self.date.pack_forget()
        self.hour_start_combo.pack_forget()
        self.minute_start_combo.pack_forget()
        self.hour_end_combo.pack_forget()
        self.minute_end_combo.pack_forget()

    def show_time_picker(self):
        self.date.pack()
        self.hour_start_combo.pack()
        self.minute_start_combo.pack()
        self.hour_end_combo.pack()
        self.minute_end_combo.pack()
