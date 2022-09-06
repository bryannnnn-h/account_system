from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import QWidget 
import numpy as np
class SimpleTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = np.array(data)
        self.title = data.columns
        

    def data(self, index, role):
        if index.isValid():
            row = index.row()
            col = index.column()
            if role in {Qt.DisplayRole, Qt.EditRole}:
                return self._data[row, col]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self.rowCount() else 0

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        titles = self.title 
        if role == Qt.DisplayRole: # only change what DisplayRole returns
            if orientation == Qt.Horizontal:
                return titles[section]
            elif orientation == Qt.Vertical:
                return f'{section + 1}'
        return super().headerData(section, orientation, role) # must have this line

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row(), index.column()] = value
            return True
        return False
    
    def insertRows(self, positon, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), positon, positon + rows - 1)
        for i in range(rows):
            row = np.array([''] * self.columnCount())
            self._data = np.insert(self._data, positon + i + 1, [row], axis=0)
        self.endInsertRows()
        self.dirty = True
        return True
    
    def removeRows(self, positon, indexList, rows=1, index=QModelIndex()):
        self._data = np.delete(self._data,indexList,axis = 0)
        for i in indexList:
            self.beginRemoveRows(QModelIndex(), i, i)
            self.endRemoveRows()
        self.dirty = True
        return True
    