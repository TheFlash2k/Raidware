from .db import __init__ as db_init
from .db.actions import get_user
from utils.logger import *
from utils.utils import *

import os
from datetime import datetime

team_password = None

def get_team_password():
    global team_password
    if not team_password:
        team_password = get_random_string(50)
    return team_password

def init():
    log("Initializing Raidware", LogLevel.INFO)

    log("Checking if we're admin", LogLevel.DEBUG)
    # if not is_admin():
    #     log("Raidware Teamserver must be run as admin", LogLevel.ERROR)
    #     exit(1)
    # else:
    #     log("Admin check passed", LogLevel.DEBUG)


    log("Checking if config file exists", LogLevel.DEBUG)
    if not os.path.exists("config.json"):
        log("Config file doesn't exist. Creating with defaults.", LogLevel.WARN)
        create_config()
    else:
        log("Config file exists", LogLevel.DEBUG)

    ''' Check if the database exists '''
    log("Checking if database exists", LogLevel.DEBUG)
    db_init()

    ''' Checking if the required utilites are installed '''
    log("Checking if required utilities are installed", LogLevel.DEBUG)
    # from utils.utils import check_utils
    # if not check_utils():
    #     log("Required utilities are not installed", LogLevel.ERROR)
    #     exit(1)

    log("Initialized Raidware", LogLevel.INFO)

def get_listeners():
    return json_fetch("config.json", "Listeners")

def get_agents():
    return json_fetch("config.json", "Agents")

def check_listener(listener : dict):
    try:
        listener_name = listener['name']
    except:
        return False
    listeners = get_listeners()
    for item in listeners:
        if item['name'] == listener_name.lower():
            return True
    return False

def prepare_listener(listener : dict):

    if not check_listener(listener):
        return {
            "status" : "error",
            "message" : "Listener doesn't exist"
        }

    log("Validating....")

    ''' Validate the field NAME '''
    ret = validate_listener(listener=listener, _type=str, field='name', str_type="string")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret, 400
        except:
            pass
    
    listener_name = ret.lower()

    ''' Validate the field TYPE '''
    ret = validate_listener(listener=listener, _type=str, field='type', str_type="string")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret, 400
        except:
            pass

    listener_type = ret.lower().replace('-', '_')

    listener_types = [
        "staged",
        "non_staged",
        "addons"
    ]

    if listener_type not in listener_types:
        return {
            'status' : 'error',
            'message' : f"Field 'type' must be one of these: {listener_types}"
        }, 400

    ''' Validating the field Config '''
    ret = validate_listener(listener=listener, _type=dict, field='config', str_type="Dictionary")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret, 400
        except:
            pass

    listener_config = ret
    try:
        data = get_listeners()

        index = -1
        for i in range(len(data)):
            if data[i]['name'] == listener_name.lower():
                index = i
                break

        if index == -1:
            return {
                'status' : 'error',
                'message' : "Listener doesn't exist"
            }, 404

        data = data[index]
    except:
        return {
            'status' : 'error',
            'message' : "Listener doesn't exist"
        }, 404

    log("Validating sub fields")
    _vsf = validate_sub_fields(data=data, listener=listener)
    if type(_vsf) == dict:
        if _vsf['status'] == 'error':
            return _vsf

    ''' Preparing the listener '''
    module = f"Teamserver.listeners.{listener_type}.{listener_name}"
    from importlib import import_module
    listener_module = import_module(module)

    log(f"Imported Module: {listener_module}")
    try:
        obj = listener_module.Listener()
    except Exception as E:
        print(f"Error: {E}")

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
                return ret, 400
        except:
            pass

    ''' Checking if config field is specified'''
    ret = validate_listener(listener=listener, _type=dict, field='config', str_type="Dictionary")
    if type(ret) == dict:
        try:
            if ret['status'] == 'error':
                return ret, 400
        except:
            pass

    ''' We now have the listener id'''
    try:
        listener = [i for i in enabled_listeners if i.LID == listener.get('LID')][0]
    except:
        return {
            'status': 'error',
            'message': 'Invalid LID Specified. Listener doesn\'t exist'
        }, 404

    ''' Updating the listener '''
    if not listener:
        return {
            'status': 'error',
            'message': 'Failed to update listener'
        }, 400

    if listener.status.lower().strip() == 'running':
        return {
            'status': 'error',
            'message': 'Listener is already running. Cannot Update it.'
        }, 400

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
        }, 201

    _pop = []
    for k in listener_config.keys():
        if k not in old_config.keys():
            _pop.append(k)

    for k in _pop:
        listener_config.pop(k)

    if listener_config == {} or listener_config == old_config:
        return {
            'status': 'warning',
            'message': 'No changes were made to the listener'
        }, 201
    
    ''' Check if the port key exists and is a valid port '''
    if 'port' in listener_config.keys():
        if type(listener_config['port']) != int:
            return {
                'status': 'error',
                'message': 'Port must be an integer'
            }, 400

        if listener_config['port'] < 1 or listener_config['port'] > 65535:
            return {
                'status': 'error',
                'message': 'Port must be between 1 and 65535'
            }, 400

    log(f"Listener Config: {listener_config}")
    ''' Updating the listener with the configuration variables provided '''
    out = listener.setopts(**listener_config)

    if out['status'] == 'error':
        return out, 400

    return {
        'status' : 'success',
        'message' : 'Listener updated successfully',
        'from' : old_diff,
        'to' : listener_config
    }
    