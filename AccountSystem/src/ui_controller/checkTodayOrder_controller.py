from PyQt5 import QtCore, QtGui, QtWidgets
from ui_py.checkTodayOrder import Ui_TodayRecord
from ui_controller.RecordUnit_controller import RecordUnit_controller
import pandas as pd

class checkTodayOrder_controller(QtWidgets.QWidget, Ui_TodayRecord):
    def __init__(self, HomePageWidget, client):
        super(checkTodayOrder_controller, self).__init__()
        self.setupUi(self)
        self.HomePage = HomePageWidget
        self.client = client
        self.TodayStore, self.todayRecord = self.client.getTodayRecord()
        self.RecordList = []
        self.initUI()

    def initUI(self):
        if not self.todayRecord.empty:
            self.todayRecord[['price','amount','TotalPrice']] = self.todayRecord[['price','amount','TotalPrice']].apply(pd.to_numeric)
            itemGroup = self.todayRecord.groupby('ItemName').agg({'price':'min', 'amount':'sum', 'TotalPrice':'sum'})
            itemGroup.reset_index(inplace = True)
            itemGroup = itemGroup.rename(columns = {'index':'ItemName'})
            for index, item in itemGroup.iterrows():
                self.addRecord(index, item['ItemName'], item['price'], item['amount'], item['TotalPrice'])
        self.storeName_label.setText(self.TodayStore)
        self.Confirm_pushButton.clicked.connect(self.returnHomePage)
        self.Confirm_pushButton.clicked.connect(self.orderComplete)
        self.totalPrice_label.setText('總計：' + str(self.sumOfTotalPrice()))


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
        pass