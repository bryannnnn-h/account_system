from statistics import NormalDist
from tkinter import font
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QDate, QModelIndex
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QHeaderView, QTableView, QAbstractItemView
from ui_py.setPage import Ui_setPage
from ui_controller.adding_option_controller import adding_option_controller
from model.menuModel import menuRecordModel, menuRecordSelectDelegate, menuDetailModel
import pandas as pd

class menuRecordTableView(QTableView):
   def __init__(self, data):
      super(menuRecordTableView, self).__init__()
      font = QFont()
      font.setFamily("微軟正黑體")
      font.setPointSize(16)
      self.setFont(font)
      self.model = menuRecordModel(data)
      self.setItemDelegateForColumn(5, menuRecordSelectDelegate(self))
      self.setItemDelegateForColumn(0, menuRecordSelectDelegate(self))
      self.setModel(self.model)
      self.setSelectionMode(QAbstractItemView.MultiSelection)
      self.resizeColumnsToContents()
      self.resizeRowsToContents()
      self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
      self.horizontalHeader().setStretchLastSection(True)
      self.verticalHeader().setVisible(False)
      self.horizontalHeader().setSectionsClickable(False)

   def resetModel(self, data):
      self.model = menuRecordModel(data)
      self.setItemDelegateForColumn(5, menuRecordSelectDelegate(self))
      self.setItemDelegateForColumn(0, menuRecordSelectDelegate(self))
      self.setModel(self.model)
class menuDetailTableView(QTableView):
   def __init__(self, data=pd.DataFrame()):
      super(menuDetailTableView, self).__init__()
      font = QFont()
      font.setFamily("微軟正黑體")
      font.setPointSize(16)
      self.setFont(font)
      self.model = menuDetailModel(data)
      self.setModel(self.model)
      self.resizeColumnsToContents()
      self.resizeRowsToContents()
      self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
      self.horizontalHeader().setStretchLastSection(True)

   def resetModel(self, data):
      self.model = menuDetailModel(data)
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
      self.menuDetail_tableView = menuDetailTableView()
      self.menuDetailID = 0 
      self.initUI()

   def initUI(self):
      self.menuRecord_verticalLayout.addWidget(self.menuRecord_tableView)
      self.menuDetail_verticalLayout.addWidget(self.menuDetail_tableView)
      self.setPage_stackedWidget.setCurrentWidget(self.setDate_page)
      self.date_dateEdit.setDate(QDate.currentDate())
      newSpace = adding_option_controller(self.verticalLayout)
      self.verticalLayout.insertWidget(0, newSpace)
      self.setupComboBox()
      self.confirm_Button.clicked.connect(self.save_record)
      self.add_fav_PushButton.clicked.connect(self.addFavMenu)
      self.fav_confirm_Button.clicked.connect(self.setFavMenu)
      self.returnHomePage_pushButton.clicked.connect(self.returnHomePage)
      self.setDate_nextStep_pushButton.clicked.connect(lambda: self.head2SetMenu(self.date_dateEdit.date()))
      self.returnSetDate_pushButton.clicked.connect(self.returnSetDate)
      self.showMenuDetail_pushButton.clicked.connect(self.showMenuDetail)
      self.returnSetDate_pushButton_2.clicked.connect(self.returnSetDate)
      self.add_fav_PushButton_2.clicked.connect(self.addFavMenu)
      self.modifyMenuDetail_pushButton.clicked.connect(lambda: self.head2SetMenu(QDate.fromString(self.menuDetailDate_label.text(),"yyyy-MM-dd")))
      self.deleteMenuRecord_pushButton.clicked.connect(self.deleteMenuRecord)

   def setMenuRecordData(self):
      stateDict = {'0':'未完成', '1':'已完成'}
      menuRecordData = self.client.getMenuRecord()
      menuRecordData = menuRecordData.sort_values(by=['Year', 'Month', 'Day'],ascending=[False,True,False],ignore_index=True)
      menuIDList = list(menuRecordData['ID'])
      menuRecordData = menuRecordData.drop(columns = ['ID'])
      menuRecordData['isCompleted'] = menuRecordData['isCompleted'].apply(lambda x:stateDict.get(x) if x != '' else x)
         
      return menuIDList,menuRecordData

   def returnSetDate(self):
      if self.setPage_stackedWidget.currentWidget() == self.setMenu_page:
         reply = QMessageBox.question(
               None, 
               '提示訊息', 
               '<font size="18">返回後尚未儲存的菜單資料將會消失，請問是否繼續？</font>',
               QMessageBox.Yes | QMessageBox.No, 
               QMessageBox.No)
            
         if reply == QMessageBox.No:
            return
      self.setPage_stackedWidget.setCurrentWidget(self.setDate_page)
      self.resetLayout()
   def head2SetMenu(self, date):
      if date < QDate.currentDate():
         QMessageBox.warning(None, '警告', f'<font size="18">無法設定過去日期{date.toString(Qt.ISODate)}的菜單！</font>')
      else:
         date = date.toString(Qt.ISODate)
         todayRecord_storeName = self.client.checkTodayRecordbyDate(date)
         if todayRecord_storeName:
            messagebox = QMessageBox()
            messagebox.setWindowTitle('提示訊息')
            messagebox.setText(f'<font size="18">{date}有一筆{todayRecord_storeName}的訂單尚未完成，請前往今日訂單確認完成或刪除訂單</font>')
            messagebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messagebox.button(QMessageBox.Yes).setText('前往今日訂單')
            messagebox.button(QMessageBox.No).setText('取消')
            messagebox.exec_()
            if messagebox.clickedButton() == messagebox.button(QMessageBox.Yes):
               self.returnHomePage()
               self.HomePage.jump_TodayRecord()
            return
         else:
            if self.setPage_stackedWidget.currentWidget() == self.setDate_page:
               menuRecord_id,menuRecord_storeName = self.client.checkMenuRecordbyDate(date)
               if menuRecord_id:
                  messagebox = QMessageBox()
                  messagebox.setWindowTitle('提示訊息')
                  messagebox.setText(f'<font size="18">{date}已經有設定"{menuRecord_storeName}"菜單且該菜單尚未被使用，請問要修改嗎？</font>')
                  messagebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                  messagebox.button(QMessageBox.Yes).setText('修改菜單')
                  messagebox.button(QMessageBox.No).setText('取消')
                  messagebox.exec_()
                  if messagebox.clickedButton() == messagebox.button(QMessageBox.Yes):
                     self.store_name_lineEdit.setText(menuRecord_storeName)
                     self.setupMenuDetailbyID(menuRecord_id)
                  else:
                     return
            elif self.setPage_stackedWidget.currentWidget() == self.menuDetail_page:
               menuRecord_storeName = self.menuDetailStoreName_label.text()
               self.store_name_lineEdit.setText(menuRecord_storeName)
               self.setupMenuDetailbyArray(self.menuDetail_tableView.model.AllData())
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
   def setupMenuDetailbyArray(self, menu):
      if menu.size != 0:
         for index, item in enumerate(menu):
            spaceRow = adding_option_controller(self.verticalLayout)
            spaceRow.option_label.setText(item[0])
            spaceRow.price_label.setText(item[1])
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
         QMessageBox.warning(None, '警告', f'<font size="18">尚未輸入店名！</font>')
         return
      if self.verticalLayout.itemAt(0).widget().option_lineEdit.text():
         reply = QMessageBox.question(
            None, 
            '提示訊息', 
            f'<font size="18">{self.verticalLayout.itemAt(0).widget().option_lineEdit.text()}尚未新增，請問是否繼續？</font>',
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
            QMessageBox.warning(None, '警告', f'<font size="18">品項不可為空！</font>')
            return
         if item.price_label.text() == '':
            QMessageBox.warning(None, '警告', f'<font size="18">價格不可為空！</font>')
            return
         RecordData = pd.concat(
            [RecordData, 
            pd.DataFrame({'ItemName':[item.option_label.text()], 'price':[item.price_label.text()]})], 
            ignore_index=True)
      if not RecordData.empty:
         self.client.setMenu(y,m,d,store_name,RecordData)
         self.client.deleteFavMenu('上次菜單')
         self.saveFavtoDB('上次菜單')
         QMessageBox.information(None, '提示', f'<font size="18">成功設定{self.setDate}的菜單！</font>')
         self.resetMenuRecord()
      else:
         QMessageBox.warning(None, '警告', f'<font size="18">無填寫菜單資料！</font>')
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
            QMessageBox.warning(None, '警告', '<font size="18">\"上次菜單\"為系統預設菜單名，請重新命名。</font>')
            return
         if menuName in self.client.getFavNameList():
            reply = QMessageBox.question(
            None, 
            '更名提示', 
            f'<font size="18">\"{menuName}\"已使用過,按Yes更新菜單,或按No重新命名。</font>',
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
      if self.setPage_stackedWidget.currentWidget() == self.setMenu_page:
         if not self.store_name_lineEdit.text():
            QMessageBox.warning(None, '警告', f'<font size="18">尚未輸入店名！</font>')
            return
         store_name = self.store_name_lineEdit.text()
         if self.verticalLayout.itemAt(0).widget().option_lineEdit.text():
            reply = QMessageBox.question(
               None, 
               '提示訊息', 
               f'<font size="18">{self.verticalLayout.itemAt(0).widget().option_lineEdit.text()}尚未新增，請問是否繼續？</font>',
               QMessageBox.Yes | QMessageBox.No, 
               QMessageBox.No)
            
            if reply == QMessageBox.No:
               return
         FavData = pd.DataFrame(columns=['StoreName', 'FavMenuName', 'ItemName', 'price'])
         for i in range(1, self.verticalLayout.count()-1):
            item = self.verticalLayout.itemAt(i).widget()
            if item.option_label.text() == '':
               QMessageBox.warning(None, '警告', f'<font size="18">品項不可為空！</font>')
               return
            if item.price_label.text() == '':
               QMessageBox.warning(None, '警告', f'<font size="18">價格不可為空！</font>')
               return
            FavData = pd.concat(
               [FavData, 
               pd.DataFrame({'StoreName':[store_name], 'FavMenuName':[FavMenuName], 'ItemName':[item.option_label.text()], 'price':[item.price_label.text()]})], 
               ignore_index=True)
         if not FavData.empty:
            self.client.addFavMenu(FavData)
            if FavMenuName != '上次菜單':
               QMessageBox.information(None, '提示', f'<font size="18">成功新增至最愛！</font>')
         else:
            QMessageBox.warning(None, '警告', f'<font size="18">無填寫菜單資料！</font>')
      elif self.setPage_stackedWidget.currentWidget() is self.menuDetail_page:
         store_name = self.menuDetailStoreName_label.text()
         FavData = pd.DataFrame(columns=['StoreName', 'FavMenuName', 'ItemName', 'price'])
         for i in range(self.menuDetail_tableView.model.rowCount()):
            item = self.menuDetail_tableView.model.getRow(i)
            FavData = pd.concat(
               [FavData, 
               pd.DataFrame({'StoreName':[store_name], 'FavMenuName':[FavMenuName], 'ItemName':[item[0]], 'price':[item[1]]})], 
               ignore_index=True)
         self.client.addFavMenu(FavData)
         if FavMenuName != '上次菜單':
            QMessageBox.information(None, '提示', f'<font size="18">成功新增至最愛！</font>')

   def returnHomePage(self):
      if self.setPage_stackedWidget.currentWidget() == self.setMenu_page:
         reply = QMessageBox.question(
               None, 
               '提示訊息', 
               '<font size="18">返回後尚未儲存的菜單資料將會消失，請問是否繼續？</font>',
               QMessageBox.Yes | QMessageBox.No, 
               QMessageBox.No)
            
         if reply == QMessageBox.No:
            return
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
      self.menuRecord_tableView.model.dataChanged.connect(self.setMenuRecordDataSelected)
   
   def showMenuDetail(self):
      if self.menuRecordData.at[0, 'Year'] == '':
         return
      if self.setPage_stackedWidget.currentWidget() == self.setMenu_page:
         reply = QMessageBox.question(
               None, 
               '提示訊息', 
               '<font size="18">返回後尚未儲存的菜單資料將會消失，請問是否繼續？</font>',
               QMessageBox.Yes | QMessageBox.No, 
               QMessageBox.No)
            
         if reply == QMessageBox.No:
            return
         self.resetLayout()
      indexes = self.menuRecord_tableView.selectionModel().selectedIndexes()
      if len(indexes) != 0:
         index = indexes[-1].row()
      else:
         index = -1
      if index != -1:
         self.menuDetailID = self.menuIDList[index]
         menuDetailDf = self.client.getMenuDetailbyID(self.menuDetailID)
         self.menuDetailStoreName_label.setText(self.menuRecordData.at[index,'StoreName'])
         self.menuDetailDate_label.setText('-'.join([self.menuRecordData.at[index,'Year'],self.menuRecordData.at[index,'Month'],self.menuRecordData.at[index,'Day']]))
         self.menuDetail_tableView.resetModel(menuDetailDf)
         self.setPage_stackedWidget.setCurrentWidget(self.menuDetail_page)
   
   def deleteMenuRecord(self):
      if self.menuRecordData.at[0, 'Year'] == '':
         return
      indexes = self.menuRecord_tableView.selectionModel().selectedIndexes()
      if len(indexes) == 0: 
         QMessageBox.warning(None, '錯誤', '<font size="18">沒有選擇要刪除的欄位。</font>')
         return
      popIdList = []
      popItemMsg = ''
      for index in indexes:
         if not index.isValid(): 
               continue
         popId = self.menuIDList[index.row()]
         popIdList.append(popId)
         popItemMsg+=('-'.join(list(self.menuRecordData.loc[index.row(),['Year','Month','Day','StoreName']]))+'\n')
      reply = QMessageBox.question(
               None, 
               '提示訊息', 
               '<font size="18">確定要刪除以下項目嗎？\n'+popItemMsg+'</font>',
               QMessageBox.Yes | QMessageBox.No, 
               QMessageBox.No)
            
      if reply == QMessageBox.No:
         return
      for id in popIdList:
         if id == self.menuDetailID:
            self.menuDetailID = 0
            self.setPage_stackedWidget.setCurrentWidget(self.setDate_page)
         self.client.deleteMenuByID(id)
      self.resetMenuRecord()
            
      


   
      



     
        