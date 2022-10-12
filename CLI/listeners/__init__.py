from abc import abstractmethod

class Listener:

    type : str

    @abstractmethod
    def onLoad(self):
        pass

    @abstractmethod
    def onDownload(self):
        pass

    @abstractmethod
    def onUpload(self):
        pass

    def onCommand(self):
        pass


class CallBackHandler:
    connections = [ Listener ]