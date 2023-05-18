import requests
import os, sys
from threading import Thread
from time import sleep

base_url = "http://haxors.ddns.net:7000/v1"
team_password = "123"

methods = {
    "GET" : requests.get,
    "POST" : requests.post,
    "PUT" : requests.put,
}

def _req(url, token = None, _method = "GET", data = {}, verbose=True):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = methods[_method.upper()](url, headers=headers, json=data)
    if verbose:
        print(f"Response ==> {r.text}")
    return r

def _runbg(file):
    os.system(file + " > NUL")


def main():
    # file = r"L:\GIT\Raidware-Agents\windows\RaidwareAgents\Release\TCP-Agent.exe"
    # Thread(target=_runbg, args=(file,), daemon=True).start()
    
    r = _req(f"{base_url}/version")
    print(f"==> Raidware Teamserver version: {r.text}")

    token = ""
    r = _req(f"{base_url}/login", _method="POST", data = {
        "username": "raidware",
        "password" : "raidware",
        "team_password" : team_password
    })

    token = r.json()['access_token']
    print("==> Token: ", token)

    r = _req(f"{base_url}/prepare", _method="POST", token=token,
        data = {
            "listener" : {
                "name" : "base-tcp-listener",
                "protocol" : "tcp",
                "type" : "non-staged",
                "config" : {
                    "host" : "0.0.0.0",
                    "port" : 5252,
                    
                }
            }
        }
    )

    if not "already exists" in r.text.lower():
        listener_id = r.json()['listener']['LID']
        print(f"==> Listener ID: {listener_id}")

        r = _req(f"{base_url}/enable", _method="POST", token=token, data = { 'LID' : listener_id })
        print(f"==> Enable listener: {r.text}")
    else:
        print("==> Listener is already running...")

    # print("==> Executing the exe to get a session: ")
    # print("Checking if a session has been created...")
    # print("Sleeping for 5 seconds to wait for session...")
    # sleep(5)
    # r = _req(f"{base_url}/sessions", _method="GET", token=token)
    # print(f"==> Sessions: {r.text}")
    # sid = r.json()['sessions'][0]['UID']
    # print("==> Session ID: ", sid)
    # print("==> Executing command whoami:")
    # r = _req(f"{base_url}/interact", _method="POST", token=token, data = { 'SID' : sid,  'mode' : 'shell', 'payload' : 'whoami' })
    # print("==> Response: ", r.text)

    # print("==> Press any key to continue...")
    # input()
    # os.system("taskkill /f /im TCP-Agent.exe")

if __name__ == "__main__":
    main()