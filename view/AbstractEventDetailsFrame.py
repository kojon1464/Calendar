import tkinter as tk
from abc import ABC, abstractmethod
from tkinter.messagebox import showerror

from controller.MainControllerInterface import MainControllerInterface
from data.EventEntity import EventEntity
from view.ObjectDetailsObserverInterface import ObjectDetailsObserverInterface


class AbstractEventDetailsFrame(tk.Frame, ObjectDetailsObserverInterface, ABC):
    controller: MainControllerInterface

    def __init__(self, parent, controller: MainControllerInterface):

        self.controller = controller

        self.parent = parent
        tk.Frame.__init__(self, parent)

        self.button_frame = tk.Frame(self)

    def create_button(self):
        self.create_btn = tk.Button(self.button_frame, text='Create', command=lambda: self.validate_before_call(self.controller.create_event))
        self.create_btn.pack(side=tk.LEFT, padx=5)

    def update_button(self):
        self.update_btn = tk.Button(self.button_frame, text='Update', command=lambda: self.validate_before_call(self.controller.update_event))
        self.update_btn.pack(side=tk.LEFT, padx=5)

    def delete_button(self):
        self.delete_btn = tk.Button(self.button_frame, text='Delete', command=lambda: self.controller.delete_event(self.get_event()))
        self.delete_btn.pack(side=tk.LEFT, padx=5)

    def validate_before_call(self, callback):
        event = self.get_event()
        error = event.validate()
        if error is None:
            callback(event)
        else:
            showerror(title='Validation Error', message=error)

    @abstractmethod
    def get_event(self) -> EventEntity:
        pass
