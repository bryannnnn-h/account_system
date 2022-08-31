from statistics import NormalDist
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_py.setPage import Ui_setPage
from ui_controller.adding_option_controller import adding_option_controller
import pandas as pd
import sys


class setPage_controller(QtWidgets.QWidget, Ui_setPage):
   def __init__(self, HomePageWidget, client):
      super(setPage_controller, self).__init__()
      self.setupUi(self)
      self.HomePage = HomePageWidget
      self.client = client
      self.initUI()

   def initUI(self):
      newSpace = adding_option_controller(self.verticalLayout)
      self.verticalLayout.insertWidget(0, newSpace)
      self.confirm_Button.clicked.connect(self.save_record)
      self.add_fav_PushButton.clicked.connect(self.addFavMenu)
      self.fav_confirm_Button.clicked.connect(self.setFavMenu)
      self.returnHomePage_pushButton.clicked.connect(self.returnHomePage)
      self.setupComboBox()
      self.data = []
      
   def setupComboBox(self):
      self.favoStore_comboBox.addItems(['-----常用菜單-----', '無', '上次菜單'])
      self.favoStore_comboBox.setCurrentIndex(0)
      self.favoStore_comboBox.model().item(0).setEnabled(False)
      self.favoStore_comboBox.addItems(list(self.client.getFavNameList()))
      self.favoStore_comboBox.currentTextChanged.connect(self.changeComboBox)

   def save_record(self):
      if self.verticalLayout.itemAt(0).widget().option_lineEdit.text():
         reply = QtWidgets.QMessageBox.question(
            None, 
            '提示訊息', 
            f'{self.verticalLayout.itemAt(0).widget().option_lineEdit.text()}尚未新增，請問是否繼續？',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No)
         
         if reply == QtWidgets.QMessageBox.No:
            return
         
      store_name = self.store_name_lineEdit.text()
      RecordData = pd.DataFrame(columns=['StoreName', 'ItemName', 'price'])
      for i in range(1, self.verticalLayout.count()-1):
         item = self.verticalLayout.itemAt(i).widget()
         print(item.option_label.text())
         RecordData = pd.concat(
            [RecordData, 
            pd.DataFrame({'StoreName':[store_name], 'ItemName':[item.option_label.text()], 'price':[item.price_label.text()]})], 
            ignore_index=True)
      if not RecordData.empty:
         self.client.setTodayMenu(RecordData)
         self.client.deleteFavMenu('上次菜單')
         self.saveFavtoDB('上次菜單')

      self.close()
      self.HomePage.show()
   
   def changeComboBox(self):
      if self.favoStore_comboBox.currentIndex() == 1:
         self.favoStore_comboBox.setCurrentIndex(0)
         self.resetLayout()

      if(self.favoStore_comboBox.currentIndex() > 1):
         self.fav_confirm_Button.setEnabled(True)
      else:
         self.fav_confirm_Button.setEnabled(False)


   def resetLayout(self):
      self.store_name_lineEdit.setText('')
      for i in reversed(range(self.verticalLayout.count())):
         widget = self.verticalLayout.itemAt(i).widget()
         if widget != None:
            widget.setParent(None)
      newSpace = adding_option_controller(self.verticalLayout)
      self.verticalLayout.insertWidget(0, newSpace)

   def setFavMenu(self):
      self.resetLayout()
      FavName = self.favoStore_comboBox.currentText()
      FavMenuContent = self.client.getFavMenuContent(FavName)
      if not FavMenuContent.empty:
         self.store_name_lineEdit.setText(FavMenuContent.at[0,'StoreName'])
         for index,item in FavMenuContent.iterrows():
            spaceRow = adding_option_controller(self.verticalLayout)
            spaceRow.option_label.setText(item.at['ItemName'])
            spaceRow.price_label.setText(item.at['price'])
            spaceRow.stackedWidget.removeWidget(spaceRow.page)
            self.verticalLayout.insertWidget(index+1, spaceRow)

   def addFavMenu(self):
      dialog = QtWidgets.QInputDialog(None)
      font = QtGui.QFont()
      font.setFamily('微軟正黑體')
      font.setPointSize(14)
      dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
      dialog.setWindowTitle('命名提示')
      dialog.setLabelText('請為此菜單命名:')
      dialog.setFont(font)
      ok = dialog.exec_()
      menuName = dialog.textValue()
      if ok and menuName != '':
         if menuName == '上次菜單':
            QtWidgets.QMessageBox.warning(None, '警告', '"上次菜單"為系統預設菜單名，請重新命名。')
            return
         if menuName in self.client.getFavNameList():
            reply = QtWidgets.QMessageBox.question(
            None, 
            '更名提示', 
            f'"{menuName}"已使用過,按Yes更新菜單,或按No重新命名。',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No)
         
            if reply == QtWidgets.QMessageBox.No:
               return
            elif reply == QtWidgets.QMessageBox.Yes:
               self.client.deleteFavMenu(menuName)
         self.saveFavtoDB(menuName)
      else:
         return
      

   def saveFavtoDB(self,FavMenuName):
      store_name = self.store_name_lineEdit.text()
      FavData = pd.DataFrame(columns=['StoreName', 'FavMenuName', 'ItemName', 'price'])
      for i in range(1, self.verticalLayout.count()-1):
         item = self.verticalLayout.itemAt(i).widget()
         print(item.option_label.text())
         FavData = pd.concat(
            [FavData, 
            pd.DataFrame({'StoreName':[store_name], 'FavMenuName':[FavMenuName], 'ItemName':[item.option_label.text()], 'price':[item.price_label.text()]})], 
            ignore_index=True)

      self.client.addFavMenu(FavData)

   def returnHomePage(self):
      self.close()
      self.HomePage.show()



     
        