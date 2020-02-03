

import sys
from PyQt5 import QtWidgets
import interface


class MessengerWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def send_message(self):
        message = self.lineEdit.text()
        self.plainTextEdit.appendPlainText(message)
        self.lineEdit.clear()


app = QtWidgets.QApplication(sys.argv)
window = MessengerWindow()
window.show()
app.exec_()

