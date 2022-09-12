from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QHeaderView, QMessageBox
from ui_py.AccountPage import Ui_AccountPage
from model.CostumTableModel import SimpleTableModel
import pandas as pd
import numpy as np


class AccountPage_controller(QWidget, Ui_AccountPage):
    state = [0,1,2]
    tableNameDict = {'基本資料':'basic_info'}
    def __init__(self, HomePageWidget, client):
        super(AccountPage_controller, self).__init__()
        self.setupUi(self)
        self.HomePage = HomePageWidget
        self.client = client
        self.model = SimpleTableModel()
        self.MainData = None
        self.stateList = None
        self.deleteData = None
        self.Insertable = False
        
        self.initUI()    
    
    def initUI(self):
        self.setupComboBox()
        self.changeTable()
        
        self.showTable.resizeColumnsToContents()
        self.showTable.resizeRowsToContents()
        self.showTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.showTable.horizontalHeader().setStretchLastSection(True)

        self.deleteRow_PushButton.clicked.connect(self.deleteRow)
        self.insertRow_PushButton.clicked.connect(self.insertRow)
        self.read_radioButton.toggled.connect(self.changeMode)
        self.write_radioButton.toggled.connect(self.changeMode)

        self.insertRow_PushButton.setEnabled(False)
        self.deleteRow_PushButton.setEnabled(False)
        print('origin ', self.MainData)


    def setupComboBox(self):
        self.selectTable_comboBox.currentTextChanged.connect(self.changeTable)
    
    def changeTable(self):
        TableName = self.selectTable_comboBox.currentText()
        self.MainData= self.client.getTableContent(self.tableNameDict[TableName])
        self.deleteData = pd.DataFrame(columns = self.MainData.columns)
        if self.MainData.at[0, 'name'] == '':
            self.stateList = [2]
        else:
            self.stateList = [0]*len(self.MainData)
        self.model = SimpleTableModel(self.MainData)
        self.model.dataChanged.connect(self.rewriteData)
        self.showTable.setModel(self.model)
        
        if not self.read_radioButton.isChecked():
            self.read_radioButton.toggle()
            self.write_radioButton.toggle()
        if self.tableNameDict[TableName] == 'basic_info':
            self.Insertable = True

    def changeMode(self):
        self.insertRow_PushButton.setEnabled(False)
        self.deleteRow_PushButton.setEnabled(False)

        if self.read_radioButton.isChecked():
            self.model.changeMode('r')  
            
        elif self.write_radioButton.isChecked():
            self.model.changeMode('w')
            if self.Insertable:
                self.insertRow_PushButton.setEnabled(True)
                self.deleteRow_PushButton.setEnabled(True)
            
            

    def insertRow(self):
        if not self.sender():
            return
        indexes=self.showTable.selectionModel().selectedIndexes().sort()
        if indexes:
            if indexes[-1].isValid():
                self.stateList.insert(indexes[-1] + 1, 2)
                print(self.stateList)
                self.showTable.model().insertRows(indexes[-1].row(), 1, QModelIndex())
        else:
            self.stateList.insert(len(self.stateList), 2)
            print(self.stateList)
            self.showTable.model().insertRows(self.showTable.model().rowCount()-1, 1, QModelIndex())
        

    def deleteRow(self):
        if not self.sender():
            return
        indexes=self.showTable.selectionModel().selectedIndexes()
        if len(indexes) == 0: 
            QMessageBox.warning(None, '錯誤', '沒有選擇要刪除的欄位。')
            return
        rows = indexes[-1].row() - indexes[0].row() + 1
        indexList = []
        for index in indexes:
            if not index.isValid(): 
                continue
            indexList.append(index.row())
        indexList = sorted(indexList, reverse=True)
        for i in indexList:
            self.stateList.pop(i)
            self.deleteData = pd.concat([self.deleteData, self.MainData.iloc[[i]]], axis=0)
        self.showTable.model().removeRows(indexes[0].row(), indexList, rows, QModelIndex())

    def rewriteData(self):
        self.MainData = self.model.getAllDataByDf()
        print('this is ')
        print(self.MainData)
        print('')
        print('del \n',self.deleteData)

        

        

    

 

      