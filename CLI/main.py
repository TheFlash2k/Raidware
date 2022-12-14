from re import S
from time import sleep
from typing import List
from colorama import init, Fore, Back
from utils.utils import *
import listeners

''' Disabling .pyc files from generating '''
import sys
sys.dont_write_bytecode = True

def main():
    print(f"Welcome to {RAIDWARE}. Type 'help' for help. To exit, type 'exit' || (CTRL+Z+ENTER in WINDOWS or CTRL+D in UNIX)\n")

    ''' Test Code'''
    from listeners.non_staged.tcp import Listener
    lis = Listener(port = 9001)
    lis.onLoad()
    sleep(1)

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


if __name__ == "__main__":
    main()