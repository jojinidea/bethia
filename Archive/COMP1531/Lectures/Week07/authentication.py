class AuthenticationError(Exception):
    "User-defined exception for authentication"
    pass 

class InputError(Exception):
    pass

class AuthenticationError(InputError):
    def __init__(self, 

#defined built-in-exception. Must extend base-case exception

def authenticate(password):
    if password != "hello":
        raise AuthenticationError("Invalid password was provider") #when exception is raised, the control passes to the caller (validate_user - line 16)
    return True
    # no built in exception handling, raise error 

def validate_user(username, password):
    try:
        return username == "test" and authenticate(password)
    except AuthenticationError as e: 
        print(e)
        #print(e.args)
        #print(e.args[0]) #additional parameters stored as tuple
        #print(e.args[1])
        #print(e._message)
        #print(e._pwd)

validate_user('test', 'hello')
print("Validating user: {}".format(str(validate_user('test','apple'))))

