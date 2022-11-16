''' This will initialize all the raidware modules '''
from utils.utils import *
from utils.crypto import quick_crypt, quick_decrypt
from utils.logger import log, LogLevel
from Teamserver.db.actions import get_user

import os
from datetime import datetime

team_password = None

def generate_token(username : str):
    ''' Getting the secret key from config '''
    
    return quick_crypt(f"{username}|{get_team_password()}|{datetime.today().strftime('%d-%m-%y')}")

def decrypt_token(token : str):
    ''' url decode the token '''
    from urllib.parse import unquote
    token = unquote(token)
    return quick_decrypt(token)

def check_token(token : str):

    ''' url decode the token '''
    from urllib.parse import unquote
    token = unquote(token)

    ''' Check if the token is valid '''
    
    try:
        decrypted = quick_decrypt(token)
        if decrypted == None:
            return False
        
        uname, team_password, date = decrypted.split("|")

        if not get_user(uname):
            return False

        if team_password != get_team_password():
            return False
        
        ''' Check if a day has been passed, the token will not work '''
        curr = datetime.today().strftime('%d-%m-%y')
        if curr > date:
            return False

        return True
    except Exception as E:
        print(f"Exception: {E}")
        return False

def get_team_password():
    global team_password
    if not team_password:
        team_password = get_random_string(50)
    return team_password

def init():
    log("Initializing Raidware", LogLevel.INFO)

    ''' Check if we're running as admin, if we're not, prompt the user '''
    log("Checking if we're admin", LogLevel.DEBUG)
    if not is_admin():
        log("Raidware Teamserver must be run as admin", LogLevel.ERROR)
        exit(1)
    else:
        log("Admin check passed", LogLevel.DEBUG)

    ''' Check if the config file exists, if it doesn't, create it '''
    log("Checking if config file exists", LogLevel.DEBUG)
    if not os.path.exists("Teamserver/config/config.json"):
        log("Config file doesn't exist. Creating with defaults.", LogLevel.WARN)
        create_config()
    else:
        log("Config file exists", LogLevel.DEBUG)

    ''' Check if the listeners file exists, if it doesn't, create it '''
    log("Checking if listeners file exists", LogLevel.DEBUG)
    if not os.path.exists("Teamserver/config/listeners.json"):
        log("Listeners config file doesn't exist. Creating with defaults.", LogLevel.WARN)
        create_listeners_config()
    else:
        log("Listeners config file exists", LogLevel.DEBUG)

    ''' Check if the agents file exists, if it doesn't, create it '''
    log("Checking if agents file exists", LogLevel.DEBUG)
    if not os.path.exists("Teamserver/config/agents.json"):
        log("Agents config file doesn't exist. Creating with defaults.", LogLevel.WARN)
        create_agents_config()
    else:
        log("Agents config file exists", LogLevel.DEBUG)

    ''' Check if the database exists '''
    log("Checking if database exists", LogLevel.DEBUG)
    from .db.init_db import initialize
    initialize()

    log("Initialized Raidware", LogLevel.INFO)

def get_listeners():
    return json_fetch("Teamserver/config/listeners.json", "Listeners")

def get_agents():
    return json_fetch("Teamserver/config/agents.json", "Agents")

def check_listener(listener : dict):
    listener_name = listener['name']
    listeners = get_listeners()
    for item in listeners.keys():
        if item.lower() == listener_name.lower():
            return True

    return False

def prepare_listener(listener : dict):

    if not check_listener(listener):
        return None

    listener_name = listener['name'].lower()
    data = get_listeners()[listener_name]

    base_keys = list(data['Common']['config'].keys())
    passed_keys = list(listener['config'].keys())
    

    ''' Verifying if the fields match '''
    for item in passed_keys:
        if item not in base_keys:
            return {
                'status' : 'error',
                'message' : f'Invalid key "{item}" provided'
            }

    ''' Preparing the listener '''
    