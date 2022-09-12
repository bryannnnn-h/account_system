from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui_py.checkTodayOrder import Ui_TodayRecord
from ui_controller.RecordUnit_controller import RecordUnit_controller
import pandas as pd

class checkTodayOrder_controller(QtWidgets.QWidget, Ui_TodayRecord):
    def __init__(self, HomePageWidget, client):
        super(checkTodayOrder_controller, self).__init__()
        self.setupUi(self)
        self.HomePage = HomePageWidget
        self.client = client
        self.menuID, self.menuDate, self.TodayStore = self.client.getSelectedMenuInfo()
        self.todayRecord = self.client.getTodayRecord()
        self.RecordList = []
        self.numOfPeople = 0
        self.initUI()

    def initUI(self):
        if not self.todayRecord.empty:
            self.todayRecord[['price','amount','TotalPrice']] = self.todayRecord[['price','amount','TotalPrice']].apply(pd.to_numeric)
            itemGroup = self.todayRecord.groupby('ItemName').agg({'price':'min', 'amount':'sum', 'TotalPrice':'sum'})
            self.numOfPeople = len(itemGroup)
            itemGroup.reset_index(inplace = True)
            itemGroup = itemGroup.rename(columns = {'index':'ItemName'})
            for index, item in itemGroup.iterrows():
                self.addRecord(index, item['ItemName'], item['price'], item['amount'], item['TotalPrice'])
            self.Confirm_pushButton.setEnabled(True)
            self.Cancel_pushButton.setEnabled(True)
        else:
            self.Confirm_pushButton.setEnabled(False)
            self.Cancel_pushButton.setEnabled(False)
        self.storeName_label.setText(self.TodayStore)
        self.menuDate_label.setText(self.menuDate)
        self.ReturnHomePage_pushButton.clicked.connect(self.returnHomePage)
        self.Confirm_pushButton.clicked.connect(self.orderComplete)
        self.Cancel_pushButton.clicked.connect(self.deleteOrder)
        self.Refresh_pushButton.clicked.connect(self.refreshPage)
        self.totalPrice_label.setText('總計：' + str(self.sumOfTotalPrice()))
        self.totalPeople_label.setText('人數：' + str(self.numOfPeople))

    def addRecord(self, index, itemName, price, amount, TotalPrice):
        new_Record = RecordUnit_controller(itemName, price, amount, TotalPrice)
        self.RecordList.append(new_Record)
        self.verticalLayout.insertWidget(index, new_Record)

    def sumOfTotalPrice(self):
        sumOfPrice = 0
        for row in self.RecordList:
            sumOfPrice += int(row.total_label.text())
        return sumOfPrice
    def returnHomePage(self):
        self.close()
        self.HomePage.show()
    
    def orderComplete(self):
        reply = QMessageBox.question(
            None, 
            '提示訊息', 
            f'本筆訂單將記錄至「歷史訂單」並且無法再次修改，請問是否繼續？',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)
         
        if reply == QMessageBox.No:
            return
        else:
            self.client.TodayCopy2History()
            self.client.updateMenuState(self.menuID,Complete = True)
            self.client.clearTable('TodayRecord')
            self.refreshPage()

    def deleteOrder(self):
        reply = QMessageBox.question(
            None, 
            '提示訊息', 
            f'本筆訂單將永久被刪除，請問是否繼續？',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)
         
        if reply == QMessageBox.No:
            return
        else:
            self.client.updateMenuState(self.menuID,Complete = False)
            self.client.clearTable('TodayRecord')
            self.refreshPage()

    def resetLayout(self):
        for i in reversed(range(self.verticalLayout.count())):
            widget = self.verticalLayout.itemAt(i).widget()
            if widget != None:
                widget.setParent(None)

    def refreshPage(self):
        self.resetLayout()
        self.menuID, self.menuDate, self.TodayStore = self.client.getSelectedMenuInfo()
        self.todayRecord = self.client.getTodayRecord()
        self.RecordList = []
        if not self.todayRecord.empty:
            self.todayRecord[['price','amount','TotalPrice']] = self.todayRecord[['price','amount','TotalPrice']].apply(pd.to_numeric)
            itemGroup = self.todayRecord.groupby('ItemName').agg({'price':'min', 'amount':'sum', 'TotalPrice':'sum'})
            self.numOfPeople = len(itemGroup)
            itemGroup.reset_index(inplace = True)
            itemGroup = itemGroup.rename(columns = {'index':'ItemName'})
            for index, item in itemGroup.iterrows():
                self.addRecord(index, item['ItemName'], item['price'], item['amount'], item['TotalPrice'])
            self.Confirm_pushButton.setEnabled(True)
            self.Cancel_pushButton.setEnabled(True)
        else:
            self.Confirm_pushButton.setEnabled(False)
            self.Cancel_pushButton.setEnabled(False)
        self.storeName_label.setText(self.TodayStore)
        self.menuDate_label.setText(self.menuDate)
        self.totalPrice_label.setText('總計：' + str(self.sumOfTotalPrice()))
        self.totalPeople_label.setText('人數：' + str(self.numOfPeople))
