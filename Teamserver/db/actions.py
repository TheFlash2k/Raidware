''' All the functions that will be performed on the database will exist in this file. '''
import sqlite3
from utils.crypto import SHA512

prefix = 'Teamserver/db/'

def get_db_connection():
    conn = sqlite3.connect(f'{prefix}teamserver.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_user(
    username : str,
    password : str
):
    if get_user(username):
        return False

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, SHA512(password)))
    conn.commit()
    conn.close()
    return True

def get_user(
    username : str
):
    ''' Check if the username exists in the database '''
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user