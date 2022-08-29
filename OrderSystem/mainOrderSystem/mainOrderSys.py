import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget
from ui_logic.call_orderSystem import OrderSystem
from client.client_orderSystem import client_orderSystem

def main():
    client = client_orderSystem()
    if client.client_error:
        sys.exit(0)
    app = QApplication(sys.argv)
    MyWin = OrderSystem(client)
    if client.client_error:
        sys.exit(0)
    MyWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()