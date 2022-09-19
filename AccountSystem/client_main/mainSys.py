import sys
from pathlib import Path
#sys.path[0]=str(Path(sys.path[0]).parent)
from PyQt5 import QtWidgets
from ui_controller.HomePage_controller import HomePage_controller
from client.client import clientHandler

client = clientHandler()
app = QtWidgets.QApplication(sys.argv)
myWin = HomePage_controller(client)
myWin.show()
sys.exit(app.exec_())

 