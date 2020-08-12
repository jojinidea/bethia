# if we don't have a built-in exception, we can define our own exception

class AuthenticationError(Exception):
    "User-defined exception for authentication"
    pass
        
    
def authenticate(password):
    if password != 'hello':
        raise AuthenticationError("Invalid password was provided")
    return True
    
def validate_user(username, password):
    try:
        return username == 'test' and authenticate(password)
    except AuthenticationError as e: #store object instance of exception in variable
        print(e)
    
validate_user('test', 'h')
