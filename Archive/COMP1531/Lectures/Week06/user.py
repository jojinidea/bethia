class User: 
    def __init__(self,name,password):
        self._name = name
        self._password = password
        
    @property
        def name(self):
            return self._name
    
    @property 
        def password(self):
            return self._password

#this is a basic user class, we need a way of storing multiple users (we could add as a list to a class reddit)

# we could instead create a usermanager.py file with

from models.User import User #from folder models, file User, import User
class UserManager:
    def __init__(self):
        self._users = []
    
    #given a name and password, add a user to the list
    def add_user(self, name, password):
        #verification logic - making sure user doesn't exist, password restricted to certain amount of logic etc
        user = User(name, password) #if user is coming from another file, we need to import this
    self._users.append(user)
    return True #could return T/False if the function added the user to the list
    
    #we might want to verify the user exists
    def verify_user(self,name,password):
        for user in self._users:
            if user.name == name and user.password == password:
                return user
        
        
        return None
        
        
    def get_user(self, name):
        for user in self._users:
            if user.name == name:
                return user
        return None
