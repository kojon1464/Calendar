from controller import MainController
from data.CalendarEntity import CalendarEntity
from view.CalendarObserverInterface import CalendarObserverInterface

import tkinter as tk

from view.WeekViewFrame import WeekViewFrame

TITLE = "Calendar"
WINDOW_SIZE = "1500x700"

class MainView(CalendarObserverInterface):

    controller: MainController
    root: tk.Tk

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title(TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frame = WeekViewFrame(self.root, self)
        self.frame.grid(column=0, row=0, sticky='nsew')

        self.root.update()


    def start(self):
        self.root.mainloop()

    def update_calendar(self, calendar: CalendarEntity):
        self.frame.update_view(calendar)
