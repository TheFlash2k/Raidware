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

''' Colors the string and returns the output '''
def colorize(msg : str) -> str:
    for color in colors.items():
        msg = msg.replace(color[0].upper(), color[1])
    return msg

def log_error(msg, *args):
    print(f"[{Fore.RED}-{Fore.RESET}] {colorize(msg)}", file=sys.stderr, *args)

def log_info(msg, *args):
    print(f"[{Fore.GREEN}+{Fore.RESET}] {colorize(msg)}", *args)

def color_print(msg, *args):
    print(colorize(msg), *args)