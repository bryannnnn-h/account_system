# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\setPage.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_setPage(object):
    def setupUi(self, setPage):
        setPage.setObjectName("setPage")
        setPage.setEnabled(True)
        setPage.resize(600, 800)
        self.store_name_label = QtWidgets.QLabel(setPage)
        self.store_name_label.setGeometry(QtCore.QRect(100, 20, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(20)
        self.store_name_label.setFont(font)
        self.store_name_label.setObjectName("store_name_label")
        self.store_name_lineEdit = QtWidgets.QLineEdit(setPage)
        self.store_name_lineEdit.setGeometry(QtCore.QRect(200, 20, 300, 50))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.store_name_lineEdit.setFont(font)
        self.store_name_lineEdit.setObjectName("store_name_lineEdit")
        self.option_input_area = QtWidgets.QScrollArea(setPage)
        self.option_input_area.setGeometry(QtCore.QRect(50, 165, 502, 517))
        self.option_input_area.setWidgetResizable(True)
        self.option_input_area.setObjectName("option_input_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 500, 515))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.option_input_area.setWidget(self.scrollAreaWidgetContents)
        self.confirm_Button = QtWidgets.QPushButton(setPage)
        self.confirm_Button.setGeometry(QtCore.QRect(250, 725, 100, 35))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.confirm_Button.setFont(font)
        self.confirm_Button.setObjectName("confirm_Button")
        self.scroll_navigater = QtWidgets.QWidget(setPage)
        self.scroll_navigater.setGeometry(QtCore.QRect(50, 135, 500, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_navigater.sizePolicy().hasHeightForWidth())
        self.scroll_navigater.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.scroll_navigater.setFont(font)
        self.scroll_navigater.setObjectName("scroll_navigater")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scroll_navigater)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.option_name_label = QtWidgets.QLabel(self.scroll_navigater)
        self.option_name_label.setObjectName("option_name_label")
        self.horizontalLayout.addWidget(self.option_name_label)
        self.price_label = QtWidgets.QLabel(self.scroll_navigater)
        self.price_label.setTextFormat(QtCore.Qt.AutoText)
        self.price_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.price_label.setObjectName("price_label")
        self.horizontalLayout.addWidget(self.price_label)
        self.horizontalLayout.setStretch(0, 7)
        self.horizontalLayout.setStretch(1, 3)
        self.returnHomePage_pushButton = QtWidgets.QPushButton(setPage)
        self.returnHomePage_pushButton.setGeometry(QtCore.QRect(400, 725, 150, 35))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.returnHomePage_pushButton.setFont(font)
        self.returnHomePage_pushButton.setObjectName("returnHomePage_pushButton")
        self.fav_confirm_Button = QtWidgets.QPushButton(setPage)
        self.fav_confirm_Button.setEnabled(False)
        self.fav_confirm_Button.setGeometry(QtCore.QRect(400, 90, 100, 35))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.fav_confirm_Button.setFont(font)
        self.fav_confirm_Button.setObjectName("fav_confirm_Button")
        self.add_fav_PushButton = QtWidgets.QPushButton(setPage)
        self.add_fav_PushButton.setGeometry(QtCore.QRect(50, 725, 150, 35))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.add_fav_PushButton.setFont(font)
        self.add_fav_PushButton.setObjectName("add_fav_PushButton")
        self.favoStore_comboBox = QtWidgets.QComboBox(setPage)
        self.favoStore_comboBox.setGeometry(QtCore.QRect(100, 90, 270, 35))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.favoStore_comboBox.setFont(font)
        self.favoStore_comboBox.setEditable(False)
        self.favoStore_comboBox.setCurrentText("")
        self.favoStore_comboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.favoStore_comboBox.setObjectName("favoStore_comboBox")

        self.retranslateUi(setPage)
        QtCore.QMetaObject.connectSlotsByName(setPage)

    def retranslateUi(self, setPage):
        _translate = QtCore.QCoreApplication.translate
        setPage.setWindowTitle(_translate("setPage", "Form"))
        self.store_name_label.setText(_translate("setPage", "店名"))
        self.confirm_Button.setText(_translate("setPage", "確認"))
        self.option_name_label.setText(_translate("setPage", "品項"))
        self.price_label.setText(_translate("setPage", "價格"))
        self.returnHomePage_pushButton.setText(_translate("setPage", "返回主選單"))
        self.fav_confirm_Button.setText(_translate("setPage", "確認"))
        self.add_fav_PushButton.setText(_translate("setPage", "加到常用菜單"))
