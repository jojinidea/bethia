from flask_login import UserMixin

class User(UserMixin): #can inherit UserMixin
    
    def __init__(self, user_id, name):
        self._id = user_id
        self._name = name
        
    def get_id(self):
        return self._id
        
    def get_name(self):
        return self._name
