from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel,QAbstractItemModel, QSortFilterProxyModel
from PyQt5.QtWidgets import QItemDelegate, QCompleter, QComboBox, QLabel
from PyQt5.QtGui import QFont
from model.CostumTableModel import basic_infoModel
import numpy as np
import pandas as pd
class AccountTableModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        self.mode = 'r'
        self.title = ['年份', '月份', '姓名', '年級', '方案月費', '伙食費', '教材費', '總額', '繳費紀錄', '備註']
        print('this is AccountTableModel')
    # def setData(self, row, value):
    #     index = self.createIndex(row,8)
    #     self._data[row, 8] = value
    #     self.dataChanged.emit(index,index)
    #     return True
    def flags(self, index):
        if index.column() == 9:            
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return super().flags(index)
class FoodExpenseDetailModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        self.mode = 'r'
        self.title = ['年份', '月份', '日', '姓名', '年級', '金額', '出帳紀錄', '備註']
        print('this is FoodExpenseDetailModel')
    # def setData(self, row, value):
    #     index = self.createIndex(row,7)
    #     self._data[row, 7] = value
    #     self.dataChanged.emit(index,index)
    #     return True
    def flags(self, index):
        if index.column() == 7:            
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return super().flags(index)
class BookExpenseDetailModel(basic_infoModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super().__init__(data, parent)
        self.mode = 'r'
        self.title = ['年份', '月份', '姓名', '年級', '金額', '出帳紀錄', '備註']
        print('this is BookExpenseDetailModel')
        
    def flags(self, index):
        if self.mode =='w':
            if index.column() in (0,1,4,6):            
                return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
            elif index.column() == 2:
                if self.data(index, Qt.DisplayRole) == '':
                    return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                else:
                    return Qt.ItemIsSelectable | Qt.ItemIsEnabled
            else:
                return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return super().flags(index)


class nameEnterDelegate(QItemDelegate):
    def __init__(self, nameList ,parent=None):
        super().__init__(parent)
        self.nameList = nameList
        
    def createEditor(self, parent, option, index):
        enterWiget = MyComboBox(parent)
        enterWiget.addItems(list(self.nameList['name']))
        return enterWiget

    
    def setModelData(self, editor, model, index):
        student_index = editor.currentIndex()
        grade = self.nameList.at[student_index, 'grade']
        gradeTableIndex = model.createIndex(index.row(), 3)
        isRecordTableIndex = model.createIndex(index.row(), 5)
        model.setData(index, editor.currentText(), Qt.EditRole)
        model.setData(gradeTableIndex, grade, Qt.EditRole)
        model.setData(isRecordTableIndex, False, Qt.EditRole)


class isRecordDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            if index.data(Qt.DisplayRole) != '':
                values = int(index.data(Qt.DisplayRole))
                print(values)
                if values == 0:
                    label = QLabel('尚未出帳', self.parent())
                else:
                    label = QLabel('已出帳', self.parent())
                label.setFont(QFont('微軟正黑體', 20))

                self.parent().setIndexWidget(index, label)
 

class MyComboBox(QComboBox):
    def __init__(self, parent=None):
        super(MyComboBox, self).__init__(parent)
      
        font = QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.setFont(font)
        self.setEditable(True)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setDuplicatesEnabled(True)
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