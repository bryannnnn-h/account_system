# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adding_unit.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_option_unit(object):
    def setupUi(self, option_unit):
        option_unit.setObjectName("option_unit")
        option_unit.resize(400, 40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(option_unit.sizePolicy().hasHeightForWidth())
        option_unit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(8)
        option_unit.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(option_unit)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(option_unit)
        self.stackedWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setLineWidth(1)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.option_lineEdit = QtWidgets.QLineEdit(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.option_lineEdit.sizePolicy().hasHeightForWidth())
        self.option_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.option_lineEdit.setFont(font)
        self.option_lineEdit.setObjectName("option_lineEdit")
        self.horizontalLayout.addWidget(self.option_lineEdit)
        self.price_lineEdit = QtWidgets.QLineEdit(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.price_lineEdit.sizePolicy().hasHeightForWidth())
        self.price_lineEdit.setSizePolicy(sizePolicy)
        self.price_lineEdit.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.price_lineEdit.setFont(font)
        self.price_lineEdit.setObjectName("price_lineEdit")
        self.horizontalLayout.addWidget(self.price_lineEdit)
        self.add_Button = QtWidgets.QPushButton(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_Button.sizePolicy().hasHeightForWidth())
        self.add_Button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.add_Button.setFont(font)
        self.add_Button.setObjectName("add_Button")
        self.horizontalLayout.addWidget(self.add_Button)
        self.horizontalLayout.setStretch(0, 7)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.option_label = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.option_label.sizePolicy().hasHeightForWidth())
        self.option_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(18)
        self.option_label.setFont(font)
        self.option_label.setText("")
        self.option_label.setObjectName("option_label")
        self.horizontalLayout_2.addWidget(self.option_label)
        self.price_label = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.price_label.sizePolicy().hasHeightForWidth())
        self.price_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.price_label.setFont(font)
        self.price_label.setText("")
        self.price_label.setObjectName("price_label")
        self.horizontalLayout_2.addWidget(self.price_label)
        self.del_Button = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.del_Button.sizePolicy().hasHeightForWidth())
        self.del_Button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.del_Button.setFont(font)
        self.del_Button.setObjectName("del_Button")
        self.horizontalLayout_2.addWidget(self.del_Button)
        self.horizontalLayout_2.setStretch(0, 7)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        self.retranslateUi(option_unit)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(option_unit)

    def retranslateUi(self, option_unit):
        _translate = QtCore.QCoreApplication.translate
        option_unit.setWindowTitle(_translate("option_unit", "Form"))
        self.add_Button.setText(_translate("option_unit", "+"))
        self.del_Button.setText(_translate("option_unit", "－"))
