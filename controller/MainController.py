from controller.MainControllerInterface import MainControllerInterface
from data.CalendarEntity import CalendarEntity
from data.EventEntity import EventEntity
from model.Model import Model
from view.AbstractEventDetailsFrame import AbstractEventDetailsFrame
from view.EventDetailsFrame import EventDetailsFrame
from view.MainViewInterface import MainViewInterface


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

    def create_event(self, event: EventEntity):
        self.model.add_event(event)
        self.top_view.destroy()

    def update_event(self, event: EventEntity):
        pass
