from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QHeaderView, QMessageBox
from ui_py.AccountPage import Ui_AccountPage
from model.CostumTableModel import SimpleTableModel
import pandas as pd
import numpy as np


class AccountPage_controller(QWidget, Ui_AccountPage):
    state = ['','Update','set']
    tableNameDict = {'基本資料':'basic_info'}
    def __init__(self, HomePageWidget, client):
        super(AccountPage_controller, self).__init__()
        self.setupUi(self)
        self.HomePage = HomePageWidget
        self.client = client
        self.model = SimpleTableModel()
        self.MainData = None
        self.stateList = None
        self.deleteId = None
        self.idList = None
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
        self.SaveTable_pushButton.clicked.connect(self.saveTable)
        self.read_radioButton.toggled.connect(self.changeMode)
        self.write_radioButton.toggled.connect(self.changeMode)

        self.insertRow_PushButton.setEnabled(False)
        self.deleteRow_PushButton.setEnabled(False)
        print('origin ', self.MainData)

    def refreshTable(self):
        TableName = self.selectTable_comboBox.currentText()
        self.MainData= self.client.getTableContent(self.tableNameDict[TableName])
        if 'ID' in self.MainData.columns:
            self.idList = list(self.MainData['ID'])
            self.MainData = self.MainData.drop(columns = ['ID'])

        self.deleteId = []
        if self.MainData.at[0, 'name'] == '':
            self.stateList = [2]
            self.idList = [0]
        else:
            self.stateList = [0]*len(self.MainData)
        self.model = SimpleTableModel(self.MainData)
        self.model.dataChanged.connect(self.rewriteData)
        self.showTable.setModel(self.model)
        self.changeMode()

    def setupComboBox(self):
        self.selectTable_comboBox.currentTextChanged.connect(self.changeTable)
    
    def changeTable(self):
        TableName = self.selectTable_comboBox.currentText()
        self.MainData= self.client.getTableContent(self.tableNameDict[TableName])
        if 'ID' in self.MainData.columns:
            self.idList = list(self.MainData['ID'])
            self.MainData = self.MainData.drop(columns = ['ID'])

        #self.deleteData = pd.DataFrame(columns = self.MainData.columns)
        self.deleteId = []
        if self.MainData.at[0, 'name'] == '':
            self.stateList = [2]
            self.idList = [0]
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
        newRow = pd.DataFrame([['']*len(self.MainData.columns)], columns = self.MainData.columns)
        if indexes:
            if indexes[-1].isValid():
                self.stateList.insert(indexes[-1] + 1, 2)
                self.idList.insert(indexes[-1] + 1, 0)
                dfs = np.split(self.MainData, [indexes[-1] + 1])
                self.MainData = pd.concat([dfs[0], newRow, dfs[1]], ignore_index=True)
                print(self.idList, '\n', self.stateList)
                self.showTable.model().insertRows(indexes[-1].row(), 1, QModelIndex())
        else:
            self.stateList.insert(len(self.stateList), 2)
            self.idList.insert(len(self.idList), 0)
            
            self.MainData = pd.concat([self.MainData, newRow], ignore_index=True)
            print(self.idList, '\n', self.stateList)
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
            popId = self.idList.pop(i)
            self.MainData = self.MainData.drop(i, axis = 0)
            self.MainData.reset_index(inplace=True, drop=True)
            print('pop ',self.idList)
            if popId != 0:
                self.deleteId.append(popId)
        self.showTable.model().removeRows(indexes[0].row(), indexList, rows, QModelIndex())

    def rewriteData(self, first_index, last_index):
        self.MainData = self.model.getAllDataByDf()
        if self.stateList[first_index.row()] == 0:
            self.stateList[first_index.row()] = 1
        print(self.MainData.iloc[first_index.row()])
        #1. deleteId
        #2. i at stateList==1 updata db 'id'==idList[id]
        #3. i at stateList==2

    def ModifyData(self):
        TableName = self.selectTable_comboBox.currentText()
        if len(self.deleteId) != 0:
            self.client.deleteTablebyId(self.tableNameDict[TableName], list(self.deleteId))
        
        insertDf = pd.DataFrame(columns = self.MainData.columns)
        for index, st in enumerate(self.stateList):
            if st == 0: continue
            elif st == 2:
                insertDf = pd.concat([insertDf, self.MainData.iloc[[index]]], ignore_index=True)
            else: 
                self.client.UpdateAccountTable(
                    self.tableNameDict[TableName], 
                    self.state[st], 
                    self.idList[index],
                    list(self.MainData.columns),
                    list(self.MainData.iloc[index]))
        if not insertDf.empty:
            self.client.InsertAccountTable(self.tableNameDict[TableName], insertDf)

    def saveTable(self):
        col = list(self.MainData.columns)
        col.remove('備註')
        checkSpace = self.MainData[col]
        
        if checkSpace.isnull().any().any() or checkSpace.apply(lambda x:x=='').any().any():
            QMessageBox.warning(None, '錯誤', '基本資料不可有空白欄位。')
            return
        self.ModifyData()
        self.refreshTable()
        
    
        




        

        

    

 

      