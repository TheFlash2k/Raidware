class User(object):
    def __init__(self, id = -1, username = "", password = "", email = ""):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
    
    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'password': self.password}
    
    def __repr__(self):
        return str(self.json())
    
    def __str__(self):
        return str(self.json())