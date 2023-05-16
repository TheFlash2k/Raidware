import sqlite3

class User(object):
    def __init__(self, id = -1, username = "", password = "", email = ""):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
    
    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'password': self.password}
    
    def json_pub(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}
    
    def __repr__(self):
        return str(self.json())
    
    def __str__(self):
        return str(self.json())

db_name = 'teamserver.sqlite3'
conn = sqlite3.connect(f'{db_name}')
cur = conn.cursor()
cur.execute("SELECT * FROM users")
users = cur.fetchall()
conn.close()

_users = []
for user in users:
    _users.append(user[0:3])

print(_users)