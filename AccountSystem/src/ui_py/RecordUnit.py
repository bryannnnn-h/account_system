# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/RecordUnit.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RecordUnit(object):
    def setupUi(self, RecordUnit):
        RecordUnit.setObjectName("RecordUnit")
        RecordUnit.resize(489, 60)
        RecordUnit.setMinimumSize(QtCore.QSize(489, 60))
        RecordUnit.setMaximumSize(QtCore.QSize(489, 60))
        self.horizontalLayout = QtWidgets.QHBoxLayout(RecordUnit)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.item_label = QtWidgets.QLabel(RecordUnit)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.item_label.setFont(font)
        self.item_label.setAlignment(QtCore.Qt.AlignCenter)
        self.item_label.setObjectName("item_label")
        self.horizontalLayout.addWidget(self.item_label)
        self.price_label = QtWidgets.QLabel(RecordUnit)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.price_label.setFont(font)
        self.price_label.setAlignment(QtCore.Qt.AlignCenter)
        self.price_label.setObjectName("price_label")
        self.horizontalLayout.addWidget(self.price_label)
        self.amount_label = QtWidgets.QLabel(RecordUnit)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.amount_label.setFont(font)
        self.amount_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amount_label.setObjectName("amount_label")
        self.horizontalLayout.addWidget(self.amount_label)
        self.total_label = QtWidgets.QLabel(RecordUnit)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.total_label.setFont(font)
        self.total_label.setAlignment(QtCore.Qt.AlignCenter)
        self.total_label.setObjectName("total_label")
        self.horizontalLayout.addWidget(self.total_label)
        self.horizontalLayout.setStretch(0, 12)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 3)

        self.retranslateUi(RecordUnit)
        QtCore.QMetaObject.connectSlotsByName(RecordUnit)

    def retranslateUi(self, RecordUnit):
        _translate = QtCore.QCoreApplication.translate
        RecordUnit.setWindowTitle(_translate("RecordUnit", "Form"))
        self.item_label.setText(_translate("RecordUnit", "品項"))
        self.price_label.setText(_translate("RecordUnit", "1000"))
        self.amount_label.setText(_translate("RecordUnit", "15"))
        self.total_label.setText(_translate("RecordUnit", "15000"))
