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
    try:
        listener_name = listener['name']
    except:
        return False

    listeners = get_listeners()
    for item in listeners.keys():
        if item.lower() == listener_name.lower():
            return True

    return False

def prepare_listener(listener : dict):

    if not check_listener(listener):
        return {
            "status" : "error",
            "message" : "Listener doesn't exist"
        }

    ''' Validate the field NAME '''
    ret = validate_listener(listener=listener, _type=str, field='name', str_type="string")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret
        except:
            pass

    listener_name = ret.lower()

    ''' Validate the field TYPE '''
    ret = validate_listener(listener=listener, _type=str, field='type', str_type="string")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret
        except:
            pass

    listener_type = ret.lower().replace('-', '_')

    if listener_type != "staged" and listener_type != "non_staged":
        return {
            'status' : 'error',
            'message' : "Field 'type' must be either 'staged' or 'non_staged'"
        }

    ''' Validating the field Config '''
    ret = validate_listener(listener=listener, _type=dict, field='config', str_type="Dictionary")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret
        except:
            pass

    listener_config = ret

    data = get_listeners()[listener_name]

    _vsf = validate_sub_fields(data=data, listener=listener)
    if type(_vsf) == dict:
        if _vsf['status'] == 'error':
            return _vsf

    ''' Preparing the listener '''
    module = f"Teamserver.listeners.{listener_type}.{listener_name}"
    from importlib import import_module
    listener_module = import_module(module)
    obj = listener_module.Listener()

    ''' Updating the listener with the configuration variables provided '''
    out = obj.setopts(**listener_config)

    ''' Checking if the listener is already running '''
    if out['status'] == 'error':
        return out

    obj.LID = get_random_string()
    enabled_listeners.append(obj)

    return {
        'status' : 'success',
        'message' : 'Listener prepared successfully',
        'listener' : obj.__dict__()
    }

def update_listener(listener : dict):
    
    ret = validate_listener(listener=listener, _type=str, field='LID', str_type="string")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret
        except:
            pass

    ''' Checking if config field is specified'''
    ret = validate_listener(listener=listener, _type=dict, field='config', str_type="Dictionary")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret
        except:
            pass

    ''' We now have the listener id'''
    try:
        listener = [i for i in enabled_listeners if i.LID == listener.get('LID')][0]
    except:
        return {
            'status': 'error',
            'message': 'Invalid LID Specified. Listener doesn\'t exist'
        }

    ''' Updating the listener '''
    if not listener:
        return {
            'status': 'error',
            'message': 'Failed to update listener'
        }

    if listener.status.lower().strip() == 'running':
        return {
            'status': 'error',
            'message': 'Listener is already running. Cannot Update it.'
        }

    listener_config = ret
    old_config = listener.options

    ''' Creating two dictionaries, one with the old config and one with the new config '''
    old_diff = {}

    for k, v in old_config.items():
        try:
            if listener_config[k] != v:
                old_diff[k] = v
        except KeyError:
            continue

    if old_diff == {}:
        return {
            'status': 'warning',
            'message': 'No changes were made to the listener'
        }

    _pop = []
    for k in listener_config.keys():
        if k not in old_config.keys():
            _pop.append(k)

    for k in _pop:
        listener_config.pop(k)

    ''' Updating the listener with the configuration variables provided '''
    out = listener.setopts(**listener_config)

    if out['status'] == 'error':
        return out

    return {
        'status' : 'success',
        'message' : 'Listener updated successfully',
        'from' : old_diff,
        'to' : listener_config
    }
    