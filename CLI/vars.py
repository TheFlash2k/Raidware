
class Config:
    SLEEP_TIME = 5

class ThreadHandles:
    prompt_updater = None
    
class Globals:
    logged_in_as = ""
    access_token = ""
    refresh_token = ""
    base_url = ""
    enabled_listeners = []
    sessions = []
    ts_ver = "0.0.0"
    new_spawn = True