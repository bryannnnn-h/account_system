from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QMessageBox
from ui_python.ui_orderSystem import Ui_orderSystem
from call_orderItem import OrderItem
import pandas as pd

class OrderSystem(QWidget, Ui_orderSystem):
    def __init__(self, client):
        super(OrderSystem, self).__init__()
        self.setupUi(self)
        self.client = client
        self.OrderItemList = []
        self.storeName, self.todayMenu = self.client.getTodayMenu()
        self.nameList = self.client.getNameList()
        self.orderRecord = pd.DataFrame()
        self.initUI()
    
    def initUI(self):
        self.orderSystem_stackedWidget.setCurrentWidget(self.nameInput_page)
        self.nameInput_lineEdit.clear()
        self.studentName_label.clear() 
        self.storeName_label.setText(self.storeName)
        '''
        for i in range(self.itemCount):
            self.add_OrderItem(self.todayMenu.at[i, 'ItemName'], int(self.todayMenu.at[i, 'price']))
        '''
        if self.todayMenu.empty:
            QMessageBox.warning(None, '警告', f'尚未設定今日菜單，請前往設定')
        else:
            for index, item in self.todayMenu.iterrows():
                self.add_OrderItem(index, item['ItemName'], int(item['price']))
        self.nameInputConfirm_pushButton.clicked.connect(self.nameInputConfirm)        
        self.orderConfirm_pushButton.clicked.connect(self.orderConfirm)
    
    def add_OrderItem(self, index, itemName, price):
        new_OrderItem = OrderItem(itemName, price)
        self.OrderItemList.append(new_OrderItem)
        self.items_verticalLayout.insertWidget(index,new_OrderItem)
    
    def nameInputConfirm(self):
        student_name = self.nameInput_lineEdit.text()
        if student_name in self.nameList:
            self.orderSystem_stackedWidget.setCurrentWidget(self.order_page)
            self.studentName_label.setText(self.nameInput_lineEdit.text())
            self.orderRecord = self.client.getTodayOrderRecordbyName(student_name)
            if not self.orderRecord.empty:
                for item in self.OrderItemList:
                    if item.itemName in self.orderRecord.index:
                        item.amount_spinBox.setValue(int(self.orderRecord.at[item.itemName,'amount']))
            if self.todayMenu.empty:
                QMessageBox.warning(None, '警告', f'尚未設定今日菜單，請前往設定')
                    
        else:
            QMessageBox.warning(None, '警告', f'找不到"{student_name}"，請確認姓名是否輸入正確')


    def orderConfirm(self):
        order = pd.DataFrame(columns=["StoreName", "StudentName", "ItemName", "price", "amount", "TotalPrice"])
        self.nameInput_lineEdit.clear()
        StudentName = self.studentName_label.text()
        self.studentName_label.clear()
        for item in self.OrderItemList:
            if item.amount_spinBox.value() > 0:
                order = pd.concat([order, pd.DataFrame({"StoreName":[self.storeName], "StudentName":[StudentName], "ItemName":[item.itemName], "price":[item.price], "amount":[item.amount_spinBox.value()], "TotalPrice":[item.price_label.text()]})], ignore_index=True)
                item.amount_spinBox.setValue(0)
        if not self.orderRecord.empty:
            self.client.deleteTodayRecord(StudentName)
        if not order.empty:
            self.client.setTodayRecord(order)
        self.orderSystem_stackedWidget.setCurrentWidget(self.nameInput_page)
    
    

        
        