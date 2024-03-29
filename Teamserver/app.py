import logging
from flask import Flask, request, jsonify, Blueprint

from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token, verify_jwt_in_request, get_jwt
)
from flask_cors import CORS

import Teamserver.Raidware as Raidware
from Teamserver.listeners import connections
from .db.actions import LocalJWT, UserManager, get_user
from .db.models.user import User
from utils.logger import *
from utils.utils import *
from utils.crypto import SHA512
from OpenSSL import SSL

''' Setting up base '''
__log__ = logging.getLogger('werkzeug')
__log__.setLevel(logging.ERROR)
app = Flask(__name__)
CORS(app)


app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies', 'json']
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# Set the JWT expire time to 1 day:
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = get_config_variable('Raidware_Configuration.SECRET_KEY')

bp = Blueprint('Raidware-Teamserver', __name__)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

''' Setting up JWT '''
jwt = JWTManager(app)
blacklist = set()

def user_logged_in():
    try:
        return get_jwt_identity()
    except:
        return None

@jwt.token_in_blocklist_loader
def token_in_blacklist(jwt_headers, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

@bp.route('/version')
def version():
    with open('version.conf', 'r') as f:
        version = f.read()
    return f"v{version.split()[0]}"

@bp.route(f'/login', methods=['POST'])
def auth():
    if user_logged_in():
        return {
            'status': 'warning',
            'msg': 'You are already logged in'
        }, 201
    
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
        else:
            data = request.form.to_dict()
    except:
        return {
            "status" : "error",
            "msg" : "Invalid request"
        }, 400

    if not data.get('username'):
        return {
            'status': "error",
            'msg': 'username field is missing'
        }, 400
    if not data.get('password'):
        return {
            'status': "error",
            'msg': 'password field is missing'
        }, 400
    if not data.get('team_password'):
        return {
            'status': "error",
            'msg': 'team_password field is missing'
        }, 400

    ''' Checking if the team password is correct '''
    if data.get('team_password') != Raidware.get_team_password():
        return {
            'status': 'error',
            'msg': 'Incorrect team password'
        }, 400
    
    ''' Checking if the user exists '''
    user = get_user(data.get('username'))
    if not user:
        return {
            'status': 'error',
            'msg': 'Invalid credentials'
        }, 400

    ''' Checking if the password is correct '''

    ip = request.remote_addr
    if user['password'] != SHA512(data.get('password')):
        log_auth(f'User {data.get("username")} tried to login with invalid credentials from {ip}')
        return {
            'status': 'error',
            'msg': 'Invalid credentials'
        }, 400

    ''' Generating a token for the user '''
    access_token = create_access_token(identity=user['username'])
    refresh_token = create_refresh_token(identity=user['username'])
    log_auth(f'User {user["username"]} logged in successfully from {ip}')
    res = jsonify(
        {
        'status': 'success',
        'msg' : 'Logged in successfully',
        'access_token': access_token,
        'refresh_token': refresh_token
        }
    )
    res.status_code = 200
    res.headers['X-Auth-Token'] = access_token
    res.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
    return res

@bp.route(f'/register', methods=['POST'])
@jwt_required(optional=True)
def register():
    if user_logged_in():
        return {
            'status': 'warning',
            'msg': 'You are already logged in'
        }, 201
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
        else:
            data = request.form.to_dict()
    except:
        return {
            "msg" : "Invalid request",
            'status' : 'error'
        }, 400

    ''' Checking if the fields are present
        - username
        - email
        - password
        - confirm_password
        - team_password
    '''
    if not data.get('username'):
        return {
            'status' : 'error',
            'msg': 'username field is missing'
        }, 400
    if not data.get('email'):
        return {
            'status' : 'error',
            'msg': 'email field is missing'
        }, 400
    if not data.get('password'):
        return {
            'status' : 'error',
            'msg': 'password field is missing'
        }, 400
    if not data.get('confirm_password'):
        return {
            'status' : 'error',
            'msg': 'confirm_password field is missing'
        }, 400

    if not data.get('team_password'):
        return {
            'status' : 'error',
            'msg': 'team_password field is missing'
        }, 400

    ''' Checking if the provided team password is valid '''
    if data.get('team_password') != Raidware.get_team_password():
        return {
            'status' : 'error',
            'msg': 'Invalid team password'
        }, 400

    ''' Checking if the passwords match '''
    if data.get('password') != data.get('confirm_password'):
        return {
            'status' : 'error',
            'msg': 'Passwords do not match'
        }, 400

    ''' Adding the user to the database and checking if it exists '''
    if not UserManager.add_user(User(username=data.get('username'), email=data.get('email'), password=data.get('password'))):
        return {
            'status' : 'error',
            'msg': 'Username already exists'
        }, 400

    msg = f'User {data.get("username")} added to database statusfully'
    log(msg, LogLevel.INFO)
    return {'status': 'success', 'msg': msg}, 200

@bp.route(f'/listeners', methods=['GET'])
@jwt_required()
def listeners():

    if UserManager.get_user_by_username(get_jwt_identity()) == None:
        return {
            "msg" : "You are not logged in",
            "status" : "error"
        }, 403
    return {"Listeners" : Raidware.get_listeners()}

# Write a function that will return detail about a specific listener based on its name:
@bp.route(f'/listeners/<name>', methods=['GET'])
@jwt_required()
def listener(name):
    
        if UserManager.get_user_by_username(get_jwt_identity()) == None:
            return {
                "msg" : "You are not logged in",
                "status" : "error"
            }, 403
        data = Raidware.get_listeners()
        for listener in data:
            try:
                if listener['name'] == name:
                    return listener
            except:
                pass
        return {
            "msg" : "Invalid listener name specified",
            "status" : "error"
        }, 404

@bp.route(f'/agents')
@jwt_required()
def agents():

    if UserManager.get_user_by_username(get_jwt_identity()) == None:
        return {
            "msg" : "You are not logged in",
            "status" : "error"
        }, 401
    return Raidware.get_agents()

@bp.route(f'/prepare', methods=['POST'])
@jwt_required()
def prepare_listener():

    ''' This method will prepare a listener '''
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'msg': 'No data provided'
            }, 400

        ''' Checking if the fields are present '''
        if not data.get('listener'):
            return {
                'status': 'error',
                'msg': '"listener" field is missing'
            }, 400
        
        ''' Checking if the listener exists '''
        if not Raidware.check_listener(data.get('listener')):
            return {
                'status': 'error',
                'msg': 'Listener does not exist'
            }, 400
        ''' Preparing the listener '''
        listener = Raidware.prepare_listener(data.get('listener'))

        if not listener:
            return {
                'status': 'error',
                'msg': 'Failed to prepare listener'
            }, 400
    
        return listener

    except Exception as E:
        return {
            "status" : "error",
            "msg" : f'Invalid Request. Error: {E.__repr__()}'
        }, 400

@bp.route(f'/update', methods=['PUT'])
@jwt_required()
def update():
    ''' This method will update a listener '''
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'msg': 'No data provided'
            }, 400

        _ = Raidware.update_listener(data)
        if type(_) == dict:
            if _['status'] == 'error':
                return _, 400

        return _

    except Exception as E:
        return {
            "status" : "error",
            "msg" : f'Error: {E}'
        }, 400

@bp.route(f'/enable', methods=['POST'])
@jwt_required()
def enable():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'msg': 'No data provided'
            }, 400

        ''' Checking if the fields are present '''
        if not data.get('LID'):
            return {
                'status': 'error',
                'msg': '"LID" field is missing'
            }, 400

        if data.get('LID'):
            if len(data) > 1:
                return {
                    'status': 'error',
                    'msg': 'Only "LID" field is required'
                }, 400

        ''' Checking if the listener exists '''
        log(f"LID: {data.get('LID')}")
        try:
            listener = [i for i in enabled_listeners if i.LID == data.get('LID')][0]
        except:
            return {
                'status': 'error',
                'msg': 'Invalid LID Specified. Listener doesn\'t exist'
            }, 404

        ''' Updating the listener '''
        if not listener:
            return {
                'status': 'error',
                'msg': 'Failed to update listener'
            }, 400

        if listener.status.lower().strip() == 'running':
            return {
                'status': 'error',
                'msg': 'Listener is already running'
            }, 400

        listener.status = 'Running'
        listener.onLoad()
        return {
            'status': 'success',
            'msg': 'Listener started successfully'
        }

    except Exception as E:
        return {
            "status" : "error",
            "msg" : f'Error: {E}'
        }, 400

@bp.route(f'/disable', methods=['POST'])
@jwt_required()
def disable():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'msg': 'No data provided'
            }, 400

        ''' Checking if the fields are present '''
        if not data.get('LID'):
            return {
                'status': 'error',
                'msg': '"LID" field is missing'
            }, 400

        if data.get('LID'):
            if len(data) > 1:
                return {
                    'status': 'error',
                    'msg': 'Only "LID" field is required'
                }, 400

        ''' Checking if the listener exists '''
        try:
            listener = [i for i in enabled_listeners if i.LID == data.get('LID')][0]
        except:
            return {
                'status': 'error',
                'msg': 'Invalid LID Specified. Listener doesn\'t exist'
            }, 404

        if listener.status.lower().strip() == 'not running':
            return {
                'status': 'error',
                'msg': 'Listener is already stopped'
            }, 400

        listener.status = 'Not Running'
        listener.onStop()
        return {
            'status': 'success',
            'msg': 'Listener stopped successfully'
        }

    except Exception as E:
        return {
            "status" : "error",
            "msg" : f'Error: {E}'
        }, 400

@bp.route(f'/delete', methods=['DELETE', 'POST'])
@jwt_required()
def delete():
    from utils.utils import enabled_listeners
    ''' This method will delete a listener '''
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'msg': 'No data provided'
            }, 400
        
        ''' Checking if the fields are present '''
        if not data.get('LID'):
            return {
                'status': 'error',
                'msg': '"LID" field is missing'
            }, 400
        
        if data.get('LID'):
            if len(data) > 1:
                return {
                    'status': 'error',
                    'msg': 'Only "LID" field is required'
                }, 400
            
        ''' Checking if the listener exists '''
        listener = [i for i in enabled_listeners if i.LID == data.get('LID')]
        if not listener:
            return {
                'status': 'error',
                'msg': 'Invalid LID Specified. Listener doesn\'t exist'
            }, 404
        listener = listener[0]

        if data.get('force'):
            if data.get('force').lower().strip() == 'true':
                listener.status = 'Not Running'
                listener.onStop()
                enabled_listeners.remove(listener)
                return {
                    'status': 'success',
                    'msg': 'Listener stopped forcefully and deleted successfully.'
                }

        ''' Checking if it is running '''
        if listener.status.lower().strip() == 'running':
            return {
                'status': 'error',
                'msg': 'Listener is running. Please stop the listener before deleting it'
            }, 400

        ''' Remove the listener from the enabled_listeners list '''
        enabled_listeners.remove(listener)
        return {
            'status': 'success',
            'msg': 'Listener deleted successfully'
        }
    
    except Exception as E:
        return {
            "status" : "error",
            "msg" : f'Error: {E}'
        }, 400

@bp.route(f'/enabled', methods=['GET'])
@jwt_required()
def enabled():
    from utils.utils import enabled_listeners
    ''' Checking if data has been passed through json '''
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            ''' This method will return a list of enabled listeners '''
            return {
                "listeners" : [i.__dict__() for i in enabled_listeners ]
            }
        
        ''' Checking if the fields are present '''
        if data.get('LID') == "":
                return {
                'status': 'error',
                'msg': '"LID" field cannot be empty'
            }, 400


        ''' Checking if there are any other fields except LID '''
        if not data.get('LID'):
            return {
                "listeners" : [i.__dict__() for i in enabled_listeners ]
            }

        if data.get('LID'):
            if len(data) > 1:
                return {
                    'status': 'error',
                    'msg': 'Invalid fields'
                }, 400
        ''' Checking if listener is in enabled listeners '''
        try:
            return {
                "listener" : [i.__dict__() for i in enabled_listeners if i.LID == data.get('LID')][0]
            }
        except:
            return {
                'status': 'error',
                'msg': 'Invalid LID Specified. Listener doesn\'t exist'
            }, 404

    except Exception as E:
        return {
            'status' : 'error',
            'msg' : f'Error: {E}'
        }, 400

@bp.route(f'/check')
@jwt_required()
def check():
    ''' This will check if any new connections have been received on the listeners. '''
    from .listeners import connections
    # Check if args contains LID
    if request.args.get('LID'):
        # Check if the LID is valid
        try:
            listener = [i for i in enabled_listeners if i.LID == request.args.get('LID')][0]
        except:
            return {
                'status': 'error',
                'msg': 'Invalid LID Specified. Listener doesn\'t exist'
            }, 404
        # Check if the listener has any new connections
        if listener.new_connections:
            return {
                'status': 'success',
                'msg': 'New connections found',
                'connections': [i.__dict__() for i in listener.new_connections]
            }
        else:
            return {
                'status': 'success',
                'msg': 'No new connections found'
            }
    return { "Connections" : [i.__dict__() for i in connections.values()]}

@bp.route('/generate')
@jwt_required()
def generate():

    return {
        'status': 'error',
        'msg'  : 'This feature is currently not available.'
    }, 400

@bp.route(f'/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    return  {
        'status': 'success',
        'access_token': create_access_token(identity=current_user)
    }

@bp.route(f'/logout', methods=['GET', 'POST'])
@jwt_required()
def logout():
    log("Inside this function")
    name = get_jwt_identity()
    jti = get_jwt()['jti']
    log(f"Logged out {name}", LogLevel.INFO)
    blacklist.add(jti)
    res = jsonify(status='success', msg=f'Successfully logged out {name}')
    res.set_cookie('access_token', '')
    return res

@bp.route(f'/logout_refresh', methods=['POST'])
@jwt_required(refresh=True)
def logout_refresh():
    name = get_jwt_identity()
    jti = get_jwt()['jti']
    if jti in blacklist:
        return {
            'status': 'error',
            'msg': 'You are already logged out'
        }, 401
    log(f"Logged out {name}", LogLevel.INFO)
    blacklist.add(jti)
    res = jsonify(status='success', msg=f'Successfully logged out {name}')
    res.set_cookie('refresh_token', '')
    return res

## A function that will have the endpoing /sessions and will return a list of sessions
@bp.route(f'/sessions', methods=['GET'])
@jwt_required()
def sessions():
    data = [connections[i].__dict__() for i in connections.keys()]
    sessions = []

    for item in data:
        for val in item.values():
            sessions.append(val)

    return {
        'status': 'success',
        'sessions': sessions
    }
    
@bp.route(f'/interact', methods=['POST'])
@jwt_required()
def interact():
    
    def upload(**kwargs):
        log("Passed Kwargs: ", kwargs)
        return {
            'status': 'success',
            'msg': 'File Uploaded Successfully!'
        }
    
    def download(**kwargs):
        return {
            'status': 'success',
            'msg': 'File Downloaded Successfully!'
        }

    def shell(**kwargs):
        print(kwargs)
        ''' Sending the command to the session '''
        try:
            __check = data["payload"].split()[0].lower()
        except:
            return {
                'status': 'error',
                'msg': 'Invalid command'
            }
        
        if __check == "put" or __check == "upload":
            return upload(**kwargs)
        
        if __check == "get" or __check == "download":
            return download(**kwargs)

        try:
            session.send(f'{data["mode"]}:{data["payload"]}')
            ret = session.recv()
        except:
            log("Unable to send command to session", LogLevel.ERROR)
            log("Removing session from connections", LogLevel.ERROR)
            connections.pop(data.get('SID'))
            return {
                "status" : "error",
                "msg" : "Unable to send command to session"
            }, 400
        
        if data["payload"][:2].lower() == "cd":
            session.pwd = ret
            
        if 'Connection Lost' in ret:
            log("Unable to send command to session", LogLevel.ERROR)
            log("Removing session from connections", LogLevel.ERROR)
            connections.pop(data.get('SID'))
            return {
                'status': 'error',
                'msg': ret
            }, 400
            
        return {
            'status': 'success',
            'msg': ret
        }

    modes = {
        'shell' : shell,
        'upload' : upload,
        'download' : download
    }

    ''' Checking if data has been passed through json '''
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    else:
        data = request.form.to_dict()

    if data == None or data == {}:
        return {
            'status': 'error',
            'msg': 'No data provided'
        }, 400

    ## Checking if the fields are present: SID, mode, arg:
    valid = ['SID', 'mode', 'payload']
    for i in valid:
        if i not in data:
            return {
                'status': 'error',
                'msg': f'"{i}" field is missing'
            }, 400

    ## Checking if an invalid field has been passed
    for k in data.keys():
        if k not in valid:
            return {
                'status': 'error',
                'msg': f'Invalid field "{k}"'
            }, 400

    ''' Checking if the session exists '''
    if data.get('SID') not in connections:
        return {
            'status': 'error',
            'msg': 'Invalid SID Specified. Session doesn\'t exist'
        }, 400

    ''' Getting the session '''
    session = connections[data.get('SID')]

    if data.get('mode') not in modes:
        return {
            'status': 'error',
            'msg': 'Invalid mode specified'
        }, 400
    
    return modes[data.get('mode')](**data)

@bp.route(f'/users', methods=['GET'])
@jwt_required()
def users():
    ''' This method will return a list of users '''
    return {
        'status': 'success',
        'users': UserManager().get_pub_users()
    }

import time
last_stats = {}
last_time = time.time()

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_sessions():
    global last_time
    global last_stats

    current_time = time.time()
    if current_time - last_time < 5:
        return last_stats

    import requests
    data = [connections[i].__dict__() for i in connections.keys()]
    sessions = []

    for item in data:
        for val in item.values():
            sessions.append(val)

    ips = [ i['ip'] for i in sessions ]
    # convert to set:
    ips = set(ips)
    log(f"IPs: {ips}")
    info = {}
    base_url = "http://ip-api.com/json/"
    
    for ip in ips:
        log(f"Current ip: {ip}")
        log("Info: => ")
        if ip != "" or ip != None:
            r = requests.get(base_url + ip)
            data = r.json()
            try:
                info[ip] = {
                    "country" : data["country"],
                    "latitude" : data["lat"],
                    "longitude" : data["lon"]
                }
            except:
                pass
    last_time = time.time()
    last_stats = info
    return info

@bp.route(f'/loot', methods=['GET', 'POST'])
@jwt_required()
def loot():
    if request.method == 'GET':
        return {
            'status': 'success',
            'loot': Raidware.get_loot()
        }
    else:
        from .db.actions import LootManager
    from .db.models.Loot import Loot
    ''' This method will add loot '''
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'msg': 'No data provided'
            }, 400

        ''' Checking if the fields are present '''
        if not data.get('type'):
            return {
                'status': 'error',
                'msg': '"type" field is missing'
            }, 400

        if not data.get('value'):
            return {
                'status': 'error',
                'msg': '"value" field is missing'
            }, 400

        if not data.get('description'):
            return {
                'status': 'error',
                'msg': '"description" field is missing'
            }, 400

        types = ('password', 'hash')

        ''' Checking if the type is valid '''
        if data.get('type').lower() not in types:
            return {
                'status': 'error',
                'msg': 'Invalid type specified. Only hash or password allowed'
            }, 400
        
        ''' Adding the loot '''
        if not LootManager.add_loot(Loot(name=data.get('name'), _type=data.get('type'), value=data.get('value'), description=data.get('description'))):
            return {
                'status': 'error',
                'msg': 'Failed to add loot'
            }, 400

        return {
            'status': 'success',
            'msg': 'Loot added successfully'
        }
    except Exception as E:
        return {
            "status" : "error",
            "msg" : f'Error: {E}'
        }, 400

@bp.route(f"/remove-loot", methods=['POST'])
@jwt_required()
def remove_loot():
    from .db.actions import LootManager
    from .db.models.Loot import Loot
    ''' This method will remove loot '''
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'msg': 'No data provided'
            }, 400

        ''' Checking if the fields are present '''
        if not data.get('id'):
            return {
                'status': 'error',
                'msg': '"id" field is missing'
            }, 400
        
        ''' Checking if the loot exists '''
        if not LootManager.get_loot_by_id(data.get('id')):
            return {
                'status': 'error',
                'msg': 'Invalid id specified. Loot doesn\'t exist'
            }, 404
        
        ''' Removing the loot '''
        if not LootManager.delete_loot(data.get('id')):
            return {
                'status': 'error',
                'msg': 'Failed to remove loot'
            }, 400
        
        return {
            'status': 'success',
            'msg': 'Loot removed successfully'
        }
    except Exception as E:
        return {
            "status" : "error",
            "msg" : f'Error: {E}'
        }, 400
        

@bp.route(f'/botnet', methods=['POST'])
@jwt_required()
def botnet():
    # check if the field 'command' is present:
    if 'command' not in request.form:
        return {
            'status': 'error',
            'msg': 'No command specified'
        }, 400
    
    command = request.form.get('command')
    log(f"Executing command [RED]{command}[RESET] on all sessions", LogLevel.INFO)
    for i in connections.keys():
        connections[i].send(command)
        connections[i].recv()
    return {
        'status': 'success',
        'msg': 'Command executed successfully'
    }


def init(
    host : str,
    port : int,
    debug : bool,
    team_pass : str = None,
    https : bool = False,
):

    import shutil
    cols, rows = shutil.get_terminal_size((80, 20))

    Raidware.init()
    log("Initializing the Teamserver API", LogLevel.INFO)
    if not team_pass:
        print(f"[{Fore.RED}!{Fore.RESET}] Note: This is the Teamserver Password that you will use when authenticating...")
    else:
        Raidware.team_password = team_pass

    print(f"\n{'=' * cols}\n{' ' * rows}{Back.RED}TEAMSERVER PASSWORD{Back.RESET}: {Fore.RED}{Raidware.get_team_password()}{Fore.RESET}")
    print(f"[{Fore.GREEN}*{Fore.RESET}] Note: This password won't be stored in the log to prevent it from being leaked.\n{'=' * cols}")

    from utils.utils import used_ports
    used_ports[port] = "Teamserver"

    context = ('Teamserver/certs/teamserver.crt', 'Teamserver/certs/teamserver.key')
    app.register_blueprint(bp, url_prefix=f'/{prefix}')
    if https:
        app.run(host=host, port=port, debug=debug, ssl_context=context)
    else:
        app.run(host=host, port=port, debug=debug)
