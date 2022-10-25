from abc import abstractmethod
from socket import socket

class BaseListener:

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
    def onRecv(self, **kwargs) -> str:
        pass

    @abstractmethod
    def setopts(self, **kwargs):
        pass

    @abstractmethod
    def __options__(self):
        pass


class Connection:
    def __init__(self, UID : str, listener = None, _type = None, base = None):
        self.UID = UID
        self.listener = listener
        self.type = _type
        self.base = base

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.UID} | {self.type}"

    def __list__(self):
        return [self.UID, self.type, self.base.__str__()]

    def send(self, msg : str):
        self.listener.onSend(msg, socket=self.base)

    def recv(self):
        return self.listener.onRecv(socket=self.base)

connections = {}
enabled_Listeners = {}