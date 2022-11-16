''' Imports '''
from Teamserver.listeners import *
from utils.logger import *

class Listener(BaseListener):
    type = "Non-Staged"

    def __init__(self, **kwargs):
        log("Initializing TCP listener", LogLevel=LogLevel.INFO)
        self.options = {
            'host' : '',
            'port' : 0,
            'begin' : '',
            'delimiter' : ''
        }

        self.setopts(**kwargs)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.thread = None


    def __repr__(self):
        return f"TCP(Hostname: {self.options['host']}, Port: {self.options['port']} | {self.type})"

    def __color__(self):
        return f"[GREEN]TCP[RESET]([MAGENTA]Hostname:[RESET][BLUE] {self.options['host']}[RESET], [MAGENTA]Port[RESET]: [CYAN]{self.options['port']}[RESET], [MAGENTA]Type: [YELLOW]{self.type.split(' | ')[0]}[RESET] -- [GREEN]{self.type}[RESET])"

    def __str__(self):
        return self.__repr__()
    
    def __listen__(self):
        log("Starting listener", LogLevel=LogLevel.INFO)
        self.sock.bind((self.options['host'], self.options['port']))
        self.sock.listen()
        log("Listening for connections", LogLevel=LogLevel.INFO)
        while True:
            conn, addr = self.sock.accept()
            log(f"Connection from {addr}", LogLevel=LogLevel.INFO)
            self.onSend(self.options['begin'], socket=conn)
            data = conn.recv(1024).decode()
            if data == self.options['delimiter']:
                log("Connection verified", LogLevel=LogLevel.INFO)
                self.onConnect(conn, addr)
            else:
                log("Connection failed", LogLevel=LogLevel.INFO)
                conn.close()