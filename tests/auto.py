import requests
import json

''' IP OF THE SERVER '''
PREFIX = "http"
HOST = "127.0.0.1"
PORT = 5000

USERNAME = "theflash2k"
PASSWORD = "theflash2k"
TEAMSERVER_PASSWORD = "123"

if __name__ == "__main__":

    print(f"[*] Logging in as user {USERNAME}")
    url = f"{PREFIX}://{HOST}:{PORT}"
    ''' Logging In '''
    r = requests.post(
        f"{url}/v1/auth",
        json={
            "username" : USERNAME,
            "password" : PASSWORD,
            "team_password" : TEAMSERVER_PASSWORD
        }
    )
    cookie = {"token" : r.cookies.get('token')}
    print("[+] Success.")
    
    ''' Preparing a listener: '''
    print("[*] Preparing a listener!")
    data = {
        "listener" : {
            "name" : "TCP",
            "type" : "non-staged",
            "config" : {
                "host" : "0.0.0.0",
                "port" : 65343
            }
        }
    }

    r = requests.post(
        f"{url}/v1/prepare",
        json=data,
        cookies=cookie
    )
    obj = json.loads(r.text)
    if obj['status'] != 'success':
        print(f"[-] Error: {obj['message']}")
        exit(1)
    
    lid = obj['listener']['LID']
    print(f"[+] Success! LID: {lid}")

    print(f"[*] Enabling the listener!")
    data = {
        "LID" : lid
    }
    r = requests.post(
        f"{url}/v1/enable",
        json=data,
        cookies=cookie
    )

    if obj['status'] != 'success':
        print(f"[-] Error: {obj['message']}")
        exit(1)

    print("[+] Success!")

    input("[*] Press enter to disable the listener...")

    data = {
        "LID" : lid
    }
    r = requests.post(
        f"{url}/v1/disable",
        json=data,
        cookies=cookie
    )

    if obj['status'] != 'success':
        print(f"[-] Error: {obj['message']}")
        exit(1)

    print("[+] Success!")