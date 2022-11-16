from time import sleep
from colorama import init, Fore, Back
from .utils.utils import *
import CLI.listeners as listeners
from utils.logger import LogLevel, log_error, log
from utils.utils import prefix

''' Disabling .pyc files from generating '''
import sys
sys.dont_write_bytecode = True

def main():
    print(f"Welcome to {RAIDWARE}. Type 'help' for help. To exit, type 'exit' || (CTRL+Z+ENTER in WINDOWS or CTRL+D in UNIX)\n")

    while True:
        _prompt = ""
        try:
            _prompt += f'[{colorize(f"[GREEN]{len(listeners.connections)}[RESET]")}]' if len(listeners.connections) > 0 else ""
            _prompt += f'[{colorize(f"[CYAN]{len(listeners.enabled_Listeners)}[RESET]")}]' if len(listeners.enabled_Listeners) > 0 else ""
            _prompt += " " if _prompt  != "" else ""

            _prompt += f"{basic_prompt} {prompt} "
            parse_input(
                input(_prompt)
            )
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            break
        except Exception as E:
            print(f"[{Fore.RED}-{Fore.RESET}] An Error Occurred: {E}")

    exit_valid()

def is_teamserver_running(
    host : str,
    port : int
):
    import requests
    try:
        requests.get(f"http://{host}:{port}/")
        return True
    except:
        return False

def init(
    host : str,
    port : int,
    username : str,
    password : str,
    team_password : str
):
    ## Check if the teamserver is running:
    if not is_teamserver_running(
        host = host,
        port = port
    ):
        print(f"[{Fore.RED}!{Fore.RESET}] Teamserver is not running OR is unavailable. Please check the provided host and port for the Teamserver.")
        exit(1)

    ## Authenticate with the Teamserver:
    import requests
    endpoint = f'{prefix}/auth'
    resp = requests.post(
        url = f"http://{host}:{port}/{endpoint}",
        json = {
            "username"      : username,
            "password"      : password,
            "team_password" : team_password
        }
    )
    try:
        import json
        resp_json = json.loads(resp.text)
        if resp_json['status'] == 'success':
            log(f"Successfully Authenticated with the Teamserver.", LogLevel.INFO)
            log(f"Welcome [YELLOW]{username}[RESET]!", LogLevel.INFO)
        else:
            log("Authentication Failed. Please check your credentials.", LogLevel.ERROR)
            log(f"Reason: {resp_json['message']}", LogLevel.ERROR)
            exit(1)
    except Exception as E:
        log(f"[[BLUE]CLI[RESET]] - An Error Occurred: [RED]{E}[RESET]", LogLevel.ERROR)
        exit(1)

    ## Start the CLI:
    main()