import json

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
    config = {
        "Raidware_Configuration": {
            "LOG_FILE": "Teamserver/logs/raidware.log",
            "DEBUG" : False
        }
    }

    write_json('Teamserver/config/config.json', config)
    
def create_listeners_config():
    listeners = {
        "Listeners" : { "tcp" : {  "Common" : {   "description" : "TCP Listener",   "config" : {    "host" : "0.0.0.0",    "port" : 9001,    "ssl" : False,    "begin-delimiter" : "|RAIDWARE-SoM|",    "end-delimiter" :  "|RAIDWARE-EoM|"   }  }, "Non-Staged" : {   "path" : "listeners/staged/tcp.py"  },  "Staged" : {   "path" : "listeners/staged/tcp.py",   "payload_size" : None,   "payload_type" : "staged",   "arch" : "x64"  } }, "udp" : {  "Common" : {   "description" : "UDP Listener",    "config" : {     "host" : "0.0.0.0",     "port" : 9001,     "ssl" : False,     "begin-delimiter" : "|RAIDWARE-SoM|",     "end-delimiter" :  "|RAIDWARE-EoM|"    }  },  "Non-Staged" : {   "path" : "listeners/staged/udp.py"  },  "Staged" : {   "status" : "UNIMPLEMENTED"  } }}
    }
    
    write_json('Teamserver/config/listeners.json', listeners)


def create_agents_config():
    agents = {
        "Agents" : {
            "Linux" : ["tcp", "udp", "http"],
            "Windows" : ["tcp", "udp", "http", "https", "DNS"],
            "MacOS" : ["tcp", "http"]
        }
    }
    write_json('Teamserver/config/agents.json', agents)


def get_default_config_vars(name : str):
    with open('Teamserver/config/listeners.json', 'r') as f:
        data  = json.load(f)

    return data['Listeners'][name.lower()]['Common']['config']

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
            'message' : f"Field '{field}' not specified"
        }

    if type(ret) != _type:
        return {
            'status' : 'error',
            'message' : f"Field '{field}' must be of type {_type}"
        }
    
    return ret

def validate_sub_fields(data, listener):
    base_keys = list(data['Common']['config'].keys())
    passed_keys = list(listener['config'].keys())
    
    ''' Verifying if the fields match '''
    for item in list(passed_keys):

        if item not in base_keys:
            return {
                'status' : 'error',
                'message' : f'Invalid key "{item}" provided in the CONFIG field.'
            }


    ''' Verifying if the fields are empty '''
    for item in list(passed_keys):
        if not listener['config'][item]:
            return {
                'status' : 'error',
                'message' : f'Field "{item}" cannot be empty'
            }

    ''' Verifying if the fields are of the correct type '''
    for item in list(passed_keys):
        if type(listener['config'][item]) != type(data['Common']['config'][item]):
            return {
                'status' : 'error',
                'message' : f'Field "{item}" must be of type {type(data["Common"]["config"][item])}'
            }

    ''' Checking if port is in passed_keys and if the port specified is in used_ports '''
    if 'port' in passed_keys:
        port = listener['config']['port']
        if type(port) != int:
            return {
                'status' : 'error',
                'message' : "Field 'port' must be an integer"
            }

        if port <= 1 or port > 65535:
            return {
                'status' : 'error',
                'message' : "Field 'port' must be between 1 and 65535"
            }

        if port in used_ports:
            _ = get_listener_by_port(port)
            if _ == None:
                used_ports.remove(port)
                return {
                    'status' : 'error',
                    'message' : "An error had occurred. Please retry."
                }
            
            return {
                'status' : 'error',
                'message' : f"Port '{port}' is already in use by the Listener {_.LID}({_.name})"
            }

        used_ports.append(port)


''' Variable Constants '''
from colorama  import Fore
RAIDWARE = f"{Fore.RED}Raid{Fore.RESET}{Fore.WHITE}ware{Fore.RESET}"
basic_prompt = f"({RAIDWARE})"
prompt = ">>"
prefix = "v1"


''' Variables '''
used_ports = []
enabled_listeners  = []
agents     = []
