from utils.logger import *
from CLI.vars import Globals

def EXIT(*args):
    pass

def CLEAR(*args):
    from os import system, name
    system("cls" if name == "nt" else "clear")

def VERSION(*args):
    try:
        with open('CLI/version.conf', 'r') as f:
            version = f.read()
    except:
        version = "<unknown>"

    color_print(f"[RED]CLI       [RESET]: [GREEN]v{version}[RESET]")
    color_print(f"[CYAN]Teamserver[RESET]: [GREEN]{Globals.ts_ver}[RESET]")

def GENERATE(*args):
    pass

def AGENTS(*args):
    pass

def SESSIONS(*args):
    pass

def INTERACT(*args):
    pass

def LISTENERS(*args):
    pass

def ENABLED(*args):
    pass

def ENABLE(*args):
    pass

def DISABLE(*args):
    pass