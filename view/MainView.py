from controller.MainControllerInterface import MainControllerInterface
from data.CalendarEntity import CalendarEntity
from view.CalendarObserverInterface import CalendarObserverInterface

import tkinter as tk

from view.ControlViewFrame import ControlViewFrame
from view.eventList.EventsListFrame import EventsListFrame
from view.MainViewInterface import MainViewInterface
from view.WeekViewFrame import WeekViewFrame
from view.eventList.ListControlsFrame import ListControlsFrame

TITLE = "Calendar"
WINDOW_SIZE = "1700x900"


class MainView(CalendarObserverInterface, MainViewInterface):

    controller: MainControllerInterface
    root: tk.Tk

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title(TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.control_frame = ControlViewFrame(self.root, self.controller)
        self.control_frame.grid(column=0, row=0, sticky='n')

        self.week_frame = WeekViewFrame(self.root, self.controller)
        self.week_frame.grid(column=1, row=0, sticky='nsew')

        self.list_control_frame = ListControlsFrame(self.root, self.controller)
        self.list_control_frame.grid(column=0, row=1, sticky='nsew')

        self.events_frame = EventsListFrame(self.root, self.controller)
        self.events_frame.grid(column=1, row=1, sticky='nsew')

        self.root.update()

    def start(self):
        self.check_notifications()
        self.root.mainloop()

    def update_calendar(self, calendar: CalendarEntity):
        self.week_frame.update_view(calendar)
        self.events_frame.update_view(calendar)

    def get_top_level(self, title):
        self.top = tk.Toplevel()
        self.top.title(title)
        self.top.resizable(False, False)
        self.top.grab_set()
        return self.top

    def check_notifications(self):
        self.controller.check_notification()
        self.root.after(1000, self.check_notifications)

    def get_root(self):
        return self.root
