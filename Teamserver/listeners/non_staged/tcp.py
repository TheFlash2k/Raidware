''' Imports '''
from Teamserver.listeners import *

class Listener(BaseListener):
    type = "tcp"

    def __init__(self, **kwargs):
        self.options = {
            'host' : '',
            'port' : 0,
            'begin' : '',
            'delimiter' : ''
        }

        self.setopts(**kwargs)

    