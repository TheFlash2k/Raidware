from abc import abstractmethod

class Listener:

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
    