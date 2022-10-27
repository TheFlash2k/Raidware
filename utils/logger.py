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

def log(
    msg,
    level : LogLevel = LogLevel.DEBUG,
    *args
):

    msg = f"[[CYAN]{current_time()}[RESET]] [{level[2]}{level[1]}[RESET]] {msg}"
    clean = uncolorize(msg)
    msg = colorize(msg)

    ''' Fetching the file from config '''
    path = 'Teamserver/config/'
    file = f'{path}config.json'
    import json
    with open(file, 'r') as f:
        config = json.load(f)

    file = config['Raidware_Configuration']['LOG_FILE']
    debug = config['Raidware_Configuration']['DEBUG']

    if not debug and level == LogLevel.DEBUG:
        return

    _file = sys.stderr if level == LogLevel.ERROR else sys.stdout

    ''' Creating the logs folder if the folder doesn't exist '''
    import os
    if not os.path.exists('Teamserver/logs'):
        os.mkdir('Teamserver/logs')
    
    ''' Writing the logs to the file '''
    with open(file, 'a') as f:
        f.write(clean + '\n')

    ''' Printing the logs to the console '''
    print(msg, file=_file, *args)

def log_error(msg, *args):
    print(f"[{Fore.RED}-{Fore.RESET}] {colorize(msg)}", file=sys.stderr, *args)
    

def log_info(msg, *args):
    print(f"[{Fore.GREEN}+{Fore.RESET}] {colorize(msg)}", *args)

def color_print(msg, *args):
    print(colorize(msg), *args)