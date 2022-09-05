from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox,QComboBox,QCompleter
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from ui_python.ui_orderSystem import Ui_orderSystem
from call_orderItem import OrderItem
import pandas as pd
class MyComboBox(QComboBox):
    def __init__(self, parent=None):
        super(MyComboBox, self).__init__(parent)
      
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.setFont(font)
        self.setEditable(True)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setDuplicatesEnabled(True)
        self.setObjectName("nameInput_comboBox")
        self.addItem("")
        self.setItemText(0, "")

        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        self.completer = QCompleter(self.pFilterModel, self)
        self.completer.popup().setFont(font)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))
    def setModel(self, model):
        super(MyComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(MyComboBox, self).setModelColumn(column)

class OrderSystem(QWidget, Ui_orderSystem):
    def __init__(self, client):
        super(OrderSystem, self).__init__()
        self.setupUi(self)
        self.nameInput_comboBox = MyComboBox(self.nameInput_widget)
        self.client = client
        self.OrderItemList = []
        self.menuDate = self.client.getMenuDate()
        self.storeName, self.todayMenu = self.client.getTodayMenu(self.menuDate)
        self.nameList = self.client.getNameList()
        self.orderRecord = pd.DataFrame()
        self.initUI()
    
    def initUI(self):
        self.orderSystem_stackedWidget.setCurrentWidget(self.nameInput_page)
        
        self.nameInput_comboBox.setGeometry(QtCore.QRect(100, 0, 300, 50))
        self.nameInput_comboBox.addItems(self.nameList)

        self.studentName_label.clear() 
        self.storeName_label.setText(self.storeName)
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
        student_name = self.nameInput_comboBox.currentText()
        if student_name in self.nameList:
            self.orderSystem_stackedWidget.setCurrentWidget(self.order_page)
            self.studentName_label.setText(student_name)
            self.orderRecord = self.client.getTodayOrderRecordbyName(student_name)
            if not self.orderRecord.empty:
                for item in self.OrderItemList:
                    if item.itemName in self.orderRecord.index:
                        item.amount_spinBox.setValue(int(self.orderRecord.at[item.itemName,'amount']))
            if self.todayMenu.empty:
                QMessageBox.warning(None, '警告', f'尚未設定今日菜單，請前往設定，若已設定請重新開啟程式')
                    
        else:
            QMessageBox.warning(None, '警告', f'找不到"{student_name}"，請確認姓名是否輸入正確')


    def orderConfirm(self):
        order = pd.DataFrame(columns=["Year","Month","Day","StoreName", "StudentName", "ItemName", "price", "amount", "TotalPrice"])
        y,m,d = self.menuDate.split('-')
        self.nameInput_comboBox.setCurrentIndex(0)
        StudentName = self.studentName_label.text()
        self.studentName_label.clear()
        for item in self.OrderItemList:
            if item.amount_spinBox.value() > 0:
                order = pd.concat([order, pd.DataFrame({"Year":[y],"Month":[m],"Day":[d],"StoreName":[self.storeName], "StudentName":[StudentName], "ItemName":[item.itemName], "price":[item.price], "amount":[item.amount_spinBox.value()], "TotalPrice":[item.price_label.text()]})], ignore_index=True)
                item.amount_spinBox.setValue(0)
        if not self.orderRecord.empty:
            self.client.deleteTodayRecord(StudentName)
        if not order.empty:
            self.client.setTodayRecord(order)
        self.orderSystem_stackedWidget.setCurrentWidget(self.nameInput_page)
    
    

        
        