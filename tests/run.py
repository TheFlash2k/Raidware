import requests

urls = {
    "Login" : "http://localhost:5000/v1/login",
    "Prepare" : "http://localhost:5000/v1/prepare",
    "Enable" : "http://localhost:5000/v1/enable",
}

headers = {
    "Content-Type" : "application/json"
}

def login():
    r = requests.post(
        url=urls['Login'],
        headers=headers,
        json={
            "username" : "raidware",
            "password" : "raidware",
            "team_password" : "123"
        }
    )
    return r.json()

def prepare_listener(token : str, listener : dict):
    r = requests.post(
        url=urls['Prepare'],
        headers={
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        },
        json=listener
    )
    return r.json()

def enable_listener(token : str, listener : dict):
    r = requests.post(
        url=urls['Enable'],
        headers={
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        },
        json=listener
    )
    return r.json()

if __name__ == "__main__":
    tokens = login()
    print(f"Tokens: {tokens}")
    listener = {
        "listener" : {
            "name" : "TCP",
            "type" : "non-staged",
            "config" : {
                "host" : "0.0.0.0",
                "port" : 9001
            }
        }
    }
    lid = prepare_listener(token=tokens['access_token'], listener=listener)['listener']['LID']
    print(f"Listener ID: {lid}")
    # print(enable_listener(token=tokens['access_token'], listener=listener))
