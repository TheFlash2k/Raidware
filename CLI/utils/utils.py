import sys
from methods.info import *
from colorama import Fore, Back, init

init()

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

msg = "([GREEN]TCP[RESET]):"

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

def log_error(msg, *args):
    for color in colors.items():
        msg = msg.replace(color[0], color[1])
    print(f"[{Fore.RED}-{Fore.RESET}] {msg}", file=sys.stderr, *args)

def log_info(msg, *args):
    for color in colors.items():
        msg = msg.replace(color[0], color[1])
    print(f"[{Fore.GREEN}+{Fore.RESET}] {msg}", *args)