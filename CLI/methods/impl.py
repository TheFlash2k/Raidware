from os import system, name
from colorama import Fore
import json
from tabulate import tabulate
import sys

from CLI.listeners import connections
from CLI.methods.verify import *
from CLI.methods.interact import _interact


def CLEAR(*args):
    from os import system, name
    system("cls" if name == "nt" else "clear")
    
def EXIT(*args):
    utils.exit_valid()
    
def VERSION(*args):
    try:
        with open('version.conf', 'r') as f:
            version = f.read()
    except:
        version = "<unknown>"

    print(f"{Fore.RED}Raid{Fore.RESET}Ware - A {Fore.RED}C2{Fore.RESET} Framework -- {Fore.GREEN}{version}{Fore.RESET}")

def GENERATE(*args):
    if args[0] == None:
        from utils.utils import basic_prompt, prompt
        prompt = (f"{basic_prompt} [{Fore.GREEN}GENERATE{Fore.RESET}] {prompt} ")
        while True:
            _ret = generate( input(prompt) )
            if not _ret:
                continue
            elif _ret:
                break
            
    else:
        # Checking if valid arguments have been passed.
        pass

    pass

def SESSIONS(*args):

    headers = ['UID', 'TYPE', 'OS', 'Process', 'PID', 'CWD', 'Logged In As']
    data = []

    if len(connections) != 0:
        for item in connections.values():
            data.append(item.__list__())

        print(
            "\n",
            tabulate(
                data,
                headers=headers,
            ),
            "\n"
        )
    else:
        from colorama import Fore
        print(f"[{Fore.RED}-{Fore.RESET}] No sessions have been received yet.")

def json_print(file, field, headers):
    with open(file) as f:
        data = json.load(f)[field]

    print(
        "\n",
        tabulate(
            data,
            headers=headers,
        ),
        "\n"
    )

def INTERACT(*args):

    def help():
        print("Usage: INTERACT <UID>")

    def err(msg : str = None, only_err : bool = False):
        if msg != None:
            utils.log_error(msg)
        if not only_err:
            help()

    if len(connections) <= 0:
        err("No sessions have been received yet.", only_err = True)
        return

    if args[0] == None:
        err("No session UID specified!")
        return
        
    data = args[0][0]
    if data.lower() == "help" or data.lower() == "-h" or data.lower() == "--help":
        err()
        return
    
    if data not in connections.keys():
        ''' Checking if an index has been provided '''
        try:
            data = int(data)
        except ValueError:
            err("Invalid session UID specified. Please type \"SESSIONS\" to check the UID of all the available sessions.", only_err=True)
            return
        
        ''' Checking if the index is valid '''
        if data > len(connections) or data < 0:
            err("Invalid session UID specified. Please type \"SESSIONS\" to check the UID of all the available sessions.", only_err=True)
            return

        ''' Getting the UID of the session '''
        data = list(connections.keys())[data]

    _interact(connections[data])

def AGENTS(*args):
    file_name = "CLI/agents/agents.json"
    utils.log_info("Available AGENTS are: ")
    json_print(file_name, "AGENTS", ["Linux", "Windows", "MacOS"])
    return json.load(open(file_name))['Listeners']

def LISTENERS(*args):
    file_name = "CLI/listeners/listeners.json"
    utils.log_info("Available Listeners are: ")
    json_print(file_name, 'Listeners', ['STAGED', 'NON-STAGED'])
    return json.load(open(file_name))['Listeners']

def ENABLED(*args):
    from CLI.listeners import enabled_Listeners
    print()
    utils.log_info("Enabled Listeners are: ")
    for uid, listen in enabled_Listeners.items():
        utils.color_print(utils.colorize(f"[RED]ID[RESET]: {uid} -- {listen.__color__()}"))
    print()
    return enabled_Listeners

def ENABLE(*args):

    def help():
        # ENABLE non-staged/TCP/192.168.0.101/9001\n
        print("Usage: ENABLE <listener>\nExample(s):\nENABLE non-staged/TCP\nENABLE staged/UDP\nNote: You will have to manually set options and then type \"RUN\" to run the listener or \"RUNBG\" to run the listener in the background.")
        LISTENERS()

    def err(msg : str = None, only_err : bool = False):
        if msg != None:
            utils.log_error(msg)
        if not only_err:
            help()


    with open('CLI/listeners/listeners.json') as f:
        _listeners = json.load(f)['Listeners']


    if args[0] == None:
        err("No listener specified!")
        return

    data = args[0][0]

    if data.lower() == "help" or data.lower() == "-h" or data.lower() == "--help":
        err()
        return

    if '/' not in data:
        err("Invalid listener specified.")
        return

    data = [i.lower() for i in data.split('/')]

    if data[0] != 'staged' and data[0] != 'non-staged':
        err("Invalid listener specified.")
        return

    if len(data) < 2:
        err("Invalid listener specified.")
        return

    try:
        lis = _listeners[data[0].title()]
    except KeyError:
        err("Invalid listener specified.")
        return

    _found = False
    for item in lis:
        try:
            _path = item[data[1]]
            _found = True
            break
        except KeyError:
            continue

    if not _found:
        err("Invalid listener specified.")
        return

    if _path == "UNIMPLEMENTED":
        err("Listener not implemented yet.", only_err = True)
        return

    _path = _path.replace('.py', '')
    file_name = _path.split('/')[-1]
    sys.path.append(_path.split(file_name)[0])
    listener = __import__(file_name)
    sys.path = sys.path[:-1]
    
    obj = listener.Listener()
    obj.setopts()

def DISABLE(*args):
    pass