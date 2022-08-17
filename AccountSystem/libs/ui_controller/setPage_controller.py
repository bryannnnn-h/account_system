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
      newSpace = adding_option_controller(self.verticalLayout)
      self.verticalLayout.insertWidget(0, newSpace)
      self.confirm_Button.clicked.connect(self.save_record)
      self.data = []
      self.client = client

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

      self.client.setTodayMenu(RecordData)
      self.close()
      self.HomePage.show()
   
      
   
      

        

if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)
   myWin = setPage_controller()
   myWin.show()
   sys.exit(app.exec_())


     
        