import json

class Connection:
    def __init__(self, UID : str, listener = None, _type = None, base = None, OS=None, proc = None, pid = None, pwd = None, user = None):
        self.UID = UID
        self.listener = listener
        self.type = _type
        self.base = base
        self.OS = OS
        self.proc = proc
        self.pid = pid
        self.pwd = pwd
        self.user = user

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return {
            self.UID : {
                'UID' : self.UID,
                'type' : self.type,
                'OS' : self.OS,
                'proc' : self.proc,
                'pid' : self.pid,
                'pwd' : self.pwd,
                'user' : self.user
            }
        }

    def __str__(self):
        return f"{self.UID} | {self.type} | {self.OS} | {self.proc} | {self.pid} | {self.pwd} | {self.user}"

    def __list__(self):
        return [self.UID, self.type, self.OS, self.proc, self.pid,  self.pwd , self.user]

    def send(self, msg : str):
        self.listener.onSend(msg, socket=self.base)

    def recv(self):
        return self.listener.onRecv(socket=self.base)

connections = {}

connections["AzzSgasdcSG"] = Connection(UID="AzzSgasdcSG", listener="TCP", _type="Non-Stage", base="Connection", OS="Windows", proc = "Test", pid = "19025", pwd = r"C:\Windows\New", user = "Ali")
connections["asdasdasd"] = Connection(UID="asdasdasd", listener="TCP", _type="Non-Stage", base="Connection", OS="Windows", proc = "Test", pid = "19025", pwd = r"C:\Windows\New", user = "Ali")

d = [i.__dict__() for i in connections.values()]

print(json.dumps(d))

# print(json.dumps(connections))