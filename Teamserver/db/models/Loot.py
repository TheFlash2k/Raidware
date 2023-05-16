class Loot:
    def __init__(self, id = 0, name="", _type='Hash', value="", description=""):
        self.id = id
        self.name = name
        self.type = _type
        self.value = value
        self.description = description
    
    def json(self):
        return {'id': self.id, 'type': self.type, 'name' : self.name, 'value': self.value, 'description': self.description}
    
    def __repr__(self):
        return str(self.json())
    
    def __str__(self):
        return str(self.json())