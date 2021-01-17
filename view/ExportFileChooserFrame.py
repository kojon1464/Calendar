import re
import tkinter as tk
from tkinter.filedialog import asksaveasfilename

from controller.MainControllerInterface import MainControllerInterface
from view.AbstractFileChooserFrame import AbstractFileChooserFrame

FRAME_SIZE = '500x200'
INFO_TEXT = 'Choose a file that calendar will be exported into. IMPORTANT: Loose events (events without specified time)' \
            ' will be exported with date set as creation date or date, which was set before event was changed to loose state.'

class ExportFileChooserFrame(AbstractFileChooserFrame):

    def __init__(self, parent, controller: MainControllerInterface):
        super().__init__(parent, controller)

        self.parent.geometry(FRAME_SIZE)
        self.info_label.configure(text=INFO_TEXT)

    def call_proceed_callback(self):
        self.controller.export_calendar(self.path.get())

    def validate_path(self):
        if re.search(r'.*\.ics', self.path.get()) is None:
            return 'Did not chose correct file'
        return None

    def get_path(self):
        file_types = [
            ('iCalendar files', '*.ics')
        ]
        return asksaveasfilename(filetypes=file_types)

