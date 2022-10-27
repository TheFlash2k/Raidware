from tkinter import E
from flask import Flask, request, jsonify, Response
import Teamserver.Raidware as Raidware
from Teamserver.db import actions as db_actions
from utils.crypto import SHA512
from utils.logger import *

import sys
sys.dont_write_bytecode = True

app = Flask(__name__)

prefix = "v1"

@app.route(f'/{prefix}/auth', methods=['POST'])
def auth():
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
    print(f"Passed Token: {token}")
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




def init(host : str, port : int, debug : bool, team_pass : str = None):

    import shutil
    cols, rows = shutil.get_terminal_size((80, 20))

    Raidware.init()
    log("Initializing the Teamserver API", LogLevel.INFO)
    if not team_pass:
        print(f"{Fore.RED}[!]{Fore.RESET} Note: This is the Teamserver Password that you will use when authenticating...")
    else:
        Raidware.team_password = team_pass

    print(f"\n{'=' * cols}\n{' ' * rows}{Back.RED}TEAMSERVER PASSWORD{Back.RESET}: {Fore.RED}{Raidware.get_team_password()}{Fore.RESET}")
    print(f"[{Fore.GREEN}*{Fore.RESET}] Note: This password won't be stored in the log to prevent it from being leaked.\n{'=' * cols}")

    app.run(host=host, port=port, debug=debug)