''' This will have a log function that will print the logs and store them as well.'''
import sys
from colorama import Fore, Back, init

init()

colors = {
    "[GREEN]" : Fore.GREEN,
    "[RESET]" : Fore.RESET,
    "[RED]" : Fore.RED,
    "[BLUE]" : Fore.BLUE,
    "[YELLOW]" : Fore.YELLOW,
    "[WHITE]" : Fore.WHITE,
    "[MAGENTA]" : Fore.MAGENTA,
    "[CYAN]" : Fore.CYAN,
    "[BLACK]" : Fore.BLACK
}

def current_time():
    from datetime import datetime
    return datetime.now().strftime("%m/%d/%y - %H:%M:%S")


''' Colors the string and returns the output '''
def colorize(msg : str) -> str:
    for color in colors.items():
        msg = msg.replace(color[0].upper(), color[1])
    return msg

def uncolorize(msg : str) -> str:
    for color in colors.items():
        msg = msg.replace(color[0].upper(), '')
    return msg


class LogLevel:
    ERROR = [ "-", "ERROR", "[RED]" ]
    INFO =  [ "+", "INFO", "[GREEN]"  ]
    DEBUG = [ "*", "DEBUG", "[BLUE]" ]
    WARN =  [ "!", "WARN", "[YELLOW]" ]
    AUTH =  [ "#", "AUTH", "[MAGENTA]" ]
    CONNECTIONS = [ ">", "CONNECTIONS", "[CYAN]" ]

def log(msg, level : LogLevel = LogLevel.DEBUG, *args, **kargs):

    msg = f"[[CYAN]{current_time()}[RESET]] [{level[2]}{level[1]}[RESET]] {msg}"
    clean = uncolorize(msg)
    msg = colorize(msg)

    file = f'config.json'
    import json
    with open(file, 'r') as f:
        config = json.load(f)

    file = config['Raidware_Configuration']['LOG_FILE']
    debug = config['Raidware_Configuration']['DEBUG']

    if not debug and level == LogLevel.DEBUG:
        return

    if level == LogLevel.AUTH:
        file = config['Raidware_Configuration']['AUTH_LOG_FILE']

    elif level == LogLevel.ERROR:
        file = config['Raidware_Configuration']['ERROR_LOG_FILE']

    elif level == LogLevel.DEBUG:
        file = config['Raidware_Configuration']['DEBUG_LOG_FILE']
    
    elif level == LogLevel.CONNECTIONS:
        file = config['Raidware_Configuration']['CONNECTIONS_LOG_FILE']

    _file = sys.stderr if level == LogLevel.ERROR else sys.stdout

    path = '/'.join(file.split('/')[:-1])
    import os
    if not os.path.exists(path):
        os.mkdir(path)
    
    if kargs.get('to_file', True) == False:
        kargs.pop('to_file')
        print(msg, file=_file, *args, **kargs)
        return

    with open(file, 'a') as f:
        f.write(clean + '\n')

    print(msg, file=_file, *args, **kargs)

def log_error(msg, *args, **kargs):
    log(msg, LogLevel.ERROR, *args, **kargs)

def log_auth(msg, *args, **kargs):
    log(f"{colorize(msg)}", level= LogLevel.AUTH, *args, **kargs)

def log_info(msg, *args, **kargs):
    print(f"[{Fore.GREEN}+{Fore.RESET}] {colorize(msg)}", *args, **kargs)

def color_print(msg, *args):
    print(colorize(msg), *args)