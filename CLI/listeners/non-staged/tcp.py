from Raidware.CLI.listeners import Listener
from socket import *

class TCP(Listener):

    def __init__(self, ip_addr="0.0.0.0", port=4444):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((ip_addr, port))

    def onLoad(self):
        pass

    def onDownload(self):
        pass

    def onUpload(self):
        pass

    def onCommand(self):
        pass