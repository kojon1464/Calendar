import tkinter as tk
from abc import ABC, abstractmethod

from controller.MainControllerInterface import MainControllerInterface
from data.EventEntity import EventEntity
from view.ObjectDetailsObserverInterface import ObjectDetailsObserverInterface


class AbstractEventDetailsFrame(tk.Frame, ObjectDetailsObserverInterface, ABC):
    controller: MainControllerInterface

    def __init__(self, parent, controller: MainControllerInterface):

        self.controller = controller

        self.parent = parent
        tk.Frame.__init__(self, parent)

    def create_button(self):
        self.create_btn = tk.Button(self, text='Create', command=lambda: self.controller.create_event(self.get_event()))
        self.create_btn.pack()

    def update_button(self):
        self.update_btn = tk.Button(self, text='Update', command=lambda: self.controller.update_event(self.get_event()))
        self.update_btn.pack()

    def delete_button(self):
        self.delete_btn = tk.Button(self, text='Delete', command=lambda: self.controller.delete_event(self.get_event()))
        self.delete_btn.pack()

    @abstractmethod
    def get_event(self) -> EventEntity:
        pass
