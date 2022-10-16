from re import S
from colorama import init, Fore, Back
from utils.utils import *

def main():
    print(f"Welcome to {RAIDWARE}. Type 'help' for help. To exit, type 'exit' || (CTRL+Z+ENTER in WINDOWS or CTRL+D in UNIX)\n")
    while True:
        try:
            parse_input(
                input(f"{basic_prompt} {prompt} ")
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