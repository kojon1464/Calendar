import tkinter as tk
from tkinter import ttk

from controller.MainControllerInterface import MainControllerInterface
from data.enums.EventSortMethod import EventSortMethod


class ListControlsFrame(tk.Frame):
    controller: MainControllerInterface

    def __init__(self, parent, controller: MainControllerInterface):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent, borderwidth=2, relief="groove")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(6, weight=2)
        self.rowconfigure(8, weight=7)

        self.columnconfigure(0, weight=1)

        tk.Label(self, text='Filter name ').grid(row=1, column=0)
        self.name_filter = tk.StringVar()
        self.name_filter.trace('w', lambda *args: self.controller.name_filter_changes(self.name_filter.get()))
        tk.Entry(self, textvariable=self.name_filter, width=23).grid(row=2, column=0)

        tk.Label(self, text='Sort by ').grid(row=4, column=0)
        self.priority = tk.StringVar()
        self.priority.set(EventSortMethod.PRIORITY.name.lower())
        self.priority.trace('w', lambda *args: self.controller.sort_changes(EventSortMethod[self.priority.get().replace(' ', '_').upper()]))
        ttk.Combobox(self, values=[i.name.replace('_', ' ').lower() for i in list(EventSortMethod)], textvariable=self.priority, state="readonly").grid(row=5, column=0)

        self.loose = tk.BooleanVar()
        tk.Checkbutton(self, text="Only loose", variable=self.loose, command=lambda: self.controller.loose_filter_changes(self.loose.get())).grid(row=7, column=0)
