from statistics import NormalDist
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QHeaderView, QTableView
from ui_py.setPage import Ui_setPage
from ui_controller.adding_option_controller import adding_option_controller
from model.menuRecordModel import menuRecordModel, menuRecordSelectDelegate
import pandas as pd

class menuRecordTableView(QTableView):
   def __init__(self, data):
      super(menuRecordTableView, self).__init__()
      font = QFont()
      font.setFamily("微軟正黑體")
      font.setPointSize(16)
      self.setFont(font)
      self.model = menuRecordModel(data)
      self.setItemDelegateForColumn(4, menuRecordSelectDelegate(self))
      self.setModel(self.model)
      self.resizeColumnsToContents()
      self.resizeRowsToContents()
      self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
      self.horizontalHeader().setStretchLastSection(True)

   def resetModel(self, data):
      self.model = menuRecordModel(data)
      self.setModel(self.model)
      

class setPage_controller(QWidget, Ui_setPage):
   def __init__(self, HomePageWidget, client):
      super(setPage_controller, self).__init__()
      self.setupUi(self)
      self.HomePage = HomePageWidget
      self.client = client
      self.setDate = QDate.currentDate()
      self.menuIDList,self.menuRecordData = self.setMenuRecordData()
      self.menuRecord_tableView = menuRecordTableView(self.menuRecordData)
      self.menuRecord_tableView.model.dataChanged.connect(self.setMenuRecordDataSelected)
      self.initUI()

   def initUI(self):
      self.menuRecord_verticalLayout.addWidget(self.menuRecord_tableView)
      self.setPage_stackedWidget.setCurrentWidget(self.setDate_page)
      self.date_dateEdit.setDate(QDate.currentDate())
      newSpace = adding_option_controller(self.verticalLayout)
      self.verticalLayout.insertWidget(0, newSpace)
      self.setupComboBox()
      self.confirm_Button.clicked.connect(self.save_record)
      self.add_fav_PushButton.clicked.connect(self.addFavMenu)
      self.fav_confirm_Button.clicked.connect(self.setFavMenu)
      self.returnHomePage_pushButton.clicked.connect(self.returnHomePage)
      self.setDate_nextStep_pushButton.clicked.connect(self.head2SetMenu)
      self.returnSetDate_pushButton.clicked.connect(self.returnSetDate)

   def setMenuRecordData(self):
      stateDict = {'0':'未完成', '1':'已完成'}
      menuRecordData = self.client.getMenuRecord()
      menuIDList = list(menuRecordData['ID'])
      menuRecordData = menuRecordData.drop(columns = ['ID'])
      menuRecordData['isCompleted'] = menuRecordData['isCompleted'].apply(lambda x:stateDict.get(x))
         
      return menuIDList,menuRecordData

   def returnSetDate(self):
      reply = QMessageBox.question(
            None, 
            '提示訊息', 
            '返回後尚未儲存的菜單資料將會消失，請問是否繼續？',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)
         
      if reply == QMessageBox.No:
         return
      self.setPage_stackedWidget.setCurrentWidget(self.setDate_page)
      self.resetLayout()
   def head2SetMenu(self):
      date = self.date_dateEdit.date()
      if date < QDate.currentDate():
         QMessageBox.warning(None, '警告', f'無法設定過去日期{date.toString(Qt.ISODate)}的菜單！')
      else:
         date = date.toString(Qt.ISODate)
         todayRecord_storeName = self.client.checkTodayRecordbyDate(date)
         if todayRecord_storeName:
            messagebox = QMessageBox()
            messagebox.setWindowTitle('提示訊息')
            messagebox.setText(f'{date}有一筆{todayRecord_storeName}的訂單尚未完成，請前往今日訂單確認完成或刪除訂單')
            messagebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messagebox.button(QMessageBox.Yes).setText('前往今日訂單')
            messagebox.button(QMessageBox.No).setText('取消')
            messagebox.exec_()
            if messagebox.clickedButton() == messagebox.button(QMessageBox.Yes):
               self.returnHomePage()
               self.HomePage.jump_TodayRecord()
            return
         else:
            menuRecord_id,menuRecord_storeName = self.client.checkMenuRecordbyDate(date)
            if menuRecord_id:
               messagebox = QMessageBox()
               messagebox.setWindowTitle('提示訊息')
               messagebox.setText(f'{date}已經有設定"{menuRecord_storeName}"菜單且該菜單尚未被使用，請問要修改嗎？')
               messagebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
               messagebox.button(QMessageBox.Yes).setText('修改菜單')
               messagebox.button(QMessageBox.No).setText('取消')
               messagebox.exec_()
               if messagebox.clickedButton() == messagebox.button(QMessageBox.Yes):
                  self.store_name_lineEdit.setText(menuRecord_storeName)
                  self.setupMenuDetailbyID(menuRecord_id)
               else:
                  return
            self.setPage_stackedWidget.setCurrentWidget(self.setMenu_page)
            self.setupComboBox()
            self.setDate = date    
   
   def setupMenuDetailbyID(self, id):
      menu = self.client.getMenuDetailbyID(id)
      if not menu.empty:
         for index,item in menu.iterrows():
            spaceRow = adding_option_controller(self.verticalLayout)
            spaceRow.option_label.setText(item.at['ItemName'])
            spaceRow.price_label.setText(item.at['price'])
            spaceRow.stackedWidget.removeWidget(spaceRow.page)
            self.verticalLayout.insertWidget(index+1, spaceRow)


   def setupComboBox(self):
      self.favoStore_comboBox.clear()
      self.favoStore_comboBox.addItems(['-----常用菜單-----', '無'])
      self.favoStore_comboBox.setCurrentIndex(0)
      self.favoStore_comboBox.model().item(0).setEnabled(False)
      self.favoStore_comboBox.addItems(list(self.client.getFavNameList()))
      self.favoStore_comboBox.currentTextChanged.connect(self.changeComboBox)

   def save_record(self):
      if not self.store_name_lineEdit.text():
         QMessageBox.warning(None, '警告', f'尚未輸入店名！')
         return
      if self.verticalLayout.itemAt(0).widget().option_lineEdit.text():
         reply = QMessageBox.question(
            None, 
            '提示訊息', 
            f'{self.verticalLayout.itemAt(0).widget().option_lineEdit.text()}尚未新增，請問是否繼續？',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)
         
         if reply == QMessageBox.No:
            return
         
      store_name = self.store_name_lineEdit.text()
      y,m,d = self.setDate.split('-')
      RecordData = pd.DataFrame(columns=['ItemName', 'price'])
      for i in range(1, self.verticalLayout.count()-1):
         item = self.verticalLayout.itemAt(i).widget()
         if item.option_label.text() == '':
            QMessageBox.warning(None, '警告', f'品項不可為空！')
            return
         if item.price_label.text() == '':
            QMessageBox.warning(None, '警告', f'價格不可為空！')
            return
         RecordData = pd.concat(
            [RecordData, 
            pd.DataFrame({'ItemName':[item.option_label.text()], 'price':[item.price_label.text()]})], 
            ignore_index=True)
      if not RecordData.empty:
         self.client.setMenu(y,m,d,store_name,RecordData)
         self.client.deleteFavMenu('上次菜單')
         self.saveFavtoDB('上次菜單')
         QMessageBox.information(None, '提示', f'成功設定{self.setDate}的菜單！')
         self.resetMenuRecord()
      else:
         QMessageBox.warning(None, '警告', f'無填寫菜單資料！')
         return
      self.setPage_stackedWidget.setCurrentWidget(self.setDate_page)
      self.resetLayout()

      
   
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
      dialog = QInputDialog(None)
      font = QFont()
      font.setFamily('微軟正黑體')
      font.setPointSize(14)
      dialog.setInputMode(QInputDialog.TextInput)
      dialog.setWindowTitle('命名提示')
      dialog.setLabelText('請為此菜單命名:')
      dialog.setFont(font)
      ok = dialog.exec_()
      menuName = dialog.textValue()
      if ok and menuName != '':
         if menuName == '上次菜單':
            QMessageBox.warning(None, '警告', '"上次菜單"為系統預設菜單名，請重新命名。')
            return
         if menuName in self.client.getFavNameList():
            reply = QMessageBox.question(
            None, 
            '更名提示', 
            f'"{menuName}"已使用過,按Yes更新菜單,或按No重新命名。',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)
         
            if reply == QMessageBox.No:
               return
            elif reply == QMessageBox.Yes:
               self.client.deleteFavMenu(menuName)
         self.saveFavtoDB(menuName)
      else:
         return
      

   def saveFavtoDB(self,FavMenuName):
      if not self.store_name_lineEdit.text():
         QMessageBox.warning(None, '警告', f'尚未輸入店名！')
         return
      store_name = self.store_name_lineEdit.text()
      if self.verticalLayout.itemAt(0).widget().option_lineEdit.text():
         reply = QMessageBox.question(
            None, 
            '提示訊息', 
            f'{self.verticalLayout.itemAt(0).widget().option_lineEdit.text()}尚未新增，請問是否繼續？',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)
         
         if reply == QMessageBox.No:
            return
      FavData = pd.DataFrame(columns=['StoreName', 'FavMenuName', 'ItemName', 'price'])
      for i in range(1, self.verticalLayout.count()-1):
         item = self.verticalLayout.itemAt(i).widget()
         if item.option_label.text() == '':
            QMessageBox.warning(None, '警告', f'品項不可為空！')
            return
         if item.price_label.text() == '':
            QMessageBox.warning(None, '警告', f'價格不可為空！')
            return
         FavData = pd.concat(
            [FavData, 
            pd.DataFrame({'StoreName':[store_name], 'FavMenuName':[FavMenuName], 'ItemName':[item.option_label.text()], 'price':[item.price_label.text()]})], 
            ignore_index=True)
      if not FavData.empty:
         self.client.addFavMenu(FavData)
         if FavMenuName != '上次菜單':
            QMessageBox.information(None, '提示', f'成功新增至最愛！')
      else:
         QMessageBox.warning(None, '警告', f'無填寫菜單資料！')
         
      

   def returnHomePage(self):
      self.close()
      self.HomePage.show()

   def setMenuRecordDataSelected(self, index):
      value = self.menuRecord_tableView.model.data(index, Qt.DisplayRole)
      self.menuRecordData.loc[index.row(), 'isSelected'] = value
      id = self.menuIDList[index.row()]
      self.client.updateMenuSelectState(id, value)
   
   def resetMenuRecord(self):
      self.menuIDList,self.menuRecordData = self.setMenuRecordData()
      self.menuRecord_tableView.resetModel(self.menuRecordData)
      


   
      



     
        