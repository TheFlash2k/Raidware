''' All the functions that will be performed on the database will exist in this file. '''
import sqlite3
from utils.crypto import SHA512
from .models.user import User
from werkzeug.security import safe_str_cmp

prefix = 'Teamserver/db/'
db_name = 'teamserver.sqlite3'
def get_db_connection():
    conn = sqlite3.connect(f'{prefix}{db_name}')
    conn.row_factory = sqlite3.Row
    return conn

class UserManager():

    def __get_base__(method, var):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE {method} = ?", (var,))
        user = cur.fetchone()
        conn.close()
        return user

    def get_user_by_username(username):
        return UserManager.__get_base__("username", username)
    
    def get_user_by_id(id):
        return UserManager.__get_base__("id", id)
    
    def get_user_by_email(email):
        return UserManager.__get_base__("email", email)

    def add_user(user : User):
        if UserManager.get_user_by_username(user.username):
            return False

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (user.username, user.email, SHA512(user.password)))
        conn.commit()
        conn.close()
        return True
    
    def get_all_users(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        conn.close()
        return users
    
    def delete_user(self, id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True


def dict_from_row(row):
    return dict(zip(row.keys(), row)) if row != None else None

def get_user(
    username : str
):
    _ck = UserManager.get_user_by_username(username)
    if _ck == None:
        _ck = UserManager.get_user_by_email(username)
    return dict_from_row(_ck)

class LocalJWT():
    def authenticate(username, password):
        user = get_user()
        
        if user and safe_str_cmp(user.passwrd, SHA512(password)):
            return user

    def identity(payload):
        user_id = payload['identity']
        return UserManager.get_user_by_id(user_id)