import requests
import json

''' IP OF THE SERVER '''
PREFIX = "http"
HOST = "127.0.0.1"
PORT = 5000

USERNAME = "theflash2k"
PASSWORD = "theflash2k"
TEAMSERVER_PASSWORD = "123"
COOKIE = "SHZI4sCdoIr7%2ByM2KpRPzyq%2Fm6MLxl8A%2BkzZZis7awaMnop8BfOo0%2FG6AzQJR7hc" # Specify the cookie here.

def make_request(url, endpoint, data, cookie = {}):
    r = requests.post(
        f"{url}/v1/{endpoint}",
        json=data,
        cookies=cookie
    )
    obj = json.loads(r.text)
    if obj['status'] != 'success':
        print(f"[-] Error: {obj['message']}")
        exit(1)

    return r, obj


if __name__ == "__main__":

    url = f"{PREFIX}://{HOST}:{PORT}"

    ''' Logging In '''
    if COOKIE == "" or COOKIE == {}:
        print("[!] No COOKIE specified!")
        print(f"[*] Logging in as user {USERNAME}")
        data = {
            "username" : USERNAME,
            "password" : PASSWORD,
            "team_password" : TEAMSERVER_PASSWORD
        }
        r = make_request(url, 'auth', data=data)[0]
        cookie = {"token" : r.cookies.get('token')}
        print(f"[+] Success! Cookie: {cookie}")
    else:
        if type(COOKIE) == str:
            cookie = {"token" : COOKIE}

        print(f"[*] Using a Pre-defined Cookie: {COOKIE}")

    ''' Preparing a listener: '''
    print("[*] Preparing a listener!")
    data = {
        "listener" : {
            "name" : "TCP",
            "type" : "non-staged",
            "config" : {
                "host" : "0.0.0.0",
                "port" : 6542
            }
        }
    }

    obj = make_request(url, "prepare", data, cookie)[1]
    lid = obj['listener']['LID']
    print(f"[+] Success! LID: {lid}")

    print(f"[*] Enabling the listener!")
    obj = make_request(url, "enable", {"LID" : lid}, cookie)[1]
    print("[+] Success!")

    input("[*] Press enter to disable the listener...")
    obj = make_request(url, "disable", {"LID" : lid}, cookie)[1]
    print("[+] Success!")