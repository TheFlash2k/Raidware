import sys
from CLI.methods.info import *

from CLI.utils.colors import *

def CLEAR(*args):
    from os import system, name
    system("cls" if name == "nt" else "clear")

def is_admin():
    import ctypes, os
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

RAIDWARE = f"{Fore.RED}Raid{Fore.RESET}{Fore.WHITE}ware{Fore.RESET}"
basic_prompt = f"({RAIDWARE})"
prompt = ">>"

if is_admin():
    basic_prompt = f"{Back.BLUE}[{Back.RED}ROOT{Back.RESET}{Back.BLUE}]{Back.RESET} {basic_prompt}"
    prompt = "#"

def parse_input(
    input_string : str
):
    if input_string == "" or input_string == None:
        return

    input_string = input_string.strip()
    cmds = input_string.split()
    
    if cmds[0].upper() not in INFO.keys():
        print(f"[{Fore.RED}-{Fore.RESET}] Invalid Command")
        return

    INFO[cmds[0].upper()][1](cmds[1:] if len(cmds) > 1 else None)

def exit_valid():
    print(f"\n[{Fore.CYAN}*{Fore.RESET}] Thanks for using {RAIDWARE}")
    exit(0)

''' This method simply creates a new UID'''
def create_new_UID():
    import string
    import random
    includes = string.ascii_letters + string.digits
    _len = 25
    return ''.join(random.choice(includes) for i in range(_len))

''' This method reads the configuration file and simply returns the read data as a dictionary'''
def fetch_config(protocol : str) -> dict:    
    import configparser
    config = configparser.ConfigParser()

    file = f"CLI/listeners/default.conf"

    config.read(file)
    try:
        data = config[protocol.upper()]
        ret = {}
        for item in data:
            curr = data[item].replace('"','')
            if data[item][0] == '[' and data[item][-1] == ']':
                curr = data[item].replace('[','').replace(']','').replace('"','').strip().split(',')

            ret[item] = curr

    except KeyError:
        return None

    return ret

def get_random_string(_len = 25):
    import string
    import random
    includes = string.ascii_letters + string.digits
    return ''.join(random.choice(includes) for i in range(_len))
