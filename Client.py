# Здесь буду пробовать всё новое, что узнаю
#
# Клиентская часть
# Библиотека Twisted
#

from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor

class ClientProtocol (LineOnlyReceiver):
    factory: 'ClientConnect'

    def connectionMade(self):
        self.sendLine("login:admin".encode())

    def lineReceived(self, line):
        print(line)


class ClientConnect (ClientFactory):
    protocol = ClientProtocol

reactor.connectTCP("localhost", 1234, ClientConnect())
reactor.run()