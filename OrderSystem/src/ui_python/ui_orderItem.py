# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/orderItem.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_orderItem(object):
    def setupUi(self, orderItem):
        orderItem.setObjectName("orderItem")
        orderItem.resize(400, 41)
        self.horizontalLayout = QtWidgets.QHBoxLayout(orderItem)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.itemName_label = QtWidgets.QLabel(orderItem)
        self.itemName_label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(18)
        self.itemName_label.setFont(font)
        self.itemName_label.setStyleSheet("border: 1px solid black;")
        self.itemName_label.setAlignment(QtCore.Qt.AlignCenter)
        self.itemName_label.setObjectName("itemName_label")
        self.horizontalLayout.addWidget(self.itemName_label)
        self.price_label = QtWidgets.QLabel(orderItem)
        self.price_label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.price_label.setFont(font)
        self.price_label.setStyleSheet("border: 1px solid black;")
        self.price_label.setAlignment(QtCore.Qt.AlignCenter)
        self.price_label.setObjectName("price_label")
        self.horizontalLayout.addWidget(self.price_label)
        self.amount_spinBox = QtWidgets.QSpinBox(orderItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount_spinBox.sizePolicy().hasHeightForWidth())
        self.amount_spinBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.amount_spinBox.setFont(font)
        self.amount_spinBox.setAutoFillBackground(False)
        self.amount_spinBox.setObjectName("amount_spinBox")
        self.horizontalLayout.addWidget(self.amount_spinBox)
        self.horizontalLayout.setStretch(0, 7)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(orderItem)
        QtCore.QMetaObject.connectSlotsByName(orderItem)

    def retranslateUi(self, orderItem):
        _translate = QtCore.QCoreApplication.translate
        self.itemName_label.setText(_translate("orderItem", "品項"))
        self.price_label.setText(_translate("orderItem", "價格"))
