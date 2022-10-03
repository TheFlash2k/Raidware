import methods.impl as impl
from tabulate import tabulate

def HELP(*args):
    data = [[item[0], item[1][0]] for item in INFO.items() if item[1][2]]
    print(tabulate(data, headers=["Command", "Description"]))

INFO = {
    "HELP" : ("Display the help menu", HELP, False),
    "EXIT" : ("Exit the program", impl.EXIT, False),
    "QUIT" : ("Exit the program", impl.EXIT, False),
    "CLEAR" : ("Clear the screen", impl.CLEAR, False),
    "CLS" : ("Clear the screen", impl.CLEAR, False),
    "VERSION" : ("Display the version of the program", impl.VERSION, False),
    "GENERATE" : ("Generate a Payload", impl.GENERATE, True),
    "GEN" : ("Generate a Payload", impl.GENERATE, False),
    "AGENTS" : ("Display the list of avaiable agents", impl.AGENTS, True),
    "SESSIONS" : ("Display the list of active sessions", impl.SESSIONS, True),
    "INTERACT" : ("Interact with a specific session", impl.SESSIONS, True),
    "LISTENERS" : ("Display the list of all avaiable listeners", impl.LISTENERS, True),
}