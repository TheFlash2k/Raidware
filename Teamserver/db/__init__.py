import sqlite3
import os
from utils.logger import *
from utils.crypto import SHA512
from .models.user import User
from .actions import UserManager

def __init__():
    prefix = 'Teamserver/db/'
    db_name = 'teamserver.sqlite3'
    ''' Check if teamserver.db file exists, then simply return '''
    if os.path.isfile(f'{prefix}{db_name}'):
        log('Database already exists', LogLevel.DEBUG)
        return

    log("Database doesn't exist. Creating with default username and password", LogLevel.DEBUG)
    connection = sqlite3.connect(f'{prefix}{db_name}')

    with open(f'{prefix}schema.sql') as schema:
        connection.executescript(schema.read())
    connection.commit()
    connection.close()
    
    UserManager.add_user(
        User(
            username="raidware",
            email="admin@raidware.me",
            password="raidware"
        )
    )

    log("Database created with default [RED]raidware[RESET]:[RED]raidware[RESET]", LogLevel.DEBUG)