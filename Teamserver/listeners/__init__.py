from abc import abstractmethod
from socket import socket

class BaseListener:

    '''
    Base class for all listeners

    Methods:
        __color__(self) -> str
            This method will return the string output in a colorized format that will be displayed in the console.

        onLoad(self):
            This method will be called when the listener is loaded.
    '''

    type : str

    @abstractmethod
    def __color__(self) -> str:
        pass

    @abstractmethod
    def onLoad(self):
        pass

    @abstractmethod
    def onDownload(self, **kwargs):
        pass

    @abstractmethod
    def onUpload(self, **kwargs):
        pass

    @abstractmethod
    def onCommand(self, **kwargs):
        pass

    @abstractmethod
    def onSend(self, msg : str, **kwargs):
        pass

    @abstractmethod
    def onRecv(self, **kwargs):
        pass

    @abstractmethod
    def setopts(self, **kwargs):
        pass

    @abstractmethod
    def __options__(self):
        pass


class Connection:
    def __init__(self, UID : str, listener = None, _type = None, base = None, OS=None, proc = None, pid = None, pwd = None, user = None):
        self.UID = UID
        self.listener = listener
        self.type = _type
        self.base = base
        self.OS = OS
        self.proc = proc
        self.pid = pid
        self.pwd = pwd
        self.user = user

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return {
            self.UID : {
                'UID' : self.UID,
                'type' : self.type,
                'OS' : self.OS,
                'proc' : self.proc,
                'pid' : self.pid,
                'pwd' : self.pwd,
                'user' : self.user
            }
        }

    def __str__(self):
        return f"{self.UID} | {self.type} | {self.OS} | {self.proc} | {self.pid} | {self.pwd} | {self.user}"

    def __list__(self):
        return [self.UID, self.type, self.OS, self.proc, self.pid,  self.pwd , self.user]

    def send(self, msg : str):
        self.listener.onSend(msg, socket=self.base)

    def recv(self):
        return self.listener.onRecv(socket=self.base)

connections = {}
enabled_Listeners = {}