from flask import Flask, request, jsonify, Response, redirect, url_for
import Teamserver.Raidware as Raidware
from Teamserver.db import actions as db_actions
from utils.crypto import SHA512
from utils.logger import *
from utils.utils import *

import sys
sys.dont_write_bytecode = True

import logging
__log__ = logging.getLogger('werkzeug')
__log__.setLevel(logging.ERROR)

app = Flask(__name__)
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route("/", methods=HTTP_METHODS)
def index():
    ''' Redirect to {prefix}/base'''
    return redirect(url_for('base'))

@app.route(f'/{prefix}/base', methods=HTTP_METHODS)
def base():

    with open('version.conf') as f:
        version = f.read()
    
    return {
        "server" : "Raidware Teamserver API",
        "version" : version
    }

@app.route(f'/{prefix}/auth', methods=['POST'])
def auth():

    ''' Checking if a valid token already exists: ''' 
    token = request.cookies.get('token')
    if token:
        if Raidware.check_token(token):
            return {
                'status': 'warning',
                'message': 'Already authenticated'
            }, 200
        else:
            return {
                'status': 'error',
                'message': 'Invalid token. Please delete/remove token to re-authenticate'
            }, 401

    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
        else:
            data = request.form.to_dict()
    except:
        return {
            "ERROR" : "Invalid request"
        }, 500

    log(f"Data: {data}")
    ''' Checking if the fields are present
        - username
        - password
        - team_password
    '''
    if not data.get('username'):
        return {
            'success': False,
            'msg': 'username field is missing'
        }, 401
    if not data.get('password'):
        return {
            'success': False,
            'msg': 'password field is missing'
        }, 401
    if not data.get('team_password'):
        return {
            'success': False,
            'msg': 'team_password field is missing'
        }, 401

    ''' Checking if the team password is correct '''
    if data.get('team_password') != Raidware.get_team_password():
        return {
            'status': 'error',
            'message': 'Incorrect team password'
        }, 403

    ''' Checking if the user exists '''
    user = db_actions.get_user(data.get('username'))
    if not user:
        return {
            'status': 'error',
            'message': 'User does not exist'
        }, 401

    ''' Checking if the password is correct '''

    if user['password'] != SHA512(data.get('password')):
        return {
            'status': 'error',
            'message': 'Incorrect password'
        }, 403

    ''' Generating a token for the user '''
    token = Raidware.generate_token(data.get('username'))

    log(f"Token set as: {token}", LogLevel.DEBUG)
    log(f"Authenticated {data.get('username')}", LogLevel.INFO)
    res = jsonify(status='success', message='Successfully authenticated')
    res.set_cookie('token', token)
    return res  

@app.route(f'/{prefix}/login', methods=['POST'])
def login():
    ''' Redirect to /auth '''
    return auth()

@app.route(f'/{prefix}/register', methods=['POST'])
def register():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
        else:
            data = request.form.to_dict()
    except:
        return {
            "ERROR" : "Invalid request"
        }, 500

    ''' Checking if the fields are present
        - username
        - password
        - confirm_password
        - team_password
    '''
    if not data.get('username'):
        return {
            'success': False,
            'msg': 'username field is missing'
        }
    if not data.get('password'):
        return {
            'success': False,
            'msg': 'password field is missing'
        }
    if not data.get('confirm_password'):
        return {
            'success': False,
            'msg': 'confirm_password field is missing'
        }

    if not data.get('team_password'):
        return {
            'success': False,
            'msg': 'team_password field is missing'
        }

    ''' Checking if the provided team password is valid '''
    if data.get('team_password') != Raidware.get_team_password():
        return {
            'success': False,
            'msg': 'Invalid team password'
        }

    ''' Checking if the passwords match '''
    if data.get('password') != data.get('confirm_password'):
        return {
            'success': False,
            'msg': 'Passwords do not match'
        }

    ''' Adding the user to the database and checking if it exists '''
    if not db_actions.add_user(data.get('username'), data.get('password')):
        return {
            'success': False,
            'msg': 'Username already exists'
        }

    msg = f'User {data.get("username")} added to database successfully'
    log(msg, LogLevel.INFO)
    return {'success': True, 'msg': msg}

''' We will use this to check if the user is authenticated '''
def validate():
    ''' We need to check if the token is valid '''
    token = request.cookies.get('token')
    if not token:
        return {
            'status': 'error',
            'message': 'Unauthenticated'
        }, 401

    if not Raidware.check_token(token):
        return {
            'status': 'error',
            'message': 'Invalid token'
        }, 401

    return None

@app.route(f'/{prefix}/listeners')
def listeners():    
    resp = validate()
    if resp:
        return resp
    return Raidware.get_listeners()

@app.route(f'/{prefix}/agents')
def agents():
    resp = validate()
    if resp:
        return resp

    return Raidware.get_agents()

@app.route(f'/{prefix}/prepare', methods=['POST'])
def prepare_listener():
    resp = validate()
    if resp:
        return resp
    
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
                'message': 'No data provided'
            }, 500

        ''' Checking if the fields are present '''
        if not data.get('listener'):
            return {
                'status': 'error',
                'message': '"listener" field is missing'
            }, 500

        ''' Checking if the listener exists '''
        if not Raidware.check_listener(data.get('listener')):
            return {
                'status': 'error',
                'message': 'Listener does not exist'
            }, 500


        ''' Preparing the listener '''
        listener = Raidware.prepare_listener(data.get('listener'))

        if not listener:
            return {
                'status': 'error',
                'message': 'Failed to prepare listener'
            }, 500

        return listener

    except Exception as E:
        return {
            "ERROR" : "Invalid request",
            "Details" : f'Error: {E}'
        }, 500


@app.route(f'/{prefix}/update', methods=['POST'])
def update():
    resp = validate()
    if resp:
        return resp

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
                'message': 'No data provided'
            }, 500

        _ = Raidware.update_listener(data)
        if type(_) == dict:
            if _['status'] == 'error':
                return _, 500

        return _

    except Exception as E:
        return {
            "status" : "error",
            "message" : f'Error: {E}'
        }, 500

@app.route(f'/{prefix}/enable', methods=['POST'])
def enable():
    resp = validate()
    if resp:
        return resp

    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'message': 'No data provided'
            }, 500

        ''' Checking if the fields are present '''
        if not data.get('LID'):
            return {
                'status': 'error',
                'message': '"LID" field is missing'
            }, 500

        if data.get('LID'):
            if len(data) > 1:
                return {
                    'status': 'error',
                    'message': 'Only "LID" field is required'
                }, 500

        ''' Checking if the listener exists '''
        log(f"LID: {data.get('LID')}")
        try:
            listener = [i for i in enabled_listeners if i.LID == data.get('LID')][0]
        except:
            return {
                'status': 'error',
                'message': 'Invalid LID Specified. Listener doesn\'t exist'
            }

        ''' Updating the listener '''
        if not listener:
            return {
                'status': 'error',
                'message': 'Failed to update listener'
            }

        if listener.status.lower().strip() == 'running':
            return {
                'status': 'error',
                'message': 'Listener is already running'
            }

        listener.status = 'Running'
        listener.onLoad()
        return {
            'status': 'success',
            'message': 'Listener started successfully'
        }

    except Exception as E:
        return {
            "status" : "error",
            "message" : f'Error: {E}'
        }, 500

@app.route(f'/{prefix}/disable', methods=['POST'])
def disable():
    resp = validate()
    if resp:
        return resp

    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        if data == None or data == {}:
            return {
                'status': 'error',
                'message': 'No data provided'
            }, 500

        ''' Checking if the fields are present '''
        if not data.get('LID'):
            return {
                'status': 'error',
                'message': '"LID" field is missing'
            }, 500

        if data.get('LID'):
            if len(data) > 1:
                return {
                    'status': 'error',
                    'message': 'Only "LID" field is required'
                }, 500

        ''' Checking if the listener exists '''
        log(f"LID: {data.get('LID')}")
        try:
            listener = [i for i in enabled_listeners if i.LID == data.get('LID')][0]
        except:
            return {
                'status': 'error',
                'message': 'Invalid LID Specified. Listener doesn\'t exist'
            }

        if listener.status.lower().strip() == 'not running':
            return {
                'status': 'error',
                'message': 'Listener is already stopped'
            }

        listener.status = 'Not Running'
        listener.onStop()
        return {
            'status': 'success',
            'message': 'Listener stopped successfully'
        }

    except Exception as E:
        return {
            "status" : "error",
            "message" : f'Error: {E}'
        }, 500

@app.route(f'/{prefix}/delete', methods=['POST'])
def delete():
    resp = validate()
    if resp:
        return resp

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
                'message': 'No data provided'
            }, 500
    
    except Exception as E:
        return {
            "status" : "error",
            "message" : f'Error: {E}'
        }, 500


@app.route(f'/{prefix}/enabled', methods=['GET'])
def enabled():
    from utils.utils import enabled_listeners
    resp = validate()
    if resp:
        return resp

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
                'message': '"LID" field cannot be empty'
            }, 500


        ''' Checking if there are any other fields except LID '''
        if not data.get('LID'):
            return {
                "listeners" : [i.__dict__() for i in enabled_listeners ]
            }

        if data.get('LID'):
            if len(data) > 1:
                return {
                    'status': 'error',
                    'message': 'Invalid fields'
                }, 500
        ''' Checking if listener is in enabled listeners '''
        try:
            return {
                "listener" : [i.__dict__() for i in enabled_listeners if i.LID == data.get('LID')][0]
            }
        except:
            return {
                'status': 'error',
                'message': 'Invalid LID Specified. Listener doesn\'t exist'
            }, 500

    except Exception as E:
        return {
            'status' : 'error',
            'message' : f'Error: {E}'
        }

@app.route(f'/{prefix}/check')
def check():
    ''' This will check if any new connections have been received on the listeners. '''
    pass
    
@app.route(f'/{prefix}/logout', methods=['POST'])
def logout():
    ''' This will logout the user '''
    resp = validate()
    if resp:
        return resp

    ''' Decrypting the received token '''
    token = request.cookies.get('token')
    token = Raidware.decrypt_token(token)
    
    if token == None:
        return {
            'status': 'error',
            'message': 'No user logged in.'
        }, 401

    name = token.split('|')[0]
    log(f"Logged out {name}", LogLevel.INFO)

    res = jsonify(status='success', message=f'Successfully logged out {name}')
    res.set_cookie('token', '')
    return res


def init(
    host : str,
    port : int,
    debug : bool,
    team_pass : str = None
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

    app.run(host=host, port=port, debug=debug)

