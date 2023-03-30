import json
import ctypes
from .logger import log

def terminate_thread(thread):
    try:
        if not thread.isAlive():
            return
    except:
        pass

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def json_fetch(file_name : str, field : str):
    with open(file_name, 'r') as f:
        data = json.load(f)
        return data[field]

def write_json(file_name : str, content : dict):
    with open(file_name, 'w') as f:
        json.dump(content, f, indent=4)

def is_admin():
    import ctypes, os
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


''' This method will generate a random string with length specified by the _len parameter '''
def get_random_string(_len = 25):
    import string
    import random
    includes = string.ascii_letters + string.digits
    return ''.join(random.choice(includes) for i in range(_len))

''' Methods that will write the default config files if they don't exist '''
def create_config():
    config = {"Raidware_Configuration" :{"LOG_FILE" : "logs/raidware.log","DEBUG" : True ,"SECRET_KEY" : "r@1dw@r3_d3faul7_k3y"},"Listeners" : [{"name" : "tcp","description" : "TCP Listener","config" : {"host" : "0.0.0.0","port" : 9001,"ssl" : False,"begin-delimiter" : "|RAIDWARE-SoM|","end-delimiter" :  "|RAIDWARE-EoM|"},"types" : ["Non-Staged", "Staged"], "details" : {"Non-Staged" : {"path" : "Teamserver/listeners/staged/tcp.py","arch" : ["x86", "x64"]},"Staged" : {"path" : "Teamserver/listeners/staged/tcp.py","payload_size" : None,"arch" : ["x86", "x64"]}}},{"name" : "udp","description" : "UDP Listener","config" : {"host" : "0.0.0.0","port" : 9001,"ssl" : False,"begin-delimiter" : "|RAIDWARE-SoM|","end-delimiter" :  "|RAIDWARE-EoM|"},"types" : ["Non-Staged", "Staged"],"details" : {"Non-Staged" : {"path" : "Teamserver/listeners/staged/udp.py"},"Staged" : {"status" : "UNIMPLEMENTED"}}}],"Agents" : {"Linux" : ["tcp","udp","http"],"Windows" : ["tcp","udp","http","https","DNS"],"MacOS" : ["tcp","http"]}}
    write_json('config.json', config)

def get_default_config_vars(name : str):
    with open('config.json', 'r') as f:
        data  = json.load(f)

    try:
        ## Fetch the index from the list where the name matches
        index = -1
        for i in range(len(data['Listeners'])):
            if data['Listeners'][i]['name'] == name.lower():
                index = i
                break
        if index == -1:
            return None
        return data['Listeners'][index]['config']
    except:
        return None

def get_listener_by_port(port : int):
    for listener in enabled_listeners:
        if listener.options['port'] == port:
            return listener

    return None

def validate_listener(listener : dict, _type : type, field : str, str_type : str):
    try:
        ret = listener[field]
    except:
        return {
            'status' : 'error',
            'msg' : f"Field '{field}' not specified"
        }

    if type(ret) != _type:
        return {
            'status' : 'error',
            'msg' : f"Field '{field}' must be of type {_type}"
        }
    
    return ret

def validate_sub_fields(data, listener):

    base_keys = list(data['config'].keys())
    passed_keys = list(listener['config'].keys())
    

    log(f"Raw Data: {data}")
    log(f"Base Keys: {base_keys}")
    log(f"Pass Keys: {passed_keys}")

    ''' Verifying if the fields match '''
    for item in list(passed_keys):
        if item not in base_keys:
            return {
                'status' : 'error',
                'msg' : f'Invalid key "{item}" provided in the CONFIG field.'
            }

    ''' Verifying if the fields are empty '''
    for item in list(passed_keys):
        if not listener['config'][item]:
            return {
                'status' : 'error',
                'msg' : f'Field "{item}" cannot be empty'
            }

    ''' Verifying if the fields are of the correct type '''
    for item in list(passed_keys):
        if type(listener['config'][item]) != type(data['config'][item]):
            return {
                'status' : 'error',
                'msg' : f'Field "{item}" must be of type {type(data["config"][item])}'
            }

    ''' Checking if port is in passed_keys and if the port specified is in used_ports '''
    if 'port' in passed_keys:
        log("Port is in passed_keys")
        port = listener['config']['port']
        if type(port) != int:
            return {
                'status' : 'error',
                'msg' : "Field 'port' must be an integer"
            }

        if port <= 1 or port > 65535:
            return {
                'status' : 'error',
                'msg' : "Field 'port' must be between 1 and 65535"
            }

        if port in used_ports.keys():
            _ = get_listener_by_port(port)
            if _ == None:
                used_ports.pop(port)
                return {
                    'status' : 'error',
                    'msg' : "An error had occurred. Please retry."
                }
            
            return {
                'status' : 'error',
                'msg' : f"Port '{port}' is already in use by the Listener {_.LID}({_.name})"
            }

        # used_ports[port] = _.LID

def check_utils():
    import shutil
    from utils.logger import log_error, log

    cmds = (
        "csc",
        "x86_64-w64-mingw32-g++",
        "x86_64-w64-mingw32-gcc",
    )

    log("Checking for required utilities...")
    for cmd in cmds:
        msg = f"Checking for '{cmd}' "
        log(f"{msg}\r", end='')
        if not shutil.which(cmd):
            log_error(f"Command '{cmd}' not found. Please install it and try again.")
            return False
        log(f"{msg} - Found")

    return True

def get_config_variable(var : str):
    with open('config.json') as f:
        data = json.load(f)
    var = var.split('.')
    for i in range(len(var)):
        data = data[var[i]]
    return data

''' Variable Constants '''
from colorama  import Fore
RAIDWARE = f"{Fore.RED}Raid{Fore.RESET}{Fore.WHITE}ware{Fore.RESET}"
basic_prompt = f"({RAIDWARE})"
prompt = ">>"
prefix = "v1"

''' Variables '''
used_ports = {  }
enabled_listeners  = []
agents     = []
