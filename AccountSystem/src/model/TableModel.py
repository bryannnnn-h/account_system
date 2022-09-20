from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel,QAbstractItemModel
from PyQt5.QtWidgets import QItemDelegate, QCheckBox
from model.CostumTableModel import basic_infoModel
import numpy as np
import pandas as pd
class AccountTableModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        self.mode = 'r'
        self.title = ['年份', '月份', '姓名', '年級', '方案月費', '伙食費', '教材費', '總額', '繳費紀錄', '備註']
    def setData(self, row, value):
        index = self.createIndex(row,8)
        self._data[row, 8] = value
        self.dataChanged.emit(index,index)
        return True
class FoodExpenseDetailModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        self.mode = 'r'
        self.title = ['年份', '月份', '日', '姓名', '年級', '金額', '出帳紀錄', '備註']
    def setData(self, row, value):
        index = self.createIndex(row,7)
        self._data[row, 7] = value
        self.dataChanged.emit(index,index)
        return True
class BookExpenseDetailModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        self.mode = 'r'
        self.title = ['年份', '月份', '姓名', '年級', '金額', '出帳紀錄', '備註']
    def setData(self, row, value):
        index = self.createIndex(row,6)
        self._data[row, 6] = value
        self.dataChanged.emit(index,index)
        return True
'''
class menuRecordSelectDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkboxList = []
    def paint(self,painter, option, index):
        if not self.parent().indexWidget(index):
            values = int(index.data(Qt.DisplayRole))
            menuSelect_checkbox = QCheckBox('選擇',self.parent())
            menuSelect_checkbox.setChecked(values)
            self.checkboxList.append(menuSelect_checkbox)
            menuSelect_checkbox.stateChanged.connect(lambda: self.changeCheck(index))
            self.parent().setIndexWidget(index, menuSelect_checkbox)
    
    def changeCheck(self, index):
        if self.checkboxList[index.row()].checkState() == Qt.Checked:
            for i, item in enumerate(self.checkboxList):
                if i != index.row():
                    item.setChecked(False)
                    self.parent().model.setData(i, '0')
            self.parent().model.setData(index.row(), '1')
        else:
            self.parent().model.setData(index.row(), '0')
 '''