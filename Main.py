from plyer import notification

from base import Base, engine
from controller.MainController import MainController
from data.EventEntity import EventEntity
from model.Model import Model
from view.MainView import MainView

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    model = Model()

    controller = MainController(model)
    view = MainView(controller)
    controller.set_view(view)

    model.subscribe_calendar(view)

    controller.start()
