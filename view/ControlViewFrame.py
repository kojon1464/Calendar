import tkinter as tk

from controller.MainControllerInterface import MainControllerInterface


class ControlViewFrame(tk.Frame):
    controller: MainControllerInterface

    def __init__(self, parent, controller: MainControllerInterface):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.next = tk.Button(self, text='next', command=lambda: controller.next_week_clicked())
        self.next.pack()

        self.previous = tk.Button(self, text='previous', command=lambda: controller.previous_week_clicked())
        self.previous.pack()

        self.create = tk.Button(self, text='create_event', command=lambda: controller.create_event_clicked())
        self.create.pack()

        self.export = tk.Button(self, text='export_file', command=lambda: controller.export_clicked())
        self.export.pack()

        self.import_btn = tk.Button(self, text='import_file', command=lambda: controller.import_clicked())
        self.import_btn.pack()

        self.statistics = tk.Button(self, text='statistics', command=lambda: controller.statistics_clicked())
        self.statistics.pack()

        self.organize = tk.Button(self, text='organize', command=lambda: controller.organize_clicked())
        self.organize.pack()
