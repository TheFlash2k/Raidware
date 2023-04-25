from .methods import INFO
from utils.logger import log, LogLevel

logged_in_as = ""
jwt = ""

def parse_input(prompt : str):
    _input = input(prompt)

    if _input == "" or _input == None:
        return

    _input = _input.strip()
    cmds = _input.split()
    
    if cmds[0].upper() not in INFO.keys():
        log(f"Invalid Command", LogLevel.ERROR)
        return
    
    INFO[cmds[0].upper()][1](cmds[1:] if len(cmds) > 1 else None)