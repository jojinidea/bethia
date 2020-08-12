# user-defined exceptions are created when we don't have standard built-in exceptions to raise an error

# e.g. let's pretend we're coding a game and a negative level is an error (should not happen). We want to raise an error when this occurs 

# need to create a class for our own exception

# any user-defined exception inherits from the base-class Exception

class InvalidLevelError(Exception):
    def __init__(self, message): #want to pass a message along with exception that we'd like to print
        self._message = message
        
# we need a way to check if our level is negative - a raise function

level = -1

try: 
    if level < 1: 
        raise InvalidLevelError("Invalid level: {}".format(level))
except InvalidLevelError as e: #want to define an instance of the exception class (e is an instance of InvalidLevelError)
    print(e._message)
    
    
