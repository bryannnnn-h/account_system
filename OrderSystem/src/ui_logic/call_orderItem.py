import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget
from ui_python.ui_orderItem import Ui_orderItem

class OrderItem(QWidget, Ui_orderItem):
    def __init__(self, itemName="", price=0):
        super(OrderItem,self).__init__()
        self.setupUi(self)
        self.itemName = itemName
        self.price = price
        self.initUI()
    
    def initUI(self):
        self.itemName_label.setText(self.itemName)
        self.price_label.setText(str(self.price))
        self.amount_spinBox.valueChanged.connect(self.change_price)
    
    def change_price(self):
        self.price_label.setText(str(self.price*max(1,self.amount_spinBox.value())))