import tkinter as tk
from datetime import datetime, time, timedelta
from tkinter import ttk

from tkcalendar import DateEntry

from controller.MainControllerInterface import MainControllerInterface
from data.enums.DayTime import DayTime
from data.EventEntity import EventEntity
from data.enums.Priority import Priority
from model.ObjectDetailsDTO import ObjectDetailsDTO
from view.eventDetails.AbstractEventDetailsFrame import AbstractEventDetailsFrame

HOURS = [item for item in range(0, 24)]
MINUTES = [item for item in range(0, 60, 5)]
DURATION = [item for item in range(0, 400, 15)]

FRAME_SIZE = '400x480'
PAD_Y = 5

class EventDetailsFrame(AbstractEventDetailsFrame):

    def __init__(self, parent, controller: MainControllerInterface):
        super().__init__(parent, controller)

        self.parent.geometry(FRAME_SIZE)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(9, weight=1)

        self.id = None
        self.uid = None

        tk.Label(self, text='Name ').grid(row=0, column=3, pady=PAD_Y, sticky=tk.E)
        self.name = tk.StringVar()
        tk.Entry(self, text=self.name).grid(row=0, column=4, pady=PAD_Y, sticky=tk.W)

        self.description = tk.Text(self, width=40, height=7)
        self.description.grid(row=1, column=2, columnspan=4, pady=PAD_Y)

        self.loose = tk.BooleanVar()
        tk.Checkbutton(self, text="Lose event (time frame not set)", variable=self.loose, command=self.looseness_changed).grid(row=3, column=3, columnspan=2, pady=PAD_Y)

        self.init_duration()
        self.init_time_picker()

        self.time_window = tk.BooleanVar()
        tk.Checkbutton(self, text="Time window", variable=self.time_window, command=self.time_window_changed).grid(row=5, column=3, columnspan=2, pady=PAD_Y)

        self.init_delta()

        tk.Label(self, text='Priority ').grid(row=7, column=3, pady=PAD_Y, sticky=tk.E)
        self.priority = tk.StringVar()
        self.priority.set(Priority.UNDEFINED.name)
        ttk.Combobox(self, values=[i.name for i in list(Priority)], textvariable=self.priority, state="readonly")\
            .grid(row=7, column=4, pady=PAD_Y, sticky=tk.W)

        tk.Label(self, text='Day time ').grid(row=8, column=3, pady=PAD_Y, sticky=tk.E)
        self.day_time = tk.StringVar()
        self.day_time.set(DayTime.UNDEFINED.name)
        ttk.Combobox(self, values=[i.name.replace('_', ' ') for i in list(DayTime)], textvariable=self.day_time, state="readonly")\
            .grid(row=8, column=4, pady=PAD_Y, sticky=tk.W)

        self.cancel_btn = tk.Button(self.button_frame, text='Cancel', command=lambda: self.winfo_toplevel().destroy())
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        self.button_frame.grid(row=9, column=4, columnspan=3, pady=PAD_Y, sticky='es', padx=10)

        self.set_start_time(datetime.now().time())
        self.set_end_time(datetime.now().time())
        self.time_window_changed()

    def init_delta(self):
        self.delta_frame = tk.Frame(self, highlightbackground="gray", highlightthickness=1)

        tk.Label(self.delta_frame, text='Before:').grid(row=0, column=0, pady=PAD_Y)
        self.hour_before = tk.IntVar()
        self.hour_before_combo = ttk.Combobox(self.delta_frame, values=HOURS, textvariable=self.hour_before, state="readonly", width=2)
        self.hour_before_combo.grid(row=0, column=1, pady=PAD_Y)

        tk.Label(self.delta_frame, text='hours ').grid(row=0, column=2, pady=PAD_Y)
        self.minute_before = tk.IntVar()
        self.minute_before_combo = ttk.Combobox(self.delta_frame, values=MINUTES, textvariable=self.minute_before, state="readonly", width=2)
        self.minute_before_combo.grid(row=0, column=3, pady=PAD_Y)
        tk.Label(self.delta_frame, text='minutes').grid(row=0, column=4, pady=PAD_Y)

        tk.Label(self.delta_frame, text=' After:').grid(row=1, column=0, pady=PAD_Y)
        self.hour_after = tk.IntVar()
        self.hour_after_combo = ttk.Combobox(self.delta_frame, values=HOURS, textvariable=self.hour_after, state="readonly", width=2)
        self.hour_after_combo.grid(row=1, column=1, pady=PAD_Y)

        tk.Label(self.delta_frame, text='hours ').grid(row=1, column=2, pady=PAD_Y)
        self.minute_after = tk.IntVar()
        self.minute_after_combo = ttk.Combobox(self.delta_frame, values=MINUTES, textvariable=self.minute_after, state="readonly", width=2)
        self.minute_after_combo.grid(row=1, column=3, pady=PAD_Y)
        tk.Label(self.delta_frame, text='minutes').grid(row=1, column=4, pady=PAD_Y)

        self.delta_frame.grid(row=6, column=3, columnspan=2, pady=PAD_Y)

    def init_duration(self):
        self.duration_frame = tk.Frame(self, highlightbackground="gray", highlightthickness=1)

        tk.Label(self.duration_frame, text='Duration ').pack(side=tk.LEFT, pady=PAD_Y)
        self.duration = tk.IntVar()
        self.duration_combo = ttk.Combobox(self.duration_frame, values=DURATION, textvariable=self.duration, state="readonly", width=4)
        self.duration_combo.pack(side=tk.LEFT, pady=PAD_Y, padx=5)

        self.duration_frame.grid(row=4, column=3, columnspan=2, pady=PAD_Y)

    def init_time_picker(self):
        self.time_frame = tk.Frame(self, highlightbackground="gray", highlightthickness=1)

        date_frame = tk.Frame(self.time_frame)

        tk.Label(date_frame, text='Date  ').pack(side=tk.LEFT, pady=PAD_Y)
        self.date = DateEntry(date_frame, state="readonly")
        self.date.set_date(datetime.now().date())
        self.date.pack(side=tk.LEFT)

        date_frame.pack(side=tk.TOP, anchor=tk.W)

        tk.Label(self.time_frame, text='From ').pack(side=tk.LEFT, pady=PAD_Y)
        self.hour_start = tk.IntVar()
        self.hour_start_combo = ttk.Combobox(self.time_frame, values=HOURS, textvariable=self.hour_start, state="readonly", width=2)
        self.hour_start_combo.pack(side=tk.LEFT, pady=PAD_Y)

        tk.Label(self.time_frame, text=':').pack(side=tk.LEFT, pady=PAD_Y)
        self.minute_start = tk.IntVar()
        self.minute_start_combo = ttk.Combobox(self.time_frame, values=MINUTES, textvariable=self.minute_start, state="readonly", width=2)
        self.minute_start_combo.pack(side=tk.LEFT, pady=PAD_Y)

        tk.Label(self.time_frame, text=' to ').pack(side=tk.LEFT, pady=PAD_Y)
        self.hour_end = tk.IntVar()
        self.hour_end_combo = ttk.Combobox(self.time_frame, values=HOURS, textvariable=self.hour_end, state="readonly", width=2)
        self.hour_end_combo.pack(side=tk.LEFT, pady=PAD_Y)

        tk.Label(self.time_frame, text=':').pack(side=tk.LEFT, pady=PAD_Y)
        self.minute_end = tk.IntVar()
        self.minute_end_combo = ttk.Combobox(self.time_frame, values=MINUTES, textvariable=self.minute_end, state="readonly", width=2)
        self.minute_end_combo.pack(side=tk.LEFT, pady=PAD_Y, padx=5)

        self.time_frame.grid(row=4, column=3, columnspan=2, pady=PAD_Y)

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

    def update_details(self, details_dto: ObjectDetailsDTO):
        event = details_dto.event
        if event is None:
            return

        self.id = event.id
        self.uid = event.uid

        self.name.set(event.name)
        self.date.set_date(event.date_start.date())
        self.set_start_time(event.date_start.time())
        self.set_end_time(event.date_end.time())
        self.duration.set(event.duration)
        self.description.insert(1.0, event.description)
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
                            , self.description.get(1.0, tk.END)
                            , self.duration.get()
                            , self.loose.get()
                            , Priority[self.priority.get()]
                            , DayTime[self.day_time.get().replace(' ', '_')]
                            , self.time_window.get()
                            , self.get_before_timedelta()
                            , self.get_after_timedelta())
        event.id = self.id
        if self.uid is not None:
            event.uid = self.uid
        return event

    def time_window_changed(self):
        if self.time_window.get() == True:
            self.show_delta_picker()
        else:
            self.hide_delta_picker()

    def hide_delta_picker(self):
        self.delta_frame.grid_forget()

    def show_delta_picker(self):
        self.delta_frame.grid(row=6, column=3, columnspan=2, pady=PAD_Y)

    def looseness_changed(self):
        if self.loose.get() == False:
            self.show_time_picker()
            self.duration_frame.grid_forget()
        else:
            self.hide_time_picker()
            self.duration_frame.grid(row=4, column=3, columnspan=2, pady=PAD_Y)

    def hide_time_picker(self):
        self.time_frame.grid_forget()

    def show_time_picker(self):
        self.time_frame.grid(row=4, column=3, columnspan=2, pady=PAD_Y)
