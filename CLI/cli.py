from time import sleep
from colorama import init, Fore, Back
import requests
import json
import threading

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

    ThreadHandles.prompt_updater = threading.Thread(target=prompt_updater, daemon=True)
    ThreadHandles.prompt_updater.start()

    log("Fetching prompt...")
    prompt_updater(_self=False)

    while True:
        _prompt = ""
        try:
            TabComplete(get_args_list())
            lis_len = len(Globals.enabled_listeners)
            ses_len = len(Globals.sessions)
            listener_prompt = colorize( f"[GREEN]Listeners: [BLUE] {lis_len}[RESET]\n")
            session_prompt  = colorize(f"[YELLOW]Sessions : [BLUE] {ses_len}[RESET]\n")
            _prompt += listener_prompt# if lis_len else ""
            _prompt += session_prompt# if ses_len else ""
            _prompt += f"{basic_prompt} {prompt} "
            parse_input(
                _prompt
            )
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            terminate_thread(ThreadHandles.prompt_updater)
            break
        except Exception as E:
            print(f"[{Fore.RED}-{Fore.RESET}] An Error Occurred: {E.__repr__()}")


def is_teamserver_running(
    host : str,
    port : int,
    https : bool = True
):
    try:
        r = requests.get(f"http{'s' if https else ''}://{host}:{port}/{prefix}/version")
        return r.text
    except:
        return False

def init(
    host : str,
    port : int,
    username : str,
    password : str,
    team_password : str,
    https : bool = True
):
    log(f"Checking if the Teamserver is running...")
    Globals.ts_ver = is_teamserver_running(host=host, port=port, https=https)
    if not Globals.ts_ver:
        log(f"{cli_prompt} [RED]Teamserver[RESET] is not running OR is unavailable. Please check the provided host and port for the Teamserver.", LogLevel.ERROR)
        exit(1)

    log(f"[RED]Raid[WHITE]ware[RESET] Teamserver Version: [CYAN]{Globals.ts_ver}[RESET]", LogLevel.INFO)

    Globals.base_url = f"http{'s' if https else ''}://{host}:{port}/{prefix}"

    resp = requests.post(
        url = f"{Globals.base_url}/login",
        json = {
            "username"      : username,
            "password"      : password,
            "team_password" : team_password
        }
    )
    try:
        if resp.status_code == 403 or resp.status_code >= 500:
            log(f"{cli_prompt} - An error occurred while trying to make request to {Globals.base_url}/login. Please make sure you have the endpoint right.")
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

    Globals.logged_in_as = username
    Globals.access_token = resp.json()['access_token']
    Globals.refresh_token = resp.json()['refresh_token']

    main()
    