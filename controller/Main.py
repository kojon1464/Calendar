from controller.MainController import MainController
from model.Model import Model
from view.MainView import MainView

if __name__ == '__main__':
    model = Model()


    controller = MainController()
    view = MainView(controller)
    model.subscribe(view)
    model.initialize()
    view.start()
