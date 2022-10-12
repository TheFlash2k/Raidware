''' Raidware imports '''
from email import utils
from Raidware.CLI.listeners import Listener, CallBackHandler
from Raidware.CLI.utils import utils

from socket import *
from threading import Thread

class TCP(Listener):

    def __init__(self, ip_addr="0.0.0.0", port=4444):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            self.sock.bind((ip_addr, port))
        except:
            utils.log_error("([GREEN]TCP[RESET]) Failed to bind to the specified address and port.")

    def __listen__(self):
        self.sock.listen(5)
        utils.log_info("([GREEN]TCP[RESET]) Listening for incoming connections...")
        while True:
            conn, addr = self.sock.accept()
            utils.log_info(f"([GREEN]TCP[RESET]) Connection from {addr[0]}:{addr[1]}")
            CallBackHandler.connections.append(conn)

    def onLoad(self):
        ''' Spawing a new thread to listen for incoming connections. '''
        # Create a new thread
        Thread(target=self.__listen__).start()

    def onDownload(self):
        pass

    def onUpload(self):
        pass

    def onCommand(self):
        ## All the command parsing goes here.
        
        pass