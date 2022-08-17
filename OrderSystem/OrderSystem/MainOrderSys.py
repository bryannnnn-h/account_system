import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget
from ui_logic.call_orderSystem import OrderSystem

def getTodayMenu():
    itemCount = 10
    storeName = "無"
    itemNameList = ["無"]*10
    priceList = [100]*10
    '''
    read db
    '''
    return itemCount, storeName, itemNameList, priceList

def main():
    app = QApplication(sys.argv)
    itemCount, storeName, itemNameList, priceList = getTodayMenu()
    MyWin = OrderSystem(itemCount, storeName, itemNameList, priceList)
    MyWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()