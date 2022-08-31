from PyQt5 import QtCore, QtGui, QtWidgets
from ui_py.RecordUnit import Ui_RecordUnit

class RecordUnit_controller(QtWidgets.QWidget, Ui_RecordUnit):
    def __init__(self, itemName, price, amount, Total):
        super(RecordUnit_controller, self).__init__()
        self.setupUi(self)
        self.amount_label.setText(str(amount))
        self.item_label.setText(itemName)
        self.price_label.setText(str(price))
        self.total_label.setText(str(Total))

        