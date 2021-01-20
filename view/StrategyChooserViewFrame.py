from datetime import datetime, time
from tkinter import ttk
from tkinter.messagebox import showerror

from tkcalendar import DateEntry

from controller.MainControllerInterface import MainControllerInterface
from data.CalendarEntity import CalendarEntity
from data.enums.OrganizationStrategy import OrganizationStrategy
from view.CalendarObserverInterface import CalendarObserverInterface
import tkinter as tk

from view.eventList.EventsListFrame import EventsListFrame

HOURS = [item for item in range(0, 24)]
MINUTES = [item for item in range(0, 60, 5)]

PAD_Y = 5


class StrategyChooserViewFrame(tk.Frame, CalendarObserverInterface):

    def __init__(self, parent, controller: MainControllerInterface):

        self.controller = controller
        self.parent = parent

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(6, weight=8)

        self.info = tk.StringVar()
        tk.Label(self, textvariable=self.info).grid(row=1, column=0, columnspan=9, pady=PAD_Y)

        self.strategy_frame = tk.Frame(self)

        tk.Label(self.strategy_frame, text='Select strategy used for organizing: ').pack(side=tk.LEFT)
        self.strategy = tk.StringVar()
        self.strategy.set(OrganizationStrategy.GREEDY.name.lower())
        self.combo = ttk.Combobox(self.strategy_frame, values=[i.name.lower() for i in list(OrganizationStrategy)], textvariable=self.strategy, state="readonly")
        self.combo.bind('<<ComboboxSelected>>', self.combo_changed)
        self.combo_changed(None)
        self.combo.pack(side=tk.LEFT)

        self.strategy_frame.grid(row=0, column=4, pady=PAD_Y)

        self.init_date_widgets()
        self.init_time_widgets()

        self.event_list = EventsListFrame(self, self.controller)
        self.event_list.configure(width=100)
        self.event_list.disable_double_click()
        self.event_list.grid(row=4, column=0, columnspan=9, pady=PAD_Y, padx=10)

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.winfo_toplevel().destroy())
        self.cancel_btn.grid(row=5, column=7, pady=PAD_Y, padx=10)

        self.organize_btn = tk.Button(self, text='Organize', command=lambda: self.organize_clicked())
        self.organize_btn.grid(row=5, column=8, pady=PAD_Y, padx=10)

    def init_date_widgets(self):
        self.date_frame = tk.Frame(self)

        tk.Label(self.date_frame, text='Organize in period from ').pack(side=tk.LEFT)
        self.date_start = DateEntry(self.date_frame, state="readonly")
        self.date_start.set_date(datetime.now().date())
        self.date_start.pack(side=tk.LEFT)

        tk.Label(self.date_frame, text=' to ').pack(side=tk.LEFT)
        self.date_end = DateEntry(self.date_frame, state="readonly")
        self.date_end.set_date(datetime.now().date())
        self.date_end.pack(side=tk.LEFT)

        self.date_frame.grid(row=2, column=4, pady=PAD_Y)

    def init_time_widgets(self):
        self.time_frame = tk.Frame(self)

        tk.Label(self.time_frame, text='Select time period considered:').pack(side=tk.LEFT)
        self.hour_start = tk.IntVar()
        self.hour_start_combo = ttk.Combobox(self.time_frame, values=HOURS, textvariable=self.hour_start, state="readonly", width=2)
        self.hour_start_combo.pack(side=tk.LEFT)
        tk.Label(self.time_frame, text=':').pack(side=tk.LEFT)

        self.minute_start = tk.IntVar()
        self.minute_start_combo = ttk.Combobox(self.time_frame, values=MINUTES, textvariable=self.minute_start, state="readonly", width=2)
        self.minute_start_combo.pack(side=tk.LEFT)
        tk.Label(self.time_frame, text=' to ').pack(side=tk.LEFT)

        self.hour_end = tk.IntVar()
        self.hour_end_combo = ttk.Combobox(self.time_frame, values=HOURS, textvariable=self.hour_end, state="readonly", width=2)
        self.hour_end_combo.pack(side=tk.LEFT)
        tk.Label(self.time_frame, text=':').pack(side=tk.LEFT)

        self.minute_end = tk.IntVar()
        self.minute_end_combo = ttk.Combobox(self.time_frame, values=MINUTES, textvariable=self.minute_end, state="readonly", width=2)
        self.minute_end_combo.pack(side=tk.LEFT)

        self.time_frame.grid(row=3, column=4, pady=PAD_Y)

    def combo_changed(self, e):
        strategy = OrganizationStrategy[self.strategy.get().upper()]
        self.info.set(strategy.value[1])

    def organize_clicked(self):
        error = self.validate_inputs()
        if error is None:
            self.controller.organize_events(self.event_list.get_selected_ids(),
                                            self.date_start.get_date(),
                                            self.date_end.get_date(),
                                            self.get_start_time(),
                                            self.get_end_time(),
                                            OrganizationStrategy[self.strategy.get().upper()])
        else:
            showerror(title='Validation Error', message=error)

    def validate_inputs(self):
        if self.date_start.get_date() > self.date_end.get_date():
            return 'Start date cannot be after end date'
        if self.get_start_time() > self.get_end_time():
            return 'Start time cannot be after end time'
        if len(self.event_list.get_selected_ids()) < 1:
            return 'Select at least one event'
        return None

    def update_calendar(self, calendar: CalendarEntity):
        self.event_list.update_view(calendar)

    # region time helpers
    def set_start_time(self, time: datetime.time):
        self.hour_start.set(time.hour)
        self.minute_start.set(time.minute)

    def set_end_time(self, time: datetime.time):
        self.hour_end.set(time.hour)
        self.minute_end.set(time.minute)

    def get_start_time(self) -> time:
        return time(self.hour_start.get(), self.minute_start.get())

    def get_end_time(self) -> time:
        return time(self.hour_end.get(), self.minute_end.get())
    # endregion
