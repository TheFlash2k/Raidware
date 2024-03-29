import CLI.methods.base as impl
from tabulate import tabulate

def HELP(*args):
    data = [[item[0], item[1][0]] for item in INFO.items() if item[1][2]]
    print(
        "\n",
        tabulate(
            data, headers=["Command", "Description"]
        ),
        "\n"
    )

def get_args_list():
    args = []
    for arg in INFO.keys():
        # if INFO[arg][2]:
        args.append(arg)
    return args

INFO = {
    "HELP"      : ("Display the help menu", HELP, False),
    "OPTIONS"   : ("Display the help menu", HELP, False),
    "EXIT"      : ("Exit the program", impl.EXIT, False),
    "QUIT"      : ("Exit the program", impl.EXIT, False),
    "CLEAR"     : ("Clear the screen", impl.CLEAR, False),
    "CLS"       : ("Clear the screen", impl.CLEAR, False),
    "VERSION"   : ("Display the version of the program", impl.VERSION, False),
    "GENERATE"  : ("Generate a Payload", impl.GENERATE, True),
    "GEN"       : ("Generate a Payload", impl.GENERATE, False),
    "AGENTS"    : ("Display the list of avaiable agents", impl.AGENTS, True),
    "SESSIONS"  : ("Display the list of active sessions", impl.SESSIONS, True),
    "INTERACT"  : ("Interact with a specific session", impl.INTERACT, True),
    "USE"  : ("Interact with a specific session", impl.INTERACT, False),
    "LISTENERS" : ("Display the list of all avaiable listeners", impl.LISTENERS, True),
    "SHOW"      : ("Display the list of enabled listeners", impl.ENABLED, False),
    "ENABLED"      : ("Display the list of enabled listeners", impl.ENABLED, True),
    "RUNNING"      : ("Display the list of enabled listeners", impl.ENABLED, False),
    "ENABLE"    : ("Enables a listener", impl.ENABLE, True),
    "DISABLE" : ("Disables a running listener", impl.DISABLE, True),
    "KILL" : ("Disables a running listener", impl.DISABLE, False),
}