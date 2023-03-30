''' Imports '''
from Teamserver.listeners import *
from utils.logger import *
from utils.utils import get_default_config_vars

class Listener(BaseListener):
    name = "UDP"
    type = "Non-Staged"
    LID = "" # Listener ID

    def __init__(self, **kwargs):
        log(f"Initializing {self.name} listener", LogLevel.INFO)
        self.options = get_default_config_vars(name=self.name)

    def onLoad(self):
        log(f"({self.name}) OnLoad function called.")

    def onStop(self):
        log(f"({self.name}) OnStop Function Called")

    def __dict__(self):
        return {
            'LID' : self.LID,
            'name' : self.name,
            'type' : self.type,
            'options' : self.options
        }

    def setopts(self, **kwargs):

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

        return {
            'status' : 'success',
            'msg' : "Updated the values."
        }