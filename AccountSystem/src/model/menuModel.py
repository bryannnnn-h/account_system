from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel,QAbstractItemModel
from PyQt5.QtWidgets import QItemDelegate, QCheckBox
from model.CostumTableModel import basic_infoModel
import numpy as np
import pandas as pd
class menuRecordModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        if self._data[0, 0] != '':
            self._data = np.insert(self._data, 0, '選擇', axis=1)
        else:
            self._data = np.insert(self._data, 0, '', axis=1)
        self.title = ['','年','月','日','店名','設定為今日菜單','完成狀態']
    def setData(self, row, value):
        index = self.createIndex(row,5)
        self._data[row, 5] = value
        self.dataChanged.emit(index,index)
        return True
    def flags(self, index):
        if self.data(index, Qt.DisplayRole) == '':
            return Qt.NoItemFlags
        if index.column() == 0:
            return super().flags(index)
        else:
            return Qt.NoItemFlags
class menuDetailModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        self.title = ['品項','價格']
    def getRow(self, row):
        return self._data[row]

class menuRecordSelectDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkboxList = []
    def paint(self,painter, option, index):
        if not self.parent().indexWidget(index):
            if index.data(Qt.DisplayRole):
                values = int(index.data(Qt.DisplayRole))
                #if values == 1:
                #   self.parent().setCurrentIndex(index)
                menuSelect_checkbox = QCheckBox('設定',self.parent())
                menuSelect_checkbox.setChecked(values)
                self.checkboxList.append(menuSelect_checkbox)
                menuSelect_checkbox.stateChanged.connect(lambda: self.changeCheck(index))
                self.parent().setIndexWidget(index, menuSelect_checkbox)
    
    def changeCheck(self, index):
        if self.checkboxList[index.row()].checkState() == Qt.Checked:
            #self.parent().setCurrentIndex(index)
            for i, item in enumerate(self.checkboxList):
                if i != index.row():
                    item.setChecked(False)
            self.parent().model.setData(index.row(), '1')
        else:
            self.parent().model.setData(index.row(), '0')
        
        
        