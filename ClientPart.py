# Мой тестовый мессенджер
#
# 2019 - 2020
# Клиенсткая часть
# Twisted, PyQt, QtDesigner
#

from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import ClientFactory

import sys
from PyQt5 import QtWidgets
import interface


class ClientProtocol (LineOnlyReceiver):
    factory: 'ClientConnect'

    def connectionMade(self):
        self.factory.window.protocol = self
        #self.factory.window.plainTextEdit.appendPlainText("Connected")


    def lineReceived(self, line):
        message = line.decode()
        self.factory.window.plainTextEdit.appendPlainText(message)


class ClientConnect (ClientFactory):
    protocol = ClientProtocol
    window: 'MessengerWindow'

    def __init__(self, window):
        self.window = window

class MessengerWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    reactor = None
    protocol: 'ClientProtocol'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        message = self.lineEdit.text()

        self.protocol.sendLine(message.encode())
        self.lineEdit.clear()

app = QtWidgets.QApplication(sys.argv)
import qt5reactor
window = MessengerWindow()
window.show()
qt5reactor.install()
from twisted.internet import reactor
reactor.connectTCP("localhost", 1234, ClientConnect(window))
window.reactor = reactor
reactor.run()