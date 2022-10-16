from abc import abstractmethod

class Listener:

    type : str

    @abstractmethod
    def __color__(self) -> str:
        pass

    @abstractmethod
    def onLoad(self):
        pass

    @abstractmethod
    def onDownload(self):
        pass

    @abstractmethod
    def onUpload(self):
        pass

    @abstractmethod
    def onCommand(self):
        pass

    @abstractmethod
    def onSend(self):
        pass

    @abstractmethod
    def onRecv(self):
        pass

class CallBackHandler:
    connections = [ Listener ]

enabled_Listeners = []