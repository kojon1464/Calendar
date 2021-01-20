import tkinter as tk
from typing import List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

from controller.MainControllerInterface import MainControllerInterface
from data.Statistics import Statistics
from view.statistic.StatisticsViewInterface import StatisticsViewInterface

FRAME_SIZE = '400x500'

NUMBER_OF_COLUMNS = 2


class StatisticsViewFrame(tk.Frame, StatisticsViewInterface):

    def __init__(self, parent, controller: MainControllerInterface):

        self.controller = controller
        self.parent = parent

        tk.Frame.__init__(self, parent)

    def create_bar_plot(self, data_frame: DataFrame, title: str):
        figure = plt.Figure(figsize=(4, 4), dpi=100, tight_layout='tight')
        ax = figure.add_subplot(111)
        bar = FigureCanvasTkAgg(figure, self)
        data_frame.plot(kind='bar', legend=True, ax=ax)
        ax.set_title(title)

        return bar.get_tk_widget()

    def set_statistics(self, statistics: List[Statistics]):
        counter = 0
        for stat in statistics:
            widget = self.create_bar_plot(stat.data_frame, stat.title)
            widget.configure(borderwidth=2, relief="groove")
            widget.grid(column=counter//NUMBER_OF_COLUMNS, row=counter % NUMBER_OF_COLUMNS, pady=1, padx=1)
            counter = counter + 1
