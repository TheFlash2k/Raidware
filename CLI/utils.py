import requests
from time import sleep

from .methods import INFO
from .vars import *
from utils.logger import log, LogLevel

def parse_input(prompt : str):
    _input = input(prompt)

    if _input == "" or _input == None:
        return

    _input = _input.strip()
    cmds = _input.split()
    
    if cmds[0].upper() not in INFO.keys():
        log(f"Invalid Command", LogLevel.ERROR)
        return
    
    INFO[cmds[0].upper()][1](cmds[1:] if len(cmds) > 1 else None)
    print()

def base_request(endpoint, method='GET', body={}):
    methods = {
        'GET' : requests.get,
        'POST' : requests.put,
        'DELETE' : requests.delete,
        'PUT' : requests.put
    }

    method = method.upper()
    if method not in methods.keys():
        log(f"Cannot make request of method {method}!", LogLevel.ERROR)
        return
    
    r = methods[method](
        url = f"{Globals.base_url}{endpoint}",
        headers={
            'Content-Type' : 'application/json',
            'Authorization': f"Bearer {Globals.access_token}"
        },
        json=body
    )
    return r
    
def prompt_updater(_self=True):
    try:
        while True:
            Globals.enabled_listeners = base_request('/enabled').json()['listeners']
            sess = base_request('/sessions').json()['sessions']
            if len(sess) > len(Globals.sessions) and not Globals.new_spawn:
                log("A new sessions has been received!", LogLevel.CONNECTIONS)
            Globals.sessions = sess
            Globals.new_spawn = False
            if not _self:
                break
            sleep(Config.SLEEP_TIME)
    except Exception as E:
        log(f"An error occurred while fetching information for prompt. Error: {E.__repr__()}", LogLevel.ERROR)
        if not _self:
            return
        sleep(Config.SLEEP_TIME)

