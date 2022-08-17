from PyQt5 import QtCore, QtGui, QtWidgets
from ui_py.adding_unit import Ui_option_unit
import sip

class adding_option_controller(QtWidgets.QWidget, Ui_option_unit):
    def __init__(self, Layout):
        super(adding_option_controller, self).__init__()
        self.setupUi(self)
        self.Layout = Layout
        self.add_Button.clicked.connect(self.add_option)
        self.del_Button.clicked.connect(lambda: self.del_option(self))
        self.stackedWidget.setCurrentWidget(self.page)
    
    def add_option(self):
        cur_option_name = self.option_lineEdit.text()
        cur_price = self.price_lineEdit.text()
        self.option_label.setText(cur_option_name)
        self.price_label.setText(cur_price)
        self.stackedWidget.removeWidget(self.page)
        newSpace = adding_option_controller(self.Layout)
        self.Layout.insertWidget(0, newSpace)

    def del_option(self, cur_option):
        self.Layout.removeWidget(cur_option)
        sip.delete(cur_option)
