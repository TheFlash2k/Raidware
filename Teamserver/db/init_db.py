import sqlite3
import os
from utils.logger import *
from utils.crypto import SHA512

def initialize():
    prefix = 'Teamserver/db/'
    ''' Check if teamserver.db file exists, then simply return '''
    if os.path.isfile(f'{prefix}teamserver.db'):
        log('Database already exists', LogLevel.DEBUG)
        return

    log("Database doesn't exist. Creating with default username and password", LogLevel.DEBUG)
    connection = sqlite3.connect(f'{prefix}teamserver.db')

    with open(f'{prefix}schema.sql') as schema:
        connection.executescript(schema.read())
    
    cuur = connection.cursor()
    _pass = SHA512('raidware')
    cuur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('raidware', _pass))
    cuur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin',    _pass))
    cuur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('root',     _pass))

    connection.commit()
    connection.close()
    log("Database created with default [RED]raidware[RESET]:[RED]raidware[RESET]", LogLevel.DEBUG)