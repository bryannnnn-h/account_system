from PyQt5 import QtCore, QtGui, QtWidgets
from ui_py.HomePage import Ui_HomePage
from ui_controller.setPage_controller import setPage_controller
from ui_controller.checkTodayOrder_controller import checkTodayOrder_controller
from ui_py.setPage import Ui_setPage


class HomePage_controller(QtWidgets.QWidget, Ui_HomePage):
    def __init__(self, client):
        super(HomePage_controller, self).__init__()
        self.setupUi(self)
        self.the_window=self
        self.TodayOrderButton.clicked.connect(self.jump_TodayRecord)
        self.SetMenuButton.clicked.connect(self.jump_setting_page)
        self.client = client
    def jump_setting_page(self):
        self.the_window=setPage_controller(self, self.client)
        self.hide()
        self.the_window.show()
    def jump_TodayRecord(self):
        self.the_window=checkTodayOrder_controller(self, self.client)
        self.hide()
        self.the_window.show()

    


        
        