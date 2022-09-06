from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget 
from ui_py.AccountPage import Ui_AccountPage
from model.CostumTableModel import SimpleTableModel
import pandas as pd
import numpy as np


class AccountPage_controller(QWidget, Ui_AccountPage):
    def __init__(self, HomePageWidget, client):
        super(AccountPage_controller, self).__init__()
        self.setupUi(self)
        self.HomePage = HomePageWidget
        self.client = client

        data = client.getFavMenuContent('丹丹1')

        self.model = SimpleTableModel(data)
        self.showTable.setModel(self.model)

        self.deleteRow_PushButton.clicked.connect(self.deleteRow)
        self.insertRow_PushButton.clicked.connect(self.insertRow)

    def insertRow(self):
        if not self.sender():
            return
        indexes=self.showTable.selectionModel().selectedIndexes()
        if indexes:
            if indexes[-1].isValid():
                self.showTable.model().insertRows(indexes[-1].row(), len(indexes), QModelIndex())
        else:
            self.showTable.model().insertRows(self.showTable.model().rowCount()-1, 1, QModelIndex())
        

    def deleteRow(self):
        if not self.sender():
            return
        indexes=self.showTable.selectionModel().selectedIndexes()
        rows = indexes[-1].row() - indexes[0].row() + 1
        indexList = []
        for index in indexes:
            if not index.isValid(): continue
            indexList.append(index.row())
        indexList = sorted(indexList, reverse=True)
        self.showTable.model().removeRows(indexes[0].row(), indexList, rows, QModelIndex())

    def del_row(self):
        del_row = self.showTable.currentIndex().row()
        self.model.removeRow(del_row)
        

        

    

 

      