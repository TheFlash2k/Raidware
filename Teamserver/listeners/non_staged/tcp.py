''' Imports '''
from Teamserver.listeners import *
from utils.logger import *
from utils.utils import *
from utils.crypto import decrypt, encrypt


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
        global used_ports
        # check if 'name' is in kwargs
        self.listener_name = kwargs['name'] if 'name' in kwargs.keys() else "tcp-" + get_random_string(6)
        log(f"Data: {kwargs['data']}")
        self.curr_port = None

        self.options = {}
        if 'data' in kwargs.keys():
            self.options = kwargs['data']
        log("Initializing TCP listener", LogLevel.INFO)

        ''' Checking if the port is already being used: '''
        log(f"Options: {self.options}")
        try:
            port = self.options.get('port', None)
        except Exception as E:
            log_error(f"Exception: {E}")
            port = None

        log(f"Passed Port: {port}")
        log(f"Used Ports: {used_ports}")
        if port:
            if port not in used_ports.keys():
                update_used_ports(port, self.name)
                self.curr_port = port
            else:
                ret_msg = f"Port {self.curr_port} is already being used by {used_ports[self.curr_port]}"
                log(ret_msg, LogLevel.ERROR)
                raise Exception(ret_msg)

    def __listen__(self):
    
        def __verify__(conn : socket):
            print()
            log("A connection has been received. Verifying the connection...")
            uid = get_random_string()
            self.onSend(uid, socket=conn)
            recv = self.onRecv(socket=conn).split('|')
            try:
                return (recv[0] == "RAIDWARE_INIT"), recv[1], uid, recv[2], recv[3], recv[4], recv[5], recv[6]
            except:
                return None
            
        if not self.bind:
            try:
                self.sock.bind((self.options['host'], self.options['port']))
                self.bind = 1
            except Exception as E:
                log_error(f"Exception: {E}")
                log_error(f"([GREEN]{self.listener_name}[RESET]) Failed to bind to the specified address and port.")
                self.sock = None

        if self.sock == None:
            log(f"([GREEN]{self.listener_name}[RESET]) An error had occurred when creating the socket for listener. Please check...", LogLevel.ERROR)
            return

        self.sock.listen()
        log(f"([GREEN]{self.listener_name}[RESET]) Listening on [CYAN]{self.options['host']}[RESET]:[CYAN]{self.options['port']}[RESET]", LogLevel.INFO)

        while True:
            conn, addr = self.sock.accept()

            ''' Verifying the received connection... '''
            try:
                ret = __verify__(conn)
            except:
                try:
                    ret = __verify__(conn)
                except Exception as E:
                    print("Exception: ", E)
                    log_error("Connection was received but we were unable to validate if it was our own.")
                continue

            if not ret:
                log_error("Connection was received but we were unable to validate if it was our own.")
                continue

            if not ret[0]:
                log_error("Connection was received but we were unable to validate if it was our own.")
                continue

            connections[ret[2]] = Connection(name=self.listener_name, UID=ret[2], listener=self, _type=self.type, base=conn, OS=ret[1], proc = ret[3], pid = ret[4], pwd = ret[5], user = ret[6], ip=ret[7])
            log(f"([GREEN]{self.listener_name}[RESET]) Connection with UID [CYAN]{ret[2]}[RESET] has been established.", LogLevel.CONNECTIONS)

    def onLoad(self):
        try:
            self.thread = Thread(target=self.__listen__, daemon=True)
            self.thread.start()
        except:
            pass

    def onStop(self):
        terminate_thread(self.thread)

    def __dict__(self):
        return {
            'LID' : self.LID,
            'name' : self.listener_name,
            'protocol' : self.name,
            'type' : f"{self.name}|{self.type}",
            'status' : self.status,
            'options' : self.options
        }

    def setopts(self, **kwargs):
        global used_ports
        ''' Check if all the keys in kwargs match the keys in self.options '''
        for item in kwargs.keys():
            if item not in self.options.keys():
                return {
                    'status' : 'error',
                    'msg' : f'Invalid key "{item}" provided'
                }


        ''' Setting the values '''
        for k, v in kwargs.items():
            self.options[k] = v

        ''' Checking if the port value is being updated: '''
        if 'port' in kwargs.keys():
            _port = kwargs['port']
            # Firstly check if the port is already being used by another listener:
            if _port in used_ports.keys():
                if used_ports[_port] != "" and used_ports[_port] != self.name:
                    ret_msg = f"Port {_port} is already being used by {used_ports[_port]}"
                    log(ret_msg, LogLevel.ERROR)
                    return {
                        'status' : 'error',
                        'msg' : ret_msg
                    }
                else:
                    if self.curr_port != _port:
                        used_ports[_port] = self.name
                        try:
                            used_ports.pop(self.curr_port)
                        except:
                            pass
                        self.curr_port = _port
                    else:
                        pass

        return {
            'status' : 'success',
            'msg' : "Updated the values."
        }

    def onSend(self, msg : str, **kwargs):
        socket = self.sock if 'socket' not in kwargs.keys() else kwargs['socket']

        msg = self.options['begin_delimiter'] + "{" + msg + "}" + self.options['end_delimiter']
        try:
            socket.send(encrypt(self.options['encryption-key'], msg.encode()))
        except ConnectionResetError:
            log_error(f"Connection lost...")
            return "Connection Lost"

    def onRecv(self, **kwargs):

        socket = self.sock if 'socket' not in kwargs.keys() else kwargs['socket']
        try:
            buf = socket.recv(1024).decode()
            buf = decrypt(self.options['encryption-key'], buf)

            # First buf will be the number of chunks in the output:
            if buf == "":
                return ""
            log(f"Buffer: {buf}")
            try:
                __len = int(buf)
                buf = ""
                for _ in range(__len):
                    __locl = socket.recv(1024).decode()
                    buf += __locl
                buf = buf.split('|')
                __f_buffer = []
                for i in buf:
                    if i == "":
                        continue
                    _ = decrypt(self.options['encryption-key'], i)
                    __f_buffer.append(_)

                buf = "".join(__f_buffer)
            except Exception as E:
                log(f"An error occurred when parsing data from the socket. Returning the raw data. {E.__str()}", LogLevel.ERROR)
                return E.__str__()

        except ConnectionResetError:
            log_error(f"Connection lost...")
            return "Connection Lost"
        
        try:
            buf = buf.split(self.options['begin_delimiter'])[1].split(self.options['end_delimiter'])[0][1:]
        except:
            log_error(f"Unable to parse the received data ({buf}). Returning the raw data...")
            return buf
        return buf[:-1]