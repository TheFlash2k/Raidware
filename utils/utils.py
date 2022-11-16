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

''' Variable Constants '''
from colorama  import Fore
RAIDWARE = f"{Fore.RED}Raid{Fore.RESET}{Fore.WHITE}ware{Fore.RESET}"
basic_prompt = f"({RAIDWARE})"
prompt = ">>"
prefix = "v1"