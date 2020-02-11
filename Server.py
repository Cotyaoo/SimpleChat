# Серверная часть
# Библиотека Twisted
#

from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.internet import reactor
import time

class Protocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None

    def lineReceived(self, line: bytes):
        content = line.decode()

        if self.login is not None:
            content = f"Message from {self.login}: {content}"

            for user in self.factory.clients:
                user.sendLine(content.encode())
        else:
            if content.startswith("login:"):
                login = content.replace("login:", "")
                for user in self.factory.clients:
                    if user.login == login:
                        self.sendLine("Login exists already".encode())
                        return

                self.login = login
                self.sendLine("Welcome".encode())

            else:
                self.sendLine("Invalid login".encode())

    def connectionMade(self):
        print(f"Connection made")
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)


class Server(ServerFactory):
    protocol = Protocol
    clients: list

    def startFactory(self):
        self.clients = []
        print("Server started...")

    def stopFactory(self):
        print("Server stoped...")


reactor.listenTCP(1234, Server())
reactor.run()
