from time import sleep
from colorama import init, Fore, Back
import requests
import json

from utils.utils import *
from utils.logger import *

from .reader import TabComplete
from .methods import get_args_list
from .utils import *

''' Disabling .pyc files from generating '''
import sys
sys.dont_write_bytecode = True

def main():
    print(f"Welcome to {RAIDWARE}. Type 'help' for help. To exit, type 'exit' || (CTRL+Z+ENTER in WINDOWS or CTRL+D in UNIX)\n")

    while True:
        _prompt = ""
        try:
            TabComplete(get_args_list())
            # _prompt += f'[{colorize(f"[GREEN]{len(listeners.connections)}[RESET]")}]' if len(listeners.connections) > 0 else ""
            # _prompt += f'[{colorize(f"[CYAN]{len(listeners.enabled_Listeners)}[RESET]")}]' if len(listeners.enabled_Listeners) > 0 else ""

            _prompt += " " if _prompt  != "" else ""
            _prompt += f"{basic_prompt} {prompt} "
            parse_input(
                _prompt
            )
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            break
        except Exception as E:
            print(f"[{Fore.RED}-{Fore.RESET}] An Error Occurred: {E.__repr__()}")

    # exit_valid()

def is_teamserver_running(
    host : str,
    port : int
):
    try:
        r = requests.get(f"http://{host}:{port}/{prefix}/version")
        return r.text
    except:
        return False

def init(
    host : str,
    port : int,
    username : str,
    password : str,
    team_password : str
):
    log(f"Checking if the Teamserver is running...")
    ts_ver = is_teamserver_running(host = host, port = port)
    if not ts_ver:
        log(f"{cli_prompt} [RED]Teamserver[RESET] is not running OR is unavailable. Please check the provided host and port for the Teamserver.", LogLevel.ERROR)
        exit(1)

    log(f"[RED]Raid[WHITE]ware[RESET] Teamserver Version: [CYAN]{ts_ver}[RESET]", LogLevel.INFO)

    ## Authenticate with the Teamserver:
    endpoint = f'{prefix}/login'
    resp = requests.post(
        url = f"http://{host}:{port}/{endpoint}",
        json = {
            "username"      : username,
            "password"      : password,
            "team_password" : team_password
        }
    )
    try:
        if resp.status_code == 403 or resp.status_code >= 500:
            log(f"{cli_prompt} - An error occurred while trying to make request to {http://{host}:{port}/{endpoint}}. Please make sure you have the endpoint right.")
        resp_json = json.loads(resp.text)
        if resp_json['status'] == 'success':
            log(f"Successfully Authenticated with the Teamserver.", LogLevel.INFO)
            log(f"Welcome [YELLOW]{username}[RESET]!", LogLevel.INFO)
        else:
            log("Authentication Failed. Please check your credentials.", LogLevel.ERROR)
            log(f"Reason: {resp_json['message']}", LogLevel.ERROR)
            exit(1)
    except Exception as E:
        log(f"{cli_prompt} - An Error Occurred: [RED]{E.__repr__()}[RESET]", LogLevel.ERROR)
        exit(1)

    global logged_in_as
    logged_in_as = username

    # Store the jwt from the response:


    ## Start the CLI:
    main()
    