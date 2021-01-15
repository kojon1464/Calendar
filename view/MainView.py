from controller import MainController
from controller.MainControllerInterface import MainControllerInterface
from data.CalendarEntity import CalendarEntity
from view.CalendarObserverInterface import CalendarObserverInterface

import tkinter as tk

from view.ControlViewFrame import ControlViewFrame
from view.MainViewInterface import MainViewInterface
from view.WeekViewFrame import WeekViewFrame

TITLE = "Calendar"
WINDOW_SIZE = "1600x900"


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
        self.control_frame.grid(column=0, row=0)

        self.week_frame = WeekViewFrame(self.root, self.controller)
        self.week_frame.grid(column=1, row=0, sticky='nsew')

        self.root.update()

    def start(self):
        self.check_notifications()
        self.root.mainloop()

    def update_calendar(self, calendar: CalendarEntity):
        self.week_frame.update_view(calendar)

    def get_top_level(self, title):
        self.top = tk.Toplevel()
        self.top.title(title)
        self.top.grab_set()
        return self.top

    def check_notifications(self):
        self.controller.check_notification()
        self.root.after(1000, self.check_notifications)

    def get_root(self):
        return self.root
