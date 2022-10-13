''' Raidware imports '''
from email import utils
from listeners import Listener, CallBackHandler, enabled_Listeners
from utils.utils import log_error, log_info

from socket import *
from threading import Thread

class TCP(Listener):

    type = "TCP | Non-Staged"

    def __init__(self, ip_addr="0.0.0.0", port=4444):
        self.ip_addr = ip_addr
        self.port = port

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        try:
            self.sock.bind((ip_addr, port))
        except:
            log_error("([GREEN]TCP[RESET]) Failed to bind to the specified address and port.")
            self.sock = None

    def __repr__(self):
        return f"TCP(Hostname: {self.ip_addr}, Port: {self.port} | {self.type})"

    def __str__(self):
        return self.__repr__()

    def __listen__(self):
        self.sock.listen(5)
        log_info("([GREEN]TCP[RESET]) Listening for incoming connections...")

        enabled_Listeners.append(self)

        while True:
            conn, addr = self.sock.accept()
            log_info(f"([GREEN]TCP[RESET]) Connection from {addr[0]}:{addr[1]}")
            CallBackHandler.connections.append(conn)

    def onLoad(self):
        ''' Spawing a new thread to listen for incoming connections. '''
        Thread(target=self.__listen__,daemon=True).start()

    def onDownload(self):
        pass

    def onUpload(self):
        pass

    def onCommand(self):
        pass

    def onSend(self):
        pass

    def onRecv(self):
        pass