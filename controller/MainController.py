from tkinter.messagebox import askquestion, showerror

from controller.MainControllerInterface import MainControllerInterface
from data.EventEntity import EventEntity
from model.Model import Model
from view.AbstractEventDetailsFrame import AbstractEventDetailsFrame
from view.EventDetailsFrame import EventDetailsFrame
from view.ExportFileChooserFrame import ExportFileChooserFrame
from view.ImportFileChooserFrame import ImportFileChooserFrame
from view.MainViewInterface import MainViewInterface
from plyer.utils import platform
from plyer import notification


class MainController(MainControllerInterface):

    def __init__(self, model: Model):
        self.model = model

    def set_view(self, view: MainViewInterface):
        self.view = view

    def start(self):
        self.model.initialize()
        self.view.start()

    def previous_week_clicked(self):
        self.model.change_to_previous_week()

    def next_week_clicked(self):
        self.model.change_to_next_week()

    def create_event_clicked(self):
        self.top_view = self.view.get_top_level("Create Event")
        frame: AbstractEventDetailsFrame = EventDetailsFrame(self.top_view, self)
        frame.create_button()
        frame.pack()

    def update_event_clicked(self, event_id):
        self.top_view = self.view.get_top_level("Create Event")

        frame: AbstractEventDetailsFrame = EventDetailsFrame(self.top_view, self)
        frame.update_button()
        frame.delete_button()
        frame.pack()

        self.top_view.bind('<Destroy>', self.on_details_subscriber_close(frame))
        self.model.subscribe_details(frame)
        self.model.send_event_details(event_id)

    def on_details_subscriber_close(self, frame):
        def destroy(event):
            if not event.widget is event.widget.winfo_toplevel():
                return  # not actually the window
            self.model.unsubscribe_details(frame)
        return destroy

    def create_event(self, event: EventEntity):
        self.model.add_event(event)
        self.top_view.destroy()

    def update_event(self, event: EventEntity):
        self.model.update_event(event)
        self.top_view.destroy()

    def delete_event(self, event):
        self.model.delete_event(event)
        self.top_view.destroy()

    def check_notification(self):
        events = self.model.get_events_to_notify()
        for event in events:
            notification.notify(
                title='Event starts soon',
                message=event.name + " starts at " + event.date_start.time().strftime('%H:%M'),
                app_name='Calendar',
                # app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
            )

    def import_clicked(self):
        self.top_view = self.view.get_top_level("Import Calendar")
        frame = ImportFileChooserFrame(self.top_view, self)
        frame.pack()

    def export_clicked(self):
        self.top_view = self.view.get_top_level("Export Calendar")
        frame = ExportFileChooserFrame(self.top_view, self)
        frame.pack()

    def export_calendar(self, path):
        self.model.export_calendar(path)
        self.top_view.destroy()

    def import_calendar(self, path):
        self.model.import_calendar(path)
        self.top_view.destroy()
