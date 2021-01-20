import tkinter as tk
from abc import ABC, abstractmethod
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from controller.MainControllerInterface import MainControllerInterface

PAD_Y = 15

class AbstractFileChooserFrame(tk.Frame, ABC):
    controller: MainControllerInterface

    def __init__(self, parent, controller: MainControllerInterface):

        self.controller = controller

        self.parent = parent
        tk.Frame.__init__(self, parent)

        self.info_label = tk.Label(self, wraplength=400)
        self.info_label.grid(row=0, column=0, columnspan=4, pady=PAD_Y)

        self.path = tk.StringVar()
        self.path.set('...')
        self.path_label = tk.Label(self, textvariable=self.path, width=40, anchor=tk.E)
        self.path_label.grid(row=1, column=0, pady=PAD_Y)

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.winfo_toplevel().destroy())
        self.cancel_btn.grid(row=3, column=2, pady=PAD_Y)

        self.choose_btn = tk.Button(self, text='Choose file', command=lambda: self.choose_file())
        self.choose_btn.grid(row=1, column=1, pady=PAD_Y)

        self.proceed_btn = tk.Button(self, text='Proceed', command=self.validate_before_call)
        self.proceed_btn.grid(row=3, column=3, pady=PAD_Y)

    def validate_before_call(self):
        error = self.validate_path()
        if error is None:
            self.call_proceed_callback()
        else:
            showerror(title='Validation Error', message=error)

    def choose_file(self):
        path = self.get_path()
        if not path == ' ':
            self.path.set(path)

    @abstractmethod
    def call_proceed_callback(self):
        pass

    @abstractmethod
    def validate_path(self):
        pass

    @abstractmethod
    def get_path(self):
        pass