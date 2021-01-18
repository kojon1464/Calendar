import tkinter as tk
from abc import ABC
from tkinter import ttk
from typing import List, Set, re

from controller.MainControllerInterface import MainControllerInterface
from data.CalendarEntity import CalendarEntity
from data.EventEntity import EventEntity
from view.EventsListInterface import EventsListInterface
from view.EventsViewInterface import EventsViewInterface


class EventsListFrame(tk.Frame, EventsViewInterface, EventsListInterface):
    controller: MainControllerInterface

    calendar: CalendarEntity
    def __init__(self, parent, controller: MainControllerInterface):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind('<Double-1>', self.on_double_click)

        self.create_columns()
        self.create_heading()

    def create_columns(self):
        self.tree['columns'] = ('name', 'description', 'priority', 'day_time')
        self.tree.column('#0', width=0, stretch=tk.NO)

        self.tree.column('name', width=200, minwidth=150)
        self.tree.column('description', width=400, minwidth=200)
        self.tree.column('priority', width=150, minwidth=100)
        self.tree.column('day_time', width=150, minwidth=100)

    def create_heading(self):
        self.tree.heading('name', text='Name', anchor=tk.W)
        self.tree.heading('description', text='Description', anchor=tk.W)
        self.tree.heading('priority', text='Priority', anchor=tk.W)
        self.tree.heading('day_time', text='Time of the Day', anchor=tk.W)

    def update_rows(self, events: Set[EventEntity]):
        self.tree.delete(*self.tree.get_children())
        for event in events:
            self.insert_event(event)

    def insert_event(self, event: EventEntity):
        self.tree.insert('', 'end', text=event.id, values=(event.name
                                                           , event.get_single_line_description()
                                                           , event.priority.name
                                                           , event.day_time.name.replace('_', ' ')))

    def on_double_click(self, event):
        item_id = event.widget.focus()
        item = event.widget.item(item_id)
        event_id = item['text']
        self.controller.update_event_clicked(event_id)

    def update_view(self, calendar: CalendarEntity):
        self.update_rows(calendar.events_loose)

    def disable_double_click(self):
        self.tree.unbind('<Double-1>')

    def get_selected_ids(self) -> List[int]:
        return list(self.tree.selection())
