from Teamserver.listeners import BaseListener
from utils.logger import *


class Listener(BaseListener):
    
    def __init__(self):
        log("Working UDO listener", LogLevel.INFO)

    def onLoad(self):
        log("UDP")

    def __dict__(self):
        return {
            'name' : 'UDP',
            'type' : 'Non-Staged',
            'options' : {
                'host' : '',
                'port' : 0,
                'begin' : '',
                'delimiter' : ''
            }
        }