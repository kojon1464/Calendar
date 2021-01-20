import re
from tkinter.filedialog import askopenfilename

from controller.MainControllerInterface import MainControllerInterface
from view.fileChooser.AbstractFileChooserFrame import AbstractFileChooserFrame

FRAME_SIZE = '500x200'
INFO_TEXT = 'Choose a file that contains calendar data. IMPORTANT: Note that this application does not take all' \
            'iCalendar attributes into consideration but also defines own tags.'

class ImportFileChooserFrame(AbstractFileChooserFrame):

    def __init__(self, parent, controller: MainControllerInterface):
        super().__init__(parent, controller)

        self.parent.geometry(FRAME_SIZE)
        self.info_label.configure(text=INFO_TEXT)

    def call_proceed_callback(self):
        self.controller.import_calendar(self.path.get())

    def validate_path(self):
        if re.search(r'.*\.ics', self.path.get()) is None:
            return 'Did not chose correct file'
        return None

    def get_path(self):

        file_types = [
            ('iCalendar files', '*.ics')
        ]
        return askopenfilename(filetypes=file_types)
