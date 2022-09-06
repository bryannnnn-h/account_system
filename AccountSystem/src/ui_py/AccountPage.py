# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\AccountPage.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AccountPage(object):
    def setupUi(self, AccountPage):
        AccountPage.setObjectName("AccountPage")
        AccountPage.resize(1297, 763)
        self.verticalLayout = QtWidgets.QVBoxLayout(AccountPage)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AccountPage)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(AccountPage)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(AccountPage)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_3 = QtWidgets.QPushButton(AccountPage)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.horizontalLayout_2.setStretch(0, 8)
        self.horizontalLayout_2.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.showTable = QtWidgets.QTableView(AccountPage)
        self.showTable.setObjectName("showTable")
        self.verticalLayout.addWidget(self.showTable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.insertRow_PushButton = QtWidgets.QPushButton(AccountPage)
        self.insertRow_PushButton.setObjectName("insertRow_PushButton")
        self.horizontalLayout.addWidget(self.insertRow_PushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.deleteRow_PushButton = QtWidgets.QPushButton(AccountPage)
        self.deleteRow_PushButton.setObjectName("deleteRow_PushButton")
        self.horizontalLayout.addWidget(self.deleteRow_PushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AccountPage)
        QtCore.QMetaObject.connectSlotsByName(AccountPage)

    def retranslateUi(self, AccountPage):
        _translate = QtCore.QCoreApplication.translate
        AccountPage.setWindowTitle(_translate("AccountPage", "Form"))
        self.label.setText(_translate("AccountPage", "選擇表單"))
        self.label_2.setText(_translate("AccountPage", "TextLabel"))
        self.label_3.setText(_translate("AccountPage", "TextLabel"))
        self.pushButton_3.setText(_translate("AccountPage", "輸出表格"))
        self.insertRow_PushButton.setText(_translate("AccountPage", "新增"))
        self.deleteRow_PushButton.setText(_translate("AccountPage", "刪除"))
