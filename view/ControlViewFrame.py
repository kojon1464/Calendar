import tkinter as tk

from tkcalendar import Calendar

from controller.MainControllerInterface import MainControllerInterface

BUTTON_FONT = 'Helvetica 13'

class ControlViewFrame(tk.Frame):
    controller: MainControllerInterface

    def __init__(self, parent, controller: MainControllerInterface):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.previous = tk.Button(self, text='<-', command=lambda: controller.previous_week_clicked(), font=BUTTON_FONT)
        self.previous.grid(row=0, column=0, sticky='we')

        self.next = tk.Button(self, text='->', command=lambda: controller.next_week_clicked(), font=BUTTON_FONT)
        self.next.grid(row=0, column=1, sticky='we')

        self.calendar = Calendar(self)
        self.calendar.bind('<<CalendarSelected>>', lambda e: self.controller.calendar_date_chosen(self.calendar.get_date()))
        self.calendar.grid(row=1, column=0, columnspan=2, sticky='we')

        self.create = tk.Button(self, text='create event', command=lambda: controller.create_event_clicked(), font=BUTTON_FONT)
        self.create.grid(row=2, column=0, columnspan=2, sticky='we')

        self.export = tk.Button(self, text='export file', command=lambda: controller.export_clicked(), font=BUTTON_FONT)
        self.export.grid(row=3, column=0, columnspan=2, sticky='we')

        self.import_btn = tk.Button(self, text='import file', command=lambda: controller.import_clicked(), font=BUTTON_FONT)
        self.import_btn.grid(row=4, column=0, columnspan=2, sticky='we')

        self.statistics = tk.Button(self, text='statistics', command=lambda: controller.statistics_clicked(), font=BUTTON_FONT)
        self.statistics.grid(row=5, column=0, columnspan=2, sticky='we')

        self.organize = tk.Button(self, text='organize', command=lambda: controller.organize_clicked(), font=BUTTON_FONT)
        self.organize.grid(row=6, column=0, columnspan=2, sticky='we')
