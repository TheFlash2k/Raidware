from os import system, name
from colorama import Fore
from methods.verify import *
import json
from tabulate import tabulate

def CLEAR(*args):
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
    pass

def json_print(file, field, headers):
    with open(file) as f:
        data = json.load(f)[field]
    print(
        "\n",
        tabulate(
            data,
            headers=headers
        ),
        "\n"
    )


def AGENTS(*args):
    json_print("agents/agents.json", "AGENTS", ["Linux", "Windows", "MacOS"])

def LISTENERS(*args):
    json_print("listeners/listeners.json", 'Listeners', ['STAGED', 'NON-STAGED'])

def ENABLED(*args):
    from listeners import enabled_Listeners
    print()
    utils.log_info("Enabled Listeners are: ")
    for listen in enabled_Listeners:
        utils.color_print(listen.__color__())
    print()

def ENABLE(*args):
    from listeners.non_staged.tcp import TCP
    tcp = TCP("0.0.0.0", 9001)
    tcp.onLoad()
    from time import sleep
    sleep(1)