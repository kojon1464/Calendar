import tkinter as tk

from data.EventEntity import EventEntity


class EventView(tk.Frame):

    def __init__(self, parent, event: EventEntity, color: str):
        self.parent = parent

        tk.Frame.__init__(self, parent, bg=color, highlightbackground="black", highlightcolor="black", highlightthickness=1,)

        self.name = tk.Label(self, text=event.name, bg=color)
        self.name.grid(row=0, column=0, sticky='w')

        self.time = tk.Label(self, text=event.get_time_label(), bg=color)
        self.time.grid(row=1, column=0,  sticky='w')
