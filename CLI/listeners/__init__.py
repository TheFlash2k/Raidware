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

class CallBackHandler:
    connections = [ BaseListener ]

enabled_Listeners = {}