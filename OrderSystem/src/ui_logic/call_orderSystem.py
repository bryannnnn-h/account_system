import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QMessageBox
from ui_python.ui_orderSystem import Ui_orderSystem
from call_orderItem import OrderItem

class OrderSystem(QWidget, Ui_orderSystem):
    def __init__(self, itemCount=1, storeName="無", itemNameList=["無"], priceList=[0], nameList=['']):
        super(OrderSystem, self).__init__()
        self.setupUi(self)
        self.itemCount = itemCount
        self.storeName = storeName
        self.itemNameList = itemNameList
        self.priceList = priceList
        self.OrderItemList = []
        self.nameList = nameList
        self.initUI()
    
    def initUI(self):
        self.orderSystem_stackedWidget.setCurrentWidget(self.nameInput_page)
        self.nameInput_lineEdit.clear()
        self.studentName_label.clear() 
        self.storeName_label.setText(self.storeName)
        for i in range(self.itemCount):
            self.add_OrderItem(self.itemNameList[i], self.priceList[i])
        self.nameInputConfirm_pushButton.clicked.connect(self.nameInputConfirm)        
        self.orderConfirm_pushButton.clicked.connect(self.orderConfirm)
    
    def add_OrderItem(self, itemName="", price=0):
        new_OrderItem = OrderItem(itemName, price)
        self.OrderItemList.append(new_OrderItem)
        self.items_verticalLayout.insertWidget(0,new_OrderItem)
    
    def nameInputConfirm(self):
        student_name = self.nameInput_lineEdit.text()
        if student_name in self.nameList:
            self.orderSystem_stackedWidget.setCurrentWidget(self.order_page)
            self.studentName_label.setText(self.nameInput_lineEdit.text())
        else:
            QMessageBox.warning(None, '警告', f'找不到"{student_name}"，請確認姓名是否輸入正確')


    def orderConfirm(self):
        self.orderSystem_stackedWidget.setCurrentWidget(self.nameInput_page)
        self.nameInput_lineEdit.clear()
        self.studentName_label.clear()
        for item in self.OrderItemList:
            item.amount_spinBox.setValue(0)
        